from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


extras = {}

extras["docs"] = [
    "recommonmark",
    "nbsphinx",
    "sphinx-autobuild",
    "sphinx-rtd-theme",
    "docutils<0.18"
]

# Packages required for formatting code & running tests.
extras["test"] = [
    "pytest",
]
extras["cv"] = [
    "torchvision==0.11.1",
    "opencv_python==4.5.4.60",
    "Pillow==8.4.0",
    "scikit-image",
]

extras["tensorflow"] = [
    "tensorflow==2.7.0",
    "tensorflow_gpu==2.7.0",
]

extras["nlp"] = [
    "textattack==0.3.4",
    "spacy==3.2.1",
    "nltk==3.6.5",
    "transformers==4.13.0",
    "tensorflow_text"

]

extras["dev"] = (
    extras["docs"] + extras["test"] + extras["tensorflow"] + extras["nlp"] + extras["cv"]
)

setup(
    name="troj",
    version="1.0.0",
    packages=find_packages(),
    author="TrojAI",
    author_email="stan.petley@troj.ai",
    description="TrojAI provides the troj Python convenience package to allow users to integrate TrojAI adversarial protections and robustness metrics seamlessly into their AI development pipelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://troj.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require=extras,
    install_requires=open("./requirements.txt").readlines(),

    python_requires=">=3.6",
    entry_points ={
            'console_scripts': [
                'troj = trojai.cmd.troj:main'
            ]
        },
)
