import logging
import re

from functools import cached_property
from typing import Any, MutableMapping, Sequence

import yaml

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.utils import OptionsDict

# Core plugins, always enabled
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.colon_fence import colon_fence_plugin
from mdit_py_plugins.myst_role import myst_role_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name

DELIMITER = "---"
BOUNDARY = re.compile(r"^{0}$".format(DELIMITER), re.MULTILINE)
STR_TAG = "tag:yaml.org,2002:str"

INTERNAL_LINK = re.compile(r"^%7B(\w+)%7D")

log = logging.getLogger(__name__)

PLUGINS = dict(
    tasklist=tasklists_plugin,
)


class HtmlRenderer(RendererHTML):
    """
    An altered MarkdownIt HTML rendered taking reader settings in account.
    """
    def fence(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: MutableMapping,
    ) -> str:
        highlighted = super().fence(tokens, idx, options, env)
        if env.get("pygments"):
            return (
                "<div class=highlight>"
                + highlighted
                + "</div>\n"
            )
        return highlighted


class MystCodeFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        """
        Wrap the ``source``, which is a generator yielding
        individual lines, in custom generators. See docstring
        for `format`. Can be overridden.
        """
        return source


class MystIt(MarkdownIt):
    def __init__(self, **options):
        super().__init__("gfm-like", options_update=options, renderer_cls=HtmlRenderer)
        self.use(front_matter_plugin).use(colon_fence_plugin).use(myst_role_plugin).user(myst_block_plugin)

    # def normalizeLink(self, url: str) -> str:
    #     normalized = super().normalizeLink(url)
    #     return INTERNAL_LINK.sub(r"{\g<1>}", normalized)
