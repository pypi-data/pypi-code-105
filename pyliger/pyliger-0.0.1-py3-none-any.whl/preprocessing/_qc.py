import numpy as np
import pandas as pd


def calculate_qc(liger_object):
    for adata in liger_object.adata_list:
        pass
    return None


def calculate_mt_pct(liger_object,
                     data_source):
    if data_source == 'human':
        pattern = 'MT-'
    elif data_source == 'mouse':
        pattern = 'mt-'

    for idx, adata in enumerate(liger_object.adata_list):
        liger_object.adata_list[idx] = _find_mt_gene(adata, pattern)
        liger_object.adata_list[idx] = _cal_mt_pct(adata)

    return None


def _find_mt_gene(adata,
                  pattern):
    """helper function to find mitochondrial genes"""
    adata.var['mt'] = adata.var.index.str.startswith(pattern)

    return adata


def _cal_mt_pct(adata):
    """helper function to calculate mt percentage"""
    adata.obs['mt_pct'] = np.ravel(np.sum(adata.X[:, adata.var['mt']], axis=1)) / adata.obs['nUMI']
    return adata

def filtering(liger_object,
              datasets_use = None,
              min_cells = 0,
              max_cells = np.inf,
              min_genes = 0,
              max_genes = np.inf,
              min_counts = 0,
              max_counts = np.inf,
              min_mt_pct = 0,
              max_mt_pct = np.inf,
              combine=False):

    num_samples = liger_object.num_samples

    if datasets_use is None:
        datasets_use = list(range(num_samples))

    if combine:
        gene_union = pd.concat([adata.var for adata in liger_object.adata_list])
        pass
    else:
        for i in datasets_use:
            liger_object.adata_list[i] = _filter_adata(liger_object.adata_list[i],
                                                      min_cells, max_cells, min_genes, max_genes,
                                                      min_counts, max_counts, min_mt_pct, max_mt_pct)

def _filter_union():

    pass

def _filter_adata(adata,
                  min_cells,
                  max_cells,
                  min_genes,
                  max_genes,
                  min_counts,
                  max_counts,
                  min_mt_pct,
                  max_mt_pct):

    gene_filter = (adata.obs['nGene'] >= min_genes) & (adata.obs['nGene'] <= max_genes)
    mt_filter = (adata.obs['mt_pct'] >= min_mt_pct) & (adata.obs['mt_pct'] <= max_mt_pct)
    cell_filter = (adata.var['nCell'] >= min_cells) & (adata.var['nCell'] <= max_cells)
    count_filter = (adata.var['gene_sum'] >= min_counts) & (adata.var['gene_sum'] <= max_counts)

    num_cell_rm = np.sum(~gene_filter&~mt_filter)
    num_gene_rm = np.sum(~cell_filter&~count_filter)
    if num_cell_rm > 0:
        print('Removing {} cells not passed the threshold.'.format(num_cell_rm))

    if num_gene_rm > 0:
        print('Removing {} genes not passed the threshold.'.format(num_gene_rm))

    return adata[gene_filter&mt_filter, cell_filter&count_filter].copy()
