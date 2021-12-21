import os
import re
import warnings
import nibabel
import copy
import numpy as np


def calc_e_in_midlayer_roi(phi_dadt, roi, subject, phi_scaling=1., mesh_idx=0, mesh=None, roi_hem='lh', depth=.5,
                           qoi=None):
    """
    This is to be called by Simnibs as postprocessing function per FEM solve.

    Parameters
    ----------
    phi_dadt : (array-like, elmdata)
    roi : pynibs.roi.RegionOfInterestSurface()
    subject: pynibs.Subject()
    phi_scaling : float
    mesh_idx : int
    mesh : simnibs.msh.Mesh()
    roi_hem : 'lh'
    depth : float
    qoi : list of str

    Returns
    -------
    (roi.n_tris,4) : np.vstack((e_mag, e_norm, e_tan, e_angle)).transpose()
    """
    from .main import data_nodes2elements
    import simnibs.msh.mesh_io as mesh_io
    import simnibs.simulation.fem as fem
    from simnibs.msh.transformations import get_surface_names_from_folder_structure
    from simnibs.msh.mesh_io import Msh
    from simnibs.msh.mesh_io import Nodes
    from simnibs.msh.mesh_io import Elements

    mesh_folder = subject.mesh[mesh_idx]["mesh_folder"]

    # set default return quantities
    if qoi is None:
        qoi = ['E', 'mag', 'norm', 'tan', 'angle']
    qois_to_calc = copy.copy(qoi)
    ret_arr_shape = len(qoi)

    # some special care for E
    if 'E' in qoi:
        ret_arr_shape += 2  # E is 3D
        qois_to_calc.remove('E')  # we don't need this to be computed, it already is

    # simnibs calls this with empty data so find out about the results dimensions
    if isinstance(phi_dadt, tuple):
        phi = phi_dadt[0] * phi_scaling
        # dadt = phi_dadt[1].elm_data2node_data().value
    else:
        return np.zeros((roi.n_tris, ret_arr_shape))

    def calc_quantities(nd, quants):
        quants = dict.fromkeys(quants)
        for quant in quants:
            if quant == 'mag':
                quants[quant] = nd.norm()
            elif quant == 'norm':
                quants[quant] = nd.normal()
                quants[quant].value *= -1
            elif quant == 'tan':
                quants[quant] = nd.tangent()
            elif quant == 'angle':
                quants[quant] = nd.angle()
            else:
                raise ValueError('Invalid quantity: {0}'.format(quant))
        return quants

    # prepare mesh_local
    mesh_local = copy.deepcopy(mesh)

    # write phi and dAdt in msh
    # dadt = mesh_io.NodeData(dadt, name='D', mesh=mesh_local)
    try:
        dadt = phi_dadt[1].value
    except AttributeError:
        dadt = phi_dadt[1]
    dadt = mesh_io.ElementData(dadt, name='D', mesh=mesh_local)
    phi = mesh_io.NodeData(phi.flatten(), name='v', mesh=mesh_local)

    mesh_local = fem.calc_fields(phi, "vDEe", cond=None, dadt=dadt)
    mesh_local = mesh_local.crop_mesh(2)

    # get folder names and such
    m2m_folder = os.path.join(mesh_folder, "m2m_" + subject.id)
    m2m_folder = os.path.abspath(os.path.normpath(m2m_folder))
    names, segtype = get_surface_names_from_folder_structure(m2m_folder)
    # middle_surf = {}

    # get midlayer
    if segtype == 'mri2mesh':
        # for hemi in ['lh', 'rh']:
        wm_surface = mesh_io.read_freesurfer_surface(names[roi_hem + '_wm'])
        gm_surface = mesh_io.read_freesurfer_surface(names[roi_hem + '_gm'])
        middle_surf = mesh_io._middle_surface(wm_surface, gm_surface, depth)
    elif segtype == 'headreco':
        # for hemi in ['lh', 'rh']:
        middle_surf = mesh_io.read_gifti_surface(names[roi_hem + '_midgm'])
    else:
        raise NotImplementedError(f"segtype {segtype} unknown.")

    # initialize ROI surface
    surface = Msh(nodes=Nodes(node_coord=roi.node_coord_mid),
                  elements=Elements(triangles=roi.node_number_list+1))

    # calc QOIs
    qois_dict = {}
    data = mesh_local.field['E']
    data = data.as_nodedata()
    interpolated = data.interpolate_to_surface(surface)

    q = calc_quantities(interpolated, qois_to_calc)
    for q_name, q_data in q.items():
        qois_dict[q_name] = q_data.value

    for q_name in qoi:
        if q_name == 'E':
            qois_dict[q_name] = interpolated.value

        # transform point data to element data
        qois_dict[q_name] = data_nodes2elements(data=qois_dict[q_name], con=roi.node_number_list)
        # crop results data to ROI
        qois_dict[q_name] = qois_dict[q_name]
        if qois_dict[q_name].ndim == 1:
            qois_dict[q_name] = qois_dict[q_name][:, np.newaxis]

    res = tuple(qois_dict[q_name] for q_name in qoi)
    return np.hstack(res)


