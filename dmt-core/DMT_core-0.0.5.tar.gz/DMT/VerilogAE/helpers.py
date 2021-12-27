""" Helpers to integrate VerilogAE into DMT
"""
import numpy as np
from inspect import signature
from collections import OrderedDict
from DMT.core import MCard, McParameter
from DMT.core import unit_registry as ur

# VAE models known to DMT
HICUM_L2 = "HICUM_L2"
SGP = "SGP"
HICUM_L0 = "HICUM_L0"


def get_param_list(meq_function, all_parameters=False, info=None):
    """Returns a list with the McParameter names for the given callable in correct order, assuming that only the top-most function is not from VerilogAE

    Parameters
    -----------
    meq_function : function
        Function of the model equation which shall be used.
    all_parameters : {False, True}, optional
        If True, the independent_vars are ignored and the full parameter list is returned.

    Returns
    --------
    params : list
        List of parameters for this function
    """
    if info is None:
        info = {}

    try:
        sig = signature(meq_function)
        func_params = list(sig.parameters)

        # only kwargs : https://stackoverflow.com/questions/196960/can-you-list-the-keyword-arguments-a-function-receives
        func_params = [p.name for p in sig.parameters.values() if (p.kind == p.KEYWORD_ONLY)]
    except TypeError:
        # if meq_function is directly a verilogae function
        func_params = meq_function.parameters

    for attr in ["depends", "depends_optional", "independent_vars"]:
        if not attr in info:
            info[attr] = tuple()

    if not isinstance(info["depends"], tuple):
        raise NotImplementedError("MUST be tuple! Error in " + meq_function.__name__ + "_info")
    if not isinstance(info["depends_optional"], tuple):
        raise NotImplementedError("MUST be tuple! Error in " + meq_function.__name__ + "_info")
    if not isinstance(info["independent_vars"], tuple):
        raise NotImplementedError("MUST be tuple! Error in " + meq_function.__name__ + "_info")

    for dependence in info["depends"]:
        if isinstance(dependence, str):
            func_params.append(dependence)
        else:
            try:
                func_params += dependence.parameters
            except AttributeError:
                func_params += get_param_list(dependence, all_parameters=all_parameters)

    # unique it!
    func_params = list(OrderedDict.fromkeys(func_params))

    if all_parameters:
        func_params = list(OrderedDict.fromkeys(func_params))
        return func_params

    # delete the parameters which are independent and without the opti_params
    params = []
    for param in func_params:
        if not param in info["independent_vars"]:
            params.append(param)

    return params


# TODO remove this function as it is now integrated into the modelcard
unit_converter = {
    "s": ur.second,
    "A": ur.ampere,
    "A^2s": ur.ampere * ur.ampere * ur.second,
    "V": ur.volt,
    "1/V": 1 / ur.volt,
    "K": ur.kelvin,
    "1/K": 1 / ur.kelvin,
    "C": ur.celsius,
    "Ohm": ur.ohm,
    "F": ur.farad,
    "Coul": ur.coulomb,
    "K/W": ur.kelvin / ur.watt,
    "J/W": ur.joule / ur.watt,
    "V/K": ur.volt / ur.kelvin,
    "1/K^2": 1 / ur.kelvin / ur.kelvin,
    "Ws/K": ur.watt * ur.second / ur.kelvin,
    "M^(1-AF)": ur.dimensionless,
    "": ur.dimensionless,
}


def get_modelcard(model, nodes, default_circuit):
    """Returns a DMT modelcard from the VAE compiled model.

    Better is to read the va_code to generate the proper mc object...
    Advantages: Correct saving using json, groups, and other attributes.

    Input
    -----
    model : VAE model
        Compiled VAE model.

    Output
    ------
    modelcard : DMT.Mcard
        DMT modelcard.

    Todo
    -----
    Pascal can you please check this.
    """
    vae_modelcard = model.modelcard
    dmt_modelcard = MCard(nodes, "Q", "dummy", "1.0")
    # add properties needed for circuit simulation
    dmt_modelcard.default_circuit = default_circuit
    for para_name, para_properties in vae_modelcard.items():
        try:
            group = (para_properties.group,)
        except AttributeError:
            group = None
        try:
            unit = (unit_converter[para_properties.unit],)
        except KeyError:
            unit = None
        para_dmt = McParameter(
            para_name,
            value=para_properties.default,
            minval=para_properties.min,
            maxval=para_properties.max,
            value_type=np.dtype(type(para_properties.default)),
            inc_min=para_properties.min_inclusive,
            inc_max=para_properties.max_inclusive,
            exclude=None,  # ? really needed
            group=group,
            unit=unit,
            description=para_properties.description,
        )
        dmt_modelcard.add(para_dmt)

    try:
        for opvar_name, opvar_info in model.op_vars.items():
            dmt_modelcard.list_opvars.append(opvar_name)
            setattr(
                dmt_modelcard,
                "opvar_" + opvar_name,
                {
                    "desc": opvar_info.description,
                    "unit": opvar_info.unit,
                    "data_type": np.float64,  # TODO get data_type from VAE
                },
            )
    except AttributeError:
        pass

    # instead of inheriting we monkey patch the required methods...
    # should be moved somewhere else

    return dmt_modelcard


def get_dmt_model(vae_module, model_type, version):
    """Retrieving a DMT fitting model for XSteps from a VAE compiled VA-Code.

    This function also adds the needed attributes.

    Parameter
    ----------
    vae_module : module
        VAE compiled and installed VA-Code
    model_type : {'HICUM_L0', 'HICUM_L2'}
        Currently supporting only the two HICUM levels
    version : float
        Version of the compiled va-code

    Returns
    --------
    model : module
        The VAE module with added attributes

    """
    model = vae_module

    if model_type not in [HICUM_L0, HICUM_L2, SGP]:
        raise IOError("DMT->VerilogAE: Currently only 'HICUM' is supported by VAE+DMT.")

    model.model_type = model_type
    model.version = version
    if "HICUM" in model_type:
        if "L0" in model_type:
            model.hicum_level = 0
        elif "L2" in model_type:
            model.hicum_level = 2
        else:
            raise IOError("DMT->VerilogAE: The HICUM level must be inside the model_type!")
    elif "SGP" in model_type:
        model.hicum_level = 0  # Markus: why do we need that
    else:
        raise IOError("DMT->VerilogAE: Currently only 'HICUM' is supported")

    return model


# if __name__ == "__main__":
#     from DMT.hl2 import McHicum
#     dmt_modelcard = McHicum()
#     import hl2 #VAE module
#     vae_modelcard = get_modelcard(hl2, ['B','E','C','S'], 'common_emitter')

#     for para in vae_modelcard:
#         if not para.name in dmt_modelcard.name:
#             raise IOError('Parameter ' + para.name + ' not in dmt_modelcard that is hand implemented.')
#         else:
#             print('ok')
