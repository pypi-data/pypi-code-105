from blinker import signal

myst_yaml_frontmatter_register = signal("myst_yaml_frontmatter_register")
"""
Register custom YAML types for frontmatter processing
"""

myst_yaml_frontmatter_render = signal("myst_yaml_frontmatter_render")
"""
Render some Myst content from frontmatter 
"""
