from __future__ import annotations

import collections

import yaml

from markdown_it import MarkdownIt

from .signals import myst_yaml_frontmatter_register, myst_yaml_frontmatter_render


STR_TAG = "tag:yaml.org,2002:str"
MYST_PREFIXES = "!md", "!myst"


class FrontmatterLoader(yaml.Loader):
    """
    Custom YAML Loader for Myst Frontmatter

    - Mapping order is respected (wiht OrderedDict)
    """
    def __init__(self, stream, myst: MarkdownIt):
        super().__init__(self, stream)
        for _, pair in myst_yaml_frontmatter_register.send(self):
            if not len(pair) == 2:
                log.warning(
                    "Ignoring YAML type (%s), expected a (tag, handler) tuple", pair
                )
                continue
            tag, constructor = pair
            self.add_constructor(tag, constructor)
        

    def construct_mapping(self, node, deep=False):
        """User OrderedDict as default for mappings"""
        return collections.OrderedDict(self.construct_pairs(node))


def render(content: str) -> str:
    results = myst_yaml_frontmatter_render.send("myst", content)
    if len(results) < 1:
        # TODO: warn missing rendered
        pass
    elif len(results) > 1:
        # TODO: warn ignored renderers
        pass
    rendered = results[0][1]
    return rendered.strip()

def myst_constructor(loader, node):
    """Allows to optionnaly parse Markdown in multiline literals"""
    value = loader.construct_scalar(node)
    return render(value)

def multiline_myst_constructor(loader, node):
    """Allows to optionnaly parse Markdown in multiline literals"""
    value = loader.construct_scalar(node)
    return render(value) if node.style == "|" else value


for prefix in MYST_PREFIXES:
    FrontmatterLoader.add_constructor(prefix, myst_constructor)


class LiteralFrontmatterLoader(FrontmatterLoader):
    """
    A custom YAML loader for Myst Frontmatter considering all literals as Myst content
    """

LiteralFrontmatterLoader.add_constructor(STR_TAG, multiline_myst_constructor)



@property
def loader_class(self):

    FrontmatterLoader.add_constructor("!md", self.yaml_markdown_constructor)
    if self.settings.get("MYST_FRONTMATTER_PARSE_LITERAL", True):
        FrontmatterLoader.add_constructor(
            STR_TAG, self.yaml_multiline_as_markdown_constructor
        )
    for _, pair in myst_yaml_register.send(self):
        if not len(pair) == 2:
            log.warning(
                "Ignoring YAML type (%s), expected a (tag, handler) tuple", pair
            )
            continue
        tag, constructor = pair
        FrontmatterLoader.add_constructor(tag, constructor)

    return FrontmatterLoader
