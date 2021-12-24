#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Command line interface to 1D CDFT calculations
"""

import datetime
import decimal
import json
import math
import pathlib
import sys

import click
import numpy as np
from prettytable import PrettyTable, PLAIN_COLUMNS
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.validation import Validator

from cdftpy.cdft1d.config import DATA_DIR
from cdftpy.cdft1d.io_utils import read_key_value
from cdftpy.cdft1d.io_utils import read_solute
from cdftpy.cdft1d.rdf import analyze_rdf_peaks_sim
from cdftpy.cdft1d.rdf import write_rdf_sim
from cdftpy.cdft1d.rism import rism_1d
from cdftpy.cdft1d.rsdft import rsdft_1d
from cdftpy.cdft1d.solvent import solvent_model_locate, Solvent
from cdftpy import __version__
from cdftpy.cdft1d.exceptions import ConvergenceError
from cdftpy.cdft1d.viz import single_point_viz

HEADER = """
==================================
1D-CDFT PROGRAM

Marat Valiev and Gennady Chuev
==================================
"""

_RUNNERS = dict(rism=rism_1d, rsdft=rsdft_1d)


def my_linspace(start, stop, nsteps):

    values, dv = np.linspace(start, stop, num=nsteps, retstep=True)

    if dv < 1:
        nr = int(-math.log10(dv)) + 1
    else:
        nr = 1
    return list(map(lambda x: x.round(nr), values))

def cdft1d_multi_point(input_file, method, var,
                       values=None,
                       stop=None,
                       nsteps=11,
                       start=None
                       ):

    try:
        solute = read_solute(input_file)
    except FileNotFoundError:
        print(f"Cannot locate input file {input_file}")
        sys.exit(1)

    for k, v in solute.items():
        solute[k] = v[0]

    if values is None:
        if stop is None:
            print("Neither values or stop is provided")
            sys.exit(1)

        if start is None:
            start = solute[var]

        values = my_linspace(start, stop, nsteps)


    parameters = read_key_value(input_file, section="simulation")

    solvent_name = parameters["solvent"]
    filename = solvent_model_locate(solvent_name)




    rism_patch = (method == "rism")
    solvent = Solvent.from_file(filename, rism_patch=rism_patch)

    runner = _RUNNERS[method]
    sim = []
    gr_guess = None
    for v in values:
        solute[var] = v
        try:
            s = runner(solute, solvent, params=parameters, gr_guess=gr_guess)
        except ConvergenceError as e:
            print(F"cannot converge {var}={v} point")
            print("skipping the rest of the cycle")
            break
        gr_guess = s.g_r
        sim.append(s)

    tbl = PrettyTable()

    tbl.set_style(PLAIN_COLUMNS)
    tbl.field_names = [var.capitalize(), "Free Energy"]

    for v, s in zip(values, sim):
        tbl.add_row([v,s.fe_tot.round(3)])
    tbl.align = "r"
    print(tbl)

def cdft1d_single_point(input_file, method, html_serve=False, html_file=None):

    try:
        solute = read_solute(input_file)
    except FileNotFoundError:
        print(f"Cannot locate input file {input_file}")
        sys.exit(1)

    for k, v in solute.items():
        solute[k] = v[0]

    parameters = read_key_value(input_file, section="simulation")

    solvent_name = parameters["solvent"]
    filename = solvent_model_locate(solvent_name)

    if method == "rism":
        solvent = Solvent.from_file(filename, rism_patch=True)
        sim = rism_1d(solute, solvent, params=parameters)
    elif method == "rsdft":
        solvent = Solvent.from_file(filename, rism_patch=False)
        sim = rsdft_1d(solute, solvent, params=parameters)
    else:
        print(f"Unknown method {theory}")
        sys.exit(1)

    analysis = read_key_value(input_file, section="analysis")
    if analysis is not None:
        if "rdf_peaks" in analysis:
            analyze_rdf_peaks_sim(sim)

    output = read_key_value(input_file, section="output")
    if output is not None:
        if "rdf" in output:
            write_rdf_sim(sim)

    viz = (html_serve or html_file)
    if viz:
        single_point_viz(sim, serve=html_serve, html_file=html_file)

if __name__ == '__main__':
    # raise ConvergenceError("crap")
    cdft1d_single_point("../../examples/cdft1d/cl.dat", "rism", html_serve=True, html_save=True)
    # cdft1d_multi_point("../../examples/cdft1d/cl.dat", "rism", "sigma", stop=20, nsteps=30)
