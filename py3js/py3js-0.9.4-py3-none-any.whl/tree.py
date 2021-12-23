import dataclasses
from dataclasses import dataclass, asdict
from typing import List
from enum import Enum
import json

from py3js.visualisation import Visualisation


class TreeKind(Enum):
    TIDY = 1
    RADIAL_TIDY = 2


@dataclass
class Node:
    name: str
    children: List["Node"] or None = dataclasses.field(default_factory=list)


class Tree(Visualisation):
    def __init__(self, root: Node, kind: TreeKind = TreeKind.TIDY, width=1000, height=600):
        Visualisation.__init__(self, width, height)
        self._root = root

        if kind == TreeKind.RADIAL_TIDY:
            self.add_radial()
        elif kind == TreeKind.TIDY:
            self.add_normal()

    def add_radial(self):
        self.add_script("const radius = width/2;")
        self.add_script(
            f"const data = d3.hierarchy({json.dumps(asdict(self._root))}).sort((a, b) => d3.ascending(a.data.name, b.data.name));")
        self.add_script(
            "tree = d3.tree().size([2 * Math.PI, radius]).separation((a, b) => (a.parent == b.parent ? 1 : 2) / a.depth);")
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

    def add_normal(self):
        self.add_script("""
        const padding = 1;
        const stroke = "#555";
        const strokeOpacity = 0.4;
        const strokeLinecap = null;
        const strokeLinejoin = null;
        const strokeWidth = 1.5;
        const fill = "#999";
        const r = 3;
        const halo = "#fff";
        const haloWidth = 3;""")

        self.add_script(f"""const data = {json.dumps(asdict(self._root))}""")

        self.add_script("""
            const root = d3.hierarchy(data);

    const dx = 10;
    const dy = width / (root.height + padding);
    d3.tree().nodeSize([dx, dy])(root);

    // Center the tree.
    let x0 = Infinity;
    let x1 = -x0;
    root.each(d => {
        if (d.x > x1) x1 = d.x;
        if (d.x < x0) x0 = d.x;
    });

    height = x1 - x0 + dx * 2;

    svg
        .attr("viewBox", [-dy * padding / 2, x0 - dx, width, height])
        .attr("width", width)
        .attr("height", height)
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10);

    svg.append("g")
        .attr("fill", "none")
        .attr("stroke", stroke)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-linejoin", strokeLinejoin)
        .attr("stroke-width", strokeWidth)
        .selectAll("path")
        .data(root.links())
        .join("path")
        .attr("d", d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x));

    const node = svg.append("g")
        .selectAll("a")
        .data(root.descendants())
        .join("a")
        .attr("xlink:href", null)
        .attr("target", null)
        .attr("transform", d => `translate(${d.y},${d.x})`);

    node.append("circle")
        .attr("fill", d => d.children ? stroke : fill)
        .attr("r", r);

    node.append("text")
        .attr("dy", "0.32em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text((d, i) => d.data.name)
        .call(text => text.clone(true))
        .attr("fill", "none")
        .attr("stroke", halo)
        .attr("stroke-width", haloWidth);
        """)




