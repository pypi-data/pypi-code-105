# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['havi', 'havi.bayes', 'havi.physics']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.5,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pyro-ppl>=1.8.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'torch>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'havi',
    'version': '0.1.1',
    'description': 'perform bayesian inference over physical models',
    'long_description': '[![Version](https://img.shields.io/pypi/v/havi)](https://pypi.org/project/havi)\n# Havi\n[stands for Odin](https://en.wikipedia.org/wiki/H%C3%A1r_and_H%C3%A1rr)\n\n\nscatering model and bayesian inference\n\n---\n**Note from author**\n\nIf you use our library on a research or paper please give us a citation\n\n- [PyPi](https://pypi.org/project/havi/)\n\n- [Github](https://github.com/bjornaer/havi)\n\n---\n\n### Installation\n\n    pip install havi\n\n### Usage\n\n```python\nimport havi as h\n\n# scatering angles\nincident_angles = [theta, phi, psi] # incidence angles - floats\nscatered_angles = [theta, phi, psi] # scatering angles - floats\nwavelength = 0.5\n\nhavi = h.Havi(incident_angles, scatered_angles, wavelength)\n\n# surface boudaries for random variables\nrms_height = (0.1, 0.8) # lower and higher boundaries\ncorrelation_longitude = (0.1, 0.8) # lower and higher boundaries\ndielectric_constant = (0.1, 0.8) # lower and higher boundaries\n\nhavi.set_boundaries(rms_height, correlation_longitude, dielectric_constant)\n\nsigma = h.Tensor([0.5])\nobserved_data = h.Tensor([-12,-7,-8])\n\ntrace = havi.inference(sigma, observed) # you can plot the trace however you want OR\nhavi.plot()\n```\n\n### API\n\nThis package exports:\n\nA pytorch Tensor type\n\n    havi.Tensor\n\nOur inference model abstraction, holds data of incident wave, scatered wave and their wave length:\n        \n    havi.Havi(incident_angles: List[float], scatered_angles: List[float], wavelength: float)\n\nSet boundaries for probabilistic variables\n\n    Havi.set_boundaries(rms_height: Tuple[float], correlation_longitude: Tuple[float], dielectric_constant: Tuple[float]) -> None\n\nRuns MCMC(Monte Carlo Markov Chain) bayesian inference with NUTS kernel over scatering model\n\n    Havi.inference(sigma: Tensor, observed: Tensor) -> trace: dict\n\nPlots all of the traced values from MCMC bayesian inference\n\n    Havi.plot() -> None\n\n',
    'author': 'bjornaer',
    'author_email': 'maxemijo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
