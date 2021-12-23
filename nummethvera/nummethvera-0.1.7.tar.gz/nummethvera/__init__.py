from nummethvera.approxinterp import *
from nummethvera.diffequat import *
from nummethvera.diffintegr import *
from nummethvera.matrixop import *
from nummethvera.otjigants import *
from nummethvera.slau import *
from nummethvera.veivletfurie import *

from . import approxinterp
from . import diffequat
from . import diffintegr
from . import matrixop
from . import otjigants
from . import slau
from . import veivletfurie

__version__ = '0.1.7'
__all__ = """
    approxinterp_read_csv
    polinom_chebyshev
    lagranje
    newton
    jdmethod_fast
    qubic_splines
    linear_approximation
    dispersion_linear
    quadratic_approximation
    dispersion_quadratic
    Gauss_approximation
    dispersion_Gauss
    slau_inp_matr
    csv_inp_matr
    slau_outp_matr
    det
    matrix_of_coefficients_is_square
    norma
    ab
    fix_diagonal
    iakobi
    jdmethod
    linang_inv_jdmethod
    fraction_jbmethod
    isdegenerate
    draw_plot
    draw_plots
    input_expression
    lambda_func
    parse_string
    eyler_cauchy
    runge_kutti
    eyler_cauchy_system
    runge_kutti_system
    solve_expressions
    input_func
    diff
    integ
    matrixop_inp_matr
    matrixop_outp_matr
    transp
    summfunc
    subtfunc
    multnumfunc
    multfunc
    process
    f
    collect_nodes
    draw_graph
    transfer_labels
    get_matrix
    ant_colony_algoritm
    otjig
    veivletfurie_read_csv
    custom_fft
    no_sin_coef
    dobeshi
    haar
    wavelets_4lvl_gm
    """.split()
