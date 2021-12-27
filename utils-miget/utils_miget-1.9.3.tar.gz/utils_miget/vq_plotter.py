
# Useful plotting functions to represent a defined V/Q distribution with given parameters and to graph MIGET output data

def plot_defined_vq(qt, sdq1, sdq2, qmean1, qmean2, qratio, vdvt, qsqt, 
save = False, name_saved_file = None, file_extension = "jpg", resolution = 600):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.interpolate import interp1d

    qrest = qt*(1-qsqt/100)
    vqlo = 0.005
    vqhi = 100
    ncomp = 48
    slo = 0.001
    shi = 1000
    nsol = 11

    df_comps = pd.DataFrame()
    df_comps["comparts"] = np.arange(1, 49)

    b1 = 1
    b2 = 2
    b3 = 3
    b4 = 4
    b5 = 5
    b6 = 6
    b7 = 7
    b8 = 8
    b9 = 9
    b10 = 10
    b11 = 11
    delta = (np.log(vqhi/vqlo))/(ncomp-1)

    df_comps["vq_comparts"] = vqlo*(np.exp(delta*(df_comps.comparts-1)))

    d11 = np.log(qmean1) - np.log(df_comps.vq_comparts)
    d12 = np.log(qmean2) - np.log(df_comps.vq_comparts)
    rexp1 = -0.5 * d11 * d11/(sdq1*sdq1)
    rexp2 = -0.5 * d12*d12/(sdq2*sdq2)

    df_comps["main_mode_bf"] = np.exp(rexp1)
    df_comps["secondary_mode_bf"] = qratio*np.exp(rexp2)
    df_comps["bf_combined"] = df_comps.main_mode_bf + df_comps.secondary_mode_bf
    sumq = np.sum(df_comps.bf_combined)
    df_comps["perfusion_normalized"] = qrest*df_comps.bf_combined/sumq
    df_comps["ventilation_normalized"] = df_comps.perfusion_normalized * df_comps.vq_comparts

    va = np.sum(df_comps.ventilation_normalized)
    ve = va/(1-vdvt/100)

    df_gas = pd.DataFrame()
    df_gas["gases"] = np.arange(1, 12)

    deltas = (np.log(shi/slo))/(nsol-1)
    df_gas["partition_coefficients"] = slo*(np.exp(deltas*(df_gas.gases-1)))

    df_gas["retentions_no_shunt"] = np.repeat(np.nan, 11)
    df_gas["excretions_no_deadspace"] = np.repeat(np.nan, 11)


    a1 = df_gas.loc[b1-1, "partition_coefficients"]
    df_gas.loc[b1-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a1/(a1+df_comps.vq_comparts))/qrest
    df_gas.loc[b1-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a1/(a1+df_comps.vq_comparts))/va

    a2 = df_gas.loc[b2-1, "partition_coefficients"]
    df_gas.loc[b2-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a2/(a2+df_comps.vq_comparts))/qrest
    df_gas.loc[b2-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a2/(a2+df_comps.vq_comparts))/va

    a3 = df_gas.loc[b3-1, "partition_coefficients"]
    df_gas.loc[b3-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a3/(a3+df_comps.vq_comparts))/qrest
    df_gas.loc[b3-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a3/(a3+df_comps.vq_comparts))/va


    a4 = df_gas.loc[b4-1, "partition_coefficients"]
    df_gas.loc[b4-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a4/(a4+df_comps.vq_comparts))/qrest
    df_gas.loc[b4-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a4/(a4+df_comps.vq_comparts))/va


    a4 = df_gas.loc[b4-1, "partition_coefficients"]
    df_gas.loc[b4-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a4/(a4+df_comps.vq_comparts))/qrest
    df_gas.loc[b4-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a4/(a4+df_comps.vq_comparts))/va

    a4 = df_gas.loc[b4-1, "partition_coefficients"]
    df_gas.loc[b4-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a4/(a4+df_comps.vq_comparts))/qrest
    df_gas.loc[b4-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a4/(a4+df_comps.vq_comparts))/va

    a5 = df_gas.loc[b5-1, "partition_coefficients"]
    df_gas.loc[b5-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a5/(a5+df_comps.vq_comparts))/qrest
    df_gas.loc[b5-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a5/(a5+df_comps.vq_comparts))/va


    a6 = df_gas.loc[b6-1, "partition_coefficients"]
    df_gas.loc[b6-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a6/(a6+df_comps.vq_comparts))/qrest
    df_gas.loc[b6-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a6/(a6+df_comps.vq_comparts))/va


    a7 = df_gas.loc[b7-1, "partition_coefficients"]
    df_gas.loc[b7-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a7/(a7+df_comps.vq_comparts))/qrest
    df_gas.loc[b7-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a7/(a7+df_comps.vq_comparts))/va


    a8 = df_gas.loc[b8-1, "partition_coefficients"]
    df_gas.loc[b8-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a8/(a8+df_comps.vq_comparts))/qrest
    df_gas.loc[b8-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a8/(a8+df_comps.vq_comparts))/va

    a9 = df_gas.loc[b9-1, "partition_coefficients"]
    df_gas.loc[b9-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a9/(a9+df_comps.vq_comparts))/qrest
    df_gas.loc[b9-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a9/(a9+df_comps.vq_comparts))/va


    a10 = df_gas.loc[b10-1, "partition_coefficients"]
    df_gas.loc[b10-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a10/(a10+df_comps.vq_comparts))/qrest
    df_gas.loc[b10-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a10/(a10+df_comps.vq_comparts))/va

    a10 = df_gas.loc[b10-1, "partition_coefficients"]
    df_gas.loc[b10-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a10/(a10+df_comps.vq_comparts))/qrest
    df_gas.loc[b10-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a10/(a10+df_comps.vq_comparts))/va

    a11 = df_gas.loc[b11-1, "partition_coefficients"]
    df_gas.loc[b11-1, "retentions_no_shunt"] = np.sum(df_comps.perfusion_normalized*a11/(a11+df_comps.vq_comparts))/qrest
    df_gas.loc[b11-1, "excretions_no_deadspace"] = np.sum(df_comps.ventilation_normalized*a11/(a11+df_comps.vq_comparts))/va

    df_gas["retentions_shunt"] = qsqt/100 + (1-qsqt/100)*df_gas.retentions_no_shunt
    df_gas["excretions_deadspace"] = (1-vdvt/100)*df_gas.excretions_no_deadspace
    df_gas["retentions_homogeneous"] = df_gas["partition_coefficients"]/(df_gas["partition_coefficients"] + va/qt)
    df_gas["excretions_homogeneous"] = (1-vdvt/100)*df_gas["partition_coefficients"]/(df_gas["partition_coefficients"]+va/qt)

    df_shunt = pd.DataFrame()
    df_shunt["vq_shunt"] = np.array([0.0016, 0.0016])
    df_shunt["bf_shunt"] = np.array([(0.01*qsqt*qt), 0])
    df_shunt["ventilation_shunt"] = np.repeat(0, 2)


    comparts_interpolated = np.linspace(0.005, 99, num=100000, endpoint=True)

    interpolated_perfusion_f = interp1d(df_comps.vq_comparts,  df_comps.perfusion_normalized, kind='cubic')
    perfusion_smoothed = interpolated_perfusion_f(comparts_interpolated)

    interpolated_ventilation_f = interp1d(df_comps.vq_comparts,  df_comps.ventilation_normalized, kind='cubic')
    ventilation_smoothed = interpolated_ventilation_f(comparts_interpolated)


    fig, (ax, ax2) = plt.subplots(1,2,figsize=(15,8))
    ax.grid(alpha = 0.2)

    ax.plot(comparts_interpolated, perfusion_smoothed, c = "firebrick")
    ax.scatter(df_comps.vq_comparts, df_comps.perfusion_normalized, label = "Perfusion", color = "firebrick")

    ax.plot(comparts_interpolated, ventilation_smoothed, "--", color = "cornflowerblue")
    ax.scatter(df_comps.vq_comparts, df_comps.ventilation_normalized, label = "Ventilation", marker="s", color = "cornflowerblue")

    ax.plot(df_shunt.vq_shunt, df_shunt.bf_shunt, linewidth = 0.5, c = "firebrick")
    ax.scatter(df_shunt.vq_shunt[0], df_shunt.bf_shunt[0], c = "firebrick")

    ax.semilogx()
    ax.set_xlabel("Ventilation/Perfusion", fontsize = 14)
    ax.set_ylabel("Blood flow & ventilation (l/min)", fontsize = 14)
    ax.legend(fontsize = 14)
    ax.set_title("Distribution of Ventilation and Perfusion", fontsize = 16)

    ################



    ax2.grid(alpha = 0.2)
    ax2.plot(df_gas.partition_coefficients, df_gas.retentions_homogeneous, c = "steelblue", linestyle = "dashed", linewidth = 1, label = "Retentions, homogeneous")
    ax2.scatter(df_gas.partition_coefficients, df_gas.retentions_homogeneous, s = 20, c = "steelblue")

    ax2.plot(df_gas.partition_coefficients, df_gas.retentions_shunt, c = "steelblue", linestyle = "solid", linewidth = 2, label = "Retentions, measured")
    ax2.scatter(df_gas.partition_coefficients, df_gas.retentions_shunt, s = 50, c = "steelblue")


    ax2.plot(df_gas.partition_coefficients, df_gas.excretions_homogeneous, c = "darkorange", linestyle = "dashed", linewidth = 1, label = "Excretions, homogeneous")
    ax2.scatter(df_gas.partition_coefficients, df_gas.excretions_homogeneous, s = 20, c = "darkorange", marker = "s")

    ax2.plot(df_gas.partition_coefficients, df_gas.excretions_deadspace, c = "darkorange", linestyle = "solid", linewidth = 2, label = "Excretions, measured")
    ax2.scatter(df_gas.partition_coefficients, df_gas.excretions_deadspace, s = 50, c = "darkorange", marker = "s")


    ax2.semilogx()
    ax2.set_xlabel("Gas-blood partition coefficient", fontsize = 14)
    ax2.set_ylabel(r"$\frac {P_a}{P_v}$   or   $\frac {P_e}{P_v}$", fontsize = 14)

    ax2.legend(fontsize = 11, loc = "upper left")

    ax2.set_title("Retentions and Excretions of inert gases", fontsize = 16)

    if save == True:
        name_to_save = name_saved_file + "." + file_extension
        plt.savefig(name_to_save, dpi = resolution)
    else:
        pass


    plt.show()


