# write COOS input file ... todo: later replace by proper wrapper
# DMT is so awesome!
from DMT.core import DutType, DutLib, DutMeas, DataFrame, specifiers, MCard, McParameter, Technology
from DMT.extraction import Model, Xtraction
from DMT.gui import XtractionGUI
from DMT.COOS import Si, init_user, DutCOOS, sige_hbt, XVelocityField

import COOS
import numpy as np
import os
import copy

# create a COOS made from Silicon
inp = sige_hbt("coos")
dut_coos = DutCOOS(None, DutType.npn, inp, reference_node="E")

# get mobility from COOS
f = np.linspace(0, 20e5, 21)
for i in range(3):
    mob = dut_coos.get_mobility("Si", "X", f, 300, 0, 0)
    print(mob)

df = DataFrame()
df[specifiers.FIELD] = f
df[specifiers.MOBILITY] = mob
df[specifiers.VELOCITY] = mob * f
df[specifiers.NET_DOPING] = 0
dut_coos.data["T300.00K/mu"] = df

# put mobility into DutView and Safe into lib
save_dir = os.path.join("DMT", "DMT", "COOS", "test", "tmp")
lib = DutLib(save_dir=save_dir, force=True)
lib.add_duts([dut_coos])
lib.dut_ref = lib[0]

# init an empty modelcard with all mobility parameters
mc = MCard(["B", "E", "C"], "", "", 1)
mob_params = dut_coos.get_mobility_paras("Si", "X")
mob_paras = (name for name in dir(mob_params) if not name.startswith("_"))
for name in mob_paras:
    try:
        para = McParameter(
            name,
            value=float(getattr(mob_params, name)),
            minval=-float(getattr(mob_params, name)),
            maxval=float(3 * getattr(mob_params, name)),
            unit=None,
        )
        mc.add(para)  # External collector series resistance" unit="Ohm);
    except (ValueError, TypeError):
        pass

### Extraction
v_extraction = Xtraction("velo", mc, os.path.join("test", "tmp", "extractions", "resistances"), lib)
v_extraction.set_technology(Technology)

step = XVelocityField(
    "v(E)",
    mc,
    lib,
    op_definition={},
    valley="X",
    mat="Si",
    key="mu",
    relevant_duts=dut_coos,
    possible_parameters=["mu_l"],
)
v_extraction.add_xstep(step)

gui = XtractionGUI(v_extraction)  # We set the form to be our ExampleApp (design)
gui.start()
