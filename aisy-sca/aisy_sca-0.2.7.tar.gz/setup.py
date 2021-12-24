import setuptools

setuptools.setup(
    name="aisy_sca",
    version="0.2.7",
    author="Guilherme Perin",
    author_email="guilhermeperin7@gmail.com",
    description="Deep Learning-based Framework for Side Channel Analysis",
    long_description="""
    # AISY - Deep Learning-based Framework for Side Channel Analysis

    Welcome to the first deep learning-based side-channel analysis framework.
    This AISY Framework was developed by AISYLab from TU Delft.

    If you use our framework, please consider citing:

    @misc{AISY_Framework,
        author = {Guilherme Perin and Lichao Wu and Stjepan Picek},
        title  = {{AISY - Deep Learning-based Framework for Side-Channel Analysis}},
        howpublished = {AISyLab repository},
        note   = {{\\url{https://github.com/AISyLab/AISY_Framework}}},
        year   = {2021}
    }
    """,
    long_description_content_type='text/markdown',
    keywords="side-channel analysis deep learning profiled attacks",
    packages=['aisy_sca', 'aisy_sca/analysis', 'aisy_sca/crypto', 'aisy_sca/crypto/aes', 'aisy_sca/datasets', 'aisy_sca/callbacks',
              'aisy_sca/metrics', 'aisy_sca/optimization', 'aisy_sca/sca', 'aisy_sca/utils', 'tests'],
    url="https://aisylab.github.io/AISY_docs/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"]
)
