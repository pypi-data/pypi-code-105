from pathlib import Path
from anndata import AnnData, read_h5ad

from .._utilities import _create_h5_using_adata

PARRENT_PATH = Path(__file__).parent


def kang17_downsampled(backed=False,
                       chunk_size = 1000):
    """
    Reference
    ---------

    """
    p_ctrl = PARRENT_PATH / 'pbmc_ctrl_downsampled.h5ad'
    p_stim = PARRENT_PATH / 'pbmc_stim_downsampled.h5ad'
    print(p_stim)
    if p_ctrl.is_file():
        ctrl_dge = read_h5ad(p_ctrl, backed=backed)

    if p_stim.is_file():
        stim_dge = read_h5ad(p_stim, backed=backed)

    if backed:
        _create_h5_using_adata(ctrl_dge, chunk_size)
        _create_h5_using_adata(stim_dge, chunk_size)

    return ctrl_dge, stim_dge


def kang17(backed=False,
           chunk_size=1000):
    """

    Reference
    ---------
    """
    p_ctrl = PARRENT_PATH / 'pbmc_ctrl.h5ad'
    p_stim = PARRENT_PATH / 'pbmc_stim.h5ad'

    if p_ctrl.is_file():
        ctrl_dge = read_h5ad(p_ctrl, backed=backed)

    if p_stim.is_file():
        stim_dge = read_h5ad(p_stim, backed=backed)

    if backed:
        _create_h5_using_adata(ctrl_dge, chunk_size)
        _create_h5_using_adata(stim_dge, chunk_size)

    return ctrl_dge, stim_dge


def allen_smarter_cells(backed=False,
                        chunk_size=1000):
    """

    :param backed:
    :return:
    """
    #TODO: add web download function
    p = PARRENT_PATH / 'allen_smarter_cells.h5ad'

    if p.is_file():
        adata = read_h5ad(p, backed=backed)

    if backed:
        _create_h5_using_adata(adata, chunk_size)

    return adata


def allen_smarter_nuclei(backed=False,
                         chunk_size=1000):
    """

    :param backed:
    :return:
    """
    p = PARRENT_PATH / 'allen_smarter_nuclei.h5ad'

    if p.is_file():
        adata = read_h5ad(p, backed=backed)

    if backed:
        _create_h5_using_adata(adata, chunk_size)

    return adata
