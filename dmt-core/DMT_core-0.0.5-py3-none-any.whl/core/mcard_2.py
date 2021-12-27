""" Base class to handle verilog-a modelcards.

Author: Mario Krattenmacher | Mario.Krattenmacher@tu-dresden.de
Author: Markus Müller       | Markus.Mueller3@tu-dresden.de
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
import json
import warnings
from DMT.core import unit_registry
from DMT.core.mc_parameter import McParameterComposition, McParameter
from importlib import import_module
from typing import Optional, Tuple, Dict, Union, List
from types import ModuleType
from semver import VersionInfo


unit_converter = {
    "s": unit_registry.second,
    "A": unit_registry.ampere,
    "A^2s": unit_registry.ampere * unit_registry.ampere * unit_registry.second,
    "V": unit_registry.volt,
    "1/V": 1 / unit_registry.volt,
    "K": unit_registry.kelvin,
    "1/K": 1 / unit_registry.kelvin,
    "C": unit_registry.celsius,
    "Ohm": unit_registry.ohm,
    "F": unit_registry.farad,
    "Coul": unit_registry.coulomb,
    "K/W": unit_registry.kelvin / unit_registry.watt,
    "J/W": unit_registry.joule / unit_registry.watt,
    "V/K": unit_registry.volt / unit_registry.kelvin,
    "1/K^2": 1 / unit_registry.kelvin / unit_registry.kelvin,
    "Ws/K": unit_registry.watt * unit_registry.second / unit_registry.kelvin,
    "M^(1-AF)": unit_registry.dimensionless,
    "": unit_registry.dimensionless,
}

CURRENT_SEMVER = VersionInfo(major=0, minor=1)
OLDEST_COMPATIBLE_SEMVER = VersionInfo(major=0, minor=1)


class MCard(McParameterComposition):
    """DMT class that implements attributes and methods that are common between all ModelCards such as HICUM and BSIM.

    Parameters
    -----------
    nodes_list      :  tuple(str)
        Port list for this model.
    model_version   :  str
        Version of the model.
    list_opvars : list
        Names of all the operation point variables available from the analyzed VA-Code.
    semvar:

    Attributes
    -----------
    nodes_list : tuple(str)
        Port list for this model.
    model_version : float
        Version of the model.
    list_opvars : list
        Names of all the operation point variables aviable from the analyzed VA-Code.
    """

    def __init__(
        self,
        nodes_list: Optional[Tuple[str]] = None,
        model_version: Optional[str] = None,
        vae_module: Optional[str] = None,
    ):
        super().__init__()

        self.nodes_list = nodes_list
        self.model_version = model_version
        self.vae_module = vae_module

    @property
    def vae_module(self) -> Optional[ModuleType]:
        """

        A python module that contains information and functions describing the model.
        This module is compiled from the VerilogA sourcefile of the model using `VerilogAE <https://dspom.gitlab.io/verilogae/>`__ and needs to be manually set.
        DMT bundles packages containing these modules for the models it has extensive support for  (currently HICUM L2 and L0)


        """
        if self._vae_module is None:
            return None
        try:
            return import_module(self._vae_module)
        except ImportError:
            return None

    @vae_module.setter
    def vae_module(self, val: str):
        """
        Sets the `VerilogAE <https://dspom.gitlab.io/verilogae/>`__ module associated with this Modelcard.
        The value of this attribute can only be set to a string while the return value is the imported module.
        If you wish to access the string again use the `_vae_module` field.

        Parameters
        ----------
        val     : ModuleType
            The name of the VerilogAE module as a string
        """
        if val is None:
            warnings.warn(
                "No VerilogAE module was set for this modelcard! Detailed model information may not be available."
            )
        else:
            try:
                vae_module = import_module(val)
                self.update_from_vae_module(vae_module)
            except ImportError as err:
                print(err)
                warnings.warn(
                    "The VerilogAE module {} was not found! Parameter boundries, units and default values and Operating Point variables will not be available.".format(
                        val
                    )
                )
                self._vae_module = None
                return
            except AttributeError as err:
                print(err)
                warnings.warn(
                    "The VerilogAE module {} seems to be missing required attributes. It may be outdated (VerilogAE 0.7.2+ is required). Parameter boundries, units and default values and Operating Point variables will not be available. If you are using DMT_other you can install up to date models with pip install -e .[vae-models].".format(
                        val
                    )
                )
                self._vae_module = None
                return

        self._vae_module = val

    def update_from_vae_module(self, vae_module: ModuleType):
        """
        Updates the modelcard with information such as parameter boundries and default values, nodes, modules and op vars
        obtained from the Verilog-A source code using `VerilogAE <https://dspom.gitlab.io/verilogae/>`__.

        Parameters
        ----------
        vae_module  : ModuleType
            The module generated by VerilogAE that described the Verilog-A model associated with this modelcard
        """

        for para_name, para_properties in vae_module.modelcard.items():
            try:
                para = next(para for para in self.paras if para.name == para_name)
                ty = type(para_properties.default)

                if para.minval > para_properties.min:
                    para.minval = para_properties.min
                    para.inc_min = para_properties.min_inclusive

                if para.maxval < para_properties.max:
                    para.maxval = para_properties.max
                    para.inc_max = para_properties.max_inclusive

                para.unit = unit_converter[para_properties.unit]
                para.description = para_properties.description
                para.group = para_properties.group
                para.val_type = ty
            except StopIteration:
                para = McParameter(
                    para_name,
                    value=para_properties.default,
                    minval=para_properties.min,
                    maxval=para_properties.max,
                    value_type=type(para_properties.default),
                    inc_min=para_properties.min_inclusive,
                    inc_max=para_properties.max_inclusive,
                    group=para_properties.group,
                    unit=unit_converter[para_properties.unit],
                    description=para_properties.description,
                )
                self.add(para)

    def json_dict(
        self,
    ) -> Dict[str, Dict[str, Union[float, int, str, bool, List[Union[float, int, str]]]]]:
        """Returns a dict with serializeable content for the json file to create."""

        info_dict = super().json_dict()
        info_dict["__SEMVER__"] = str(CURRENT_SEMVER)

        if self.model_version:
            info_dict["__MODEL_VERSION__"] = self.model_version

        if self.nodes_list:
            info_dict["__NODES__"] = self.nodes_list

        if self._vae_module:
            info_dict["__VAE_MODULE__"] = self._vae_module

        return info_dict

    @classmethod
    def loads_json(cls, dict_parameter: Dict[str]):
        """Creates a McCard from a dictionary obtained by a json.load."""
        if "__SEMVER__" in dict_parameter:
            if VersionInfo.parse(dict_parameter["__SEMVER__"]) > OLDEST_COMPATIBLE_SEMVER:
                vae_module = dict_parameter.get("__VAE_MODULE__")
                nodes_list = dict_parameter.get("__NODES__")
                model_version = dict_parameter.get("__MODEL_VERSION__")

                MCard(vae_module=vae_module, model_version=model_version, nodes_list=nodes_list)
        else:
            raise IOError("DMT->MCard: The given dict has no __MCard__ key!")

    def __eq__(self, other):
        """Allows comparing 2 model cards using mc1 == mc2

        mc1 != mc2 is included per default using python3:
        https://docs.python.org/3/reference/datamodel.html#object.__ne__

        """
        if isinstance(other, MCard):
            if self.model_version == other.model_version:
                # class, version and parameters equal is enough in most cases!
                return self.eq_paras(other)
            else:
                return False

        return NotImplemented
