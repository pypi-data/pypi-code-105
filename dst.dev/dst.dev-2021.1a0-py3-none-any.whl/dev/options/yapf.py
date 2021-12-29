import yapf

from . import utils


CONFIG_FILE = yapf.style.LOCAL_STYLE
DEFAULTS = {
    "based_on_style": "google",
    "align_closing_bracket_with_visual_indent": "True",
    "allow_split_before_dict_value": "False",
    "blank_lines_between_top_level_imports_and_variables": "2",
    "coalesce_brackets": "True",
    "column_limit": "119",
    "continuation_align_style": "VALIGN-RIGHT",
    "dedent_closing_brackets": "True",
    "force_multiline_dict": "True",
    "indent_dictionary_value": "False",
    "space_between_ending_comma_and_closing_bracket": "True",
    "split_arguments_when_comma_terminated": "True",
    "split_before_dict_set_generator": "False",
}


def generate_config() -> None:
    config = utils.get_config()
    data = dict(DEFAULTS)
    for header in config.sections():
        if header == "yapf":
            for key, value in config[header].items():
                data[key] = utils.fix_value(value)
    assert data["based_on_style"] == "google"  # ToDo assert bad
    text = "\n".join(f"{k}={v}" for k, v in data.items())
    with open(utils.get_file_path(CONFIG_FILE), "wt") as fd:
        fd.write(f"[style]\n{text}\n")
        if utils.get_options()["yapf-exclude"]:
            parts = (f"{utils.get_package_path()}/{x.strip('/')}/" for x in utils.get_options()["yapf-exclude"])
            text = "\n    ".join(("exclude=", *parts))
            fd.write(f"\n[dst.dev]\n{text}\n")
