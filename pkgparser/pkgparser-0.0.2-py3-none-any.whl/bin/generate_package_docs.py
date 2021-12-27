#!/usr/bin/env python3

import argparse
import json

from mkdpdf.documentation.documentation import Documentation

from pkgparser.pypackage.pypackage import PyPackage
from pkgparser.bin.parameters import param_package_name, param_output

def main():
    """
    Parse documentation from Python package and generate Markdown files for each class/function.
    """

    result = None

    # parse arguments
    opt = parse_args()
    
    # parse package
    p = PyPackage(package_name=opt.package_name)

    # loop through classes
    for c in p.classes:

        # initialize
        r = Documentation(
            directory_name_templates="class",
            directory_path_output=opt.output,
            filename=c.object_path.replace(".", "-"),
            format="md"
        )

        # render markdown
        r.generate(
            header={
                "CLASS_NAME": c.class_name,
                "PACKAGE_DESCRIPTION": p.description,
                "PACKAGE_NAME": p.name,
                "PACKAGE_VERSION": p.version,
                "URL_GIT": p.url_git,
                "URL_RELEASE": p.url_release
            },
            main={
                "CLASS_DESCRIPTION": ". ".join([d for d in c.descriptions]),
                "CLASS_IMPORT": ".".join(c.object_path.split(".")[0:-1]),
                "CLASS_NAME": c.class_name,
                "CLASS_NOTES": "".join(["**%s**: %s" % (d["key"], d["value"]) for d in c.notes]),
                "SUBTEMPLATE_INIT": c,
                "SUBTEMPLATE_FUNCTIONS": c.methods
            }
        )

    # initialize for functions
    r = Documentation(
        directory_name_templates="functions",
        directory_path_output=opt.output,
        filename="functions",
        format="md"
    )

    # render markdown
    r.generate(
        header={
            "PACKAGE_DESCRIPTION": p.description,
            "PACKAGE_NAME": p.name,
            "PACKAGE_VERSION": p.version,
            "URL_GIT": p.url_git,
            "URL_RELEASE": p.url_release
        },
        main={
            "SUBTEMPLATE_FUNCTIONS": p.functions
        }
    )

def parse_args():
    """
    Parse user input.

    Returns:
        A Namespace with attributes for each provided argument.
    """

    # create arguments
    parser = argparse.ArgumentParser()

    # define optional values
    param_package_name(parser)
    param_output(parser)

    # parse user input
    args, unknown = parser.parse_known_args()

    return args

if __name__ == "__main__":
    main()
