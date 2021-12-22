# -*- coding: utf-8 -*-
# import click
# import logging
# from pathlib import Path
# from dotenv import find_dotenv, load_dotenv


# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
# def main(input_filepath, output_filepath):
#     """ Runs data processing scripts to turn raw data from (../raw) into
#         cleaned data ready to be analyzed (saved in ../processed).
#     """
#     logger = logging.getLogger(__name__)
#     logger.info('making final data set from raw data')


# if __name__ == '__main__':
#     log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_fmt)

#     # not used in this stub but often useful for finding various files
#     project_dir = Path(__file__).resolve().parents[2]

#     # find .env automagically by walking up directories until it's found, then
#     # load up the .env entries as environment variables
#     load_dotenv(find_dotenv())

#     main()

# import pandas as pd

# from mba.config.core import config
# from mba.data.data_management import DataFlow

# def merge_all():
#     dataflow = DataFlow()
#     df = dataflow.read_data_csv(config.data_config.cart_filenames[0])
#     other = dataflow.read_data_csv(config.data_config.cart_filenames[1])
#     df = pd.concat([df, other])

#     products_df = dataflow.read_data_csv(config.data_config.product_filename)

#     aisles_df = dataflow.read_data_csv(config.data_config.aisle_filename) 
#     departments_df = dataflow.read_data_csv(config.data_config.department_filename)

#     bigger_df = pd.merge(left=df, right=products_df, how='inner')
#     biggest_df = pd.merge(left=bigger_df, right=aisles_df, on='aisle_id')
#     giant_df = pd.merge(left=biggest_df, right=departments_df,on='department_id')

#     return giant_df