def plot_miget_output(path_to_txt, save = False, name_saved_file = None, file_extension = "jpg", resolution = 600):

    import pandas as pd
    import numpy as np
    from scipy.interpolate import interp1d
    import matplotlib.pyplot as plt

    # The function takes as input a file output of VQBOHR to plot publication-ready MIGET plots
    # The various arguments are used to adjust the saving process: name, extension and resolution

    f = open(path_to_txt)

    comparts = np.array([])
    perfusions = np.array([])
    ventilations = np.array([])

    for counter, line in enumerate(f):

        for order, element in enumerate(line.split()):
            
            if order == 0:
                comparts = np.append(comparts, float(element))
            elif order == 1:
                ventilations = np.append(ventilations, float(element))
            elif order == 2:
                perfusions = np.append(perfusions, float(element))

        if counter == 0:
            shunt = float(line.split()[3])
        elif counter == 49:
            deadspace = float(line.split()[4])


    qs = shunt/(shunt + perfusions.sum())
    qs_100 = np.round(qs*100, 1)

    vd_vt = deadspace/(ventilations.sum() + deadspace)
    vd_vt_100 = np.round(vd_vt * 100, 1)

    comparts_interpolated = np.linspace(0.005, 99, num=100000, endpoint=True)

    interpolated_perfusion_f = interp1d(comparts,  perfusions, kind='cubic')
    perfusion_smoothed = interpolated_perfusion_f(comparts_interpolated)

    interpolated_ventilation_f = interp1d(comparts,  ventilations, kind='cubic')
    ventilation_smoothed = interpolated_ventilation_f(comparts_interpolated)


    perfusions = np.delete(perfusions, [0, -1])
    comparts = np.delete(comparts, [0, -1])
    ventilations = np.delete(ventilations, [0, -1])


    if perfusions.max() > ventilations.max():
        top = perfusions.max()
    else:
        top = ventilations.max()


    fig, (ax) = plt.subplots(1,1,figsize=(10,8))
    ax.grid(alpha = 0.2)


    ax.plot(comparts_interpolated, ventilation_smoothed, "--", color = "cornflowerblue", alpha = 0.8)
    ax.scatter(comparts, ventilations, label = "Ventilation", marker="s", color = "cornflowerblue", alpha = 0.8)

    ax.plot(comparts_interpolated, perfusion_smoothed, c = "firebrick", alpha = 0.8)
    ax.scatter(comparts, perfusions, label = "Perfusion", color = "firebrick", alpha = 0.8)

    if shunt >= perfusions.max():

        ax.plot(0.001, top, 'firebrick', marker=r'$\uparrow$', markersize=20)
        ax.annotate(f"Shunt = {qs_100}%", (0.0006, top-0.06), color = "firebrick", fontsize = 13)
    else:
        ax.plot([0.001, 0.001], [shunt, 0], color = "firebrick", linewidth = 1, alpha = 0.8)
        ax.scatter(0.001, shunt, color = "firebrick", s = 70)
        ax.annotate(f"Shunt = {qs_100}%", (0.0014, shunt-0.025), color = "firebrick", fontsize = 13)


    ax.plot(1000, top, 'cornflowerblue', marker=r'$\uparrow$', markersize=20)
    ax.annotate(f"Deadspace = {vd_vt_100}%", (40, top-0.06), color = "cornflowerblue", fontsize = 13)


    ax.semilogx()
    ax.set_xlabel("Ventilation/Perfusion", fontsize = 14)
    ax.set_ylabel("Blood flow & ventilation (l/min)", fontsize = 14)
    ax.legend(fontsize = 14)
    ax.set_title("Distribution of Ventilation and Perfusion", fontsize = 16)

    if save == True:
        name_to_save = name_saved_file + "." + file_extension
        plt.savefig(name_to_save, dpi = resolution)
    else:
        pass


    plt.show()