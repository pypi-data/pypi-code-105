from dominate.tags import a
from more_itertools import first
from rdflib import URIRef

from octadocs.iolanta import render
from octadocs.octiron import Octiron
from octadocs_table.models import TABLE


def render_th(octiron: Octiron, iri: str):
    """Render a table column header."""
    iri = URIRef(iri)

    return render(
        node=iri,
        octiron=octiron,
        environments=[TABLE.th],
    )
