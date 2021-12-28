# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tennisim']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tennisim',
    'version': '0.1.2',
    'description': 'Simple pure python functions for simulating tennis matches',
    'long_description': '# tennisim\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/tennisim.svg)](https://pypi.org/project/tennisim/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/tennisim.svg)](https://pypi.python.org/pypi/tennisim/)\n[![Actions Status](https://github.com/mjam03/tennisim/workflows/Tests/badge.svg)](https://github.com/mjam03/tennisim/actions)\n[![Actions Status](https://github.com/mjam03/tennisim/workflows/Release/badge.svg)](https://github.com/mjam03/tennisim/actions)\n[![codecov](https://codecov.io/gh/mjam03/tennisim/branch/main/graph/badge.svg?token=948J8ECAQT)](https://codecov.io/gh/mjam03/tennisim)\n\nSimulate tennis points, games, sets and matches.\n\nSmall pure python package (no dependencies outside of standard lib) to simulate tennis using points-based modelling i.e. given a probability of a server winning a given point, simulate the outcome of:\n - points\n - games\n - sets\n - tiebreaks\n - matches\n\nwith the ability to alter various parameters to gain some intuition behind how the tennis scoring system impacts matches. Using this we can answer various questions like:\n - what effect does removing the second serve have on match duration?\n - if the probability of winning a point on serve is reflective of skill, then how do rule alterations affect the likelihood that the more skillful player will actually end up winning the match (not just a given point)?\n\n # Installing\n\n `pip install tennisim`\n\n# Points-based Modelling\n\nPoints-based modelling is a popular model for modelling tennis matches where predictions for games, sets and matches depends on modelling every constituent point. This can lead to a wealth of data that can be used to generate in-play match odds as we can output distributions e.g. for a given starting point, if we simulate 1000 outcomes how many show that player 1 wins the next set?\n\nFor more background I wrote [this article on Towards Data Science](https://towardsdatascience.com/building-a-tennis-match-simulator-in-python-3add9af6bebe).\n\n# Example\n\nSuppose we want to simulate a game of tennis. We define the probability that the server will win a given point:\n```python\nfrom tennisim.sim import sim_game\n\np = 0.7\nsim_game(p)\n```\n\nThis will simulate 1 game of tennis where the probability that the server will win any given point is `0.7`. It will return a tuple containing:\n - boolean result for if the server won the game\n - list of tuples for the score progression of the game\n\n We can then take this further and simulate 1,000 groups of 100 games to generate a distribution of results. This can be interesting when looking at how changes in the probability p or the length of a game impacts the servers win probability for the game.\n\n ```python\nimport numpy as np\nfrom tennisim.sim import sim_game\n\n# set params for simulation\ngames = 100\nsims = 1000\nprobabs = np.linspace(0.5, 0.8, 4)\nresults = {}\n\n# for each serve win probability\nfor p in probabs:\n    # we now need to generate sims\n    means = []\n    game_lengths = []\n    for i in range(0, sims):\n        g_results = [sim_game(p) for x in range(games)]\n        # get mean result\n        mean_res = np.mean([x[0] for x in g_results])\n        # get mean game length\n        mean_length = np.mean([len(x[1]) for x in g_results])\n        # join to results holders\n        means.append(mean_res)\n        game_lengths.append(mean_length)\n    # add data to probab dict\n    results[p] = (means, game_lengths)\n ```\n\n # Help\n \n For more info see the [documentation](https://mjam03.github.io/tennisim/)\n\n # License\n \n `tennisim` is free and open source software, distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT).',
    'author': 'Mark Jamison',
    'author_email': 'markjamison03@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mjam03/tennisim',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
