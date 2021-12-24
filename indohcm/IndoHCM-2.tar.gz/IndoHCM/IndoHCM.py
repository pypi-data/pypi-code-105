#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from scipy import optimize


# In[2]:


def Indo_HCMSDT_I(Input_file, Maximum_Cycle_Time , Analysis_Period, method, effective_g_int):
    def PCE_Table(Table):
        if Table == 'Indo_HCM':
            PCE_Table1 = pd.DataFrame([['TW' , 0.4 , 0.16], ['Auto' , 0.5 , 0.21], ['Car' , 1.0 , 0], ['LCV' , 1.1 , 0.05], ['HCV' , 1.6 , 0.16], 
                                      ['Bus' , 1.6 , 0.35], ['Bicycle' , 0.3 , 0.14], ['Cycle rickshaw' , 1.8 , 0], ['cart' , 4.0 , 0]], columns = ['Type', 'PCE' , 'SD'])
        else:
            PCE_Table1 = Table
        return (PCE_Table1)
    def Design_Volume(Hourly_vol, Peak_fifteen_min_vol, PHF):
        if PHF == None:
            Design_Volume1 = Peak_fifteen_min_vol * 4
        if PHF != None:
            Design_Volume1 = Hourly_vol / PHF
        return (Design_Volume1)
    def PCE(Vol, PCE_Table1, Type_of_veh,  Dev):
        Table = PCE_Table(PCE_Table1)
        print(Table)
        PCU = float(Table.loc[Table['Type'] == Type_of_veh]['PCE'])
        try:
            PCU_std = Dev * float(Table.loc[Table['Type'] == Type_of_veh]['SD'])
        except: 
            PCU_std = 0
            pass
        PCU = PCU + PCU_std
        Vol1 = Vol* PCU
        return(Vol1)
    def Base_Saturation_Flow(width):
        if width <=0:
            BSF =False
            print('Enter correct width')
        elif width < 7:
            BSF = 630
        elif width <= 10.5:
            BSF = 1140 - 60 * width
        else:
            BSF = 500
        return(BSF)
    def Adjustment_factor_Bus_Blockage(width, ABT , NB, dfs):
        if dfs <= 75:
            fbb = (width - 3 * (ABT * NB) / 3600) / width
        elif dfs > 75:
            fbb = 1
        return(fbb)
    def Adjustment_factor_SRTV(width, width_right, exclusive_lane, right_turn_obstruction):
        if right_turn_obstruction == 0:
            fbr = 1
        else:
            if width_right == 0:
                width_right = 2.5
            if width >= 7: 
                if exclusive_lane == 0:
                    fbr = (width - width_right)/width
                if exclusive_lane > 0:
                    fbr = 1
            if width < 7:
                fbr = 1
        return (fbr)
    def Adjustment_factor_Surge(effective_green, surge_duration, surge_ratio, anticipation, flare):
        if anticipation == 1 and flare == 0:
            fis = 1
        elif anticipation == 1 and flare == 1:
            fis = (effective_green + (surge_duration * surge_ratio )) /effective_green 
        elif anticipation == 0 and flare == 1:
            fis = 1 + ((surge_ratio)-1 ) *surge_duration / effective_green
        else:
            fis = 1
        return (fis)
    def sat_flow(width, fbb, fbr, fis):
        sat_flow = Base_Saturation_Flow(width) *width * fbb * fbr * fis
        return (sat_flow)
    def capacity_movement_group(Sat_flow , eff_green , Cy_Time):
        capacity_MG = Sat_flow *  eff_green / Cy_Time
        return (capacity_MG)
    def v_by_c(vol_MG , Sat_flow , eff_green , Cy_Time):
        v_by_c = vol_MG * Cy_Time/ (Sat_flow * eff_green) 
        return (v_by_c)
    def critical_v_by_c(n_phase, vol_MG_list , Sat_flow_list , Cy_Time, L):
        X = 0
        for i in range(n_phase):
            X = X + (vol_MG_list[i]/Sat_flow_list[i]) * (Cy_Time/ (Cy_Time - L))
        return (X)
    def Uniform_delay(C, green, X):
        d1 = 0.50 * C * (1- green/C)* (1- green/C)/(1-min(1,X) *green/C)
        return (d1)
    def incremental_delay(X, T, CSI):
        d2 = 900 * T * (X-1 + np.sqrt((X-1) * (X-1) + 4 * X / (CSI * T)))
        return (d2)

    def delay_initial_queue( X,  T, CSI, Qb , C):
        if Qb ==0:
            t = 0
        elif Qb != 0:
            t = min(T, Qb/(CSI * (1 - min(1 , X))))
        if t <= T:
            u = 0
        elif t == T:
            u = 1- C*T/(Qb * (1- min(1,X)))
        if Qb == 0:
            d3 = 0
        elif Qb!= 0:
            d3 = 1800 * Qb * (1+u) * t / (CSI * T)
        return (d3)
    def approach_delay(V, C, green, X, T, CSI, Qb):
        d1 = Uniform_delay(C, green, X)
        d2 = incremental_delay(X, T, CSI)
        d3 = delay_initial_queue( X,  T, CSI, Qb , C)
        d = V * (0.9 * d1+d2+d3)
        return (d)
    def intersection_delay(n_phase, list_of_volume , C, list_of_X, T, list_of_greens, CSI, list_of_Qb):
        intersection_delay = 0
        total_veh = 0
        for i in range(n_phase):
            intersection_delay = intersection_delay + approach_delay(list_of_volume[i], C, list_of_greens[i], list_of_X[i], T, CSI, list_of_Qb[i])
            total_veh = total_veh + list_of_volume[i]
        average_delay = intersection_delay / total_veh
        return (intersection_delay, average_delay)
    def LOS_CD(average_delay):
        if average_delay <= 20:
            LOS = 'A'
        elif average_delay <= 40:
            LOS = 'B'
        elif average_delay <= 65:
            LOS = 'C'
        elif average_delay <= 95:
            LOS = 'D'
        elif average_delay <= 130:
            LOS = 'E'
        else:
            LOS = 'F'
        return (LOS)
    def LOS_VC(X):
        if X <= 0.45:
            LOS = 'A'
        elif X <= 0.75:
            LOS = 'B'
        elif X <= 0.95:
            LOS = 'C'
        elif X <= 1.05:
            LOS = 'D'
        elif X <= 1.10:
            LOS = 'E'
        else:
            LOS = 'F'
        return (LOS)
    def cap_and_list_of_X(Input_file, Cycle_Length, list_of_volume, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        cap = 0
        list_a = []
        for i in range(number_of_phases):
            BSF = Base_Saturation_Flow(approach_widths[i])
            fbb = Adjustment_factor_Bus_Blockage(approach_widths[i], Average_Bus_Blockage_Time[i] , Number_of_buses_stopping[i], distance_of_Bus_stops_from_stopline[i])
            fbr = Adjustment_factor_SRTV(approach_widths[i], right_turning_width[i], Exclusive_right_turning_Lanes[i], right_turn_obstruction[i])
            fis = Adjustment_factor_Surge(effective_green_time[i], surge_duration[i], surge_ratio[i], 
                                         Presence_of_anticipation[i], Presence_of_flare[i])
            sf = sat_flow( approach_widths[i], fbb, fbr, fis)
            capacity = capacity_movement_group(sf , effective_green_time[i] , Cycle_Length)
            cap = cap + capacity
            vc = v_by_c(list_of_volume[i] , sf , effective_green_time[i] , Cycle_Length)
            list_a.append(vc)
        return (cap, list_a)
    def Signal_Design(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        list_of_greens = effective_green_time 
        T = Analysis_Period
        Cycle_Length = sum(effective_green_time) + sum(Yellow) + sum(All_Red_Time)
        list_of_volume = list(np.array(Peak_hour_volume) * np.array(PHF))
        CSI , list_of_X = cap_and_list_of_X(Input_file , Cycle_Length, list_of_volume, effective_green_time)
        idl, average_delay = intersection_delay(number_of_phases, list_of_volume , Cycle_Length, list_of_X, T, list_of_greens, CSI, list_of_Qb)
        los = LOS_CD(average_delay)
        return(average_delay)
    def Output_file(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        list_of_greens = effective_green_time 
        T = Analysis_Period
        Cycle_Length = sum(effective_green_time) + sum(Yellow) + sum(All_Red_Time)
        list_of_volume = list(np.array(Peak_hour_volume) * np.array(PHF))
        CSI , list_of_X = cap_and_list_of_X(Input_file , Cycle_Length, list_of_volume, effective_green_time)
        idl, average_delay = intersection_delay(number_of_phases, list_of_volume , Cycle_Length, list_of_X, T, list_of_greens, CSI, list_of_Qb)
        los = LOS_CD(average_delay)
        print('Cycle Length: ' + str(round(Cycle_Length,0)) + '  seconds')
        print('Average Control Delay Per Vehicle: ' + str(round(average_delay,2)) + '  seconds')
        print('Intersection Level of Service (based on control delay): ' + str(los) )
        print(' ')
        print(bold_print('Detailed design'))
        print('..............................................................')
        print('Approachwise Green Time: ')
        print('..............................................................')
        for i in range(0, len(effective_green_time)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(effective_green_time[i],0)) + '  seconds')
        print('..............................................................')
        print('Approachwise All Red Time: ')
        print('..............................................................')
        for i in range(0, len(All_Red_Time)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(All_Red_Time[i],0)) + '  seconds')
        print('..............................................................')
        print('Approachwise Yellow Time: ')
        print('..............................................................')
        for i in range(0, len(Yellow)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(Yellow[i],0)) + '  seconds')
        print('..............................................................')
        print('Approach wise a) Degree of Saturation; and b) LOS ')
        print('..............................................................')
        for i in range(0, len(list_of_X)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(list_of_X[i],2)) + '                        ' + str(LOS_VC(list_of_X[i])))
        print('..............................................................')
        return(Cycle_Length, effective_green_time, idl, average_delay, CSI , list_of_X)
    def Optimum(effective_g, args):
        try:
            Input_file = args[0]
            Maximum_Cycle_Time = args[1]
            Analysis_Period = args[2]
        except:
            Input_file = args[0][0]
            Maximum_Cycle_Time = args[0][1]
            Analysis_Period = args[0][1]
            pass
        return(Signal_Design(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_g))
    def bounds(Input_file, Maximum_Cycle_Time ):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        bnds = []
        for i in range(number_of_phases):
            bnds.append((Minimum_Phase_Time[i], Maximum_Cycle_Time))
        return(bnds)
    def bold_print(txt):
        bolded_string = "\033[1m" + txt + "\033[0m"
        print(bolded_string)
        return ('  ')
    number_of_phases = Input_file.shape[0]
    approach_widths = Input_file['approach_widths'].tolist()
    Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
    right_turning_width = Input_file['right_turning_width'].tolist()
    right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
    Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
    Bus_bays = Input_file['Bus_bays'].tolist()
    distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
    Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
    Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
    PHF = Input_file['PHF'].tolist()
    Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
    Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
    Presence_of_flare = Input_file['Presence_of_flare'].tolist()
    Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
    surge_duration = Input_file['surge_duration'].tolist()
    surge_ratio = Input_file['surge_ratio'].tolist()
    Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
    Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
    Yellow= Input_file['Yellow'].tolist()
    All_Red_Time = Input_file['All_Red_Time'].tolist()
    list_of_Qb = Initial_Queue_Length
    effective_g = effective_g_int
    
    def constraint_max(effective_g):
        return(Maximum_Cycle_Time -sum(effective_g) - sum(Yellow) - sum(All_Red_Time))
    
    con1 = {'type': 'ineq' , 'fun' : constraint_max}
    cons = [con1]
    cons
    bnds = bounds(Input_file, Maximum_Cycle_Time )
    history = []
    print(bold_print('Summary of optimization'))
    print(bold_print('Method   : '  + method))
    tup = Input_file, Maximum_Cycle_Time, Analysis_Period
    res = optimize.minimize(Optimum, effective_g_int, args = (tup,), method=method,
               options={'xatol': 1e-2, 'disp': True}, bounds = bnds, constraints = cons)
    print('    ')
    print(bold_print('Summary of Signal Design'))
    
    print(Output_file(Input_file, Maximum_Cycle_Time , Analysis_Period, res.x))
    
    return (res)


