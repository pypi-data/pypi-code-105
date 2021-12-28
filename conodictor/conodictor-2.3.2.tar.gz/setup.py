# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conodictor']

package_data = \
{'': ['*']}

install_requires = \
['bio>=1.3.3,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pyfastx>=0.8.4,<0.9.0']

entry_points = \
{'console_scripts': ['conodictor = conodictor.conodictor:main']}

setup_kwargs = {
    'name': 'conodictor',
    'version': '2.3.2',
    'description': 'Prediction and classification of conopeptides',
    'long_description': '[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n[![Docker](https://img.shields.io/docker/pulls/ebedthan/conodictor.svg)]()\n\n\n## ConoDictor: A fast and accurate prediction and classification tool for conopeptides\n\n\n### Introduction\n\nCone snails are among the richest sources of natural peptides with promising pharmacological and therapeutic applications. With the reduced costs of RNAseq, scientists now heavily rely on venom gland transcriptomes for the mining of novel bioactive conopeptides, but the bioinformatic analyses often hamper the discovery process.\n\nConoDictor 2 is a standalone and user-friendly command-line program. We have updated the program originally published as a web server 10 years ago using novel and updated tools and algorithms and improved our classification models with new and higher quality sequences. ConoDictor 2 is now more accurate, faster, multiplatform, and able to deal with a whole cone snail venom gland transcriptome (raw reads or contigs) in a very short time.\n\nThe only input ConoDictor 2 requires is the assembled transcriptome or the raw reads file either in DNA or amino acid: used alphabet is automatically recognized. ConoDictor 2 run predictions directly on the proteins file (submitted or dynamically generated) and tries to report the longest conopeptide  precursor-like sequence.\n\n### Installation\n\n#### Docker\n\nAccessible at https://hub.docker.com/u/ebedthan or on [BioContainers](https://github.com/BioContainers/containers/tree/master/conodictor/2.2.2).\n\n\n#### Get the container\n\n```\ndocker pull ebedthan/conodictor:latest\ndocker run ebedthan/conodictor:latest conodictor -h\n```\n\n#### Example of a run\n\n```\ndocker run --rm=True -v $PWD:/data -u $(id -u):$(id -g) ebedthan/conodictor:latest conodictor --out /data/outdir /data/input.fa.gz\n```\n\nSee https://staph-b.github.io/docker-builds/run_containers/ for more informations on how to properly run a docker container.\n\n\n#### Singularity\n\nThe singularity container does not need admin privileges making it\nsuitable for university clusters and HPC.\n\n```\nsingularity build conodictor.sif docker://ebedthan/conodictor:latest\nsingularity exec conodictor.sif conodictor -h\n```\n\n\n#### Unix-like operating systems \n\n```\n# Download ConoDictor latest version\nwget https://github.com/koualab/conodictor/releases/tag/v2.3.0\n\n# or Download ConoDictor development version\ngit clone https://github.com/koualab/conodictor.git conodictor\n\ncd conodictor\n\n# Copy conodictor bin folder: Requires admin privileges\nsudo cp conodictor /usr/local/bin\n\n# Copy conodictor databases: Requires admin privileges\nsudo mkdir /usr/share/conodictor/db\nsudo cp db/* /usr/share/conodictor/db\n\n# Add path to databases in .bashrc and/or .bash_profile\nexport CONODB=/usr/share/conodictor/db\n\n# Create new python environment conoenv\ncd ..\npython3 -m venv conoenv\npython3 -m pip install -r conodictor/requirements.txt\n\n# Restart terminal or source .bashrc or .bash_profile\n# Test conodictor is correctly installed\nconodictor -h\n```\n\n## Test\n\n* Type `conodictor -h` and it should output something like:\n\n```\nconodictor [FLAGS/OPTIONS] <file>\nExamples:\n\tconodictor file.fa.gz\n\tconodictor --out outfolder --cpus 4 --mlen 51 file.fa\n\npositional arguments:\n  file                  Specifies input file.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -o OUT, --out OUT     Specify output folder.\n  --mlen MLEN           Set the minimum length of the sequence to be\n                        considered as a match\n  --ndup NDUP           Minimum sequence occurence of a sequence to be\n                        considered\n  --faa                 Create a fasta file of matched sequences. Default:\n                        False.\n  --filter              Activate the removal of sequences that matches only\n                        the signal and/or proregions. Default: False.\n  -a, --all             Display sequence without hits in output. Default:\n                        False.\n  -j CPUS, --cpus CPUS  Specify the number of threads. Default: 1.\n  --force               Force re-use output directory. Default: Off.\n  -q, --quiet           Decrease program verbosity\n  --debug               Activate debug mode\n```\n\n\n## Invoking conodictor\n\n```\nconodictor file.fa.gz\nconodictor --out outfolder --cpus 4 --mlen 51 file.fa\n```\n  \n\n## Output files\n\n```\nsummary.csv\n\nsequence  hmm_pred  pssm_pred definitive_pred\nSEQ_ID_1  A A A\nSEQ_ID_2  B D CONFLICT B and D\nSEQ_ID_3  O1  O1  O1\n...\n\n```\n\n## Command line options\n\n```\nGeneral:\n         file              Specify input fasta file [required]\n\nOutputs:\n         -o, --out         Specify output folder.\n         --faa             Create a fasta file of matched sequences. Default: False.\n         -a, --all         Display sequence without hits in output. Default: False.\n         --force           Force re-use output directory. Default: Off.\nComputation:\n         -j, --cpus        Specify number of threads. Default: 1.\n         \nSetup:\n         -q, --quiet       Decrease verbosity\n         --debug           Activate debug mode\n\nStandard meta-options:\n         --help, -h    Print help and exit\n\n```\n  \n## Bugs\n\nSubmit problems or requests to the [Issue Tracker](https://github.com/koualab/conodictor/issues).\n\n\n## Dependencies\n\n### Mandatory\n\n* [**HMMER 3**](https://hmmer.org)  \n  Used for HMM profile prediction.   \n  *Eddy SR, Accelerated Profile HMM Searches. PLOS Computational Biology 2011, 10.1371/journal.pcbi.1002195*\n\n* [**Pftools**](https://github.com/sib-swiss/pftools3)  \n  Used for PSSM prediction.    \n  *Schuepbach P et al. pfsearchV3: a code acceleration and heuristic to search PROSITE profiles. Bioinformatics 2013, 10.1093/bioinformatics/btt129*\n\n\n## Licence\n\n[GPL v3](https://github.com/koualab/conodictor/blob/main/LICENSE)\n\n## Authors\n\n* [Anicet Ebou](https://orcid.org/0000-0003-4005-177X)\n* [Dominique Koua](https://www.researchgate.net/profile/Dominique_Koua)',
    'author': 'Anicet Ebou',
    'author_email': 'anicet.ebou@gmail.com',
    'maintainer': 'Anicet Ebou',
    'maintainer_email': 'anicet.ebou@gmail.com',
    'url': 'https://github.com/koualab/conodictor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
