import numpy as np
import matplotlib.pyplot as plt





def sample_func(xx, yy):
  zz = xx + yy * 2
  return zz



if __name__ == '__main__':
  draw_2d_contour(sample_func)
