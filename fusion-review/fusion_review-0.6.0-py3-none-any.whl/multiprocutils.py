"""

"""


from fusion_review.intensities import IntensityDatabase
from fusion_review.figpan import IntensityTraceFigurePanel
from fusion_review.utilog import UserInputHandler, DataWriter
import matplotlib.pyplot as plt
from functools import partial
import multiprocessing
import numpy as np
import imageio
import os


def mpu_draw_to_tifs(intensity_superstructure):
    flow_start_dict = intensity_superstructure.get_flux_start()
    src_tuple = tuple(source for source in intensity_superstructure.sources)

    num_cores = multiprocessing.cpu_count() - 1
    pool = multiprocessing.Pool(num_cores)
    temp = partial(draw, flow_start_dict, intensity_superstructure)
    res = pool.map(func=temp, iterable=src_tuple)
    pool.close()
    pool.join()
    print("Processes converged.")


def draw(flow_dict, iss, src):
    print("Drawing in progress, source:\n{}".format(src))
    datum_key = iss.get_datum_key(src)
    ID = IntensityDatabase(iss.par, datum_key)
    ID.set_source(src)
    ID.get_traces(iss)
    ID.set_times(flow_dict[datum_key])

    itfp = IntensityTraceFigurePanel(ID.num_traces, 3, 4, ID)
    imarr = []
    dw = DataWriter(ID)
    dst_path = dw.set_drawings_dst()
    dw.set_output_dst()
    uih = UserInputHandler(itfp.rows, itfp.cols, itfp.curridx, ID)
    if os.path.exists(dw.output):
        uih.handle_resume(dw.output)
    trace_drawings_subdir = os.path.split(dst_path)[0]
    temp_path = os.path.join(trace_drawings_subdir, str(datum_key) + "-temp.tif")
    itfp.disp = False
    for panel in range(itfp.stidx, itfp.figs):
        if itfp.isSingle:
            itfp.handle_single_plot(panel + 1)
        else:
            fig, axes = itfp.form_panel(panel + 1)
            itfp.handle_multiple_plots(axes)
            fig.savefig(temp_path)
        plt.close()
        im = imageio.imread(temp_path, format="TIFF")
        imarr.append(im)
    os.remove(temp_path)
    imageio.mimwrite(dst_path, np.asarray(imarr), format="TIFF")
    print("Drawing completed:\n{}".format(dst_path))
