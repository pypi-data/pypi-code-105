###########################
####    v4yve corp.    ####
####  bomber by v4yve  ####
##### setup.py - файл #####
###########################

from setuptools import setup

NAME            = "v4yve"
DESCRIPTION     = "SmSBomb"
URL             = "https://vk.com/v4yve"
EMAIL           = "v4yve@yandex.ru"
AUTHOR          = "v4vye"
REQUIRES_PYTHON = ">=3.7.0"
VERSION         = "0.1"                    # Beta test

# Файл зависимостей requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    REQUIRED = f.readlines()

# Запись зависимостей в файл requirements.txt
try:
    with open("README.md", encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Установщик
setup(
    name                            = NAME,
    version                         = VERSION,
    description                     = DESCRIPTION,
    long_description                = DESCRIPTION,
    long_description_content_type   = "text/markdown",
    author                          = AUTHOR,
    author_email                    = EMAIL,
    python_requires                 = REQUIRES_PYTHON,
    url                             = URL,
    packages                        = ["v4yve"],
    entry_points                    = {
                "console_scripts" : ['v4yve=v4yve.cli:main',"v4yv3=v4yve.cli:main","v4b=v4yve.cli:main"]
    },
    install_requires                = REQUIRED,
    extras_require                  = {},
    package_data                    = {"v4yve" : ["services/*", "app/*", "app/*/*", "app/static/*/*"]},
    license                         = "Mozilla Public License 2.0", # Купить лицензию
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Android",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ],
)

# Конец ["setup.py"]