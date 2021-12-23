# import itertools
# import os
import argparse
from transparentpath import Path
import numpy as np
import pandas as pd
from adlinear import nmfmodel as nmf
from randomgenerators import randomgenerators as rng
import dotenv

Path.set_global_fs("gcs", bucket="nmf_experiments_dev", token="cred_gcs.json")
dotenv.load_dotenv()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Creates the yaml file to launch several iterations of a program on GCP",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-o", "--output", type=str, default="wfold_scree_plots", help="Output file path")
    parser.add_argument("-r", "--runs", type=int, default=100, help="Number of iterations per node")
    parser.add_argument("-w", "--writefreq", type=int, default=20, help="Write frequency")
    parser.add_argument("-e", "--epsilon", type=float, default=0.10, help="Other argument you need")
    args = parser.parse_args()
    output = Path(args.output)
    epsilon = args.epsilon

    nruns = args.runs
    writefreq = args.writefreq

    rand_norms = True
    df_mini_scree_plots = pd.DataFrame(index=[], columns=[])
    for itrial in range(nruns):
        nb_clusters = np.random.randint(low=5, high=40)
        min_corr = np.random.uniform(low=0.75, high=0.95)
        max_corr = np.random.uniform(low=0.05, high=0.25)
        h_size = np.random.randint(low=100, high=200)
        w_size = np.random.randint(low=100, high=200)
        eps = np.random.uniform(low=0.0, high=epsilon)
        wclust_factor = np.random.uniform(0.25, 1.0)

        generated_M, _, _, _ = rng.generate_nmf_reconstruction(n_comp=nb_clusters, n_feat=h_size,
                                                               n_obs=w_size, min_intra_corr=min_corr,
                                                               max_inter_corr=max_corr, epsilon=eps,
                                                               random_norms=rand_norms,
                                                               wclust_factor=wclust_factor)
        rnstr = "RandNorms" if rand_norms else "ConstNorms"
        # generated_M.to_csv(res_path / "random_nmf" / f"M_t{itrial}_nc{nb_clusters}_corrmin{round(min_corr,2)}_"
        #                                f"corrmax{round(max_corr,2)}_noise{round(eps,2)}_{rnstr}.csv",
        #                    float_format="%.4f")
        df_scree_plot = nmf.generate_scree_plot(generated_M, ncmin=2, ncmax=45)
        df_mini_scree_plots = nmf.add_miniscree_plots_from_scree_plot(df_mini_scree_plots, df_scree_plot, nb_clusters)

        if itrial % writefreq == 0:
            output.write(df_mini_scree_plots)

