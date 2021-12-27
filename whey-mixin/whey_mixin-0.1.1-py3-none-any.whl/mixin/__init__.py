from functools import lru_cache
from typing import Type

import dom_toml
from domdf_python_tools.compat.importlib_metadata import EntryPoint
from whey import builder
from whey.config.whey import get_entry_points

from .paths import PathPlusPlus


default_class = {
	"sdist": builder.SDistBuilder,
	"wheel": builder.WheelBuilder,
	"binary": builder.WheelBuilder,
}

@lru_cache(1)
def get_base_config():
	config = dom_toml.load("pyproject.toml", decoder=dom_toml.decoder.TomlPureDecoder)
	return config.get("tool", {}).get("whey", {}).get("mixin", {})

def get_config(mode: str):
	base_config = get_base_config()
	mixin_config = base_config.get(mode, {})

	mixin_config.setdefault("hooks", [])
	if "hooks" in base_config:
		mixin_config["hooks"] = base_config["hooks"] + mixin_config["hooks"]

	hooks = [
		EntryPoint("", hook, "whey.builder.hook").load()
		for hook in mixin_config["hooks"]
	]

	cls: Type[builder.AbstractBuilder]
	if "class" in mixin_config:
		cls = EntryPoint(
			f"custom_{mode}",
			mixin_config["class"],
			"whey.builder"
		).load()
	elif "entry-point" in mixin_config:
		cls = get_entry_points()[mixin_config["entry-point"]].load()
	else:
		cls = default_class[mode]

	return cls, hooks


class BuilderMixin(builder.AbstractBuilder):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.pkgdir = PathPlusPlus(self.project_dir / self.config["source-dir"] / self.config["package"])


class BuilderFactory:
	def __getattr__(self, name: str):
		cls, hooks = get_config(name)

		class Builder(BuilderMixin, cls):
			def call_additional_hooks(self):
				super().call_additional_hooks()
				for hook in hooks:
					hook(self)

		return Builder

BuilderFor = BuilderFactory()