# In[3]:


def Indo_HCMSDT_Adv(Input_file, Predefined_cycle_time , Analysis_Period, method, effective_g_int, Maximum_Cycle_Time):
    def PCE_Table(Table):
        if Table == 'Indo_HCM':
            PCE_Table1 = pd.DataFrame([['TW' , 0.4 , 0.16], ['Auto' , 0.5 , 0.21], ['Car' , 1.0 , 0], ['LCV' , 1.1 , 0.05], ['HCV' , 1.6 , 0.16], 
                                      ['Bus' , 1.6 , 0.35], ['Bicycle' , 0.3 , 0.14], ['Cycle rickshaw' , 1.8 , 0], ['cart' , 4.0 , 0]], columns = ['Type', 'PCE' , 'SD'])
        else:
            PCE_Table1 = Table
        return (PCE_Table1)
    def Design_Volume(Hourly_vol, Peak_fifteen_min_vol, PHF):
        if PHF == None:
            Design_Volume1 = Peak_fifteen_min_vol * 4
        if PHF != None:
            Design_Volume1 = Hourly_vol / PHF
        return (Design_Volume1)
    def PCE(Vol, PCE_Table1, Type_of_veh,  Dev):
        Table = PCE_Table(PCE_Table1)
        print(Table)
        PCU = float(Table.loc[Table['Type'] == Type_of_veh]['PCE'])
        try:
            PCU_std = Dev * float(Table.loc[Table['Type'] == Type_of_veh]['SD'])
        except: 
            PCU_std = 0
            pass
        PCU = PCU + PCU_std
        Vol1 = Vol* PCU
        return(Vol1)
    def Base_Saturation_Flow(width):
        if width <=0:
            BSF =False
            print('Enter correct width')
        elif width < 7:
            BSF = 630
        elif width <= 10.5:
            BSF = 1140 - 60 * width
        else:
            BSF = 500
        return(BSF)
    def Adjustment_factor_Bus_Blockage(width, ABT , NB, dfs):
        if dfs <= 75:
            fbb = (width - 3 * (ABT * NB) / 3600) / width
        elif dfs > 75:
            fbb = 1
        return(fbb)
    def Adjustment_factor_SRTV(width, width_right, exclusive_lane, right_turn_obstruction):
        if right_turn_obstruction == 0:
            fbr = 1
        else:
            if width_right == 0:
                width_right = 2.5
            if width >= 7: 
                if exclusive_lane == 0:
                    fbr = (width - width_right)/width
                if exclusive_lane > 0:
                    fbr = 1
            if width < 7:
                fbr = 1
        return (fbr)
    def Adjustment_factor_Surge(effective_green, surge_duration, surge_ratio, anticipation, flare):
        if anticipation == 1 and flare == 0:
            fis = 1
        elif anticipation == 1 and flare == 1:
            fis = (effective_green + (surge_duration * surge_ratio )) /effective_green 
        elif anticipation == 0 and flare == 1:
            fis = 1 + ((surge_ratio)-1 ) *surge_duration / effective_green
        else:
            fis = 1
        return (fis)
    def sat_flow(width, fbb, fbr, fis):
        sat_flow = Base_Saturation_Flow(width) *width * fbb * fbr * fis
        return (sat_flow)
    def capacity_movement_group(Sat_flow , eff_green , Cy_Time):
        capacity_MG = Sat_flow *  eff_green / Cy_Time
        return (capacity_MG)
    def v_by_c(vol_MG , Sat_flow , eff_green , Cy_Time):
        v_by_c = vol_MG * Cy_Time/ (Sat_flow * eff_green) 
        return (v_by_c)
    def critical_v_by_c(n_phase, vol_MG_list , Sat_flow_list , Cy_Time, L):
        X = 0
        for i in range(n_phase):
            X = X + (vol_MG_list[i]/Sat_flow_list[i]) * (Cy_Time/ (Cy_Time - L))
        return (X)
    def Uniform_delay(C, green, X):
        d1 = 0.50 * C * (1- green/C)* (1- green/C)/(1-min(1,X) *green/C)
        return (d1)
    def incremental_delay(X, T, CSI):
        d2 = 900 * T * (X-1 + np.sqrt((X-1) * (X-1) + 4 * X / (CSI * T)))
        return (d2)

    def delay_initial_queue( X,  T, CSI, Qb , C):
        if Qb ==0:
            t = 0
        elif Qb != 0:
            t = min(T, Qb/(CSI * (1 - min(1 , X))))
        if t <= T:
            u = 0
        elif t == T:
            u = 1- C*T/(Qb * (1- min(1,X)))
        if Qb == 0:
            d3 = 0
        elif Qb!= 0:
            d3 = 1800 * Qb * (1+u) * t / (CSI * T)
        return (d3)
    def approach_delay(V, C, green, X, T, CSI, Qb):
        d1 = Uniform_delay(C, green, X)
        d2 = incremental_delay(X, T, CSI)
        d3 = delay_initial_queue( X,  T, CSI, Qb , C)
        d = V * (0.9 * d1+d2+d3)
        return (d)
    def intersection_delay(n_phase, list_of_volume , C, list_of_X, T, list_of_greens, CSI, list_of_Qb):
        intersection_delay = 0
        total_veh = 0
        for i in range(n_phase):
            intersection_delay = intersection_delay + approach_delay(list_of_volume[i], C, list_of_greens[i], list_of_X[i], T, CSI, list_of_Qb[i])
            total_veh = total_veh + list_of_volume[i]
        average_delay = intersection_delay / total_veh
        return (intersection_delay, average_delay)
    def LOS_CD(average_delay):
        if average_delay <= 20:
            LOS = 'A'
        elif average_delay <= 40:
            LOS = 'B'
        elif average_delay <= 65:
            LOS = 'C'
        elif average_delay <= 95:
            LOS = 'D'
        elif average_delay <= 130:
            LOS = 'E'
        else:
            LOS = 'F'
        return (LOS)
    def LOS_VC(X):
        if X <= 0.45:
            LOS = 'A'
        elif X <= 0.75:
            LOS = 'B'
        elif X <= 0.95:
            LOS = 'C'
        elif X <= 1.05:
            LOS = 'D'
        elif X <= 1.10:
            LOS = 'E'
        else:
            LOS = 'F'
        return (LOS)
    def cap_and_list_of_X(Input_file, Cycle_Length, list_of_volume, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        cap = 0
        list_a = []
        for i in range(number_of_phases):
            BSF = Base_Saturation_Flow(approach_widths[i])
            fbb = Adjustment_factor_Bus_Blockage(approach_widths[i], Average_Bus_Blockage_Time[i] , Number_of_buses_stopping[i], distance_of_Bus_stops_from_stopline[i])
            fbr = Adjustment_factor_SRTV(approach_widths[i], right_turning_width[i], Exclusive_right_turning_Lanes[i], right_turn_obstruction[i])
            fis = Adjustment_factor_Surge(effective_green_time[i], surge_duration[i], surge_ratio[i], 
                                         Presence_of_anticipation[i], Presence_of_flare[i])
            sf = sat_flow( approach_widths[i], fbb, fbr, fis)
            capacity = capacity_movement_group(sf , effective_green_time[i] , Cycle_Length)
            cap = cap + capacity
            vc = v_by_c(list_of_volume[i] , sf , effective_green_time[i] , Cycle_Length)
            list_a.append(vc)
        return (cap, list_a)
    def Signal_Design(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        list_of_greens = effective_green_time 
        T = Analysis_Period
        Cycle_Length = sum(effective_green_time) + sum(Yellow) + sum(All_Red_Time)
        list_of_volume = list(np.array(Peak_hour_volume) * np.array(PHF))
        CSI , list_of_X = cap_and_list_of_X(Input_file , Cycle_Length, list_of_volume, effective_green_time)
        idl, average_delay = intersection_delay(number_of_phases, list_of_volume , Cycle_Length, list_of_X, T, list_of_greens, CSI, list_of_Qb)
        los = LOS_CD(average_delay)
        return(average_delay)
    def Output_file(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        list_of_greens = effective_green_time 
        T = Analysis_Period
        Cycle_Length = sum(effective_green_time) + sum(Yellow) + sum(All_Red_Time)
        list_of_volume = list(np.array(Peak_hour_volume) * np.array(PHF))
        CSI , list_of_X = cap_and_list_of_X(Input_file , Cycle_Length, list_of_volume, effective_green_time)
        idl, average_delay = intersection_delay(number_of_phases, list_of_volume , Cycle_Length, list_of_X, T, list_of_greens, CSI, list_of_Qb)
        los = LOS_CD(average_delay)
        print('Cycle Length: ' + str(round(Cycle_Length,0)) + '  seconds')
        print('Average Control Delay Per Vehicle: ' + str(round(average_delay,2)) + '  seconds')
        print('Intersection Level of Service (based on control delay): ' + str(los) )
        print(' ')
        print(bold_print('Detailed design'))
        print('..............................................................')
        print('Approachwise Green Time: ')
        print('..............................................................')
        for i in range(0, len(effective_green_time)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(effective_green_time[i],0)) + '  seconds')
        print('..............................................................')
        print('Approachwise All Red Time: ')
        print('..............................................................')
        for i in range(0, len(All_Red_Time)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(All_Red_Time[i],0)) + '  seconds')
        print('..............................................................')
        print('Approachwise Yellow Time: ')
        print('..............................................................')
        for i in range(0, len(Yellow)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(Yellow[i],0)) + '  seconds')
        print('..............................................................')
        print('Approach wise a) Degree of Saturation; and b) LOS ')
        print('..............................................................')
        for i in range(0, len(list_of_X)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(list_of_X[i],2)) + '                        ' + str(LOS_VC(list_of_X[i])))
        print('..............................................................')
        return(Cycle_Length, effective_green_time, idl, average_delay, CSI , list_of_X)
    def Optimum(effective_g, args):
        try:
            Input_file = args[0]
            Maximum_Cycle_Time = args[1]
            Analysis_Period = args[2]
        except:
            Input_file = args[0][0]
            Maximum_Cycle_Time = args[0][1]
            Analysis_Period = args[0][2]
            pass
        return(Signal_Design(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_g))
    def Optimum1(effective_g, args):
        try:
            Input_file = args[0]
            Analysis_Period = args[1]
        except:
            Input_file = args[0][0]
            Analysis_Period = args[0][1]
            pass
        return(Signal_Design(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_g))
    def bounds(Input_file, Maximum_Cycle_Time ):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        bnds = []
        for i in range(number_of_phases):
            bnds.append((Minimum_Phase_Time[i], Maximum_Cycle_Time))
        return(bnds)
    def bold_print(txt):
        bolded_string = "\033[1m" + txt + "\033[0m"
        print(bolded_string)
        return ('  ')
    number_of_phases = Input_file.shape[0]
    approach_widths = Input_file['approach_widths'].tolist()
    Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
    right_turning_width = Input_file['right_turning_width'].tolist()
    right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
    Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
    Bus_bays = Input_file['Bus_bays'].tolist()
    distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
    Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
    Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
    PHF = Input_file['PHF'].tolist()
    Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
    Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
    Presence_of_flare = Input_file['Presence_of_flare'].tolist()
    Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
    surge_duration = Input_file['surge_duration'].tolist()
    surge_ratio = Input_file['surge_ratio'].tolist()
    Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
    Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
    Yellow= Input_file['Yellow'].tolist()
    All_Red_Time = Input_file['All_Red_Time'].tolist()
    list_of_Qb = Initial_Queue_Length
    effective_g = effective_g_int
    
    def constraint_equality(effective_g):
        predef_ct = Predefined_cycle_time
        return(predef_ct -sum(effective_g) - sum(Yellow) - sum(All_Red_Time))
    
    con1 = {'type': 'eq' , 'fun' : constraint_equality}
    cons = [con1]
    bnds = bounds(Input_file, Maximum_Cycle_Time )
    history = []
    print(bold_print('Summary of optimization'))
    print(bold_print('Method   : '  + method))
    tup = Input_file, Maximum_Cycle_Time, Analysis_Period
    res = optimize.minimize(Optimum, effective_g_int, method=method,
               options={'xatol': 1e-8, 'disp': True},  args = (tup,), bounds = bnds, constraints = cons)
    print( Predefined_cycle_time -sum(effective_g) - sum(Yellow) - sum(All_Red_Time) )
    print(bold_print('Summary of Signal Design'))
    
    print(Output_file(Input_file, Maximum_Cycle_Time , Analysis_Period, res.x))
    
    return (res)


