# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['art_of_geom',
 'art_of_geom._util',
 'art_of_geom.art',
 'art_of_geom.geom',
 'art_of_geom.geom._abc',
 'art_of_geom.geom.euclid._abc',
 'art_of_geom.geom.euclid._r0',
 'art_of_geom.geom.euclid._r1',
 'art_of_geom.geom.euclid._r1._abc',
 'art_of_geom.geom.euclid._rD',
 'art_of_geom.geom.euclid._rDi',
 'art_of_geom.geom.euclid.r2',
 'art_of_geom.geom.euclid.r2._abc',
 'art_of_geom.geom.euclid.r2.conic',
 'art_of_geom.geom.euclid.r2.cubic',
 'art_of_geom.geom.euclid.r2.intersect',
 'art_of_geom.geom.euclid.r2.polygon',
 'art_of_geom.geom.euclid.r2.polygon.quadrilateral',
 'art_of_geom.geom.euclid.r2.polygon.triangle',
 'art_of_geom.geom.euclid.r2.polygon.triangle.center',
 'art_of_geom.geom.euclid.r2.polygon.triangle.center.kimberling',
 'art_of_geom.geom.euclid.r2.quartic',
 'art_of_geom.geom.euclid.r2.roulette',
 'art_of_geom.geom.euclid.r2.spiral',
 'art_of_geom.geom.euclid.r2.transform',
 'art_of_geom.geom.euclid.r2i',
 'art_of_geom.geom.euclid.r2i.conic',
 'art_of_geom.geom.euclid.r2i.conic.ellipse',
 'art_of_geom.geom.euclid.r2i.intersect',
 'art_of_geom.geom.euclid.r2i.transform',
 'art_of_geom.geom.euclid.r3',
 'art_of_geom.geom.euclid.r3._abc',
 'art_of_geom.geom.euclid.r3.intersect',
 'art_of_geom.geom.euclid.r3.polygon',
 'art_of_geom.geom.euclid.r3.polygon.triangle',
 'art_of_geom.geom.euclid.r3.polyhedron',
 'art_of_geom.geom.euclid.r3.polyhedron.tetrahedron',
 'art_of_geom.geom.euclid.r3.quadric_surface.surface_of_revolution',
 'art_of_geom.geom.euclid.r3.quadric_surface.surface_of_revolution.ellipsoid',
 'art_of_geom.geom.euclid.r3.solid',
 'art_of_geom.geom.euclid.r3.transform',
 'art_of_geom.geom.euclid.r3i',
 'art_of_geom.geom.fractal',
 'art_of_geom.geom.non_euclid',
 'art_of_geom.geom.non_euclid._abc',
 'art_of_geom.geom.non_euclid.elliptic',
 'art_of_geom.geom.non_euclid.elliptic.earth',
 'art_of_geom.geom.non_euclid.elliptic.spherical',
 'art_of_geom.geom.non_euclid.hyperbolic',
 'art_of_geom.geom.non_euclid.mobius',
 'art_of_geom.geom.non_euclid.parabolic',
 'art_of_geom.geom.non_euclid.torus']

package_data = \
{'': ['*']}

install_requires = \
['NumPy>=1.21.5,<2.0.0', 'SymPy>=1.9,<2.0']

setup_kwargs = {
    'name': 'art-of-geometry',
    'version': '0.0.0.dev0',
    'description': 'Art of Geometry',
    'long_description': '# Art of Geometry\n',
    'author': 'The Vinh LUONG (LƯƠNG Thế Vinh)',
    'author_email': 'Edu.AI@STEAMforVietNam.org',
    'maintainer': 'The Vinh LUONG (LƯƠNG Thế Vinh)',
    'maintainer_email': 'Edu.AI@STEAMforVietNam.org',
    'url': 'https://GitHub.com/Mathverse/Art-of-Geometry',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
