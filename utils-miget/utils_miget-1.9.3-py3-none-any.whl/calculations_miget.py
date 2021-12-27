
## The following functions need to run on a Pandas DataFrame (containing the dataset of the MIGET measurements)

def miget_dataset_preparation(d):

    import pandas as pd

    # The function takes as input the dataset and performs calculations to prepare it for subsequent analysis
    
    def calculate_bsa(row):  #DuBois Formula to calculate Body Surface Area

        if row["sex"] == "f":
            bsa = 0.007184 * (row["weight"]**0.425) * (row["height"]**0.725)
            return bsa
        else:
            bsa = 0.007184 * (row["weight"]**0.425) * (row["height"]**0.725)
            return bsa


    def o2_content(hb, sat, po2):

        content = 1.39 * hb * (sat/100) + 0.00304 * po2
        return content
    
    
    d["bsa_recalculated"] = d.apply(lambda row: calculate_bsa(row), axis = 1)

    # The next lines calculate the cardiac output during the actual MIGET measurement

    d["co_recalculated"] = d["ci"] * d["bsa_recalculated"]
    d["co_recalculated_a1"] = d["ci_a1"] * d["bsa_recalculated"] 
    d["co_recalculated_a2"] = d["ci_a2"] * d["bsa_recalculated"]

    # Next come the calculations related to gas exchange

    d["cao2"] = d.apply(lambda row: o2_content(row["art_hb_coox"], row["art_so2_calc"], row["art_po2"]), axis = 1)
    d["cvo2"] = d.apply(lambda row: o2_content(row["ven_hb_coox"], row["ven_so2_calc"], row["ven_po2"]), axis = 1)


    d["vo2"] = d["co_recalculated_a1"] * (d["cao2"] - d["cvo2"]) * 10     ###### FIX NEEDED: adjust BTPS and STPD!! #######
    d["r"] = d["vco2"] / d["vo2"]
    d["palv_o2"] = 713 * d["fio2"] - ((d["art_pco2"]*(1-d["fio2"]*(1-d["r"])))/d["r"])
    d["aado2"] = d["palv_o2"] - d["art_po2"]

    d["cco2"] = d.apply(lambda row: o2_content(row["art_hb_coox"], 100, row["palv_o2"]), axis = 1)
    d["qsqt"] = (d["cco2"] - d["cao2"])/(d["cco2"]- d["cvo2"])

    d["va"] = (863 * d["vco2"])/d["art_pco2"]  ### FIX NEEDED: use the alveolar ventilation with mixing box
    d["vd_vt"] = ((d["ve"]*1000) - d["va"])/(d["ve"]*1000)


    # Next we perform all the calculations to calculate blood density and all the volumes from the weights required


    d["blood_density"] = 1
    d["heparin_density"] = 1
    d["vial_volume"] = 12

    d["pooled_blood_hep_syr"] = d.c1_blood + d.a1_blood + d.a2_blood
    d["pooled_hep_syr"] = d.c1_heparin + d.a1_heparin + d.a2_heparin
    d["pooled_tare"] = d.c1_dry + d.a1_dry + d.a2_dry

    d["pooled_heparin_weight"] = d.pooled_hep_syr - d.pooled_tare
    d["pooled_heparin_volume"] = d.pooled_heparin_weight/d.heparin_density
    d["pooled_blood_weight"] = d.pooled_blood_hep_syr -  d.pooled_heparin_weight - d.pooled_tare
    d["pooled_blood_volume"] = (d.c1_tot_vol + d.a1_tot_vol + d.a2_tot_vol) - d.pooled_heparin_volume
    d["pooled_blood_density"] = d.pooled_blood_weight / d.pooled_blood_volume

    d["vial_a1_blood_volume"] = (d.vial_a1_blood - d.vial_a1_dry)/d.pooled_blood_density
    d["vial_a2_blood_volume"] = (d.vial_a2_blood - d.vial_a2_dry)/d.pooled_blood_density

    d["vial_a1_gas_volume"] = d.vial_volume - d.vial_a1_blood_volume
    d["vial_a2_gas_volume"] = d.vial_volume - d.vial_a2_blood_volume


    # Dafault partition coefficients

    d["lambda_acetone_def"] = 317
    d["lambda_dth_def"] = 12.3
    d["lambda_iso_def"] = 1.45
    d["lambda_cyclo_def"] = 0.749
    d["lambda_ethane_def"] = 0.132
    d["lambda_sf6_def"] = 0.00658


    # Equilibration of gases in the vial

    d["a1_sf6_area_volumecorrected"] = d["a1_sf6_area"] * (d["vial_a1_blood_volume"]*d["lambda_sf6_def"]+d["vial_a1_gas_volume"])/(d["vial_a1_blood_volume"]*d["lambda_sf6_def"])
    d["a2_sf6_area_volumecorrected"] = d["a2_sf6_area"] * (d["vial_a2_blood_volume"]*d["lambda_sf6_def"]+d["vial_a2_gas_volume"])/(d["vial_a2_blood_volume"]*d["lambda_sf6_def"])

    d["a1_ethane_area_volumecorrected"] = d["a1_ethane_area"] * (d["vial_a1_blood_volume"]*d["lambda_ethane_def"]+d["vial_a1_gas_volume"])/(d["vial_a1_blood_volume"]*d["lambda_ethane_def"])
    d["a2_ethane_area_volumecorrected"] = d["a2_ethane_area"] * (d["vial_a2_blood_volume"]*d["lambda_ethane_def"]+d["vial_a2_gas_volume"])/(d["vial_a2_blood_volume"]*d["lambda_ethane_def"])

    d["a1_cyclo_area_volumecorrected"] = d["a1_cyclo_area"] * (d["vial_a1_blood_volume"]*d["lambda_cyclo_def"]+d["vial_a1_gas_volume"])/(d["vial_a1_blood_volume"]*d["lambda_cyclo_def"])
    d["a2_cyclo_area_volumecorrected"] = d["a2_cyclo_area"] * (d["vial_a2_blood_volume"]*d["lambda_cyclo_def"]+d["vial_a2_gas_volume"])/(d["vial_a2_blood_volume"]*d["lambda_cyclo_def"])

    d["a1_iso_area_volumecorrected"] = d["a1_iso_area"] * (d["vial_a1_blood_volume"]*d["lambda_iso_def"]+d["vial_a1_gas_volume"])/(d["vial_a1_blood_volume"]*d["lambda_iso_def"])
    d["a2_iso_area_volumecorrected"] = d["a2_iso_area"] * (d["vial_a2_blood_volume"]*d["lambda_iso_def"]+d["vial_a2_gas_volume"])/(d["vial_a2_blood_volume"]*d["lambda_iso_def"])

    d["a1_dth_area_volumecorrected"] = d["a1_dth_area"] * (d["vial_a1_blood_volume"]*d["lambda_dth_def"]+d["vial_a1_gas_volume"])/(d["vial_a1_blood_volume"]*d["lambda_dth_def"])
    d["a2_dth_area_volumecorrected"] = d["a2_dth_area"] * (d["vial_a2_blood_volume"]*d["lambda_dth_def"]+d["vial_a2_gas_volume"])/(d["vial_a2_blood_volume"]*d["lambda_dth_def"])

    d["a1_acetone_area_volumecorrected"] = d["a1_acetone_area"] * (d["vial_a1_blood_volume"]*d["lambda_acetone_def"]+d["vial_a1_gas_volume"])/(d["vial_a1_blood_volume"]*d["lambda_acetone_def"])
    d["a2_acetone_area_volumecorrected"] = d["a2_acetone_area"] * (d["vial_a2_blood_volume"]*d["lambda_acetone_def"]+d["vial_a2_gas_volume"])/(d["vial_a2_blood_volume"]*d["lambda_acetone_def"])


    # Acetone correction for losses
    
    d["g1_acetone_area_corrected"] = d["a1_acetone_area"] * d["g1_dth_area"] / d["a1_dth_area"]
    d["g2_acetone_area_corrected"] = d["a2_acetone_area"] * d["g2_dth_area"] / d["a2_dth_area"]


    # Pv calculation through the Fick principle

    d["v1_sf6_area_fick"] = d["a1_sf6_area_volumecorrected"] + ((d["g1_sf6_area"] * d["ve_a1"])/(d["co_recalculated_a1"]*d["lambda_sf6_def"]))
    d["v2_sf6_area_fick"] = d["a2_sf6_area_volumecorrected"] + ((d["g2_sf6_area"] * d["ve_a2"])/(d["co_recalculated_a2"]*d["lambda_sf6_def"]))

    d["v1_ethane_area_fick"] = d["a1_ethane_area_volumecorrected"] + ((d["g1_ethane_area"] * d["ve_a1"])/(d["co_recalculated_a1"]*d["lambda_ethane_def"]))
    d["v2_ethane_area_fick"] = d["a2_ethane_area_volumecorrected"] + ((d["g2_ethane_area"] * d["ve_a2"])/(d["co_recalculated_a2"]*d["lambda_ethane_def"]))

    d["v1_cyclo_area_fick"] = d["a1_cyclo_area_volumecorrected"] + ((d["g1_cyclo_area"] * d["ve_a1"])/(d["co_recalculated_a1"]*d["lambda_cyclo_def"]))
    d["v2_cyclo_area_fick"] = d["a2_cyclo_area_volumecorrected"] + ((d["g2_cyclo_area"] * d["ve_a2"])/(d["co_recalculated_a2"]*d["lambda_cyclo_def"]))

    d["v1_iso_area_fick"] = d["a1_iso_area_volumecorrected"] + ((d["g1_iso_area"] * d["ve_a1"])/(d["co_recalculated_a1"]*d["lambda_iso_def"]))
    d["v2_iso_area_fick"] = d["a2_iso_area_volumecorrected"] + ((d["g2_iso_area"] * d["ve_a2"])/(d["co_recalculated_a2"]*d["lambda_iso_def"]))

    d["v1_dth_area_fick"] = d["a1_dth_area_volumecorrected"] + ((d["g1_dth_area"] * d["ve_a1"])/(d["co_recalculated_a1"]*d["lambda_dth_def"]))
    d["v2_dth_area_fick"] = d["a2_dth_area_volumecorrected"] + ((d["g2_dth_area"] * d["ve_a2"])/(d["co_recalculated_a2"]*d["lambda_dth_def"]))

    d["v1_acetone_area_fick"] = d["a1_acetone_area_volumecorrected"] + ((d["g1_acetone_area"] * d["ve_a1"])/(d["co_recalculated_a1"]*d["lambda_acetone_def"]))
    d["v2_acetone_area_fick"] = d["a2_acetone_area_volumecorrected"] + ((d["g2_acetone_area"] * d["ve_a2"])/(d["co_recalculated_a2"]*d["lambda_acetone_def"]))

    d["v1_acetone_area_corrected_fick"] = d["a1_acetone_area_volumecorrected"] + ((d["g1_acetone_area_corrected"] * d["ve_a1"])/(d["co_recalculated_a1"]*d["lambda_acetone_def"]))
    d["v2_acetone_area_corrected_fick"] = d["a2_acetone_area_volumecorrected"] + ((d["g2_acetone_area_corrected"] * d["ve_a2"])/(d["co_recalculated_a2"]*d["lambda_acetone_def"]))


    # Calculation of the retentions

    d["papv1_sf6"] = d["a1_sf6_area_volumecorrected"] / d["v1_sf6_area_fick"] 
    d["papv2_sf6"] = d["a2_sf6_area_volumecorrected"] / d["v2_sf6_area_fick"] 

    d["papv1_ethane"] = d["a1_ethane_area_volumecorrected"] / d["v1_ethane_area_fick"] 
    d["papv2_ethane"] = d["a2_ethane_area_volumecorrected"] / d["v2_ethane_area_fick"] 

    d["papv1_cyclo"] = d["a1_cyclo_area_volumecorrected"] / d["v1_cyclo_area_fick"] 
    d["papv2_cyclo"] = d["a2_cyclo_area_volumecorrected"] / d["v2_cyclo_area_fick"] 

    d["papv1_iso"] = d["a1_iso_area_volumecorrected"] / d["v1_iso_area_fick"] 
    d["papv2_iso"] = d["a2_iso_area_volumecorrected"] / d["v2_iso_area_fick"] 

    d["papv1_dth"] = d["a1_dth_area_volumecorrected"] / d["v1_dth_area_fick"] 
    d["papv2_dth"] = d["a2_dth_area_volumecorrected"] / d["v2_dth_area_fick"] 

    d["papv1_acetone"] = d["a1_acetone_area_volumecorrected"] / d["v1_acetone_area_fick"] 
    d["papv2_acetone"] = d["a2_acetone_area_volumecorrected"] / d["v2_acetone_area_fick"] 

    d["papv1_acetone_corrected"] = d["a1_acetone_area_volumecorrected"] / d["v1_acetone_area_corrected_fick"] 
    d["papv2_acetone_corrected"] = d["a2_acetone_area_volumecorrected"] / d["v2_acetone_area_corrected_fick"] 

    d["papv_sf6_ref"] = 0.0001639
    d["papv_ethane_ref"] = 0.034450
    d["papv_cyclo_ref"] = 0.440427
    d["papv_iso_ref"] = 0.750213
    d["papv_dth_ref"] = 0.965825
    d["papv_acetone_ref"] = 0.998811


    # Calculation of the excretions

    d["pepv1_sf6"] = d["g1_sf6_area"] / d["v1_sf6_area_fick"]
    d["pepv2_sf6"] = d["g2_sf6_area"] / d["v2_sf6_area_fick"]

    d["pepv1_ethane"] = d["g1_ethane_area"] / d["v1_ethane_area_fick"]
    d["pepv2_ethane"] = d["g2_ethane_area"] / d["v2_ethane_area_fick"]

    d["pepv1_cyclo"] = d["g1_cyclo_area"] / d["v1_cyclo_area_fick"]
    d["pepv2_cyclo"] = d["g2_cyclo_area"] / d["v2_cyclo_area_fick"]

    d["pepv1_iso"] = d["g1_iso_area"] / d["v1_iso_area_fick"]
    d["pepv2_iso"] = d["g2_iso_area"] / d["v2_iso_area_fick"]

    d["pepv1_dth"] = d["g1_dth_area"] / d["v1_dth_area_fick"]
    d["pepv2_dth"] = d["g2_dth_area"] / d["v2_dth_area_fick"]

    d["pepv1_acetone"] = d["g1_acetone_area"] / d["v1_acetone_area_fick"]
    d["pepv2_acetone"] = d["g2_acetone_area"] / d["v2_acetone_area_fick"]

    d["pepv1_acetone_corrected"] = d["g1_acetone_area_corrected"] / d["v1_acetone_area_corrected_fick"]
    d["pepv2_acetone_corrected"] = d["g2_acetone_area_corrected"] / d["v2_acetone_area_corrected_fick"]

    d["pepv_sf6_ref"] = 0.007
    d["pepv_ethane_ref"] = 0.141
    d["pepv_cyclo_ref"] = 0.4638
    d["pepv_iso_ref"] = 0.400
    d["pepv_dth_ref"] = 0.4652
    d["pepv_acetone_ref"] = 0.417

    
    # Calculations of the partition coefficients

    d["vb_net"] = (d.vb - d.c1_dry)/d.pooled_blood_density
    d["vg_net"] = d.vg - d.vb_net

    d["vbx_net"] = (d.vbx - d.syrx_dry)/d.pooled_blood_density
    d["vgx_net"] = d.vgx - d.vbx_net

    d["lambda_sf6"] = d.vg_net/d.vb_net/(d.s_sf6_area/d.sr_sf6_area - 1)
    d["lambda_ethane"] = d.vg_net/d.vb_net/(d.s_ethane_area/d.sr_ethane_area - 1)
    d["lambda_cyclo"] = d.vg_net/d.vb_net/(d.s_cyclo_area/d.sr_cyclo_area - 1)
    d["lambda_iso"] = d.vg_net/d.vb_net/(d.s_iso_area/d.sr_iso_area - 1)

    d["lambda_dth"] = d.vgx_net/d.vbx_net/(d.sr_dth_area/d.srx_dth_peak - 1)
    d["lambda_acetone"] = d.vgx_net/d.vbx_net/(d.sr_acetone_area/d.srx_acetone_peak - 1)

    return d


