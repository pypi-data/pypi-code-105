
from ibmJupyterNotebookStyles.StylingBase import StyleComponent

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


class CustomColorMaps(StyleComponent):
    divergent_colorlist = ['#491d8b', '#6929c4', '#8a3ffc', '#a56eff', '#be95ff', '#d4bbff', '#e8daff',
                           '#f6f2ff', '#ffffff', '#d9fbfb', '#9ef0f0', '#3ddbd9', '#08bdba', '#009d9a', '#007d79', '#005d5d', '#004144']
    monochromatic_pos_colorlist = ['#ffffff', '#d9fbfb', '#9ef0f0', '#3ddbd9',
                                   '#08bdba', '#009d9a', '#007d79', '#005d5d', '#004144', '#022b30', '#081a1c']
    monochromatic_neg_colorlist = ['#1c0f30', '#31135e', '#491d8b', '#6929c4',
                                   '#8a3ffc', '#a56eff', '#be95ff', '#d4bbff', '#e8daff', '#f6f2ff', '#ffffff']

    def apply(self) -> None:
        CustomColorMaps.register_color_map(
            'divergent', self.divergent_colorlist)
        CustomColorMaps.register_color_map(
            'monochromatic_pos', self.monochromatic_pos_colorlist)
        CustomColorMaps.register_color_map(
            'monochromatic_neg', self.monochromatic_neg_colorlist)

    @classmethod
    def register_color_map(cls, cmap_name, colorlist):
        if cmap_name in plt.colormaps():
            return

        cmap = LinearSegmentedColormap.from_list(cmap_name, colorlist)
        plt.cm.register_cmap(cmap=cmap)
        plt.cm.register_cmap(cmap=cls.reverse_cmap(cmap))

    @classmethod
    def cmap_xmap(cls, function, cmap, name=None):
        """Applies function on the indices of colormap cmap. Beware, function
        should map the [0, 1] segment to itself, or you are in for surprises."""
        import copy
        cmap = copy.deepcopy(cmap)
        cdict = cmap._segmentdata
        for key in cdict:
            cdict[key] = sorted([(function(x[0]), x[1], x[2])
                                for x in cdict[key]])
        if name is not None:
            cmap.name = name
        return LinearSegmentedColormap(cmap.name, cdict, cmap.N)

    @classmethod
    def reverse_cmap(cls, cmap, newname=None):
        """Reverse a given matplotlib colormap instance"""
        if newname is None:
            newname = cmap.name + '_r'
        return cls.cmap_xmap(lambda x: -1.*(x-1.), cmap, name=newname)