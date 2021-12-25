# -*- coding: utf-8 -*-
import draftapp
import os
import shutil
import stat
from .constants import Frameworks, ErrorMessages, TemplateFileContentReplace
from .validations import validate_name


def get_templates(framework, type):
    for item in Frameworks.python[framework]:
        if type == item:
            template = "project_template_" + type
    return os.path.join(draftapp.__path__[0], "conf", template)


def apply_umask(old_path, new_path):
    current_umask = os.umask(0)
    os.umask(current_umask)
    current_mode = stat.S_IMODE(os.stat(old_path).st_mode)
    os.chmod(new_path, current_mode & ~current_umask)


def make_writeable(filename):
    """
    Make sure that the file is writeable.
    Useful if our source is read-only.
    """
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)


def update_content(path, name):
    reading_file = open(path, "r")

    new_file_content = ""
    for line in reading_file:
        stripped_line = line
        new_line = stripped_line.replace("project_name", name)
        new_file_content += new_line
    reading_file.close()

    writing_file = open(path, "w")
    writing_file.write(new_file_content)
    writing_file.close()


def build_app(name, target, framework, type):
    # Validating the name provided
    validate_name(name)

    # Checking if target directory is provided, if not wil create the app in current working directory
    if target is None:
        top_dir = os.path.join(os.getcwd(), name)
        try:
            os.makedirs(top_dir)
        except FileExistsError:
            raise Exception(ErrorMessages.FileAlreadyExistsError)
        except OSError as e:
            raise Exception(e)
    else:
        top_dir = os.path.abspath(os.path.expanduser(target))
        if not os.path.exists(top_dir):
            raise Exception(
                "Destination directory '%s' does not "
                "exist. Kindly create it first." % top_dir
            )

    template_dir = get_templates(framework, type)

    prefix_length = len(template_dir) + 1

    for root, dirs, files in os.walk(template_dir):

        path_rest = root[prefix_length:]
        relative_dir = path_rest.replace("project_name", name)
        if relative_dir:
            target_dir = os.path.join(top_dir, relative_dir)
            os.makedirs(target_dir, exist_ok=True)

        for dirname in dirs[:]:
            if dirname == '__pycache__':
                dirs.remove(dirname)

        for filename in files:
            replace_content = (
                True if filename in TemplateFileContentReplace.filenames else False
            )

            if filename.endswith((".pyo", ".pyc", ".py.class")):
                # Ignore some files as they cause various breakages.
                continue
            old_path = os.path.join(root, filename)
            new_path = os.path.join(
                top_dir, relative_dir, filename.replace("project_name", name)
            )

            if os.path.exists(new_path):
                raise Exception(
                    "%s already exists. Kindly remove conflicting files from the directory."
                    % (new_path,)
                )

            shutil.copyfile(old_path, new_path)

            if replace_content:
                update_content(new_path, name)

            try:
                apply_umask(old_path, new_path)
                make_writeable(new_path)
            except OSError:
                print(
                    "Notice: Couldn't set permission bits on %s. You're "
                    "probably using an uncommon filesystem setup. No "
                    "problem." % new_path
                )
