import operator
from typing import TypedDict, Optional, List

from dominate.tags import table, thead, tr, td, th, tbody, ul, li, a
from dominate.util import raw, text
from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from octadocs.iolanta import render
from octadocs_table.models import TABLE
from rdflib.term import Node


class Row(TypedDict):
    """Raw response."""

    node: Node
    comment: Optional[str]
    count: int


class ColumnLegend(Facet):
    """
    Render a legend for a column.

    FIXME: This facet could have been implemented in a more generic way.

    ```yaml
    $id: RDFLibSupportLegend
    $type: ColumnLegend
    column: supports-rdflib
    ```

    Via OWL rules, this construct would generate a new `Table` node in the graph
    which would be dynamically rendered.

    Unfortunately, current feature set of `octadocs-table` does not permit that.
    In particular,

    - we do not have `table:self` to make system render the node itself,
    - `table:class` property of a table is required, cannot draw a table
      without it,
    - YAML description of a table cannot describe aggregation functions.

    We will be implementing those points over time and perhaps this widget will
    be thereupon refactored.
    """

    def render_comment(self, row: Row):
        """Render description column."""
        comment = row.get('comment', '') or ''

        if comment:
            yield raw(comment)

        see_also_links = list(
            map(
                operator.itemgetter('link'),
                self.query(
                    '''
                    SELECT ?link WHERE {
                        $node rdfs:seeAlso ?link .

                        OPTIONAL {
                            $node octa:position ?position .
                        }
                    }
                    ORDER BY ?position
                    ''',
                    node=row['node'],
                ),
            ),
        )

        if see_also_links:
            yield ul(
                li(
                    render(
                        node=link,
                        octiron=self.octiron,
                    ),
                )
                for link in see_also_links
            )

    def render(self):
        """Print unique values for a column."""
        rows: List[Row] = self.query(
            '''
            SELECT ?node ?comment (COUNT(?node) AS ?count) WHERE {
                {
                    ?instance $column ?node .
                    FILTER isLiteral(?node) .
                } UNION {
                    ?instance $column ?prov_value .
                    ?prov_value prov:value ?node .
                }

                {
                    ?prov_value rdfs:comment ?comment .
                } UNION {
                    ?node rdfs:comment ?comment .
                }
            }
            GROUP BY ?node ?comment
            ORDER BY DESC(?count)
            ''',
            column=self.iri,
        )

        table_rows = [
            tr(
                td(
                    raw(
                        render(
                            node=row['node'],
                            octiron=self.octiron,
                            environments=[
                                TABLE.td,
                                IOLANTA.html,
                            ],
                        ),
                    ),
                ),
                td(*self.render_comment(row)),
                td(row['count']),
            )
            for row in rows
        ]

        return table(
            thead(
                tr(
                    # These are hard coded, and I cannot change that. See the
                    # docstring for details.
                    th('Value'),
                    th('Description'),
                    th('Count'),
                ),
            ),
            tbody(*table_rows),
        )