def graph_retentions(d, row_selected, sample, corrected = True):
    
    import pandas as pd
    import matplotlib.pyplot as plt

    # The function takes a dataset as input, a determined entry and the set 1 or 2 and plots the retention/excretion curves
    # This is useful to avoid running the more complex SHORT and VQBOHR programs.
    # The argument "corrected" performs the acetone correction to compensate for expired losses

    lambdas = d.loc[row_selected, ["lambda_sf6_def", "lambda_ethane_def", "lambda_cyclo_def", "lambda_iso_def", "lambda_dth_def", "lambda_acetone_def"]].values
    ref_ret = d.loc[row_selected, ["papv_sf6_ref", "papv_ethane_ref","papv_cyclo_ref", "papv_iso_ref", "papv_dth_ref", "papv_acetone_ref"]].values
    ref_exc = d.loc[row_selected, ["pepv_sf6_ref", "pepv_ethane_ref","pepv_cyclo_ref", "pepv_iso_ref", "pepv_dth_ref", "pepv_acetone_ref"]].values

    if sample == 1 and corrected == False:
        retentions = d.loc[row_selected, ["papv1_sf6", "papv1_ethane", "papv1_cyclo", "papv1_iso", "papv1_dth", "papv1_acetone"]].values
        excretions = d.loc[row_selected, ["pepv1_sf6", "pepv1_ethane", "pepv1_cyclo", "pepv1_iso", "pepv1_dth", "pepv1_acetone"]].values
    elif sample == 2 and corrected == False:
        retentions = d.loc[row_selected, ["papv2_sf6", "papv2_ethane", "papv2_cyclo", "papv2_iso", "papv2_dth", "papv2_acetone"]].values
        excretions = d.loc[row_selected, ["pepv2_sf6", "pepv2_ethane", "pepv2_cyclo", "pepv2_iso", "pepv2_dth", "pepv2_acetone"]].values
    elif sample == 1 and corrected == True:
        retentions = d.loc[row_selected, ["papv1_sf6", "papv1_ethane", "papv1_cyclo", "papv1_iso", "papv1_dth", "papv1_acetone_corrected"]].values
        excretions = d.loc[row_selected, ["pepv1_sf6", "pepv1_ethane", "pepv1_cyclo", "pepv1_iso", "pepv1_dth", "pepv1_acetone_corrected"]].values
    elif sample == 2 and corrected == True:
        retentions = d.loc[row_selected, ["papv2_sf6", "papv2_ethane", "papv2_cyclo", "papv2_iso", "papv2_dth", "papv2_acetone_corrected"]].values
        excretions = d.loc[row_selected, ["pepv2_sf6", "pepv2_ethane", "pepv2_cyclo", "pepv2_iso", "pepv2_dth", "pepv2_acetone_corrected"]].values

    figure, (ax1, ax2) = plt.subplots(1,2, figsize = (14,8))

    ax1.grid(alpha = 0.2)
    ax1.scatter(lambdas, retentions, s = 100)
    ax1.plot(lambdas, retentions)
    ax1.scatter(lambdas, ref_ret, s = 100)
    ax1.plot(lambdas, ref_ret, "--")
    ax1.semilogx()
    ax1.set_ylim(0,1.1)
    ax1.legend(["Patient", "Reference"], loc = "lower right", fontsize = 14)
    ax1.set_title("Retention", fontsize = 18)
    ax1.set_ylabel(r"$ \frac {P_a}{P_v}$", fontsize = 14)
    ax1.set_xlabel("Blood:gas partition coefficient", fontsize = 14)


    ax2.grid(alpha = 0.2)
    ax2.scatter(lambdas, excretions, s = 100)
    ax2.plot(lambdas, excretions)
    ax2.scatter(lambdas, ref_exc, s = 100)
    ax2.plot(lambdas, ref_exc, "--")
    ax2.semilogx()
    ax2.set_ylim(0,1.1)
    ax2.legend(["Patient", "Reference"], loc = "upper right", fontsize = 14)
    ax2.set_title("Excretion", fontsize = 18)
    ax2.set_ylabel(r"$ \frac {P_e}{P_v}$", fontsize = 14)
    ax2.set_xlabel("Blood:gas partition coefficient", fontsize = 14)