# def calc_e_in_midlayer_roi(phi_dadt, roi, subject, phi_scaling=1., mesh_idx=0, mesh=None, roi_hem='lh', depth=.5,
#                            qoi=None):
#     """
#     This is to be called by Simnibs as postprocessing function per FEM solve.
#
#     Parameters
#     ----------
#     phi_dadt : (array-like, elmdata)
#     roi : pynibs.roi.RegionOfInterestSurface()
#     subject: pynibs.Subject()
#     phi_scaling : float
#     mesh_idx : int
#     mesh : simnibs.msh.Mesh()
#     roi_hem : 'lh'
#     depth : float
#     qoi : list of str
#
#     Returns
#     -------
#     (roi.n_tris,4) : np.vstack((e_mag, e_norm, e_tan, e_angle)).transpose()
#     """
#     from .main import data_nodes2elements
#     import simnibs.msh.mesh_io as mesh_io
#     import simnibs.simulation.fem as fem
#     from simnibs.msh.transformations import get_surface_names_from_folder_structure
#
#     mesh_folder = subject.mesh[mesh_idx]["mesh_folder"]
#
#     # set default return quantities
#     if qoi is None:
#         qoi = ['E', 'mag', 'norm', 'tan', 'angle']
#     qois_to_calc = copy.copy(qoi)
#     ret_arr_shape = len(qoi)
#
#     # some special care for E
#     if 'E' in qoi:
#         ret_arr_shape += 2  # E is 3D
#         qois_to_calc.remove('E')  # we don't need this to be computed, it already is
#
#     # simnibs calls this with empty data so find out about the results dimensions
#     if isinstance(phi_dadt, tuple):
#         phi = phi_dadt[0] * phi_scaling
#         # dadt = phi_dadt[1].elm_data2node_data().value
#     else:
#         return np.zeros((roi.n_tris, ret_arr_shape))
#
#     def calc_quantities(nd, quants):
#         quants = dict.fromkeys(quants)
#         for quant in quants:
#             if quant == 'mag':
#                 quants[quant] = nd.norm()
#             elif quant == 'norm':
#                 quants[quant] = nd.normal()
#                 quants[quant].value *= -1
#             elif quant == 'tan':
#                 quants[quant] = nd.tangent()
#             elif quant == 'angle':
#                 quants[quant] = nd.angle()
#             else:
#                 raise ValueError('Invalid quantity: {0}'.format(quant))
#         return quants
#
#     # prepare mesh_local
#     mesh_local = copy.deepcopy(mesh)
#
#     # write phi and dAdt in msh
#     # dadt = mesh_io.NodeData(dadt, name='D', mesh=mesh_local)
#     try:
#         dadt = phi_dadt[1].value
#     except AttributeError:
#         dadt = phi_dadt[1]
#     dadt = mesh_io.ElementData(dadt, name='D', mesh=mesh_local)
#     phi = mesh_io.NodeData(phi.flatten(), name='v', mesh=mesh_local)
#
#     mesh_local = fem.calc_fields(phi, "vDEe", cond=None, dadt=dadt)
#     mesh_local = mesh_local.crop_mesh(2)
#
#     # get folder names and such
#     m2m_folder = os.path.join(mesh_folder, "m2m_" + subject.id)
#     m2m_folder = os.path.abspath(os.path.normpath(m2m_folder))
#     names, segtype = get_surface_names_from_folder_structure(m2m_folder)
#     # middle_surf = {}
#
#     # get midlayer
#     if segtype == 'mri2mesh':
#         # for hemi in ['lh', 'rh']:
#         wm_surface = mesh_io.read_freesurfer_surface(names[roi_hem + '_wm'])
#         gm_surface = mesh_io.read_freesurfer_surface(names[roi_hem + '_gm'])
#         middle_surf = mesh_io._middle_surface(wm_surface, gm_surface, depth)
#     elif segtype == 'headreco':
#         # for hemi in ['lh', 'rh']:
#         middle_surf = mesh_io.read_gifti_surface(names[roi_hem + '_midgm'])
#     else:
#         raise NotImplementedError(f"segtype {segtype} unknown.")
#
#     # calc QOIs
#     qois_dict = {}
#     data = mesh_local.field['E']
#     name = 'E'
#
#     data = data.as_nodedata()
#     interpolated = data.interpolate_to_surface(middle_surf)
#
#     q = calc_quantities(interpolated, qois_to_calc)
#     for q_name, q_data in q.items():
#         qois_dict[q_name] = q_data.value
#         middle_surf.add_node_field(q_data, name + '_' + q_name)
#
#     # load freesurfer surface
#     if type(roi.gm_surf_fname) is np.ndarray:
#         if roi.gm_surf_fname.ndim == 0:
#             roi.gm_surf_fname = [roi.gm_surf_fname.astype(str).tolist()]
#         else:
#             roi.gm_surf_fname = roi.gm_surf_fname.astype(str).tolist()
#
#     # if not isinstance(roi.gm_surf_fname, str):
#     #     raise NotImplementedError
#
#     if roi.gm_surf_fname in ('None', None, ''):
#         nodes_gm, tri_gm = nibabel.freesurfer.read_geometry(os.path.join(mesh_folder, roi.midlayer_surf_fname))
#     else:
#         nodes_gm, tri_gm = nibabel.freesurfer.read_geometry(os.path.join(mesh_folder, roi.gm_surf_fname))
#
#     if roi.fn_mask is None:
#         roi_mask_bool = (roi.node_coord_mid[:, 0] > min(roi.X_ROI)) & (
#                 roi.node_coord_mid[:, 0] < max(roi.X_ROI)) & \
#                         (roi.node_coord_mid[:, 1] > min(roi.Y_ROI)) & (
#                                 roi.node_coord_mid[:, 1] < max(roi.Y_ROI)) & \
#                         (roi.node_coord_mid[:, 2] > min(roi.Z_ROI)) & (
#                                 roi.node_coord_mid[:, 2] < max(roi.Z_ROI))
#         roi_mask_idx = np.where(roi_mask_bool)
#
#     else:
#         if type(roi.fn_mask) is np.ndarray:
#             if roi.fn_mask.ndim == 0:
#                 roi.fn_mask = roi.fn_mask.astype(str).tolist()
#
#         # read mask from freesurfer mask file (mask for freesurfer .pial)
#         mask = nibabel.freesurfer.mghformat.MGHImage.from_filename(os.path.join(mesh_folder, roi.fn_mask)).dataobj[:]
#         roi_mask_idx = np.where(mask > 0.5)
#
#     # get row index where all points are lying inside ROI
#     # find triangles idx which have all nodes in mask
#     # this is the old version:
#     # con_row_idx = [i for i in range(tri_gm.shape[0]) if len(np.intersect1d(tri_gm[i,], roi_mask_idx)) == 3]
#     # new, faster verion. might be more picky on dimensions
#     con_row_idx = np.where(np.isin(tri_gm[:, 0], roi_mask_idx) &
#                            np.isin(tri_gm[:, 1], roi_mask_idx) &
#                            np.isin(tri_gm[:, 2], roi_mask_idx))[0]
#     # assert np.all(con_row_idx_fast == con_row_idx) # yep
#
#     if roi_hem == 'rh':
#         warnings.warn("rh is untested")
#     # elif roi_hem == 'rh':
#     #     hem_idx = 1
#     #     warnings.warn("Right hemisphere roi is untested.")
#     # else:
#     #     raise NotImplementedError
#
#     for q_name in qoi:
#         if q_name == 'E':
#             qois_dict[q_name] = interpolated.value
#         # else:
#         #     qois_dict[q_name] = qois_dict[q_name]
#
#         # transform point data to element data
#         qois_dict[q_name] = data_nodes2elements(data=qois_dict[q_name], con=tri_gm)
#         # crop results data to ROI
#         qois_dict[q_name] = qois_dict[q_name][con_row_idx]
#         if qois_dict[q_name].ndim == 1:
#             qois_dict[q_name] = qois_dict[q_name][:, np.newaxis]
#
#     res = tuple(qois_dict[q_name] for q_name in qoi)
#     return np.hstack(res)


def read_coil_geo(fn_coil_geo):
    """
    Parameters
    ----------
    fn_coil_geo : str
        Filename of *.geo file created from SimNIBS containing the dipole information

    Returns
    -------
    dipole_pos : ndarray of float [n_dip x 3]
        Dipole positions (x, y, z)
    dipole_mag : ndarray of float [n_dip x 1]
        Dipole magnitude
    """
    regex = r"\((.*?)\)\{(.*?)\}"
    file = open(fn_coil_geo)
    read = True
    dipole_pos = []
    dipole_mag = []

    while read:
        te = file.readline()

        if te == "":
            break

        matches = re.finditer(regex, te, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                if groupNum == 1:
                    dipole_pos.append([float(x) for x in match.group(groupNum).split(',')])
                if groupNum == 2:
                    dipole_mag.append(float(match.group(groupNum)))

    dipole_pos = np.vstack(dipole_pos)
    dipole_mag = np.array(dipole_mag)[:, np.newaxis]

    return dipole_pos, dipole_mag
