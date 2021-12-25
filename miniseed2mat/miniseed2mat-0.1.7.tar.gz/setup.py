# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miniseed2mat']

package_data = \
{'': ['*']}

install_requires = \
['obspy>=1.2.2,<2.0.0', 'scipy>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['mseed2mat = miniseed2mat.main:convertmseed2mat']}

setup_kwargs = {
    'name': 'miniseed2mat',
    'version': '0.1.7',
    'description': 'Analyzing MiniSEED seismic data in MATLAB',
    'long_description': '## Analyzing MiniSEED seismic data in MATLAB \n\nFor details on the usage, visit the earthinversion post: https://www.earthinversion.com/utilities/converting-mseed-data-to-mat-and-analyzing-in-matlab/\n\n## Output data structure\n\n- `stats` contains all the meta data information corresponding to each trace, and\n- `data` contain the time series data\n\n```\nmat_file.mat -> stats, data\nstats -> stats_0, stats_1, ...\ndata -> data_0, data_1, ...\n```\n\n## Usage\n```\nfrom miniseed2mat.miniseed2mat import convertmseed2mat\nmseedfile = "myStream.mseed"\nconvertmseed2mat(mseedfile, output_mat=None)\n```\n\n## Read `mat` file in MATLAB\n\n```\nclear; close all; clc;\n\nwdir=\'./\';\n\nfileloc0=[wdir,\'myStream\'];\nfileloc_ext = \'.mat\';\nfileloc = [fileloc0 fileloc_ext];\n\nif exist(fileloc,\'file\')\n    disp([\'File exists \', fileloc]);\n    load(fileloc);\n    \n    all_stats = fieldnames(stats);\n    all_data = fieldnames(data);\n    \n        \n%     for id=1:length(fieldnames(data))\n    for id=1\n        stats_0 = stats.(all_stats{id});\n        data_0 = data.(all_data{id});\n\n        sampling_rate = getfield(stats_0,\'sampling_rate\');\n        delta = getfield(stats_0,\'delta\');\n        starttime = getfield(stats_0,\'starttime\');\n        endtime = getfield(stats_0,\'endtime\');\n        t1 = datetime(starttime,\'InputFormat\',"yyyy-MM-dd\'T\'HH:mm:ss.SSS\'Z\'");\n        t2 = datetime(endtime,\'InputFormat\',"yyyy-MM-dd\'T\'HH:mm:ss.SSS\'Z\'");\n        datetime_array = t1:seconds(delta):t2;\n\n        %% plot time series\n        fig = figure(\'Renderer\', \'painters\', \'Position\', [100 100 1000 400], \'color\',\'w\');\n        plot(t1:seconds(delta):t2, data_0, \'k-\')\n        title([getfield(stats_0,\'network\'),\'-\', getfield(stats_0,\'station\'), \'-\', getfield(stats_0,\'channel\')])\n        axis tight;\n        print(fig,[\'./\',fileloc0, \'_ts\', num2str(id),\'.jpg\'],\'-djpeg\')\n\n%         close all;\n    end\nend\n\n```\n\n![Output Waveforms](myStream_ts1.jpg)\n',
    'author': 'Utpal Kumar',
    'author_email': 'utpalkumar50@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.earthinversion.com/utilities/converting-mseed-data-to-mat-and-analyzing-in-matlab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
