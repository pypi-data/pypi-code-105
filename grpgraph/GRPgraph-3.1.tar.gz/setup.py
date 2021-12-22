from setuptools import setup  
requirements = ["Pygame==2.1.0","keyboard"]
setup(name='GRPgraph',
       version='3.1',
      description='small and compact graphick distributions',
      packages=['GRPgraph'],       
      author_email='pvana621@gmail.com', 
      install_requires=requirements,      
      zip_safe=False)