def write_raw_report(study_name, sets, pb, body_t, temp_bath, coeff_var, solubility_o2, n_gas, n_comparts, smooth, min_vq, max_vq, coeff_sf6,
coeff_ethane, coeff_cyclo, coeff_iso, coeff_dth, coeff_acetone, apeak_sf6, apeak_ethane,apeak_cyclo,apeak_iso,apeak_dth,apeak_acetone,
gpeak_sf6, gpeak_ethane, gpeak_cyclo, gpeak_iso, gpeak_dth, gpeak_acetone, ve, qt, t_ve, gas_volume_vial, blood_volume_vial, heparin_volume_vial, gas_volume_vial_mix, 
blood_volume_vial_mix, heparin_volume_vial_mix, hb, hct, vo2, vco2, tol, fio2, fico2, p50, po2, pco2, ph):

    import fortranformat as ff

    # We write line by line the parameters needed by SHORT in the precise Fortran format required

    lines = []

    # We save each single line in a Python string, we add each line to a list and we finally write line by line to a .RAW file

    l1_formatter = ff.FortranRecordWriter("(60A)")
    l1 = l1_formatter.write([study_name])

    l2_formatter = ff.FortranRecordWriter("(I4, F7.1, F6.1, F6.1, F8.2, F8.4)")
    l2 = l2_formatter.write([sets, pb, body_t, temp_bath, coeff_var, solubility_o2])

    l3_formatter = ff.FortranRecordWriter("(I4, I4, F6.1, F7.3, F8.2)")
    l3 = l3_formatter.write([n_gas, n_comparts, smooth, min_vq, max_vq])

    l4_formatter = ff.FortranRecordWriter('( 6E12.3)')
    l4 = l4_formatter.write([coeff_sf6, coeff_ethane, coeff_cyclo, coeff_iso, coeff_dth, coeff_acetone])
    l4 = " " + l4

    l5_formatter = ff.FortranRecordWriter('(6F7.1)')
    l5 = l5_formatter.write([apeak_sf6, apeak_ethane,apeak_cyclo,apeak_iso,apeak_dth,apeak_acetone])

    l6 = "    1.     1.     1.     1.     1.     1."

    l7 = l5_formatter.write([gpeak_sf6, gpeak_ethane, gpeak_cyclo, gpeak_iso, gpeak_dth, gpeak_acetone])

    l8 = l6

    l9 = "    0.0    0.0    0.0    0.0    0.0    0.0"

    l10 = l6

    l11_formatter = ff.FortranRecordWriter("(F7.2, F6.2, F7.1, F6.1, F6.1, F7.2, F7.2, F7.2, F7.2, F7.2)")
    l11 = l11_formatter.write([ve, qt, pb, body_t, t_ve, gas_volume_vial, blood_volume_vial, heparin_volume_vial, gas_volume_vial_mix, blood_volume_vial_mix, heparin_volume_vial_mix])
    l11 = l11.replace("\n", "")

    l12_formatter = ff.FortranRecordWriter("(F6.1, F6.1, F7.1, F7.1, F9.2, F7.4,F6.4, F6.1)")
    l12 = l12_formatter.write([hb, hct, vo2, vco2, tol, fio2, fico2, p50])

    l13_formatter = ff.FortranRecordWriter("(F7.1, F7.1, F6.2)")
    l13 = l13_formatter.write([po2, pco2, ph])

    lines.append(l1)
    lines.append(l2)
    lines.append(l3)
    lines.append(l4)
    lines.append(l5)
    lines.append(l6)
    lines.append(l7)
    lines.append(l8)
    lines.append(l9)
    lines.append(l10)
    lines.append(l11)
    lines.append(l12)
    lines.append(l13)

    filename = study_name + ".RAW"

    # The name of the file is the patient surname + set 1 or 2 and the .RAW extension

    raw = open(filename, "w")

    for l in lines:
        raw.write(l+"\n")

    raw.close()


