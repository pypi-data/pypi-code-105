import dataclasses
from dataclasses import dataclass, asdict
from typing import List
import json

from py3js.visualisation import Visualisation


@dataclass
class Node:
    name: str
    children: List["Node"] or None = None
    value: str = None


class Tree(Visualisation):
    def __init__(self, root: Node, width=1000, height=600):
        Visualisation.__init__(self, width, height)
        self._root = root

        self.add_script("const radius = width/2;")
        self.add_script(f"const data = d3.hierarchy({json.dumps(asdict(root))}).sort((a, b) => d3.ascending(a.data.name, b.data.name));")
        self.add_script("tree = d3.tree().size([2 * Math.PI, radius]).separation((a, b) => (a.parent == b.parent ? 1 : 2) / a.depth);")
        self.add_script("const root = tree(data);")

        self.add_script("""svg.append("g")
        .attr("fill", "none")
        .attr("stroke", "#555")
        .attr("stroke-opacity", 0.4)
        .attr("stroke-width", 1.5)
        .selectAll("path")
        .data(root.links())
        .join("path")
        .attr("d", d3.linkRadial()
            .angle(d => d.x)
            .radius(d => d.y));""")

        self.add_script("""svg.append("g")
        .selectAll("circle")
        .data(root.descendants())
        .join("circle")
        .attr("transform", d => `
        rotate(${d.x * 180 / Math.PI - 90})
        translate(${d.y},0)
      `)
        .attr("fill", d => d.children ? "#555" : "#999")
        .attr("r", 2.5);""")

        self.add_script(""" svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("stroke-linejoin", "round")
        .attr("stroke-width", 3)
        .selectAll("text")
        .data(root.descendants())
        .join("text")
        .attr("transform", d => `
        rotate(${d.x * 180 / Math.PI - 90})
        translate(${d.y},0)
        rotate(${d.x >= Math.PI ? 180 : 0})
      `)
        .attr("dy", "0.31em")
        .attr("x", d => d.x < Math.PI === !d.children ? 6 : -6)
        .attr("text-anchor", d => d.x < Math.PI === !d.children ? "start" : "end")
        .text(d => d.data.name)
        .clone(true).lower()
        .attr("stroke", "white");""")


        self.add_script("""function autoBox() {
        const {x, y, width, height} = this.getBBox();
        return [x, y, width, height];
    }

    svg.attr("viewBox", autoBox);""")
