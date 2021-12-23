import sphinx_rtd_theme
import remt

extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.doctest',
    'sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.mathjax'
]
project = 'Remt'
source_suffix = '.rst'
master_doc = 'index'

title = 'Remt - Note-taking Support Tool'
version = release = remt.__version__
copyright = 'Remt team'

epub_basename = 'Remt - {}'.format(version)
epub_author = 'Remt team'

todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_static_path = ['static']
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

latex_fout = 'remt-{}.tex'.format(version)
latex_documents = [
    ('index', latex_fout, title, 'Remt team', 'manual', False)
]
latex_elements = {
    'papersize': 'a4paper',
}

# vim: sw=4:et:ai
