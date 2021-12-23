import warnings
import numpy as np
import pandas as pd
from plotnine import *
from typing import Union, Optional, Tuple, Collection, Sequence, Iterable

from ._utilities import get_gene_values

def plot_heatmap(liger_object,
                 gene_dict,
                 use_raw: bool = False,
                 use_scaled: bool = False,
                 scale_by='dataset',
                 log2scale: Optional[float] = None,
                 methylation_indices=None,
                 set_dr_lims=False,
                 pt_size=0.1,
                 min_clip=None,
                 max_clip=None,
                 clip_absolute=False,
                 points_only=False,
                 option='plasma_r',
                 cols_use=None,
                 zero_color='#F5F5F5',
                 axis_labels=None,
                 do_legend=True,
                 return_plots=False,
                 keep_scale=False):

    ### 1. Extract Gene Values
    df_list = []
    cell_name = np.concatenate([adata.obs.index.values for adata in liger_object.adata_list])
    cluster_name = np.concatenate([adata.obs['cluster'].to_numpy() for adata in liger_object.adata_list])
    for key, gene_list in gene_dict.items():
        for gene in gene_list:
            gene_vals = get_gene_values(liger_object, gene, methylation_indices=methylation_indices, log2scale=log2scale)
            df = pd.DataFrame({'gene_name': gene,
                               'cell_name': cell_name,
                               'gene_value': gene_vals,
                               'cluster': cluster_name})
            df_list.append(df)

    df = pd.concat(df_list)

    ### 2. Create plot
    ggp = (ggplot(df, aes('gene_name', 'cell_name', fill='gene_value', group='cluster')) +
           geom_tile() +
           facet_grid('cluster ~ .', scales="free") +
           theme_classic(12))

    if return_plots:
        return ggp
    else:
        ggp.draw()
        return None
