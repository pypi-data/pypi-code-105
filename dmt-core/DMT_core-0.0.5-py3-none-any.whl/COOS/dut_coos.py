""" Manges a device under test which can be simulated by COOS using the TCAD Interface class.

Author: Markus Müller 
"""
# DMT_core
# Copyright (C) 2019  Markus Müller and Mario Krattenmacher and the DMT contributors <https://gitlab.hrz.tu-chemnitz.de/CEDIC_Bipolar/DMT/>
#
# This file is part of DMT_core.
#
# DMT_core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DMT_core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
import re
import copy
import os
import numpy as np
import pandas as pd
import logging
import h5py

from DMT.core import (
    DutTcad,
    DataFrame,
    specifiers,
    sub_specifiers,
    Sweep,
    read_data,
    get_specifier_from_string,
    constants,
    DutType,
)
from DMT.config import DATA_CONFIG

from DMT.exceptions import SimulationUnsuccessful
from DMT.config import COMMANDS
from COOSpy.tools import makeinp, turn_off_recombination

try:
    import COOS
except ImportError:
    print("Warning COOSpy not available.")

# coos iv output columns not needed in current DMT framework
coos_iv_fallback = {
    "T_LATTICE": None,
    "T_CPU": None,
}


class DutCOOS(DutTcad):
    r"""Manages simulations and simulation data with COOS.

    Parameters
    -----------
    database_dir : str
        Directory for the current databases
    dut_type   : :class:`~DMT.core.dut_type.DutType`
    inp_structure : dictionary
        Dictionary that describes the simulation domain according to the COOS manual.
    name : str, {'dev'}, optional
        Prefix for the files
    nodes : str, optional
        Comma separated node list
    reference_node : str, optional
        Contact node, required reference for all output voltages. HAS TO BE SET BEFORE SIMULATION!
    simulator_command : str, optional
        System command to call the simulation. If none, config.py command is used.
    simulator_arguments : list[str], optional
        Arguments for the system command

    Attributes
    -----------
    sim_name : str
        DEVICE simulation title. Sort of a DUT-Name.

    """
    inited = False

    def __init__(
        self, database_dir, dut_type, inp_structure, name="coos_", simulator_command=None, **kwargs
    ):
        if simulator_command is None:
            simulator_command = COMMANDS["COOS"]

        super().__init__(
            database_dir,
            name,
            dut_type,
            inp_structure,
            simulator_command=simulator_command,
            inp_name="coos_inp.din",
            **kwargs,
        )

    def create_inp_header(self, inp_coos):
        """Creates the inp_header from the given parameters.

        All parameters are taken from obj_inp_device.

        Parameters
        ----------
        inp_coos : dict of dicts that describes a coos input structure

        Returns
        --------
        inp_header : str
        """
        if not "BIAS_DEF" in inp_coos:
            inp_coos["BIAS_DEF"] = {}

        if not "OUTPUT" in inp_coos:
            inp_coos["OUTPUT"] = {}

        # to be consistent with the resolving of DMT sweepdef for COOS simulation
        inp_coos["BIAS_DEF"]["list"] = 1
        inp_coos["OUTPUT"]["path"] = "output"
        inp_coos["OUTPUT"]["name"] = "dut"
        self.inp_dict = inp_coos
        inp = makeinp(inp_coos, file=None)
        return inp

    def make_input(self, sweep):
        sweep = copy.deepcopy(sweep)
        """Adds bias blocks to a coos heade file (string)"""
        inp_str = self._inp_header
        # find frequency sweep def
        has_f_def = False
        for i, sub_sweep in enumerate(sweep.sweepdef):
            if sub_sweep.var_name == specifiers.FREQUENCY:
                has_f_def = True
                break
        if has_f_def:
            f_def = sweep.sweepdef.pop(i)
        sweep.set_values()
        df = sweep.create_df()
        # add T sweep if not specified
        has_t_def = False
        for sub_sweep in sweep.sweepdef:
            if sub_sweep.var_name == specifiers.TEMPERATURE:
                has_t_def = True

        try:
            if not has_t_def:
                temp_bias_info = {
                    "cont_name": "'T'",
                    "bias_fun": "'LIN'",
                    "bias_val": "{0:f} {0:f} {1:f}".format(sweep.othervar["TEMP"], len(sweep.df)),
                }
        except KeyError:
            if not has_t_def:
                raise IOError("DutCOOS: The temperature needs to be specified explicitly!")
        # copy sweep definition:

        path_bias = os.path.join(DATA_CONFIG["directories"]["simulation"], "bias.h5")

        f = h5py.File(path_bias, "w")
        for key, val in df.items():
            try:
                cont_name = key.nodes[0]
            except IndexError:
                cont_name = str(key)[0]
            except AttributeError:
                cont_name = str(key)[0]
            f.create_dataset(cont_name, data=val)
        f.close()
        self.list_copy.append(path_bias)
        # end save sweep definition
        for sub_sweep in sweep.sweepdef:
            try:
                cont_name = "'" + sub_sweep.var_name.nodes[0] + "'"
            except IndexError:
                cont_name = "'" + str(sub_sweep.var_name)[0] + "'"

            bias_info = {
                "bias_fun": "'HDF'",
                "cont_name": cont_name,
            }

            # add sweep definition to inp file
            bias_str = (
                "&BIAS_INFO "
                + "".join([name + "=" + str(value) + " " for name, value in bias_info.items()])
                + "/"
            )
            inp_str = inp_str + "\n" + bias_str

        # add frequency def
        if has_f_def:
            sub_sweep = f_def
            if sub_sweep.sweep_type == "CON":
                bias_fun = "'TAB'"
                ac_info = {
                    "port1": "'" + self.ac_ports[0] + "'",
                    "port2": "'" + self.ac_ports[1] + "'",
                    "sweep_type": bias_fun,
                    "freq_val": sub_sweep.value_def[0],
                }
                # add sweep definition to inp file
                bias_str = (
                    "&AC_INFO "
                    + "".join([name + "=" + str(value) + " " for name, value in ac_info.items()])
                    + "/"
                )
                inp_str = inp_str + "\n" + bias_str
            elif sub_sweep.sweep_type == "LIN":
                bias_fun = "'LIN'"
                ac_info = {
                    "port1": "'" + self.ac_ports[0] + "'",
                    "port2": "'" + self.ac_ports[1] + "'",
                    "sweep_type": bias_fun,
                    "freq_val": " ".join(["{0:3.2e}".format(val) for val in sub_sweep.value_def]),
                }
                # add sweep definition to inp file
                bias_str = (
                    "&AC_INFO "
                    + "".join([name + "=" + str(value) + " " for name, value in ac_info.items()])
                    + "/"
                )
                inp_str = inp_str + "\n" + bias_str
            else:
                raise NotImplementedError

        if not has_t_def:
            bias_str = (
                "&BIAS_INFO "
                + "".join([name + "=" + str(value) + " " for name, value in temp_bias_info.items()])
                + "/"
            )
            inp_str = inp_str + "\n" + bias_str

        inp_str = inp_str + "\n"
        return inp_str

    def validate_simulation_successful(self, sweep):
        """Checks if the simulation of the given sweep was successful.

        Parameters
        ----------
        sweep  : :class:`DMT.core.sweep.Sweep`
            Sweep that has been simulated.

        Raises
        --------
        NotImplementedError
            If the Dut is not a simulatable dut.
        SimulationUnsuccessful
            If the simulation output is not valid.
        FileNotFoundError
            If the sim log file does not exist.
        """
        # get sweep folder
        sim_folder = self.get_sim_folder(sweep)
        log_str = ""
        with open(os.path.join(sim_folder, "sim.log")) as log_file:
            try:
                log_str = log_file.read()
            except:
                return True

        # if not 'simulation finished' in log_str:
        if False:
            pattern = r"(error.*)"
            r1 = re.findall(pattern, log_str)
            print("coos error message is:")
            print(r1)
            print("\n")
            raise SimulationUnsuccessful(
                "COOS Simulation of the sweep "
                + sweep.name
                + " with the hash "
                + sweep.get_hash()
                + " failed! An error was found! Director is "
                + sim_folder
                + "."
            )
        else:
            try:
                pattern = r"system time:(.*)"
                sim_time = re.findall(pattern, log_str)
                return sim_time[0]
            except (KeyError, IndexError) as e:
                # error during simulation, sim_time not printed
                raise SimulationUnsuccessful(
                    "COOS Simulation of the sweep "
                    + sweep.name
                    + " with the hash "
                    + sweep.get_hash()
                    + " failed! An error was found! Director is "
                    + str(sim_folder)
                    + "."
                ) from e

    def get_df(self, hdf_data, group, key):
        """Return the pandas prepresentation of a COOS hdf5 table."""
        if group is None:
            data_ = hdf_data[key]
        else:
            try:
                data_ = hdf_data[group + "/" + key]
            except KeyError:
                raise IOError

        cols = {}
        if group is None:
            for col, name in data_.attrs.items():
                cols[int(col.replace("col", ""))] = name.decode("ascii")
        else:
            group = hdf_data[group]
            for col, name in group.attrs.items():
                cols[int(col.replace("col", ""))] = name.decode("ascii")

        rows = np.linspace(0, data_.shape[0] - 1, data_.shape[0])
        try:
            columns = [cols[i] for i in range(len(cols))]
        except KeyError:
            dummy = 1
        return DataFrame(data_[:, : len(columns)], index=rows, columns=columns)

    def import_output_data(self, sweep, delete_sim_results=False):
        r"""Read the output files that have been produced while simulating sweep and attach them to self.db.

        This is done by scanning the input file for "\*.elpa" files and (for internal data) for "int" files.

        Parameters
        ----------
        sweep  :  :class:`DMT.core.sweep.Sweep`
            Sweep that has been simulated for the desired output files.

        Returns
        ----------
        output_files : [string]
            List of strings that contain the full path to the output files.
        delete_sim_results : {False, True}, optional
            If True, the simulation folder is deleted after reading.

        Notes
        ------
        .. todo:: Add more column renaming and resorting here!
        """
        # list_elpa_files = re.findall(
        #     r"\&ELEC_DATA file_name='(.*?\.elpa)'",
        #     str_inp_file
        # )

        sim_folder = self.get_sim_folder(sweep)
        key = self.get_sweep_key(sweep)

        try:
            df_coos = h5py.File(
                os.path.join(sim_folder, "simulation_data.h5")
            )  # hdf5 simulation data
            df_iv = self.get_df(df_coos, None, "iv")
            try:
                df_cap = self.get_df(df_coos, None, "cap")
            except:
                df_cap = None
            dfs_laplace = []
            if "laplace" in df_coos.keys():  # have laplace files
                laplace_keys = list(df_coos["laplace"].keys())
                for i in range(len(laplace_keys)):
                    dfs_laplace.append(self.get_df(df_coos, "laplace", laplace_keys[i]))
            dfs_inqu = []
            if "inqu" in df_coos.keys():  # have inqu files
                inqu_keys = list(df_coos["inqu"].keys())
                for i in range(len(inqu_keys)):
                    try:
                        dfs_inqu.append(self.get_df(df_coos, "inqu", "op" + str(i + 1)))
                    except:
                        pass
            dfs_acinqu = []
            if "acinqu" in df_coos.keys():  # have acinqu files
                acinqu_keys = list(df_coos["acinqu"].keys())
                for acinqu_key in acinqu_keys:
                    try:
                        dfs_acinqu.append(self.get_df(df_coos, "acinqu", acinqu_key))
                    except:
                        pass

            dfs_ac = []
            if "ac" in df_coos.keys():  # have ac files
                ac_keys = list(df_coos["ac"].keys())
                for i in range(len(ac_keys)):
                    dfs_ac.append(self.get_df(df_coos, "ac", "op" + str(i + 1)))

            df_coos.close()

            # add the inqu and acinqu files
            for i, df_inqu in enumerate(dfs_inqu):
                key_ = self.join_key(key, "op" + str(i + 1)) + "_inqu"
                self.data[key_] = df_inqu

            # add the inqu and acinqu files
            for i, df_laplace in enumerate(dfs_laplace):
                key_ = self.join_key(key, "laplace" + "_" + laplace_keys[i].upper())
                self.data[key_] = df_laplace

            # add the acinqu files
            for acinqu_key, df_acinqu in zip(acinqu_keys, dfs_acinqu):
                key_ = self.join_key(key, "acinqu_" + acinqu_key)
                self.data[key_] = df_acinqu

            # add the cap files
            if df_cap is not None:
                key_ = self.join_key(key, "cap")
                self.data[key_] = df_cap

            ac = False
            # read in the iv data
            pd.options.mode.chained_assignment = None  # default='warn'
            if len(dfs_ac) > 1:
                # first we sort by n_op
                dfs_temp = []
                n = 0
                for df_ac in dfs_ac:
                    # read in ac df
                    df_dc = df_iv.iloc[[n]]
                    # extend ac df with dc data
                    for col_dc in df_iv.columns:
                        if col_dc not in df_ac.columns:
                            df_ac.loc[:, col_dc] = df_iv.loc[n, col_dc]  # take over values from DC

                    # extend dc df with ac data
                    for col_ac in df_ac.columns:
                        if col_ac not in df_dc.columns:
                            df_dc.loc[:, col_ac] = 0  # set AC values to zero in DC

                    dfs_temp.append(df_dc)
                    dfs_temp.append(df_ac)

                    n = n + 1

                # create new big dataframe with DC and AC data
                df_iv = pd.concat(dfs_temp)

            # convert columns to specifiers
            df_iv = df_iv.real2cmplx()
            for _col in df_iv.columns:
                df_iv.rename(
                    columns={_col: get_specifier_from_string(_col, nodes=self.nodes)}, inplace=True
                )

            if not df_iv.columns.is_unique:
                df_iv = df_iv.loc[:, ~df_iv.columns.duplicated()]

            try:
                freqs = np.unique(df_iv[specifiers.FREQUENCY].to_numpy())
                ac = True
                if len(freqs) == 2:
                    df_iv = df_iv[df_iv[specifiers.FREQUENCY] == np.max(freqs)]

                # ensure some columns
                df_iv.ensure_specifier_column(specifiers.CAPACITANCE + "B" + "E", ports=["B", "C"])
                df_iv.ensure_specifier_column(specifiers.CAPACITANCE + "B" + "C", ports=["B", "C"])
                df_iv.ensure_specifier_column(specifiers.TRANSIT_FREQUENCY, ports=["B", "C"])
                df_iv.ensure_specifier_column(specifiers.TRANSCONDUCTANCE, ports=["B", "C"])
                df_iv.ensure_specifier_column(
                    specifiers.SS_PARA_Y + "C" + "B" + sub_specifiers.REAL, ports=["B", "C"]
                )
            except KeyError:
                pass

            if (
                ac and len(dfs_inqu) > 0
            ):  # only one frequency simulated => post process (maybe also check for 1D)
                if not len(freqs) == 2:
                    raise IOError
                # post processing
                # 1 general stuff
                x = dfs_inqu[0]["X"].to_numpy()
                d = dfs_inqu[0][specifiers.NET_DOPING].to_numpy()
                junctions = (
                    np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0] + 1
                )  # detect sign changes
                if junctions != []:  # no junction found
                    xje = x[junctions[0]]
                    xjc = x[junctions[1]]

                    # sum of charge
                    qp = np.zeros(len(df_iv))
                    qn = np.zeros(len(df_iv))
                    for i_row, _row in enumerate(df_iv.iterrows()):
                        try:
                            key_inqu = next(
                                _key
                                for _key in self.data.keys()
                                if "_inqu" in _key and "op" + str(i_row + 1) in _key
                            )
                        except:
                            continue
                        df_inqu = self.data[key_inqu]
                        qn[i_row] = np.trapz(df_inqu["N"], df_inqu["X"])
                        qp[i_row] = np.trapz(df_inqu["P"], df_inqu["X"])

                    df_iv["Q|N"] = qn
                    df_iv["Q|P"] = qp

                    # where inqu df is required for every op
                    gm = np.array(df_iv[specifiers.TRANSCONDUCTANCE])
                    tau_e = np.ones(len(df_iv))
                    tau_be = np.ones(len(df_iv))
                    tau_b = np.ones(len(df_iv))
                    tau_c = np.ones(len(df_iv))
                    tau_bc = np.ones(len(df_iv))

                    try:

                        for i_row, row in enumerate(df_iv.iterrows()):
                            key_inqu = next(
                                _key
                                for _key in self.data.keys()
                                if "_inqu" in _key and "op" + str(i_row + 1) in _key
                            )
                            key_ac_inqu = next(
                                _key
                                for _key in self.data.keys()
                                if "acinqu" in _key
                                and "op" + str(i_row + 1) in _key
                                and "port1" in _key
                            )

                            # get the necessary data
                            df_ac_inqu_i = self.data[key_ac_inqu]
                            dn_dic = df_ac_inqu_i["re_d_n_x"].to_numpy() / gm[i_row + 1]
                            dp_dic = df_ac_inqu_i["re_d_p_x"].to_numpy() / gm[i_row + 1]
                            droh_dic = dp_dic - dn_dic
                            # transit time
                            changes = (
                                np.where(np.sign(droh_dic[:-1]) != np.sign(droh_dic[1:]))[0] + 1
                            )
                            index_be = changes[np.argmin(np.abs(changes - junctions[0]))]
                            index_bc = changes[np.argmin(np.abs(changes - junctions[1]))]
                            xbe = x[index_be]
                            xbc = x[index_bc]

                            tau = np.zeros(len(x))
                            for j, x_ in enumerate(x):
                                if x_ <= xbe:
                                    tau[j] += np.trapz(dp_dic[:j], x[:j])
                                    tau[j] += np.trapz(dn_dic[:j], x[:j]) - np.trapz(
                                        dp_dic[:j], x[:j]
                                    )
                                elif x_ <= xbc:
                                    tau[j] += np.trapz(dn_dic[:j], x[:j])
                                else:
                                    tau[j] += np.trapz(dp_dic[:j], x[:j])
                                    tau[j] += np.trapz(dn_dic[:j], x[:j]) - np.trapz(
                                        dp_dic[:j], x[:j]
                                    )

                            tau = tau * constants.P_Q

                            tau_e[i_row] = np.trapz(dp_dic[:index_be], x[:index_be]) * constants.P_Q
                            tau_be[i_row] = (
                                np.trapz(dn_dic[:index_be], x[:index_be]) * constants.P_Q
                                - tau_e[i_row]
                            )
                            tau_b[i_row] = (
                                np.trapz(dn_dic[index_be:index_bc], x[index_be:index_bc])
                                * constants.P_Q
                            )
                            tau_c[i_row] = np.trapz(dp_dic[index_bc:], x[index_bc:]) * constants.P_Q
                            tau_bc[i_row] = (
                                np.trapz(dn_dic[index_bc:], x[index_bc:]) * constants.P_Q
                                - tau_c[i_row]
                            )

                            dm_dic = np.where(dn_dic < dp_dic, dn_dic, dn_dic)

                            # for j in range(len(tau)):
                            #     tau[j] = constants.P_Q * np.trapz(dm_dic[:j], x[:j])

                            self.data[key_inqu][specifiers.TRANSIT_TIME] = tau

                        df_iv["tau_e"] = tau_e
                        df_iv["tau_be"] = tau_be
                        df_iv["tau_b"] = tau_b
                        df_iv["tau_bc"] = tau_bc
                        df_iv["tau_c"] = tau_c

                    except:
                        pass

            key_iv = self.join_key(key, "iv")
            self.data[key_iv] = df_iv

            logging.info(
                "Read the COOS simulation output data of the sweep %s. \nThe simulation folder is %s",
                sweep.name,
                sim_folder,
            )
        except KeyError:
            pass

        # charge partitioning
        # if (
        #     ac and len(dfs_inqu) > 0
        # ):  # only one frequency simulated => post process (maybe also check for 1D)
        #     if not len(freqs) == 2:
        #         raise IOError
        #     # post processing
        #     # 1 general stuff
        #     x = dfs_inqu[0]["X"].to_numpy()
        #     d = dfs_inqu[0][specifiers.NET_DOPING].to_numpy()

        #     junctions = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0] + 1  # detect sign changes
        #     if junctions != []:  # no junction found
        #         xje = x[junctions[0]]
        #         xjc = x[junctions[1]]

        #         # sum of charge
        #         qp = np.zeros(len(df_iv))
        #         qn = np.zeros(len(df_iv))
        #         for i_row, _row in enumerate(df_iv.iterrows()):
        #             try:
        #                 key_inqu = next(
        #                     _key
        #                     for _key in self.data.keys()
        #                     if "_inqu" in _key and "op" + str(i_row + 1) in _key
        #                 )
        #             except:
        #                 continue
        #             df_inqu = self.data[key_inqu]
        #             qn[i_row] = np.trapz(df_inqu["N"], df_inqu["X"])
        #             qp[i_row] = np.trapz(df_inqu["P"], df_inqu["X"])

        #         df_iv["Q|N"] = qn
        #         df_iv["Q|P"] = qp

        #         # where inqu df is required for every op
        #         gm = np.array(df_iv[specifiers.TRANSCONDUCTANCE])
        #         tau_e = np.ones(len(df_iv))
        #         tau_be = np.ones(len(df_iv))
        #         tau_b = np.ones(len(df_iv))
        #         tau_c = np.ones(len(df_iv))
        #         tau_bc = np.ones(len(df_iv))

        #         try:

        #             for i_row, row in enumerate(df_iv.iterrows()):
        #                 key_inqu = next(
        #                     _key
        #                     for _key in self.data.keys()
        #                     if "_inqu" in _key and "op" + str(i_row + 1) in _key
        #                 )
        #                 key_ac_inqu = next(
        #                     _key
        #                     for _key in self.data.keys()
        #                     if "port1_acinqu" in _key and "op" + str(i_row + 1) in _key
        #                 )

        #                 # get the necessary data
        #                 df_ac_inqu_i = self.data[key_ac_inqu]
        #                 dn_dic = df_ac_inqu_i["re_d_n_x"].to_numpy() / gm[i_row]
        #                 dp_dic = df_ac_inqu_i["re_d_p_x"].to_numpy() / gm[i_row]
        #                 droh_dic = dp_dic - dn_dic
        #                 # transit time
        #                 changes = np.where(np.sign(droh_dic[:-1]) != np.sign(droh_dic[1:]))[0] + 1
        #                 index_be = changes[np.argmin(np.abs(changes - junctions[0]))]
        #                 index_bc = changes[np.argmin(np.abs(changes - junctions[1]))]
        #                 xbe = x[index_be]
        #                 xbc = x[index_bc]

        #                 tau = np.zeros(len(x))
        #                 for j, x_ in enumerate(x):
        #                     if x_ <= xbe:
        #                         tau[j] += np.trapz(dp_dic[:j], x[:j])
        #                         tau[j] += np.trapz(dn_dic[:j], x[:j]) - np.trapz(dp_dic[:j], x[:j])
        #                     elif x_ <= xbc:
        #                         tau[j] += np.trapz(dn_dic[:j], x[:j])
        #                     else:
        #                         tau[j] += np.trapz(dp_dic[:j], x[:j])
        #                         tau[j] += np.trapz(dn_dic[:j], x[:j]) - np.trapz(dp_dic[:j], x[:j])

        #                 tau = tau * constants.P_Q

        #                 tau_e[i_row] = np.trapz(dp_dic[:index_be], x[:index_be]) * constants.P_Q
        #                 tau_be[i_row] = (
        #                     np.trapz(dn_dic[:index_be], x[:index_be]) * constants.P_Q - tau_e[i_row]
        #                 )
        #                 tau_b[i_row] = (
        #                     np.trapz(dn_dic[index_be:index_bc], x[index_be:index_bc])
        #                     * constants.P_Q
        #                 )
        #                 tau_c[i_row] = np.trapz(dp_dic[index_bc:], x[index_bc:]) * constants.P_Q
        #                 tau_bc[i_row] = (
        #                     np.trapz(dn_dic[index_bc:], x[index_bc:]) * constants.P_Q - tau_c[i_row]
        #                 )

        #                 dm_dic = np.where(dn_dic < dp_dic, dn_dic, dn_dic)

        #                 for j in range(len(tau)):
        #                     tau[j] = constants.P_Q * np.trapz(dm_dic[:j], x[:j])

        #                 self.data[key_inqu][specifiers.TRANSIT_TIME] = tau

        #             df_iv["tau_e"] = tau_e
        #             df_iv["tau_be"] = tau_be
        #             df_iv["tau_b"] = tau_b
        #             df_iv["tau_bc"] = tau_bc
        #             df_iv["tau_c"] = tau_c

        #         except:
        #             pass

        key_iv = self.join_key(key, "iv")
        self.data[key_iv] = df_iv
        pd.options.mode.chained_assignment = "warn"  # default='warn'

        logging.info(
            "Read the COOS simulation output data of the sweep %s. \nThe simulation folder is %s",
            sweep.name,
            sim_folder,
        )
        if delete_sim_results:
            self.delete_sim_results(sweep)

    def get_bias_info(self, sweep, sub_sweep):
        # get contact
        nodes = sub_sweep.var_name.nodes
        if len(nodes) > 1:
            raise IOError("DMT -> DutCOOS: currently only potential sweeps are supported.")

        try:
            cont_name = "'" + nodes[0] + "'"
        except IndexError:
            cont_name = "'" + str(sub_sweep.var_name)[0] + "'"

        if sub_sweep.sweep_type == "LIN":
            bias_fun = "'LIN'"
            bias_info = {
                "cont_name": cont_name,
                "bias_fun": bias_fun,
            }
        elif sub_sweep.sweep_type[0:3] == "CON":
            bias_fun = "'LIN'"  # we convert to list, to support list=1 setting used by DMT in COOS
            bias_info = {
                "cont_name": cont_name,
                "bias_fun": bias_fun,
                "bias_val": [sub_sweep.value_def[0], sub_sweep.value_def[0], len(bias_val)],
            }
        elif sub_sweep.sweep_type[0:4] == "SYNC":
            # find master sweep
            for other_sub_sweep in sweep.sweepdef:
                if other_sub_sweep.var_name == sub_sweep.master_var:
                    bias_info = self.get_bias_info(sweep, other_sub_sweep)
                    bias_info["cont_name"] = cont_name
                    if bias_info["bias_fun"] == "'LIN'":
                        bias_info["bias_val"][0] = bias_info["bias_val"][0] + sub_sweep.offset
                        bias_info["bias_val"][1] = bias_info["bias_val"][1] + sub_sweep.offset
                    else:
                        raise NotImplementedError
                    dummy = 1
                    break

        elif sub_sweep.sweep_type[0:4] == "LIST":
            bias_fun = "'TAB'"  # we convert to list, to support list=1 setting used by DMT in COOS
            bias_info = {"cont_name": cont_name, "bias_fun": bias_fun, "bias_val": sub_sweep.values}
        else:
            raise NotImplementedError

        return bias_info

    def get_mobility(self, semiconductor, valley, field, temperature, doping, grading):
        if not DutCOOS.inited:
            self.init_coos()

        mob = np.zeros_like(field)
        for i in range(len(field)):
            if doping > 0:
                mob[i] = COOS.coos_py.get_mobility_py(
                    semiconductor, valley, field[i], 1, 1, 1, temperature, 0, doping, 0, grading
                )
                # def get_mobility_py(semi_name     ,valley,f       , ec_l, ec_r, dim, t, dens, don, acc,  grad):
            else:
                mob[i] = COOS.coos_py.get_mobility_py(
                    semiconductor, valley, field[i], 1, 1, 1, temperature, 0, 0, -doping, grading
                )

        return mob

    def get_intervalley_rate(self, semiconductor, valley_1, valley_2, field, temperature, doping):
        if not DutCOOS.inited:
            self.init_coos()

        rec = np.zeros_like(field)
        for i in range(len(field)):
            rec[i] = COOS.coos_py.get_intervalley_rate_py(
                semiconductor, valley_1, valley_2, field[i], doping, temperature
            )

        return rec

    def get_mobility_paras(self, semi, valley):
        if not DutCOOS.inited:
            self.init_coos()

        paras = COOS.coos_py.get_mobility_paras_py(semi, valley)
        return paras

    def get_recombination_paras(self, semi, rec_type):
        if not DutCOOS.inited:
            self.init_coos()

        paras = COOS.coos_py.get_recombination_paras_py(semi, rec_type)
        return paras

    def set_mobility_paras(self, semi, valley, paras):
        if not DutCOOS.inited:
            self.init_coos()

        COOS.coos_py.set_mobility_paras_py(semi, valley, paras)
        return

    def set_recombination_paras(self, semi, paras):
        if not DutCOOS.inited:
            self.init_coos()

        COOS.coos_py.set_recombination_paras_py(semi, paras)
        return

    def init_coos(self):
        DutCOOS.inited = True
        # load structure
        inp_str = makeinp(self._inp_structure)
        # load sweep
        # create a sweep
        sweepdef = []
        n = 1
        for region_def in self._inp_structure["REGION_DEF"]:
            if "cont_name" in region_def.keys():
                sweepdef.append(
                    {
                        "var_name": specifiers.VOLTAGE + region_def["cont_name"],
                        "sweep_order": n,
                        "sweep_type": "CON",
                        "value_def": [0],
                    }
                )
                n = n + 1
        outputdef = [
            specifiers.VOLTAGE + ["B", "C"],
            specifiers.CURRENT + "C",
            specifiers.CURRENT + "B",
            "internal",
            "QU",
            "Q_Y11E",
            "Q_Y22E",
        ]
        othervar = {"TEMP": 300}
        sweep = Sweep("gummel", sweepdef=sweepdef, outputdef=outputdef, othervar=othervar)
        inp_str = self.make_input(sweep)

        home = os.path.expanduser("~")
        tmp_path = os.path.join(home, "tmp", "coos_inp.din")
        inp_file = open(tmp_path, "w+")
        inp_file.write(inp_str)
        inp_file.close()
        COOS.coos_py.init(inp_file.name)

    def scale_modelcard(self, *_args, **_kwargs):
        """COOS currently has no scaling"""
        pass


