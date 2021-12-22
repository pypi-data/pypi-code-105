from torch.utils.data import Dataset
import random
from nmesh import NMesh
from ctdataset.functional import *
import numpy as np
from gnutools.fs import name, parent, listfiles
from gnutools.concurrent import ProcessPoolExecutorBar

class FolderVox:
    def __init__(self,
                 folder,
                 dims=(12, 96),
                 return_matrix=False):
        self._return_matrix = return_matrix
        self._folder = folder
        self._dims = dims
        self.x, self.y = self.run()

    def run(self):
        x, y = self.crop_from_folder(self._folder, self._dims[0])
        x, y = self.voxelize(x, y, dims=self._dims, return_matrix=self._return_matrix)
        return x, y

    @staticmethod
    def crop_from_folder(folder, dim):
        x = NMesh(list=[NMesh(f"{folder}/antagonistscan.ply"), NMesh(f"{folder}/preparationscan.ply")])
        y = NMesh(f"{folder}/crown.ply")
        T = y.centroid
        bbox = [[-dim, -dim, -dim], [dim, dim, dim]]
        for m in [x, y]:
            m.translate(-T)
            m.crop_bounding_box(bbox)
        return x, y

    @staticmethod
    def voxelize(x, y, dims=(12, 96), return_matrix=True):
        U = np.ones(3)*dims[0]
        x_vertices = x.vertices
        y_vertices = y.vertices
        d = {}
        for cat, v in [("x", x_vertices), ("y", y_vertices)]:
            v+=U
            v/=2*U
            d[cat] = np.unique(np.array(v*(dims[1]-1), dtype=np.uint8), axis=0)
        (x, y) = (FolderVox.cp2matrix(d["x"], dims[1]), FolderVox.cp2matrix(d["y"], dims[1])) if return_matrix else (d["x"], d["y"])
        return x, y

    @staticmethod
    def cp2matrix(cp, dim=96):
        return cp2matrix(cp, dim)

    @staticmethod
    def matrix2cp(M):
        return matrix2cp(M)


class CTDataset(Dataset):
    def __init__(
            self,
            ply_root,
            cls         = FolderVox,
            dims        = (12, 96),
            cache       = False,
            limit       = -1
    ):

        self.dims = dims
        self.cls = cls
        self.cache = cache
        folders = list(set(list([parent(file) for file in listfiles(ply_root, [".ply"])])))[:limit]
        bar = ProcessPoolExecutorBar()
        _args = (self.dims, self.cache, self.cls)
        bar.submit([(self.load_folder, folder, *_args) for folder in folders])
        self.records  = dict([(k, r[1]) for k, r in enumerate(bar._results)])
        self.ids    = list(self.records.keys())
        self.size   = len(self.ids)

    @staticmethod
    def load_folder(folder, dims, cache, cls):
        return (name(folder), cls(folder, dims, return_matrix=cache))

    def __getitem__(self, index):
        if not self.cache:
            return cp2matrix(self.records[index].x, self.dims[1]), \
                   cp2matrix(self.records[index].y, self.dims[1]), \
                   [], \
                   str(index), \
                   ""
        else:
            return self.records[index].x, \
                   self.records[index].y, \
                   [], \
                   str(index), \
                   ""

    def __len__(self):
        return self.size

    def shuffle(self):
        random.shuffle(self.ids)




