import numpy as np
import pandas as pd
import seaborn as sns

#from plotnine import *


def plot_qc(liger_object,
            plot_by='nGene',
            legend_text_size=12):

    if plot_by in ['nGene', 'nUMI']:
        df = pd.concat([adata.obs[['dataset', 'nGene', 'nUMI']] for adata in liger_object.adata_list])
    elif plot_by in ['nCell', 'gene_sum']:
        df = pd.concat([adata.var[['nCell', 'gene_sum']] for adata in liger_object.adata_list])
        df['dataset'] = np.concatenate([np.repeat(adata.uns['sample_name'], adata.shape[1]) for adata in liger_object.adata_list])

    ax = sns.violinplot(x="dataset", y=plot_by, data=df)

    #ggp = (ggplot(df, aes('dataset', plot_by))
    #        + geom_violin(df, fill='red')
    #      )

    #if df.shape[0] < 20000:
    #    ggp += geom_jitter(size=0.3)

    #ggp = ggp + theme_classic(legend_text_size)

    return ax