# In[4]:


def Indo_HCMSDT_II(Input_file,  Analysis_Period, grid_step, Maximum_Cycle_Time):
    def PCE_Table(Table):
        if Table == 'Indo_HCM':
            PCE_Table1 = pd.DataFrame([['TW' , 0.4 , 0.16], ['Auto' , 0.5 , 0.21], ['Car' , 1.0 , 0], ['LCV' , 1.1 , 0.05], ['HCV' , 1.6 , 0.16], 
                                      ['Bus' , 1.6 , 0.35], ['Bicycle' , 0.3 , 0.14], ['Cycle rickshaw' , 1.8 , 0], ['cart' , 4.0 , 0]], columns = ['Type', 'PCE' , 'SD'])
        else:
            PCE_Table1 = Table
        return (PCE_Table1)
    def Design_Volume(Hourly_vol, Peak_fifteen_min_vol, PHF):
        if PHF == None:
            Design_Volume1 = Peak_fifteen_min_vol * 4
        if PHF != None:
            Design_Volume1 = Hourly_vol / PHF
        return (Design_Volume1)
    def PCE(Vol, PCE_Table1, Type_of_veh,  Dev):
        Table = PCE_Table(PCE_Table1)
        print(Table)
        PCU = float(Table.loc[Table['Type'] == Type_of_veh]['PCE'])
        try:
            PCU_std = Dev * float(Table.loc[Table['Type'] == Type_of_veh]['SD'])
        except: 
            PCU_std = 0
            pass
        PCU = PCU + PCU_std
        Vol1 = Vol* PCU
        return(Vol1)
    def Base_Saturation_Flow(width):
        if width <=0:
            BSF =False
            print('Enter correct width')
        elif width < 7:
            BSF = 630
        elif width <= 10.5:
            BSF = 1140 - 60 * width
        else:
            BSF = 500
        return(BSF)
    def Adjustment_factor_Bus_Blockage(width, ABT , NB, dfs):
        if dfs <= 75:
            fbb = (width - 3 * (ABT * NB) / 3600) / width
        elif dfs > 75:
            fbb = 1
        return(fbb)
    def Adjustment_factor_SRTV(width, width_right, exclusive_lane, right_turn_obstruction):
        if right_turn_obstruction == 0:
            fbr = 1
        else:
            if width_right == 0:
                width_right = 2.5
            if width >= 7: 
                if exclusive_lane == 0:
                    fbr = (width - width_right)/width
                if exclusive_lane > 0:
                    fbr = 1
            if width < 7:
                fbr = 1
        return (fbr)
    def Adjustment_factor_Surge(effective_green, surge_duration, surge_ratio, anticipation, flare):
        if anticipation == 1 and flare == 0:
            fis = 1
        elif anticipation == 1 and flare == 1:
            fis = (effective_green + (surge_duration * surge_ratio )) /effective_green 
        elif anticipation == 0 and flare == 1:
            fis = 1 + ((surge_ratio)-1 ) *surge_duration / effective_green
        else:
            fis = 1
        return (fis)
    def sat_flow(width, fbb, fbr, fis):
        sat_flow = Base_Saturation_Flow(width) *width * fbb * fbr * fis
        return (sat_flow)
    def capacity_movement_group(Sat_flow , eff_green , Cy_Time):
        capacity_MG = Sat_flow *  eff_green / Cy_Time
        return (capacity_MG)
    def v_by_c(vol_MG , Sat_flow , eff_green , Cy_Time):
        v_by_c = vol_MG * Cy_Time/ (Sat_flow * eff_green) 
        return (v_by_c)
    def critical_v_by_c(n_phase, vol_MG_list , Sat_flow_list , Cy_Time, L):
        X = 0
        for i in range(n_phase):
            X = X + (vol_MG_list[i]/Sat_flow_list[i]) * (Cy_Time/ (Cy_Time - L))
        return (X)
    def Uniform_delay(C, green, X):
        d1 = 0.50 * C * (1- green/C)* (1- green/C)/(1-min(1,X) *green/C)
        return (d1)
    def incremental_delay(X, T, CSI):
        d2 = 900 * T * (X-1 + np.sqrt((X-1) * (X-1) + 4 * X / (CSI * T)))
        return (d2)

    def delay_initial_queue( X,  T, CSI, Qb , C):
        if Qb ==0:
            t = 0
        elif Qb != 0:
            t = min(T, Qb/(CSI * (1 - min(1 , X))))
        if t <= T:
            u = 0
        elif t == T:
            u = 1- C*T/(Qb * (1- min(1,X)))
        if Qb == 0:
            d3 = 0
        elif Qb!= 0:
            d3 = 1800 * Qb * (1+u) * t / (CSI * T)
        return (d3)
    def approach_delay(V, C, green, X, T, CSI, Qb):
        d1 = Uniform_delay(C, green, X)
        d2 = incremental_delay(X, T, CSI)
        d3 = delay_initial_queue( X,  T, CSI, Qb , C)
        d = V * (0.9 * d1+d2+d3)
        return (d)
    def intersection_delay(n_phase, list_of_volume , C, list_of_X, T, list_of_greens, CSI, list_of_Qb):
        intersection_delay = 0
        total_veh = 0
        for i in range(n_phase):
            intersection_delay = intersection_delay + approach_delay(list_of_volume[i], C, list_of_greens[i], list_of_X[i], T, CSI, list_of_Qb[i])
            total_veh = total_veh + list_of_volume[i]
        average_delay = intersection_delay / total_veh
        return (intersection_delay, average_delay)
    def LOS_CD(average_delay):
        if average_delay <= 20:
            LOS = 'A'
        elif average_delay <= 40:
            LOS = 'B'
        elif average_delay <= 65:
            LOS = 'C'
        elif average_delay <= 95:
            LOS = 'D'
        elif average_delay <= 130:
            LOS = 'E'
        else:
            LOS = 'F'
        return (LOS)
    def LOS_VC(X):
        if X <= 0.45:
            LOS = 'A'
        elif X <= 0.75:
            LOS = 'B'
        elif X <= 0.95:
            LOS = 'C'
        elif X <= 1.05:
            LOS = 'D'
        elif X <= 1.10:
            LOS = 'E'
        else:
            LOS = 'F'
        return (LOS)
    def cap_and_list_of_X(Input_file, Cycle_Length, list_of_volume, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        cap = 0
        list_a = []
        for i in range(number_of_phases):
            BSF = Base_Saturation_Flow(approach_widths[i])
            fbb = Adjustment_factor_Bus_Blockage(approach_widths[i], Average_Bus_Blockage_Time[i] , Number_of_buses_stopping[i], distance_of_Bus_stops_from_stopline[i])
            fbr = Adjustment_factor_SRTV(approach_widths[i], right_turning_width[i], Exclusive_right_turning_Lanes[i], right_turn_obstruction[i])
            fis = Adjustment_factor_Surge(effective_green_time[i], surge_duration[i], surge_ratio[i], 
                                         Presence_of_anticipation[i], Presence_of_flare[i])
            sf = sat_flow( approach_widths[i], fbb, fbr, fis)
            capacity = capacity_movement_group(sf , effective_green_time[i] , Cycle_Length)
            cap = cap + capacity
            vc = v_by_c(list_of_volume[i] , sf , effective_green_time[i] , Cycle_Length)
            list_a.append(vc)
        return (cap, list_a)
    def Signal_Design(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        list_of_greens = effective_green_time 
        T = Analysis_Period
        Cycle_Length = sum(effective_green_time) + sum(Yellow) + sum(All_Red_Time)
        list_of_volume = list(np.array(Peak_hour_volume) * np.array(PHF))
        CSI , list_of_X = cap_and_list_of_X(Input_file , Cycle_Length, list_of_volume, effective_green_time)
        idl, average_delay = intersection_delay(number_of_phases, list_of_volume , Cycle_Length, list_of_X, T, list_of_greens, CSI, list_of_Qb)
        los = LOS_CD(average_delay)
        return(average_delay)
    def Output_file(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_green_time):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        list_of_greens = effective_green_time 
        T = Analysis_Period
        Cycle_Length = sum(effective_green_time) + sum(Yellow) + sum(All_Red_Time)
        list_of_volume = list(np.array(Peak_hour_volume) * np.array(PHF))
        CSI , list_of_X = cap_and_list_of_X(Input_file , Cycle_Length, list_of_volume, effective_green_time)
        idl, average_delay = intersection_delay(number_of_phases, list_of_volume , Cycle_Length, list_of_X, T, list_of_greens, CSI, list_of_Qb)
        los = LOS_CD(average_delay)
        print('Cycle Length: ' + str(round(Cycle_Length,0)) + '  seconds')
        print('Average Control Delay Per Vehicle: ' + str(round(average_delay,2)) + '  seconds')
        print('Intersection Level of Service (based on control delay): ' + str(los) )
        print(' ')
        print(bold_print('Detailed design'))
        print('..............................................................')
        print('Approachwise Green Time: ')
        print('..............................................................')
        for i in range(0, len(effective_green_time)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(effective_green_time[i],0)) + '  seconds')
        print('..............................................................')
        print('Approachwise All Red Time: ')
        print('..............................................................')
        for i in range(0, len(All_Red_Time)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(All_Red_Time[i],0)) + '  seconds')
        print('..............................................................')
        print('Approachwise Yellow Time: ')
        print('..............................................................')
        for i in range(0, len(Yellow)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(Yellow[i],0)) + '  seconds')
        print('..............................................................')
        print('Approach wise a) Degree of Saturation; and b) LOS ')
        print('..............................................................')
        for i in range(0, len(list_of_X)):
            print('    Approach ' + str(i+1) + '  : ' +  str(round(list_of_X[i],2)) + '                        ' + str(LOS_VC(list_of_X[i])))
        print('..............................................................')
        return(Cycle_Length, effective_green_time, idl, average_delay, CSI , list_of_X)
    def Optimum(effective_g, args):
        try:
            Input_file = args[0]
            Maximum_Cycle_Time = args[1]
            Analysis_Period = args[2]
        except:
            Input_file = args[0][0]
            Maximum_Cycle_Time = args[0][1]
            Analysis_Period = args[0][1]
            pass
        return(Signal_Design(Input_file, Maximum_Cycle_Time , Analysis_Period, effective_g))
    def bounds(Input_file, Maximum_Cycle_Time ):
        number_of_phases = Input_file.shape[0]
        approach_widths = Input_file['approach_widths'].tolist()
        Exclusive_right_turning_Lanes = Input_file['Exclusive_right_turning_Lanes'].tolist()
        right_turning_width = Input_file['right_turning_width'].tolist()
        right_turn_obstruction = Input_file['right_turn_obstruction'].tolist()
        Exclusive_right_turn_phase = Input_file['Exclusive_right_turn_phase'].tolist()
        Bus_bays = Input_file['Bus_bays'].tolist()
        distance_of_Bus_stops_from_stopline = Input_file['distance_of_Bus_stops_from_stopline'].tolist()
        Average_Bus_Blockage_Time = Input_file['Average_Bus_Blockage_Time'].tolist()
        Peak_hour_volume = Input_file['Peak_hour_volume'].tolist()
        PHF = Input_file['PHF'].tolist()
        Number_of_buses_stopping = Input_file['Number_of_buses_stopping'].tolist()
        Distance_of_bus_stops = Input_file['Distance_of_bus_stops'].tolist()
        Presence_of_flare = Input_file['Presence_of_flare'].tolist()
        Presence_of_anticipation = Input_file['Presence_of_anticipation'].tolist()
        surge_duration = Input_file['surge_duration'].tolist()
        surge_ratio = Input_file['surge_ratio'].tolist()
        Initial_Queue_Length = Input_file['Initial_Queue_Length'].tolist()
        Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
        Yellow= Input_file['Yellow'].tolist()
        All_Red_Time = Input_file['All_Red_Time'].tolist()
        list_of_Qb = Initial_Queue_Length
        bnds = []
        for i in range(number_of_phases):
            bnds.append((Minimum_Phase_Time[i], Maximum_Cycle_Time))
        return(bnds)
    def bold_print(txt):
        bolded_string = "\033[1m" + txt + "\033[0m"
        print(bolded_string)
        return ('  ')
    rranges = []
    Maximum_Green_Time = Input_file['Maximum_Green_Time'].tolist()
    Minimum_Phase_Time = Input_file['Minimum_Phase_Time'].tolist()
    for i in range(0, len(Maximum_Green_Time)):
        rranges.append(slice(Minimum_Phase_Time[i],Maximum_Green_Time[i],grid_step))
        
    #rranges = [slice(20, 100, 10), slice(20, 100, 10), slice(20, 100,10), slice(20, 100,10), slice(20, 100,10)]
    print(rranges)
    
    tup = Input_file, Maximum_Cycle_Time, Analysis_Period
    resbrute = optimize.brute(Optimum, args = (tup,),ranges= rranges, full_output=True,
                              finish=None)
    print('    ')
    print(bold_print('Summary of Signal Design'))
    
    print(Output_file(Input_file, Maximum_Cycle_Time , Analysis_Period, resbrute[0]))
    return (resbrute)


# In[ ]:




