import logging
import numpy as  np


def load_xyz(self, index, dim_in=96, dim_out=64):
    # Get the path to X, Y files
    x_path, y_path = self.ids[index]
    values = {"x": np.loadtxt(x_path), "y": np.loadtxt(y_path)}
    for k, m in values.items():
        assert np.max(m)<dim_in
        m/=dim_in
        m*=(dim_out-1)
        m = np.unique(m, axis=0)
        m.astype(np.uint8)
        values[k]=m
    return self.cp2matrix(values["x"], dim=self.dim), self.cp2matrix(values["y"],dim=self.dim)


def matrix2cp(M):
    inds = np.argwhere(M==1.0)
    inds = np.array(inds).transpose()
    return inds


def cp2matrix(cp, dim=64):
    try:
        assert np.min(cp) >= 0
        assert np.max(cp) < dim
    except:
        logging.error(f"The size of the cp doesn't match the dim: {np.min(cp)} {np.max(cp)} {dim}")
        raise AssertionError
    cp = cp.astype(np.uint8)
    M = np.zeros((dim, dim, dim), dtype=np.float32)
    for x, y, z in cp:
        M[x,y,z]=1
    return M