def getITRSHBT(
    hbt_fun=None,
    fermi=False,
    nl=False,
    sat=False,
    tn=True,
    no_inqu=False,
    lambda_e=None,
    xj_l=None,
    mu_min_a=None,
    mu_min_d=None,
):
    """Return a DutCOOS for ITRS HBTS. Only for SiGe HBTs.
    Input
    -----
    hbt_fun : callable
        Function that returns a COOS HBT definition.
    fermi : bool
        If True: use Fermi-Dirac statistics, else Boltzmann
    nl : bool
        If True: use Non local energy model.
    sat : bool
        If True: use velocity saturation model.
    tn : bool
        If True: use ET model, else DD model.

    Returns
    --------
    dut_coos : DutCOOS
        A DMT.COOS.DutCOOS object ready for simulation.
    """
    if hbt_fun is None:
        raise IOError("You need to provide a function that returns a valid COOS HBT definition.")

    inp = hbt_fun()

    if no_inqu:
        inp["OUTPUT"]["inqu_lev"] = 0

    if fermi:
        for i, semi in enumerate(inp["SEMI"]):
            inp["SEMI"][i]["fermi"] = 1

    if nl:  # todo: should depend on profile
        inp["NON_LOCAL"] = {}
        inp["NON_LOCAL"]["type"] = "simple"
        inp["NON_LOCAL"]["lambda"] = lambda_e
        inp["NON_LOCAL"]["xj_l"] = xj_l
        # increase velocity sat.
        # for l, mob in enumerate(inp["MOB_DEF"]):
        #     if inp["MOB_DEF"][l]["valley"] == "X":
        #         inp["MOB_DEF"][l]["v_sat"] = inp["MOB_DEF"][l]["v_sat"] * 1.5
    if tn:
        inp["DD"]["tn"] = 1

    if not sat:
        for i, _mob in enumerate(inp["MOB_DEF"]):
            inp["MOB_DEF"][i]["hc_scat_type"] = "default"

    if mu_min_a is not None:
        # decrease lattice mobility
        for l, mob in enumerate(inp["MOB_DEF"]):
            if inp["MOB_DEF"][l]["valley"] == "X":
                inp["MOB_DEF"][l]["mu_min_a"] = inp["MOB_DEF"][l]["mu_min_a"] * mu_min_a

    if mu_min_d is not None:
        # decrease lattice mobility
        for l, mob in enumerate(inp["MOB_DEF"]):
            if inp["MOB_DEF"][l]["valley"] == "X":
                inp["MOB_DEF"][l]["mu_min_d"] = inp["MOB_DEF"][l]["mu_min_d"] * mu_min_d
    # if te:
    #     inp["THERMIONIC_EMISSION"] = {}
    #     inp["THERMIONIC_EMISSION"]["x"] = 32e-9

    inp = turn_off_recombination(inp)

    return DutCOOS(
        None,
        DutType.npn,
        inp,
        reference_node="E",
        list_copy=os.path.join(
            "/home/markus/Documents/Gitprojects/dissertation/py_scripts/tsc250_tcad/teledyne_profile.h5"
        ),
    )