def export_raw_input(dataset, record_n, default_pc = False, scaling_peak_factor = 1e-4):

    # The function takes a dataset as input and a determined entry and uses the variables stored to output a file already formatted for SHORT

    get_line = dataset.iloc[record_n]
    study_name = get_line.surname

    import pandas as pd
    import numpy as np

    # Default parameters

    sets = 1.0
    pb = 752
    coeff_var = 0.03
    temp_bath = 37.5
    solubility_o2 = 0.003
    n_gas = 6
    n_comparts = 50
    smooth = 40
    min_vq = 0.005
    max_vq = 100
    tol = 99000
    fico2 = 0
    p50 = 28.3

    body_t = get_line.temp
    t_ve = body_t

    # Choose if to use dafult or measured partition coefficients

    if default_pc == True:
        coeff_sf6 = get_line.lambda_sf6_def
        coeff_ethane = get_line.lambda_ethane_def
        coeff_cyclo = get_line.lambda_cyclo_def
        coeff_iso = get_line.lambda_iso_def
        coeff_dth = get_line.lambda_dth_def
        coeff_acetone = get_line.lambda_acetone_def
    else:
        coeff_sf6 = get_line.lambda_sf6
        coeff_ethane = get_line.lambda_ethane
        coeff_cyclo = get_line.lambda_cyclo
        coeff_iso = get_line.lambda_iso
        coeff_dth = get_line.lambda_dth
        coeff_acetone = get_line.lambda_acetone

    # The MIGET measurements are always in double, i. e., we always have two samples of arterial blood and two samples of expired gas
    # Here we first load the set 1
    # The scaling factor is to comply with the original Fortran format used in SHORT. 

    apeak_sf6 = get_line.a1_sf6_area * scaling_peak_factor
    apeak_ethane = get_line.a1_ethane_area * scaling_peak_factor
    apeak_cyclo = get_line.a1_cyclo_area * scaling_peak_factor
    apeak_iso = get_line.a1_iso_area * scaling_peak_factor
    apeak_dth = get_line.a1_dth_area * scaling_peak_factor
    apeak_acetone = get_line.a1_acetone_area * scaling_peak_factor
    
    gpeak_sf6 = get_line.g1_sf6_area * scaling_peak_factor
    gpeak_ethane = get_line.g1_ethane_area * scaling_peak_factor
    gpeak_cyclo = get_line.g1_cyclo_area * scaling_peak_factor
    gpeak_iso = get_line.g1_iso_area * scaling_peak_factor
    gpeak_dth = get_line.g1_dth_area * scaling_peak_factor
    gpeak_acetone = get_line.g1_acetone_area * scaling_peak_factor
    
    ve = get_line.ve_a1
    qt = get_line.co_recalculated_a1

    gas_volume_vial = get_line.vial_a1_gas_volume
    blood_volume_vial = get_line.vial_a1_blood_volume  
    heparin_volume_vial = 0

    gas_volume_vial_mix = 0
    blood_volume_vial_mix = 0
    heparin_volume_vial_mix = 0

    hb = get_line.art_hb_coox
    hct = get_line.art_hct
    vo2 = get_line.vo2
    vco2 = get_line.vco2
    fio2 = get_line.fio2
    po2 = get_line.art_po2
    pco2 = get_line.art_pco2
    ph = get_line.art_ph

    file_1_name = study_name + "_a1"

    # We write a .RAW file that will be fed into the SHORT Fortran Program written by P. D. Wagner

    write_raw_report(file_1_name, sets, pb, body_t, temp_bath, coeff_var, solubility_o2, n_gas, n_comparts, smooth, min_vq, max_vq, coeff_sf6,
    coeff_ethane, coeff_cyclo, coeff_iso, coeff_dth, coeff_acetone, apeak_sf6, apeak_ethane,apeak_cyclo,apeak_iso,apeak_dth,apeak_acetone,
    gpeak_sf6, gpeak_ethane, gpeak_cyclo, gpeak_iso, gpeak_dth, gpeak_acetone, ve, qt, t_ve, gas_volume_vial, blood_volume_vial, heparin_volume_vial, gas_volume_vial_mix, 
    blood_volume_vial_mix, heparin_volume_vial_mix, hb, hct, vo2, vco2, tol, fio2, fico2, p50, po2, pco2, ph)


    # We load also the set 2

    apeak_sf6 = get_line.a2_sf6_area * scaling_peak_factor
    apeak_ethane = get_line.a2_ethane_area * scaling_peak_factor
    apeak_cyclo = get_line.a2_cyclo_area * scaling_peak_factor
    apeak_iso = get_line.a2_iso_area * scaling_peak_factor
    apeak_dth = get_line.a2_dth_area * scaling_peak_factor
    apeak_acetone = get_line.a2_acetone_area * scaling_peak_factor
    
    gpeak_sf6 = get_line.g2_sf6_area * scaling_peak_factor
    gpeak_ethane = get_line.g2_ethane_area * scaling_peak_factor
    gpeak_cyclo = get_line.g2_cyclo_area * scaling_peak_factor
    gpeak_iso = get_line.g2_iso_area * scaling_peak_factor
    gpeak_dth = get_line.g2_dth_area * scaling_peak_factor
    gpeak_acetone = get_line.g2_acetone_area * scaling_peak_factor
    
    ve = get_line.ve_a2
    qt = get_line.co_recalculated_a2

    gas_volume_vial = get_line.vial_a2_gas_volume
    blood_volume_vial = get_line.vial_a2_blood_volume  
    heparin_volume_vial = 0

    gas_volume_vial_mix = 0
    blood_volume_vial_mix = 0
    heparin_volume_vial_mix = 0


    file_2_name = study_name + "_a2"

    # We write the second set in a separate .RAW file 

    write_raw_report(file_2_name, sets, pb, body_t, temp_bath, coeff_var, solubility_o2, n_gas, n_comparts, smooth, min_vq, max_vq, coeff_sf6,
    coeff_ethane, coeff_cyclo, coeff_iso, coeff_dth, coeff_acetone, apeak_sf6, apeak_ethane,apeak_cyclo,apeak_iso,apeak_dth,apeak_acetone,
    gpeak_sf6, gpeak_ethane, gpeak_cyclo, gpeak_iso, gpeak_dth, gpeak_acetone, ve, qt, t_ve, gas_volume_vial, blood_volume_vial, heparin_volume_vial, gas_volume_vial_mix, 
    blood_volume_vial_mix, heparin_volume_vial_mix, hb, hct, vo2, vco2, tol, fio2, fico2, p50, po2, pco2, ph)


