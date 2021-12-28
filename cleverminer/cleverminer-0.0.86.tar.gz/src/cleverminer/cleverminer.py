import time #line:1
import pandas as pd #line:3
class cleverminer :#line:5
    version_string ="0.0.86"#line:7
    def __init__ (O0OOO0OO00OOOOOOO ,**OO0OOO0O000OO000O ):#line:9
        O0OOO0OO00OOOOOOO ._print_disclaimer ()#line:10
        O0OOO0OO00OOOOOOO .stats ={'total_cnt':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:18
        O0OOO0OO00OOOOOOO ._init_data ()#line:19
        O0OOO0OO00OOOOOOO ._init_task ()#line:20
        if len (OO0OOO0O000OO000O )>0 :#line:21
            O0OOO0OO00OOOOOOO .kwargs =OO0OOO0O000OO000O #line:22
            O0OOO0OO00OOOOOOO ._calc_all (**OO0OOO0O000OO000O )#line:23
    def _init_data (O000O0O00O00OO0O0 ):#line:25
        O000O0O00O00OO0O0 .data ={}#line:27
        O000O0O00O00OO0O0 .data ["varname"]=[]#line:28
        O000O0O00O00OO0O0 .data ["catnames"]=[]#line:29
        O000O0O00O00OO0O0 .data ["vtypes"]=[]#line:30
        O000O0O00O00OO0O0 .data ["dm"]=[]#line:31
        O000O0O00O00OO0O0 .data ["rows_count"]=int (0 )#line:32
        O000O0O00O00OO0O0 .data ["data_prepared"]=0 #line:33
    def _init_task (OOO0OO0000OOOOO00 ):#line:35
        OOO0OO0000OOOOO00 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'traces':[],'generated_string':'','filter_value':int (0 )}#line:44
        OOO0OO0000OOOOO00 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:48
        OOO0OO0000OOOOO00 .hypolist =[]#line:49
        OOO0OO0000OOOOO00 .stats ['total_cnt']=0 #line:51
        OOO0OO0000OOOOO00 .stats ['total_valid']=0 #line:52
        OOO0OO0000OOOOO00 .stats ['control_number']=0 #line:53
        OOO0OO0000OOOOO00 .result ={}#line:54
    def _get_ver (O0000O0OOO0O0O0O0 ):#line:56
        return O0000O0OOO0O0O0O0 .version_string #line:57
    def _print_disclaimer (OO0O00OOOO000OO0O ):#line:59
        print ("***********************************************************************************************************************************************************************")#line:60
        print ("Cleverminer version ",OO0O00OOOO000OO0O ._get_ver ())#line:61
        print ("IMPORTANT NOTE: this is preliminary development version of CleverMiner procedure. This procedure is under intensive development and early released for educational use,")#line:62
        print ("    so there is ABSOLUTELY no guarantee of results, possible gaps in functionality and no guarantee of keeping syntax and parameters as in current version.")#line:63
        print ("    (That means we need to tidy up and make proper design, input validation, documentation and instrumentation before launch)")#line:64
        print ("This version is for personal and educational use only.")#line:65
        print ("***********************************************************************************************************************************************************************")#line:66
    def _prep_data (OO0OO0OOOO0OO00OO ,O0O0000OO00OO0000 ):#line:68
        print ("Starting data preparation ...")#line:69
        OO0OO0OOOO0OO00OO ._init_data ()#line:70
        OO0OO0OOOO0OO00OO .stats ['start_prep_time']=time .time ()#line:71
        OO0OO0OOOO0OO00OO .data ["rows_count"]=O0O0000OO00OO0000 .shape [0 ]#line:72
        for OOOO0O0O000O0O000 in O0O0000OO00OO0000 .select_dtypes (exclude =['category']).columns :#line:73
            O0O0000OO00OO0000 [OOOO0O0O000O0O000 ]=O0O0000OO00OO0000 [OOOO0O0O000O0O000 ].apply (str )#line:74
        O00O000O0000O00O0 =pd .DataFrame .from_records ([(O000O00OOOOOOOOOO ,O0O0000OO00OO0000 [O000O00OOOOOOOOOO ].nunique ())for O000O00OOOOOOOOOO in O0O0000OO00OO0000 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:76
        print ("Unique value counts are:")#line:77
        print (O00O000O0000O00O0 )#line:78
        for OOOO0O0O000O0O000 in O0O0000OO00OO0000 .columns :#line:79
            if O0O0000OO00OO0000 [OOOO0O0O000O0O000 ].nunique ()<100 :#line:80
                O0O0000OO00OO0000 [OOOO0O0O000O0O000 ]=O0O0000OO00OO0000 [OOOO0O0O000O0O000 ].astype ('category')#line:81
            else :#line:82
                print (f"WARNING: attribute {OOOO0O0O000O0O000} has more than 100 values, will be ignored.")#line:83
                del O0O0000OO00OO0000 [OOOO0O0O000O0O000 ]#line:84
        print ("Encoding columns into bit-form...")#line:85
        OOOO000OOO00O00O0 =0 #line:86
        O00OOO0OO0OO000O0 =0 #line:87
        for OOO000O00OO00000O in O0O0000OO00OO0000 :#line:88
            print ('Column: '+OOO000O00OO00000O )#line:90
            OO0OO0OOOO0OO00OO .data ["varname"].append (OOO000O00OO00000O )#line:91
            O0OOOO000O00OOOO0 =pd .get_dummies (O0O0000OO00OO0000 [OOO000O00OO00000O ])#line:92
            OOOOO0OOOOO0OO000 =0 #line:93
            if (O0O0000OO00OO0000 .dtypes [OOO000O00OO00000O ].name =='category'):#line:94
                OOOOO0OOOOO0OO000 =1 #line:95
            OO0OO0OOOO0OO00OO .data ["vtypes"].append (OOOOO0OOOOO0OO000 )#line:96
            OOOOO00OO00O0O000 =0 #line:99
            OO0O000OOO00O00OO =[]#line:100
            OOOOOO0OOOOO000OO =[]#line:101
            for O0OO0OO00OO00OO0O in O0OOOO000O00OOOO0 :#line:103
                print ('....category : '+str (O0OO0OO00OO00OO0O )+" @ "+str (time .time ()))#line:105
                OO0O000OOO00O00OO .append (O0OO0OO00OO00OO0O )#line:106
                O0OO0OOOO0000OOOO =int (0 )#line:107
                O0OOO00OO0000O000 =O0OOOO000O00OOOO0 [O0OO0OO00OO00OO0O ].values #line:108
                for O0OOO0OO000O00O00 in range (OO0OO0OOOO0OO00OO .data ["rows_count"]):#line:110
                    if O0OOO00OO0000O000 [O0OOO0OO000O00O00 ]>0 :#line:111
                        O0OO0OOOO0000OOOO +=1 <<O0OOO0OO000O00O00 #line:112
                OOOOOO0OOOOO000OO .append (O0OO0OOOO0000OOOO )#line:113
                OOOOO00OO00O0O000 +=1 #line:123
                O00OOO0OO0OO000O0 +=1 #line:124
            OO0OO0OOOO0OO00OO .data ["catnames"].append (OO0O000OOO00O00OO )#line:126
            OO0OO0OOOO0OO00OO .data ["dm"].append (OOOOOO0OOOOO000OO )#line:127
        print ("Encoding columns into bit-form...done")#line:129
        print ("Encoding columns into bit-form...done")#line:130
        print (f"List of attributes for analysis is: {OO0OO0OOOO0OO00OO.data['varname']}")#line:131
        print (f"List of category names for individual attributes is : {OO0OO0OOOO0OO00OO.data['catnames']}")#line:132
        print (f"List of vtypes is (all should be 1) : {OO0OO0OOOO0OO00OO.data['vtypes']}")#line:133
        OO0OO0OOOO0OO00OO .data ["data_prepared"]=1 #line:135
        print ("Data preparation finished ...")#line:136
        print ('Number of variables : '+str (len (OO0OO0OOOO0OO00OO .data ["dm"])))#line:137
        print ('Total number of categories in all variables : '+str (O00OOO0OO0OO000O0 ))#line:138
        OO0OO0OOOO0OO00OO .stats ['end_prep_time']=time .time ()#line:139
        print ('Time needed for data preparation : ',str (OO0OO0OOOO0OO00OO .stats ['end_prep_time']-OO0OO0OOOO0OO00OO .stats ['start_prep_time']))#line:140
    def bitcount (O0OOO00O000000O00 ,OO0O0000OO0O00000 ):#line:143
        O00O0O000OO000000 =0 #line:144
        while OO0O0000OO0O00000 >0 :#line:145
            if (OO0O0000OO0O00000 &1 ==1 ):O00O0O000OO000000 +=1 #line:146
            OO0O0000OO0O00000 >>=1 #line:147
        return O00O0O000OO000000 #line:148
    def _verifyCF (OOO000OOOO0000000 ,_O000OO0O0O00O000O ):#line:151
        O0OOO00O0O0O00O00 =bin (_O000OO0O0O00O000O ).count ("1")#line:152
        OO0OOOO00O0OO0OOO =[]#line:153
        O00O000O0OO0OO0O0 =[]#line:154
        O00OO0O0O000000O0 =0 #line:155
        OO00O0O00O0OO0OO0 =0 #line:156
        O00OO00000OOO0OOO =0 #line:157
        O000OOOOOOOO0O000 =0 #line:158
        O0O0OOOO0O0O0O0O0 =0 #line:159
        OO00000OO00000O0O =0 #line:160
        O0OO00000O00OO0OO =0 #line:161
        OOO0O0OO0OOO00O0O =0 #line:162
        O00OO00OO0000O00O =0 #line:163
        O0O00O00O0000O0OO =OOO000OOOO0000000 .data ["dm"][OOO000OOOO0000000 .data ["varname"].index (OOO000OOOO0000000 .kwargs .get ('target'))]#line:164
        for O000000OO000000OO in range (len (O0O00O00O0000O0OO )):#line:165
            OO00O0O00O0OO0OO0 =O00OO0O0O000000O0 #line:166
            O00OO0O0O000000O0 =bin (_O000OO0O0O00O000O &O0O00O00O0000O0OO [O000000OO000000OO ]).count ("1")#line:167
            OO0OOOO00O0OO0OOO .append (O00OO0O0O000000O0 )#line:168
            if O000000OO000000OO >0 :#line:169
                if (O00OO0O0O000000O0 >OO00O0O00O0OO0OO0 ):#line:170
                    if (O00OO00000OOO0OOO ==1 ):#line:171
                        OOO0O0OO0OOO00O0O +=1 #line:172
                    else :#line:173
                        OOO0O0OO0OOO00O0O =1 #line:174
                    if OOO0O0OO0OOO00O0O >O000OOOOOOOO0O000 :#line:175
                        O000OOOOOOOO0O000 =OOO0O0OO0OOO00O0O #line:176
                    O00OO00000OOO0OOO =1 #line:177
                    OO00000OO00000O0O +=1 #line:178
                if (O00OO0O0O000000O0 <OO00O0O00O0OO0OO0 ):#line:179
                    if (O00OO00000OOO0OOO ==-1 ):#line:180
                        O00OO00OO0000O00O +=1 #line:181
                    else :#line:182
                        O00OO00OO0000O00O =1 #line:183
                    if O00OO00OO0000O00O >O0O0OOOO0O0O0O0O0 :#line:184
                        O0O0OOOO0O0O0O0O0 =O00OO00OO0000O00O #line:185
                    O00OO00000OOO0OOO =-1 #line:186
                    O0OO00000O00OO0OO +=1 #line:187
                if (O00OO0O0O000000O0 ==OO00O0O00O0OO0OO0 ):#line:188
                    O00OO00000OOO0OOO =0 #line:189
                    O00OO00OO0000O00O =0 #line:190
                    OOO0O0OO0OOO00O0O =0 #line:191
        O0000O0O0OO0OOO0O =True #line:194
        for OO0OO00O0O0OO00OO in OOO000OOOO0000000 .quantifiers .keys ():#line:195
            if OO0OO00O0O0OO00OO =='Base':#line:196
                O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=O0OOO00O0O0O00O00 )#line:197
            if OO0OO00O0O0OO00OO =='RelBase':#line:198
                O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=O0OOO00O0O0O00O00 *1.0 /OOO000OOOO0000000 .data ["rows_count"])#line:199
            if OO0OO00O0O0OO00OO =='S_Up':#line:200
                O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=O000OOOOOOOO0O000 )#line:201
            if OO0OO00O0O0OO00OO =='S_Down':#line:202
                O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=O0O0OOOO0O0O0O0O0 )#line:203
            if OO0OO00O0O0OO00OO =='S_Any_Up':#line:204
                O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=O000OOOOOOOO0O000 )#line:205
            if OO0OO00O0O0OO00OO =='S_Any_Down':#line:206
                O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=O0O0OOOO0O0O0O0O0 )#line:207
            if OO0OO00O0O0OO00OO =='Max':#line:208
                O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=max (OO0OOOO00O0OO0OOO ))#line:209
            if OO0OO00O0O0OO00OO =='Min':#line:210
                O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=min (OO0OOOO00O0OO0OOO ))#line:211
            if OO0OO00O0O0OO00OO =='Relmax':#line:212
                if sum (OO0OOOO00O0OO0OOO )>0 :#line:213
                    O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=max (OO0OOOO00O0OO0OOO )*1.0 /sum (OO0OOOO00O0OO0OOO ))#line:214
                else :#line:215
                    O0000O0O0OO0OOO0O =False #line:216
            if OO0OO00O0O0OO00OO =='Relmin':#line:217
                if sum (OO0OOOO00O0OO0OOO )>0 :#line:218
                    O0000O0O0OO0OOO0O =O0000O0O0OO0OOO0O and (OOO000OOOO0000000 .quantifiers .get (OO0OO00O0O0OO00OO )<=min (OO0OOOO00O0OO0OOO )*1.0 /sum (OO0OOOO00O0OO0OOO ))#line:219
                else :#line:220
                    O0000O0O0OO0OOO0O =False #line:221
        O00OOO0O0OO0OOOO0 ={}#line:222
        if O0000O0O0OO0OOO0O ==True :#line:223
            OOO000OOOO0000000 .stats ['total_valid']+=1 #line:225
            O00OOO0O0OO0OOOO0 ["base"]=O0OOO00O0O0O00O00 #line:226
            O00OOO0O0OO0OOOO0 ["rel_base"]=O0OOO00O0O0O00O00 *1.0 /OOO000OOOO0000000 .data ["rows_count"]#line:227
            O00OOO0O0OO0OOOO0 ["s_up"]=O000OOOOOOOO0O000 #line:228
            O00OOO0O0OO0OOOO0 ["s_down"]=O0O0OOOO0O0O0O0O0 #line:229
            O00OOO0O0OO0OOOO0 ["s_any_up"]=OO00000OO00000O0O #line:230
            O00OOO0O0OO0OOOO0 ["s_any_down"]=O0OO00000O00OO0OO #line:231
            O00OOO0O0OO0OOOO0 ["max"]=max (OO0OOOO00O0OO0OOO )#line:232
            O00OOO0O0OO0OOOO0 ["min"]=min (OO0OOOO00O0OO0OOO )#line:233
            O00OOO0O0OO0OOOO0 ["rel_max"]=max (OO0OOOO00O0OO0OOO )*1.0 /OOO000OOOO0000000 .data ["rows_count"]#line:234
            O00OOO0O0OO0OOOO0 ["rel_min"]=min (OO0OOOO00O0OO0OOO )*1.0 /OOO000OOOO0000000 .data ["rows_count"]#line:235
            O00OOO0O0OO0OOOO0 ["hist"]=OO0OOOO00O0OO0OOO #line:236
        return O0000O0O0OO0OOO0O ,O00OOO0O0OO0OOOO0 #line:238
    def _verify4ft (O000OOOO00O0OOO00 ,_O00OO0O00O00000O0 ):#line:240
        O0OOOO00000OO000O ={}#line:241
        O000O00O000000O0O =0 #line:242
        for O0O000O0000O0OO00 in O000OOOO00O0OOO00 .task_actinfo ['cedents']:#line:243
            O0OOOO00000OO000O [O0O000O0000O0OO00 ['cedent_type']]=O0O000O0000O0OO00 ['filter_value']#line:245
            O000O00O000000O0O =O000O00O000000O0O +1 #line:246
        OOO0O0OOO0OO0OOO0 =bin (O0OOOO00000OO000O ['ante']&O0OOOO00000OO000O ['succ']&O0OOOO00000OO000O ['cond']).count ("1")#line:248
        O0O0OO0O000OO0O0O =None #line:249
        O0O0OO0O000OO0O0O =0 #line:250
        if OOO0O0OOO0OO0OOO0 >0 :#line:259
            O0O0OO0O000OO0O0O =bin (O0OOOO00000OO000O ['ante']&O0OOOO00000OO000O ['succ']&O0OOOO00000OO000O ['cond']).count ("1")*1.0 /bin (O0OOOO00000OO000O ['ante']&O0OOOO00000OO000O ['cond']).count ("1")#line:260
        OOO0OOOOOOO000O00 =1 <<O000OOOO00O0OOO00 .data ["rows_count"]#line:262
        OO0OOOO000O00O0OO =bin (O0OOOO00000OO000O ['ante']&O0OOOO00000OO000O ['succ']&O0OOOO00000OO000O ['cond']).count ("1")#line:263
        OOOOO0OO0O00O0OOO =bin (O0OOOO00000OO000O ['ante']&~(OOO0OOOOOOO000O00 |O0OOOO00000OO000O ['succ'])&O0OOOO00000OO000O ['cond']).count ("1")#line:264
        O0O000O0000O0OO00 =bin (~(OOO0OOOOOOO000O00 |O0OOOO00000OO000O ['ante'])&O0OOOO00000OO000O ['succ']&O0OOOO00000OO000O ['cond']).count ("1")#line:265
        OOOO000000O00OO00 =bin (~(OOO0OOOOOOO000O00 |O0OOOO00000OO000O ['ante'])&~(OOO0OOOOOOO000O00 |O0OOOO00000OO000O ['succ'])&O0OOOO00000OO000O ['cond']).count ("1")#line:266
        OOOO0O00OOO0O0O0O =0 #line:267
        if (OO0OOOO000O00O0OO +OOOOO0OO0O00O0OOO )*(OO0OOOO000O00O0OO +O0O000O0000O0OO00 )>0 :#line:268
            OOOO0O00OOO0O0O0O =OO0OOOO000O00O0OO *(OO0OOOO000O00O0OO +OOOOO0OO0O00O0OOO +O0O000O0000O0OO00 +OOOO000000O00OO00 )/(OO0OOOO000O00O0OO +OOOOO0OO0O00O0OOO )/(OO0OOOO000O00O0OO +O0O000O0000O0OO00 )-1 #line:269
        else :#line:270
            OOOO0O00OOO0O0O0O =None #line:271
        OOOOO0OO0O0O0OO0O =0 #line:272
        if (OO0OOOO000O00O0OO +OOOOO0OO0O00O0OOO )*(OO0OOOO000O00O0OO +O0O000O0000O0OO00 )>0 :#line:273
            OOOOO0OO0O0O0OO0O =1 -OO0OOOO000O00O0OO *(OO0OOOO000O00O0OO +OOOOO0OO0O00O0OOO +O0O000O0000O0OO00 +OOOO000000O00OO00 )/(OO0OOOO000O00O0OO +OOOOO0OO0O00O0OOO )/(OO0OOOO000O00O0OO +O0O000O0000O0OO00 )#line:274
        else :#line:275
            OOOOO0OO0O0O0OO0O =None #line:276
        O000O00O00OOO0OO0 =True #line:277
        for OOOOO000O00OOOO00 in O000OOOO00O0OOO00 .quantifiers .keys ():#line:278
            if OOOOO000O00OOOO00 =='Base':#line:279
                O000O00O00OOO0OO0 =O000O00O00OOO0OO0 and (O000OOOO00O0OOO00 .quantifiers .get (OOOOO000O00OOOO00 )<=OOO0O0OOO0OO0OOO0 )#line:280
            if OOOOO000O00OOOO00 =='RelBase':#line:281
                O000O00O00OOO0OO0 =O000O00O00OOO0OO0 and (O000OOOO00O0OOO00 .quantifiers .get (OOOOO000O00OOOO00 )<=OOO0O0OOO0OO0OOO0 *1.0 /O000OOOO00O0OOO00 .data ["rows_count"])#line:282
            if OOOOO000O00OOOO00 =='pim':#line:283
                O000O00O00OOO0OO0 =O000O00O00OOO0OO0 and (O000OOOO00O0OOO00 .quantifiers .get (OOOOO000O00OOOO00 )<=O0O0OO0O000OO0O0O )#line:284
            if OOOOO000O00OOOO00 =='aad':#line:285
                if OOOO0O00OOO0O0O0O !=None :#line:286
                    O000O00O00OOO0OO0 =O000O00O00OOO0OO0 and (O000OOOO00O0OOO00 .quantifiers .get (OOOOO000O00OOOO00 )<=OOOO0O00OOO0O0O0O )#line:287
                else :#line:288
                    O000O00O00OOO0OO0 =False #line:289
            if OOOOO000O00OOOO00 =='bad':#line:290
                if OOOOO0OO0O0O0OO0O !=None :#line:291
                    O000O00O00OOO0OO0 =O000O00O00OOO0OO0 and (O000OOOO00O0OOO00 .quantifiers .get (OOOOO000O00OOOO00 )<=OOOOO0OO0O0O0OO0O )#line:292
                else :#line:293
                    O000O00O00OOO0OO0 =False #line:294
            O0O0O0O0000000000 ={}#line:295
        if O000O00O00OOO0OO0 ==True :#line:296
            O000OOOO00O0OOO00 .stats ['total_valid']+=1 #line:298
            O0O0O0O0000000000 ["base"]=OOO0O0OOO0OO0OOO0 #line:299
            O0O0O0O0000000000 ["rel_base"]=OOO0O0OOO0OO0OOO0 *1.0 /O000OOOO00O0OOO00 .data ["rows_count"]#line:300
            O0O0O0O0000000000 ["pim"]=O0O0OO0O000OO0O0O #line:301
            O0O0O0O0000000000 ["aad"]=OOOO0O00OOO0O0O0O #line:302
            O0O0O0O0000000000 ["bad"]=OOOOO0OO0O0O0OO0O #line:303
            O0O0O0O0000000000 ["fourfold"]=[OO0OOOO000O00O0OO ,OOOOO0OO0O00O0OOO ,O0O000O0000O0OO00 ,OOOO000000O00OO00 ]#line:304
        return O000O00O00OOO0OO0 ,O0O0O0O0000000000 #line:308
    def _verifysd4ft (O000O0O0000O0OOO0 ,_O00OO0OO0OO00O00O ):#line:310
        OO0O0OOOOOOO00O00 ={}#line:311
        OO000OOO0O000000O =0 #line:312
        for OOOOO000OOOOO000O in O000O0O0000O0OOO0 .task_actinfo ['cedents']:#line:313
            OO0O0OOOOOOO00O00 [OOOOO000OOOOO000O ['cedent_type']]=OOOOO000OOOOO000O ['filter_value']#line:315
            OO000OOO0O000000O =OO000OOO0O000000O +1 #line:316
        OOOOOO0000OOO0O00 =bin (OO0O0OOOOOOO00O00 ['ante']&OO0O0OOOOOOO00O00 ['succ']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['frst']).count ("1")#line:318
        O0O00OO000O00OOO0 =bin (OO0O0OOOOOOO00O00 ['ante']&OO0O0OOOOOOO00O00 ['succ']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['scnd']).count ("1")#line:319
        OOOOOOO0O0O0OO000 =None #line:320
        O00OOOOO0O000O0O0 =0 #line:321
        O00000000OO0O0000 =0 #line:322
        if OOOOOO0000OOO0O00 >0 :#line:331
            O00OOOOO0O000O0O0 =bin (OO0O0OOOOOOO00O00 ['ante']&OO0O0OOOOOOO00O00 ['succ']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['frst']).count ("1")*1.0 /bin (OO0O0OOOOOOO00O00 ['ante']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['frst']).count ("1")#line:332
        if O0O00OO000O00OOO0 >0 :#line:333
            O00000000OO0O0000 =bin (OO0O0OOOOOOO00O00 ['ante']&OO0O0OOOOOOO00O00 ['succ']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['scnd']).count ("1")*1.0 /bin (OO0O0OOOOOOO00O00 ['ante']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['scnd']).count ("1")#line:334
        OO0O00OOOOO000O0O =1 <<O000O0O0000O0OOO0 .data ["rows_count"]#line:336
        OOO00OO000OOOO0OO =bin (OO0O0OOOOOOO00O00 ['ante']&OO0O0OOOOOOO00O00 ['succ']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['frst']).count ("1")#line:337
        O00OO0OO0O0O00OO0 =bin (OO0O0OOOOOOO00O00 ['ante']&~(OO0O00OOOOO000O0O |OO0O0OOOOOOO00O00 ['succ'])&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['frst']).count ("1")#line:338
        O0OOO0O0OO0O00000 =bin (~(OO0O00OOOOO000O0O |OO0O0OOOOOOO00O00 ['ante'])&OO0O0OOOOOOO00O00 ['succ']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['frst']).count ("1")#line:339
        OO0OOO0O0OO00OOOO =bin (~(OO0O00OOOOO000O0O |OO0O0OOOOOOO00O00 ['ante'])&~(OO0O00OOOOO000O0O |OO0O0OOOOOOO00O00 ['succ'])&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['frst']).count ("1")#line:340
        O0OOO00OO0O000OO0 =bin (OO0O0OOOOOOO00O00 ['ante']&OO0O0OOOOOOO00O00 ['succ']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['scnd']).count ("1")#line:341
        OOO000O000OO0OO0O =bin (OO0O0OOOOOOO00O00 ['ante']&~(OO0O00OOOOO000O0O |OO0O0OOOOOOO00O00 ['succ'])&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['scnd']).count ("1")#line:342
        O00O0OO00O0OO00O0 =bin (~(OO0O00OOOOO000O0O |OO0O0OOOOOOO00O00 ['ante'])&OO0O0OOOOOOO00O00 ['succ']&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['scnd']).count ("1")#line:343
        O00O0000OOOO0O0OO =bin (~(OO0O00OOOOO000O0O |OO0O0OOOOOOO00O00 ['ante'])&~(OO0O00OOOOO000O0O |OO0O0OOOOOOO00O00 ['succ'])&OO0O0OOOOOOO00O00 ['cond']&OO0O0OOOOOOO00O00 ['scnd']).count ("1")#line:344
        OOOO0O00OOO0O0O00 =True #line:345
        for OO00O00000OOO00O0 in O000O0O0000O0OOO0 .quantifiers .keys ():#line:346
            if (OO00O00000OOO00O0 =='FrstBase')|(OO00O00000OOO00O0 =='Base1'):#line:347
                OOOO0O00OOO0O0O00 =OOOO0O00OOO0O0O00 and (O000O0O0000O0OOO0 .quantifiers .get (OO00O00000OOO00O0 )<=OOOOOO0000OOO0O00 )#line:348
            if (OO00O00000OOO00O0 =='ScndBase')|(OO00O00000OOO00O0 =='Base2'):#line:349
                OOOO0O00OOO0O0O00 =OOOO0O00OOO0O0O00 and (O000O0O0000O0OOO0 .quantifiers .get (OO00O00000OOO00O0 )<=O0O00OO000O00OOO0 )#line:350
            if (OO00O00000OOO00O0 =='FrstRelBase')|(OO00O00000OOO00O0 =='RelBase1'):#line:351
                OOOO0O00OOO0O0O00 =OOOO0O00OOO0O0O00 and (O000O0O0000O0OOO0 .quantifiers .get (OO00O00000OOO00O0 )<=OOOOOO0000OOO0O00 *1.0 /O000O0O0000O0OOO0 .data ["rows_count"])#line:352
            if (OO00O00000OOO00O0 =='ScndRelBase')|(OO00O00000OOO00O0 =='RelBase2'):#line:353
                OOOO0O00OOO0O0O00 =OOOO0O00OOO0O0O00 and (O000O0O0000O0OOO0 .quantifiers .get (OO00O00000OOO00O0 )<=O0O00OO000O00OOO0 *1.0 /O000O0O0000O0OOO0 .data ["rows_count"])#line:354
            if (OO00O00000OOO00O0 =='Frstpim')|(OO00O00000OOO00O0 =='pim1'):#line:355
                OOOO0O00OOO0O0O00 =OOOO0O00OOO0O0O00 and (O000O0O0000O0OOO0 .quantifiers .get (OO00O00000OOO00O0 )<=O00OOOOO0O000O0O0 )#line:356
            if (OO00O00000OOO00O0 =='Scndpim')|(OO00O00000OOO00O0 =='pim2'):#line:357
                OOOO0O00OOO0O0O00 =OOOO0O00OOO0O0O00 and (O000O0O0000O0OOO0 .quantifiers .get (OO00O00000OOO00O0 )<=O00000000OO0O0000 )#line:358
            if OO00O00000OOO00O0 =='Deltapim':#line:359
                OOOO0O00OOO0O0O00 =OOOO0O00OOO0O0O00 and (O000O0O0000O0OOO0 .quantifiers .get (OO00O00000OOO00O0 )<=O00OOOOO0O000O0O0 -O00000000OO0O0000 )#line:360
            if OO00O00000OOO00O0 =='Ratiopim':#line:363
                if (O00000000OO0O0000 >0 ):#line:364
                    OOOO0O00OOO0O0O00 =OOOO0O00OOO0O0O00 and (O000O0O0000O0OOO0 .quantifiers .get (OO00O00000OOO00O0 )<=O00OOOOO0O000O0O0 *1.0 /O00000000OO0O0000 )#line:365
                else :#line:366
                    OOOO0O00OOO0O0O00 =False #line:367
        O000OOOOO00OOO000 ={}#line:368
        if OOOO0O00OOO0O0O00 ==True :#line:369
            O000O0O0000O0OOO0 .stats ['total_valid']+=1 #line:371
            O000OOOOO00OOO000 ["base1"]=OOOOOO0000OOO0O00 #line:372
            O000OOOOO00OOO000 ["base2"]=O0O00OO000O00OOO0 #line:373
            O000OOOOO00OOO000 ["rel_base1"]=OOOOOO0000OOO0O00 *1.0 /O000O0O0000O0OOO0 .data ["rows_count"]#line:374
            O000OOOOO00OOO000 ["rel_base2"]=O0O00OO000O00OOO0 *1.0 /O000O0O0000O0OOO0 .data ["rows_count"]#line:375
            O000OOOOO00OOO000 ["pim1"]=O00OOOOO0O000O0O0 #line:376
            O000OOOOO00OOO000 ["pim2"]=O00000000OO0O0000 #line:377
            O000OOOOO00OOO000 ["deltapim"]=O00OOOOO0O000O0O0 -O00000000OO0O0000 #line:378
            if (O00000000OO0O0000 >0 ):#line:379
                O000OOOOO00OOO000 ["ratiopim"]=O00OOOOO0O000O0O0 *1.0 /O00000000OO0O0000 #line:380
            else :#line:381
                O000OOOOO00OOO000 ["ratiopim"]=None #line:382
            O000OOOOO00OOO000 ["fourfold1"]=[OOO00OO000OOOO0OO ,O00OO0OO0O0O00OO0 ,O0OOO0O0OO0O00000 ,OO0OOO0O0OO00OOOO ]#line:383
            O000OOOOO00OOO000 ["fourfold2"]=[O0OOO00OO0O000OO0 ,OOO000O000OO0OO0O ,O00O0OO00O0OO00O0 ,O00O0000OOOO0O0OO ]#line:384
        if OOOO0O00OOO0O0O00 :#line:386
            print (f"DEBUG : ii = {OO000OOO0O000000O}")#line:387
        return OOOO0O00OOO0O0O00 ,O000OOOOO00OOO000 #line:388
    def _verifynewact4ft (OOOO0OOOOO000OO00 ,_OOO0OOO00O0O00OO0 ):#line:390
        O00OO0O00OOO0O00O ={}#line:391
        for OO0000O0000000OO0 in OOOO0OOOOO000OO00 .task_actinfo ['cedents']:#line:392
            O00OO0O00OOO0O00O [OO0000O0000000OO0 ['cedent_type']]=OO0000O0000000OO0 ['filter_value']#line:394
        OOO0O000OO0O00O0O =bin (O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['cond']).count ("1")#line:396
        OO0O0OOO00OO00OO0 =bin (O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['cond']&O00OO0O00OOO0O00O ['antv']&O00OO0O00OOO0O00O ['sucv']).count ("1")#line:397
        OO00O0OO000000000 =None #line:398
        OO0OO0OO0O00O0O0O =0 #line:399
        O000000O0O0OOO0OO =0 #line:400
        if OOO0O000OO0O00O0O >0 :#line:409
            OO0OO0OO0O00O0O0O =bin (O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['cond']).count ("1")*1.0 /bin (O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['cond']).count ("1")#line:411
        if OO0O0OOO00OO00OO0 >0 :#line:412
            O000000O0O0OOO0OO =bin (O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['cond']&O00OO0O00OOO0O00O ['antv']&O00OO0O00OOO0O00O ['sucv']).count ("1")*1.0 /bin (O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['cond']&O00OO0O00OOO0O00O ['antv']).count ("1")#line:414
        O000OO00O0OO0OOO0 =1 <<OOOO0OOOOO000OO00 .rows_count #line:416
        O0O0OO0OO00O0000O =bin (O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['cond']).count ("1")#line:417
        O0O000O000OOO0O0O =bin (O00OO0O00OOO0O00O ['ante']&~(O000OO00O0OO0OOO0 |O00OO0O00OOO0O00O ['succ'])&O00OO0O00OOO0O00O ['cond']).count ("1")#line:418
        O0OO0O0OOOOO0O000 =bin (~(O000OO00O0OO0OOO0 |O00OO0O00OOO0O00O ['ante'])&O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['cond']).count ("1")#line:419
        O0000OO0OOO0000OO =bin (~(O000OO00O0OO0OOO0 |O00OO0O00OOO0O00O ['ante'])&~(O000OO00O0OO0OOO0 |O00OO0O00OOO0O00O ['succ'])&O00OO0O00OOO0O00O ['cond']).count ("1")#line:420
        OO0OO0O0O0O00OO00 =bin (O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['cond']&O00OO0O00OOO0O00O ['antv']&O00OO0O00OOO0O00O ['sucv']).count ("1")#line:421
        O0000000O00O00OO0 =bin (O00OO0O00OOO0O00O ['ante']&~(O000OO00O0OO0OOO0 |(O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['sucv']))&O00OO0O00OOO0O00O ['cond']).count ("1")#line:422
        OOO0O0OO0O00000OO =bin (~(O000OO00O0OO0OOO0 |(O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['antv']))&O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['cond']&O00OO0O00OOO0O00O ['sucv']).count ("1")#line:423
        O0000OOOO0OO0O0OO =bin (~(O000OO00O0OO0OOO0 |(O00OO0O00OOO0O00O ['ante']&O00OO0O00OOO0O00O ['antv']))&~(O000OO00O0OO0OOO0 |(O00OO0O00OOO0O00O ['succ']&O00OO0O00OOO0O00O ['sucv']))&O00OO0O00OOO0O00O ['cond']).count ("1")#line:424
        OO00OOO0O0O0OO000 =True #line:425
        for OOO00OOOO0OO00O00 in OOOO0OOOOO000OO00 .quantifiers .keys ():#line:426
            if (OOO00OOOO0OO00O00 =='PreBase')|(OOO00OOOO0OO00O00 =='Base1'):#line:427
                OO00OOO0O0O0OO000 =OO00OOO0O0O0OO000 and (OOOO0OOOOO000OO00 .quantifiers .get (OOO00OOOO0OO00O00 )<=OOO0O000OO0O00O0O )#line:428
            if (OOO00OOOO0OO00O00 =='PostBase')|(OOO00OOOO0OO00O00 =='Base2'):#line:429
                OO00OOO0O0O0OO000 =OO00OOO0O0O0OO000 and (OOOO0OOOOO000OO00 .quantifiers .get (OOO00OOOO0OO00O00 )<=OO0O0OOO00OO00OO0 )#line:430
            if (OOO00OOOO0OO00O00 =='PreRelBase')|(OOO00OOOO0OO00O00 =='RelBase1'):#line:431
                OO00OOO0O0O0OO000 =OO00OOO0O0O0OO000 and (OOOO0OOOOO000OO00 .quantifiers .get (OOO00OOOO0OO00O00 )<=OOO0O000OO0O00O0O *1.0 /OOOO0OOOOO000OO00 .data ["rows_count"])#line:432
            if (OOO00OOOO0OO00O00 =='PostRelBase')|(OOO00OOOO0OO00O00 =='RelBase2'):#line:433
                OO00OOO0O0O0OO000 =OO00OOO0O0O0OO000 and (OOOO0OOOOO000OO00 .quantifiers .get (OOO00OOOO0OO00O00 )<=OO0O0OOO00OO00OO0 *1.0 /OOOO0OOOOO000OO00 .data ["rows_count"])#line:434
            if (OOO00OOOO0OO00O00 =='Prepim')|(OOO00OOOO0OO00O00 =='pim1'):#line:435
                OO00OOO0O0O0OO000 =OO00OOO0O0O0OO000 and (OOOO0OOOOO000OO00 .quantifiers .get (OOO00OOOO0OO00O00 )<=OO0OO0OO0O00O0O0O )#line:436
            if (OOO00OOOO0OO00O00 =='Postpim')|(OOO00OOOO0OO00O00 =='pim2'):#line:437
                OO00OOO0O0O0OO000 =OO00OOO0O0O0OO000 and (OOOO0OOOOO000OO00 .quantifiers .get (OOO00OOOO0OO00O00 )<=O000000O0O0OOO0OO )#line:438
            if OOO00OOOO0OO00O00 =='Deltapim':#line:439
                OO00OOO0O0O0OO000 =OO00OOO0O0O0OO000 and (OOOO0OOOOO000OO00 .quantifiers .get (OOO00OOOO0OO00O00 )<=OO0OO0OO0O00O0O0O -O000000O0O0OOO0OO )#line:440
            if OOO00OOOO0OO00O00 =='Ratiopim':#line:443
                if (O000000O0O0OOO0OO >0 ):#line:444
                    OO00OOO0O0O0OO000 =OO00OOO0O0O0OO000 and (OOOO0OOOOO000OO00 .quantifiers .get (OOO00OOOO0OO00O00 )<=OO0OO0OO0O00O0O0O *1.0 /O000000O0O0OOO0OO )#line:445
                else :#line:446
                    OO00OOO0O0O0OO000 =False #line:447
        OO0O0O0O00O0000O0 ={}#line:448
        if OO00OOO0O0O0OO000 ==True :#line:449
            OOOO0OOOOO000OO00 .stats ['total_valid']+=1 #line:451
            OO0O0O0O00O0000O0 ["base1"]=OOO0O000OO0O00O0O #line:452
            OO0O0O0O00O0000O0 ["base2"]=OO0O0OOO00OO00OO0 #line:453
            OO0O0O0O00O0000O0 ["rel_base1"]=OOO0O000OO0O00O0O *1.0 /OOOO0OOOOO000OO00 .data ["rows_count"]#line:454
            OO0O0O0O00O0000O0 ["rel_base2"]=OO0O0OOO00OO00OO0 *1.0 /OOOO0OOOOO000OO00 .data ["rows_count"]#line:455
            OO0O0O0O00O0000O0 ["pim1"]=OO0OO0OO0O00O0O0O #line:456
            OO0O0O0O00O0000O0 ["pim2"]=O000000O0O0OOO0OO #line:457
            OO0O0O0O00O0000O0 ["deltapim"]=OO0OO0OO0O00O0O0O -O000000O0O0OOO0OO #line:458
            if (O000000O0O0OOO0OO >0 ):#line:459
                OO0O0O0O00O0000O0 ["ratiopim"]=OO0OO0OO0O00O0O0O *1.0 /O000000O0O0OOO0OO #line:460
            else :#line:461
                OO0O0O0O00O0000O0 ["ratiopim"]=None #line:462
            OO0O0O0O00O0000O0 ["fourfoldpre"]=[O0O0OO0OO00O0000O ,O0O000O000OOO0O0O ,O0OO0O0OOOOO0O000 ,O0000OO0OOO0000OO ]#line:463
            OO0O0O0O00O0000O0 ["fourfoldpost"]=[OO0OO0O0O0O00OO00 ,O0000000O00O00OO0 ,OOO0O0OO0O00000OO ,O0000OOOO0OO0O0OO ]#line:464
        return OO00OOO0O0O0OO000 ,OO0O0O0O00O0000O0 #line:466
    def _verifyact4ft (OOOOO0O0000OOO000 ,_OO0OO000O00OOOO0O ):#line:468
        O0OO0OOOOO00OO0OO ={}#line:469
        for OOO0O00OO000O000O in OOOOO0O0000OOO000 .task_actinfo ['cedents']:#line:470
            O0OO0OOOOO00OO0OO [OOO0O00OO000O000O ['cedent_type']]=OOO0O00OO000O000O ['filter_value']#line:472
        O000O0OO0000O0O00 =bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['antv-']&O0OO0OOOOO00OO0OO ['sucv-']).count ("1")#line:474
        OOO0OOO00O0OO0O00 =bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['antv+']&O0OO0OOOOO00OO0OO ['sucv+']).count ("1")#line:475
        OOO00O000OOO0O00O =None #line:476
        O000O0OOO00OOOOO0 =0 #line:477
        O00000O00OO00O00O =0 #line:478
        if O000O0OO0000O0O00 >0 :#line:487
            O000O0OOO00OOOOO0 =bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['antv-']&O0OO0OOOOO00OO0OO ['sucv-']).count ("1")*1.0 /bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['antv-']).count ("1")#line:489
        if OOO0OOO00O0OO0O00 >0 :#line:490
            O00000O00OO00O00O =bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['antv+']&O0OO0OOOOO00OO0OO ['sucv+']).count ("1")*1.0 /bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['antv+']).count ("1")#line:492
        O00OO000O00O0OO0O =1 <<OOOOO0O0000OOO000 .data ["rows_count"]#line:494
        OO0OOOOO0OO0OOOOO =bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['antv-']&O0OO0OOOOO00OO0OO ['sucv-']).count ("1")#line:495
        OOOOOOOOOO00O0O0O =bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['antv-']&~(O00OO000O00O0OO0O |(O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['sucv-']))&O0OO0OOOOO00OO0OO ['cond']).count ("1")#line:496
        OO00O000OOOO000OO =bin (~(O00OO000O00O0OO0O |(O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['antv-']))&O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['sucv-']).count ("1")#line:497
        O000OOO00O0000000 =bin (~(O00OO000O00O0OO0O |(O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['antv-']))&~(O00OO000O00O0OO0O |(O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['sucv-']))&O0OO0OOOOO00OO0OO ['cond']).count ("1")#line:498
        OOOOOO0O0O0O00O00 =bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['antv+']&O0OO0OOOOO00OO0OO ['sucv+']).count ("1")#line:499
        O00O000OO0O0OO00O =bin (O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['antv+']&~(O00OO000O00O0OO0O |(O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['sucv+']))&O0OO0OOOOO00OO0OO ['cond']).count ("1")#line:500
        OOOOOOO0O0O000O00 =bin (~(O00OO000O00O0OO0O |(O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['antv+']))&O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['cond']&O0OO0OOOOO00OO0OO ['sucv+']).count ("1")#line:501
        OO0O0O0OOOO0000OO =bin (~(O00OO000O00O0OO0O |(O0OO0OOOOO00OO0OO ['ante']&O0OO0OOOOO00OO0OO ['antv+']))&~(O00OO000O00O0OO0O |(O0OO0OOOOO00OO0OO ['succ']&O0OO0OOOOO00OO0OO ['sucv+']))&O0OO0OOOOO00OO0OO ['cond']).count ("1")#line:502
        O000O000OOO0O0O0O =True #line:503
        for OO0OOO0O0O000O0OO in OOOOO0O0000OOO000 .quantifiers .keys ():#line:504
            if (OO0OOO0O0O000O0OO =='PreBase')|(OO0OOO0O0O000O0OO =='Base1'):#line:505
                O000O000OOO0O0O0O =O000O000OOO0O0O0O and (OOOOO0O0000OOO000 .quantifiers .get (OO0OOO0O0O000O0OO )<=O000O0OO0000O0O00 )#line:506
            if (OO0OOO0O0O000O0OO =='PostBase')|(OO0OOO0O0O000O0OO =='Base2'):#line:507
                O000O000OOO0O0O0O =O000O000OOO0O0O0O and (OOOOO0O0000OOO000 .quantifiers .get (OO0OOO0O0O000O0OO )<=OOO0OOO00O0OO0O00 )#line:508
            if (OO0OOO0O0O000O0OO =='PreRelBase')|(OO0OOO0O0O000O0OO =='RelBase1'):#line:509
                O000O000OOO0O0O0O =O000O000OOO0O0O0O and (OOOOO0O0000OOO000 .quantifiers .get (OO0OOO0O0O000O0OO )<=O000O0OO0000O0O00 *1.0 /OOOOO0O0000OOO000 .data ["rows_count"])#line:510
            if (OO0OOO0O0O000O0OO =='PostRelBase')|(OO0OOO0O0O000O0OO =='RelBase2'):#line:511
                O000O000OOO0O0O0O =O000O000OOO0O0O0O and (OOOOO0O0000OOO000 .quantifiers .get (OO0OOO0O0O000O0OO )<=OOO0OOO00O0OO0O00 *1.0 /OOOOO0O0000OOO000 .data ["rows_count"])#line:512
            if (OO0OOO0O0O000O0OO =='Prepim')|(OO0OOO0O0O000O0OO =='pim1'):#line:513
                O000O000OOO0O0O0O =O000O000OOO0O0O0O and (OOOOO0O0000OOO000 .quantifiers .get (OO0OOO0O0O000O0OO )<=O000O0OOO00OOOOO0 )#line:514
            if (OO0OOO0O0O000O0OO =='Postpim')|(OO0OOO0O0O000O0OO =='pim2'):#line:515
                O000O000OOO0O0O0O =O000O000OOO0O0O0O and (OOOOO0O0000OOO000 .quantifiers .get (OO0OOO0O0O000O0OO )<=O00000O00OO00O00O )#line:516
            if OO0OOO0O0O000O0OO =='Deltapim':#line:517
                O000O000OOO0O0O0O =O000O000OOO0O0O0O and (OOOOO0O0000OOO000 .quantifiers .get (OO0OOO0O0O000O0OO )<=O000O0OOO00OOOOO0 -O00000O00OO00O00O )#line:518
            if OO0OOO0O0O000O0OO =='Ratiopim':#line:521
                if (O000O0OOO00OOOOO0 >0 ):#line:522
                    O000O000OOO0O0O0O =O000O000OOO0O0O0O and (OOOOO0O0000OOO000 .quantifiers .get (OO0OOO0O0O000O0OO )<=O00000O00OO00O00O *1.0 /O000O0OOO00OOOOO0 )#line:523
                else :#line:524
                    O000O000OOO0O0O0O =False #line:525
        O00000O00O000000O ={}#line:526
        if O000O000OOO0O0O0O ==True :#line:527
            OOOOO0O0000OOO000 .stats ['total_valid']+=1 #line:529
            O00000O00O000000O ["base1"]=O000O0OO0000O0O00 #line:530
            O00000O00O000000O ["base2"]=OOO0OOO00O0OO0O00 #line:531
            O00000O00O000000O ["rel_base1"]=O000O0OO0000O0O00 *1.0 /OOOOO0O0000OOO000 .data ["rows_count"]#line:532
            O00000O00O000000O ["rel_base2"]=OOO0OOO00O0OO0O00 *1.0 /OOOOO0O0000OOO000 .data ["rows_count"]#line:533
            O00000O00O000000O ["pim1"]=O000O0OOO00OOOOO0 #line:534
            O00000O00O000000O ["pim2"]=O00000O00OO00O00O #line:535
            O00000O00O000000O ["deltapim"]=O000O0OOO00OOOOO0 -O00000O00OO00O00O #line:536
            if (O000O0OOO00OOOOO0 >0 ):#line:537
                O00000O00O000000O ["ratiopim"]=O00000O00OO00O00O *1.0 /O000O0OOO00OOOOO0 #line:538
            else :#line:539
                O00000O00O000000O ["ratiopim"]=None #line:540
            O00000O00O000000O ["fourfoldpre"]=[OO0OOOOO0OO0OOOOO ,OOOOOOOOOO00O0O0O ,OO00O000OOOO000OO ,O000OOO00O0000000 ]#line:541
            O00000O00O000000O ["fourfoldpost"]=[OOOOOO0O0O0O00O00 ,O00O000OO0O0OO00O ,OOOOOOO0O0O000O00 ,OO0O0O0OOOO0000OO ]#line:542
        return O000O000OOO0O0O0O ,O00000O00O000000O #line:544
    def _verify_opt (O0O0O00O00O0000O0 ,OOO0O0OOOOOOOO0O0 ,O0O00O00OO0000OO0 ):#line:546
        O000O0O0OOOO0O0O0 =False #line:547
        if not (OOO0O0OOOOOOOO0O0 ['optim'].get ('only_con')):#line:550
            return False #line:551
        OOO00O0O00OOO00O0 ={}#line:552
        for O0O00O0O000OOO00O in O0O0O00O00O0000O0 .task_actinfo ['cedents']:#line:553
            OOO00O0O00OOO00O0 [O0O00O0O000OOO00O ['cedent_type']]=O0O00O0O000OOO00O ['filter_value']#line:555
        OOOO0000O0O0O0OOO =1 <<O0O0O00O00O0000O0 .data ["rows_count"]#line:557
        O0OO0000O0O00OO0O =OOOO0000O0O0O0OOO -1 #line:558
        O00O0000OO00OO000 =""#line:559
        O00OO0O00000OO0OO =0 #line:560
        if (OOO00O0O00OOO00O0 .get ('ante')!=None ):#line:561
            O0OO0000O0O00OO0O =O0OO0000O0O00OO0O &OOO00O0O00OOO00O0 ['ante']#line:562
        if (OOO00O0O00OOO00O0 .get ('succ')!=None ):#line:563
            O0OO0000O0O00OO0O =O0OO0000O0O00OO0O &OOO00O0O00OOO00O0 ['succ']#line:564
        if (OOO00O0O00OOO00O0 .get ('cond')!=None ):#line:565
            O0OO0000O0O00OO0O =O0OO0000O0O00OO0O &OOO00O0O00OOO00O0 ['cond']#line:566
        O00O00OOOOO00O000 =None #line:569
        if (O0O0O00O00O0000O0 .proc =='CFMiner')|(O0O0O00O00O0000O0 .proc =='4ftMiner'):#line:594
            OOOOOO00OOO0O00OO =bin (O0OO0000O0O00OO0O ).count ("1")#line:595
            for O00OOO0OO0OOOO0O0 in O0O0O00O00O0000O0 .quantifiers .keys ():#line:596
                if O00OOO0OO0OOOO0O0 =='Base':#line:597
                    if not (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OOOOOO00OOO0O00OO ):#line:598
                        O000O0O0OOOO0O0O0 =True #line:599
                if O00OOO0OO0OOOO0O0 =='RelBase':#line:601
                    if not (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OOOOOO00OOO0O00OO *1.0 /O0O0O00O00O0000O0 .data ["rows_count"]):#line:602
                        O000O0O0OOOO0O0O0 =True #line:603
        return O000O0O0OOOO0O0O0 #line:606
        if O0O0O00O00O0000O0 .proc =='CFMiner':#line:609
            if (O0O00O00OO0000OO0 ['cedent_type']=='cond')&(O0O00O00OO0000OO0 ['defi'].get ('type')=='con'):#line:610
                OOOOOO00OOO0O00OO =bin (OOO00O0O00OOO00O0 ['cond']).count ("1")#line:611
                O000OO0000OOO0OO0 =True #line:612
                for O00OOO0OO0OOOO0O0 in O0O0O00O00O0000O0 .quantifiers .keys ():#line:613
                    if O00OOO0OO0OOOO0O0 =='Base':#line:614
                        O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OOOOOO00OOO0O00OO )#line:615
                        if not (O000OO0000OOO0OO0 ):#line:616
                            print (f"...optimization : base is {OOOOOO00OOO0O00OO} for {O0O00O00OO0000OO0['generated_string']}")#line:617
                    if O00OOO0OO0OOOO0O0 =='RelBase':#line:618
                        O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OOOOOO00OOO0O00OO *1.0 /O0O0O00O00O0000O0 .data ["rows_count"])#line:619
                        if not (O000OO0000OOO0OO0 ):#line:620
                            print (f"...optimization : base is {OOOOOO00OOO0O00OO} for {O0O00O00OO0000OO0['generated_string']}")#line:621
                O000O0O0OOOO0O0O0 =not (O000OO0000OOO0OO0 )#line:622
        elif O0O0O00O00O0000O0 .proc =='4ftMiner':#line:623
            if (O0O00O00OO0000OO0 ['cedent_type']=='cond')&(O0O00O00OO0000OO0 ['defi'].get ('type')=='con'):#line:624
                OOOOOO00OOO0O00OO =bin (OOO00O0O00OOO00O0 ['cond']).count ("1")#line:625
                O000OO0000OOO0OO0 =True #line:626
                for O00OOO0OO0OOOO0O0 in O0O0O00O00O0000O0 .quantifiers .keys ():#line:627
                    if O00OOO0OO0OOOO0O0 =='Base':#line:628
                        O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OOOOOO00OOO0O00OO )#line:629
                        if not (O000OO0000OOO0OO0 ):#line:630
                            print (f"...optimization : base is {OOOOOO00OOO0O00OO} for {O0O00O00OO0000OO0['generated_string']}")#line:631
                    if O00OOO0OO0OOOO0O0 =='RelBase':#line:632
                        O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OOOOOO00OOO0O00OO *1.0 /O0O0O00O00O0000O0 .data ["rows_count"])#line:633
                        if not (O000OO0000OOO0OO0 ):#line:634
                            print (f"...optimization : base is {OOOOOO00OOO0O00OO} for {O0O00O00OO0000OO0['generated_string']}")#line:635
                O000O0O0OOOO0O0O0 =not (O000OO0000OOO0OO0 )#line:636
            if (O0O00O00OO0000OO0 ['cedent_type']=='ante')&(O0O00O00OO0000OO0 ['defi'].get ('type')=='con'):#line:637
                OOOOOO00OOO0O00OO =bin (OOO00O0O00OOO00O0 ['ante']&OOO00O0O00OOO00O0 ['cond']).count ("1")#line:638
                O000OO0000OOO0OO0 =True #line:639
                for O00OOO0OO0OOOO0O0 in O0O0O00O00O0000O0 .quantifiers .keys ():#line:640
                    if O00OOO0OO0OOOO0O0 =='Base':#line:641
                        O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OOOOOO00OOO0O00OO )#line:642
                        if not (O000OO0000OOO0OO0 ):#line:643
                            print (f"...optimization : ANTE: base is {OOOOOO00OOO0O00OO} for {O0O00O00OO0000OO0['generated_string']}")#line:644
                    if O00OOO0OO0OOOO0O0 =='RelBase':#line:645
                        O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OOOOOO00OOO0O00OO *1.0 /O0O0O00O00O0000O0 .data ["rows_count"])#line:646
                        if not (O000OO0000OOO0OO0 ):#line:647
                            print (f"...optimization : ANTE:  base is {OOOOOO00OOO0O00OO} for {O0O00O00OO0000OO0['generated_string']}")#line:648
                O000O0O0OOOO0O0O0 =not (O000OO0000OOO0OO0 )#line:649
            if (O0O00O00OO0000OO0 ['cedent_type']=='succ')&(O0O00O00OO0000OO0 ['defi'].get ('type')=='con'):#line:650
                OOOOOO00OOO0O00OO =bin (OOO00O0O00OOO00O0 ['ante']&OOO00O0O00OOO00O0 ['cond']&OOO00O0O00OOO00O0 ['succ']).count ("1")#line:651
                O00O00OOOOO00O000 =0 #line:652
                if OOOOOO00OOO0O00OO >0 :#line:653
                    O00O00OOOOO00O000 =bin (OOO00O0O00OOO00O0 ['ante']&OOO00O0O00OOO00O0 ['succ']&OOO00O0O00OOO00O0 ['cond']).count ("1")*1.0 /bin (OOO00O0O00OOO00O0 ['ante']&OOO00O0O00OOO00O0 ['cond']).count ("1")#line:654
                OOOO0000O0O0O0OOO =1 <<O0O0O00O00O0000O0 .data ["rows_count"]#line:655
                OO0O0000OOOOOOO0O =bin (OOO00O0O00OOO00O0 ['ante']&OOO00O0O00OOO00O0 ['succ']&OOO00O0O00OOO00O0 ['cond']).count ("1")#line:656
                O00O0000OO0000000 =bin (OOO00O0O00OOO00O0 ['ante']&~(OOOO0000O0O0O0OOO |OOO00O0O00OOO00O0 ['succ'])&OOO00O0O00OOO00O0 ['cond']).count ("1")#line:657
                O0O00O0O000OOO00O =bin (~(OOOO0000O0O0O0OOO |OOO00O0O00OOO00O0 ['ante'])&OOO00O0O00OOO00O0 ['succ']&OOO00O0O00OOO00O0 ['cond']).count ("1")#line:658
                O0O00O0000OO00OO0 =bin (~(OOOO0000O0O0O0OOO |OOO00O0O00OOO00O0 ['ante'])&~(OOOO0000O0O0O0OOO |OOO00O0O00OOO00O0 ['succ'])&OOO00O0O00OOO00O0 ['cond']).count ("1")#line:659
                O000OO0000OOO0OO0 =True #line:660
                for O00OOO0OO0OOOO0O0 in O0O0O00O00O0000O0 .quantifiers .keys ():#line:661
                    if O00OOO0OO0OOOO0O0 =='pim':#line:662
                        O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=O00O00OOOOO00O000 )#line:663
                    if not (O000OO0000OOO0OO0 ):#line:664
                        print (f"...optimization : SUCC:  pim is {O00O00OOOOO00O000} for {O0O00O00OO0000OO0['generated_string']}")#line:665
                    if O00OOO0OO0OOOO0O0 =='aad':#line:667
                        if (OO0O0000OOOOOOO0O +O00O0000OO0000000 )*(OO0O0000OOOOOOO0O +O0O00O0O000OOO00O )>0 :#line:668
                            O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=OO0O0000OOOOOOO0O *(OO0O0000OOOOOOO0O +O00O0000OO0000000 +O0O00O0O000OOO00O +O0O00O0000OO00OO0 )/(OO0O0000OOOOOOO0O +O00O0000OO0000000 )/(OO0O0000OOOOOOO0O +O0O00O0O000OOO00O )-1 )#line:669
                        else :#line:670
                            O000OO0000OOO0OO0 =False #line:671
                        if not (O000OO0000OOO0OO0 ):#line:672
                            OOO0O000OO00OO0OO =OO0O0000OOOOOOO0O *(OO0O0000OOOOOOO0O +O00O0000OO0000000 +O0O00O0O000OOO00O +O0O00O0000OO00OO0 )/(OO0O0000OOOOOOO0O +O00O0000OO0000000 )/(OO0O0000OOOOOOO0O +O0O00O0O000OOO00O )-1 #line:673
                            print (f"...optimization : SUCC:  aad is {OOO0O000OO00OO0OO} for {O0O00O00OO0000OO0['generated_string']}")#line:674
                    if O00OOO0OO0OOOO0O0 =='bad':#line:675
                        if (OO0O0000OOOOOOO0O +O00O0000OO0000000 )*(OO0O0000OOOOOOO0O +O0O00O0O000OOO00O )>0 :#line:676
                            O000OO0000OOO0OO0 =O000OO0000OOO0OO0 and (O0O0O00O00O0000O0 .quantifiers .get (O00OOO0OO0OOOO0O0 )<=1 -OO0O0000OOOOOOO0O *(OO0O0000OOOOOOO0O +O00O0000OO0000000 +O0O00O0O000OOO00O +O0O00O0000OO00OO0 )/(OO0O0000OOOOOOO0O +O00O0000OO0000000 )/(OO0O0000OOOOOOO0O +O0O00O0O000OOO00O ))#line:677
                        else :#line:678
                            O000OO0000OOO0OO0 =False #line:679
                        if not (O000OO0000OOO0OO0 ):#line:680
                            O000O0OOOOOOO0O0O =1 -OO0O0000OOOOOOO0O *(OO0O0000OOOOOOO0O +O00O0000OO0000000 +O0O00O0O000OOO00O +O0O00O0000OO00OO0 )/(OO0O0000OOOOOOO0O +O00O0000OO0000000 )/(OO0O0000OOOOOOO0O +O0O00O0O000OOO00O )#line:681
                            print (f"...optimization : SUCC:  bad is {O000O0OOOOOOO0O0O} for {O0O00O00OO0000OO0['generated_string']}")#line:682
                O000O0O0OOOO0O0O0 =not (O000OO0000OOO0OO0 )#line:683
        if (O000O0O0OOOO0O0O0 ):#line:684
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {O0O00O00OO0000OO0['cedent_type']}")#line:685
        return O000O0O0OOOO0O0O0 #line:686
    def _print (O0OO0O0O00OOO00O0 ,OO00O00000O000OOO ,_O00O0OOO0OOOOO00O ,_O00OOOOO0O0OOOO00 ):#line:689
        if (len (_O00O0OOO0OOOOO00O ))!=len (_O00OOOOO0O0OOOO00 ):#line:690
            print ("DIFF IN LEN for following cedent : "+str (len (_O00O0OOO0OOOOO00O ))+" vs "+str (len (_O00OOOOO0O0OOOO00 )))#line:691
            print ("trace cedent : "+str (_O00O0OOO0OOOOO00O )+", traces "+str (_O00OOOOO0O0OOOO00 ))#line:692
        O0O0O00OOOO0OOO00 =''#line:693
        for O00O0O0OOO0O0OOO0 in range (len (_O00O0OOO0OOOOO00O )):#line:694
            O000O0OO0O00O0O0O =O0OO0O0O00OOO00O0 .data ["varname"].index (OO00O00000O000OOO ['defi'].get ('attributes')[_O00O0OOO0OOOOO00O [O00O0O0OOO0O0OOO0 ]].get ('name'))#line:695
            O0O0O00OOOO0OOO00 =O0O0O00OOOO0OOO00 +O0OO0O0O00OOO00O0 .data ["varname"][O000O0OO0O00O0O0O ]+'('#line:697
            for O0000OO0000OO0OOO in _O00OOOOO0O0OOOO00 [O00O0O0OOO0O0OOO0 ]:#line:698
                O0O0O00OOOO0OOO00 =O0O0O00OOOO0OOO00 +O0OO0O0O00OOO00O0 .data ["catnames"][O000O0OO0O00O0O0O ][O0000OO0000OO0OOO ]+" "#line:699
            O0O0O00OOOO0OOO00 =O0O0O00OOOO0OOO00 +')'#line:700
            if O00O0O0OOO0O0OOO0 +1 <len (_O00O0OOO0OOOOO00O ):#line:701
                O0O0O00OOOO0OOO00 =O0O0O00OOOO0OOO00 +' & '#line:702
        return O0O0O00OOOO0OOO00 #line:706
    def _print_hypo (O0O0O00O0OO0O0O0O ,OO0000O0OO0O0000O ):#line:708
        print ('Hypothesis info : '+str (OO0000O0OO0O0000O ['params']))#line:709
        for O0OO0000000O000O0 in O0O0O00O0OO0O0O0O .task_actinfo ['cedents']:#line:710
            print (O0OO0000000O000O0 ['cedent_type']+' = '+O0OO0000000O000O0 ['generated_string'])#line:711
    def _genvar (OO00OO0O000O0OOOO ,O000000O0OOO0O000 ,O0O0000OOO0000O0O ,_O00OO000O00OO0O00 ,_OO0O0OOOOOO00OOOO ,_OO0OO00000000O000 ,_OOO0O0O0OOOO0O00O ,_OO000O00OOO0O0OO0 ):#line:713
        for OO00OOOOOO00000OO in range (O0O0000OOO0000O0O ['num_cedent']):#line:714
            if len (_O00OO000O00OO0O00 )==0 or OO00OOOOOO00000OO >_O00OO000O00OO0O00 [-1 ]:#line:715
                _O00OO000O00OO0O00 .append (OO00OOOOOO00000OO )#line:716
                O00O0O00OOO00O0O0 =OO00OO0O000O0OOOO .data ["varname"].index (O0O0000OOO0000O0O ['defi'].get ('attributes')[OO00OOOOOO00000OO ].get ('name'))#line:717
                _O0O00O0OOO0O0O00O =O0O0000OOO0000O0O ['defi'].get ('attributes')[OO00OOOOOO00000OO ].get ('minlen')#line:718
                _OO0OOOOO0O0O00O0O =O0O0000OOO0000O0O ['defi'].get ('attributes')[OO00OOOOOO00000OO ].get ('maxlen')#line:719
                _O0O00O0O00000O00O =O0O0000OOO0000O0O ['defi'].get ('attributes')[OO00OOOOOO00000OO ].get ('type')#line:720
                OOO00OOOO0OOO0OO0 =len (OO00OO0O000O0OOOO .data ["dm"][O00O0O00OOO00O0O0 ])#line:721
                _OOOOOOO00OO0OOOO0 =[]#line:722
                _OO0O0OOOOOO00OOOO .append (_OOOOOOO00OO0OOOO0 )#line:723
                _OO00000O00000O000 =int (0 )#line:724
                OO00OO0O000O0OOOO ._gencomb (O000000O0OOO0O000 ,O0O0000OOO0000O0O ,_O00OO000O00OO0O00 ,_OO0O0OOOOOO00OOOO ,_OOOOOOO00OO0OOOO0 ,_OO0OO00000000O000 ,_OO00000O00000O000 ,OOO00OOOO0OOO0OO0 ,_O0O00O0O00000O00O ,_OOO0O0O0OOOO0O00O ,_OO000O00OOO0O0OO0 ,_O0O00O0OOO0O0O00O ,_OO0OOOOO0O0O00O0O )#line:725
                _OO0O0OOOOOO00OOOO .pop ()#line:726
                _O00OO000O00OO0O00 .pop ()#line:727
    def _gencomb (OO0OOOOO0000OO000 ,OOOOO00000O0OO000 ,O00O00OO0O0O0O00O ,_O00O00O000OO00O00 ,_O0O00000OOOO00O00 ,_O0O0OO0O00OOO0O00 ,_O0OO00O000O0000OO ,_OOO0OO0000O000O0O ,O0O0000000O00O000 ,_O000O0OOOOOOO00O0 ,_OOO0OOO00O0O0OO0O ,_O0OOO0OO00O0O0OOO ,_O000000O0OOO0O0O0 ,_O0OOOOOO0O000000O ):#line:729
        _O000O0OOOOOO0OOOO =[]#line:730
        if _O000O0OOOOOOO00O0 =="subset":#line:731
            if len (_O0O0OO0O00OOO0O00 )==0 :#line:732
                _O000O0OOOOOO0OOOO =range (O0O0000000O00O000 )#line:733
            else :#line:734
                _O000O0OOOOOO0OOOO =range (_O0O0OO0O00OOO0O00 [-1 ]+1 ,O0O0000000O00O000 )#line:735
        elif _O000O0OOOOOOO00O0 =="seq":#line:736
            if len (_O0O0OO0O00OOO0O00 )==0 :#line:737
                _O000O0OOOOOO0OOOO =range (O0O0000000O00O000 -_O000000O0OOO0O0O0 +1 )#line:738
            else :#line:739
                if _O0O0OO0O00OOO0O00 [-1 ]+1 ==O0O0000000O00O000 :#line:740
                    return #line:741
                OOOOOO0OO00O0O0OO =_O0O0OO0O00OOO0O00 [-1 ]+1 #line:742
                _O000O0OOOOOO0OOOO .append (OOOOOO0OO00O0O0OO )#line:743
        elif _O000O0OOOOOOO00O0 =="lcut":#line:744
            if len (_O0O0OO0O00OOO0O00 )==0 :#line:745
                OOOOOO0OO00O0O0OO =0 ;#line:746
            else :#line:747
                if _O0O0OO0O00OOO0O00 [-1 ]+1 ==O0O0000000O00O000 :#line:748
                    return #line:749
                OOOOOO0OO00O0O0OO =_O0O0OO0O00OOO0O00 [-1 ]+1 #line:750
            _O000O0OOOOOO0OOOO .append (OOOOOO0OO00O0O0OO )#line:751
        elif _O000O0OOOOOOO00O0 =="rcut":#line:752
            if len (_O0O0OO0O00OOO0O00 )==0 :#line:753
                OOOOOO0OO00O0O0OO =O0O0000000O00O000 -1 ;#line:754
            else :#line:755
                if _O0O0OO0O00OOO0O00 [-1 ]==0 :#line:756
                    return #line:757
                OOOOOO0OO00O0O0OO =_O0O0OO0O00OOO0O00 [-1 ]-1 #line:758
            _O000O0OOOOOO0OOOO .append (OOOOOO0OO00O0O0OO )#line:760
        else :#line:761
            print ("Attribute type "+_O000O0OOOOOOO00O0 +" not supported.")#line:762
            return #line:763
        for O0OO0OOOO00O0000O in _O000O0OOOOOO0OOOO :#line:766
                _O0O0OO0O00OOO0O00 .append (O0OO0OOOO00O0000O )#line:768
                _O0O00000OOOO00O00 .pop ()#line:769
                _O0O00000OOOO00O00 .append (_O0O0OO0O00OOO0O00 )#line:770
                _O0000OO000O0OO000 =_OOO0OO0000O000O0O |OO0OOOOO0000OO000 .data ["dm"][OO0OOOOO0000OO000 .data ["varname"].index (O00O00OO0O0O0O00O ['defi'].get ('attributes')[_O00O00O000OO00O00 [-1 ]].get ('name'))][O0OO0OOOO00O0000O ]#line:774
                _OOO0OO0OO00O0O0OO =1 #line:776
                if (len (_O00O00O000OO00O00 )<_OOO0OOO00O0O0OO0O ):#line:777
                    _OOO0OO0OO00O0O0OO =-1 #line:778
                if (len (_O0O00000OOOO00O00 [-1 ])<_O000000O0OOO0O0O0 ):#line:780
                    _OOO0OO0OO00O0O0OO =0 #line:781
                _O00O0OO00OO00OO0O =0 #line:783
                if O00O00OO0O0O0O00O ['defi'].get ('type')=='con':#line:784
                    _O00O0OO00OO00OO0O =_O0OO00O000O0000OO &_O0000OO000O0OO000 #line:785
                else :#line:786
                    _O00O0OO00OO00OO0O =_O0OO00O000O0000OO |_O0000OO000O0OO000 #line:787
                O00O00OO0O0O0O00O ['trace_cedent']=_O00O00O000OO00O00 #line:788
                O00O00OO0O0O0O00O ['traces']=_O0O00000OOOO00O00 #line:789
                O00O00OO0O0O0O00O ['generated_string']=OO0OOOOO0000OO000 ._print (O00O00OO0O0O0O00O ,_O00O00O000OO00O00 ,_O0O00000OOOO00O00 )#line:790
                O00O00OO0O0O0O00O ['filter_value']=_O00O0OO00OO00OO0O #line:791
                OOOOO00000O0OO000 ['cedents'].append (O00O00OO0O0O0O00O )#line:792
                OO0OO00O00O00O000 =OO0OOOOO0000OO000 ._verify_opt (OOOOO00000O0OO000 ,O00O00OO0O0O0O00O )#line:793
                if not (OO0OO00O00O00O000 ):#line:799
                    if _OOO0OO0OO00O0O0OO ==1 :#line:800
                        if len (OOOOO00000O0OO000 ['cedents_to_do'])==len (OOOOO00000O0OO000 ['cedents']):#line:802
                            if OO0OOOOO0000OO000 .proc =='CFMiner':#line:803
                                O0O000O0O00OOO00O ,OO0000OOO0OO000O0 =OO0OOOOO0000OO000 ._verifyCF (_O00O0OO00OO00OO0O )#line:804
                            elif OO0OOOOO0000OO000 .proc =='4ftMiner':#line:805
                                O0O000O0O00OOO00O ,OO0000OOO0OO000O0 =OO0OOOOO0000OO000 ._verify4ft (_O0000OO000O0OO000 )#line:806
                            elif OO0OOOOO0000OO000 .proc =='SD4ftMiner':#line:807
                                O0O000O0O00OOO00O ,OO0000OOO0OO000O0 =OO0OOOOO0000OO000 ._verifysd4ft (_O0000OO000O0OO000 )#line:808
                            elif OO0OOOOO0000OO000 .proc =='NewAct4ftMiner':#line:809
                                O0O000O0O00OOO00O ,OO0000OOO0OO000O0 =OO0OOOOO0000OO000 ._verifynewact4ft (_O0000OO000O0OO000 )#line:810
                            elif OO0OOOOO0000OO000 .proc =='Act4ftMiner':#line:811
                                O0O000O0O00OOO00O ,OO0000OOO0OO000O0 =OO0OOOOO0000OO000 ._verifyact4ft (_O0000OO000O0OO000 )#line:812
                            else :#line:813
                                print ("Unsupported procedure : "+OO0OOOOO0000OO000 .proc )#line:814
                                exit (0 )#line:815
                            if O0O000O0O00OOO00O ==True :#line:816
                                O0OO0O00O00O0O0O0 ={}#line:817
                                O0OO0O00O00O0O0O0 ["hypo_id"]=OO0OOOOO0000OO000 .stats ['total_valid']#line:818
                                O0OO0O00O00O0O0O0 ["cedents"]={}#line:819
                                for OO0O00OO0OO0OO00O in OOOOO00000O0OO000 ['cedents']:#line:820
                                    O0OO0O00O00O0O0O0 ['cedents'][OO0O00OO0OO0OO00O ['cedent_type']]=OO0O00OO0OO0OO00O ['generated_string']#line:821
                                O0OO0O00O00O0O0O0 ["params"]=OO0000OOO0OO000O0 #line:823
                                O0OO0O00O00O0O0O0 ["trace_cedent"]=_O00O00O000OO00O00 #line:824
                                OO0OOOOO0000OO000 ._print_hypo (O0OO0O00O00O0O0O0 )#line:825
                                O0OO0O00O00O0O0O0 ["traces"]=_O0O00000OOOO00O00 #line:828
                                OO0OOOOO0000OO000 .hypolist .append (O0OO0O00O00O0O0O0 )#line:829
                            OO0OOOOO0000OO000 .stats ['total_cnt']+=1 #line:830
                    if _OOO0OO0OO00O0O0OO >=0 :#line:831
                        if len (OOOOO00000O0OO000 ['cedents_to_do'])>len (OOOOO00000O0OO000 ['cedents']):#line:832
                            OO0OOOOO0000OO000 ._start_cedent (OOOOO00000O0OO000 )#line:833
                    OOOOO00000O0OO000 ['cedents'].pop ()#line:834
                    if (len (_O00O00O000OO00O00 )<_O0OOO0OO00O0O0OOO ):#line:835
                        OO0OOOOO0000OO000 ._genvar (OOOOO00000O0OO000 ,O00O00OO0O0O0O00O ,_O00O00O000OO00O00 ,_O0O00000OOOO00O00 ,_O00O0OO00OO00OO0O ,_OOO0OOO00O0O0OO0O ,_O0OOO0OO00O0O0OOO )#line:836
                else :#line:837
                    OOOOO00000O0OO000 ['cedents'].pop ()#line:838
                if len (_O0O0OO0O00OOO0O00 )<_O0OOOOOO0O000000O :#line:839
                    OO0OOOOO0000OO000 ._gencomb (OOOOO00000O0OO000 ,O00O00OO0O0O0O00O ,_O00O00O000OO00O00 ,_O0O00000OOOO00O00 ,_O0O0OO0O00OOO0O00 ,_O0OO00O000O0000OO ,_O0000OO000O0OO000 ,O0O0000000O00O000 ,_O000O0OOOOOOO00O0 ,_OOO0OOO00O0O0OO0O ,_O0OOO0OO00O0O0OOO ,_O000000O0OOO0O0O0 ,_O0OOOOOO0O000000O )#line:840
                _O0O0OO0O00OOO0O00 .pop ()#line:841
    def _start_cedent (O0OO0O0O000OO00OO ,O0OOO0OO0OO0O0OOO ):#line:843
        if len (O0OOO0OO0OO0O0OOO ['cedents_to_do'])>len (O0OOO0OO0OO0O0OOO ['cedents']):#line:844
            _OOO0O00OO00O00OOO =[]#line:845
            _OO0000OO0OOOOO0O0 =[]#line:846
            OO000OO0000000000 ={}#line:847
            OO000OO0000000000 ['cedent_type']=O0OOO0OO0OO0O0OOO ['cedents_to_do'][len (O0OOO0OO0OO0O0OOO ['cedents'])]#line:848
            O00OOOO0OO0000O0O =OO000OO0000000000 ['cedent_type']#line:849
            if ((O00OOOO0OO0000O0O [-1 ]=='-')|(O00OOOO0OO0000O0O [-1 ]=='+')):#line:850
                O00OOOO0OO0000O0O =O00OOOO0OO0000O0O [:-1 ]#line:851
            OO000OO0000000000 ['defi']=O0OO0O0O000OO00OO .kwargs .get (O00OOOO0OO0000O0O )#line:853
            if (OO000OO0000000000 ['defi']==None ):#line:854
                print ("Error getting cedent ",OO000OO0000000000 ['cedent_type'])#line:855
            _OOOOO0O00OO0O000O =int (0 )#line:856
            OO000OO0000000000 ['num_cedent']=len (OO000OO0000000000 ['defi'].get ('attributes'))#line:861
            if (OO000OO0000000000 ['defi'].get ('type')=='con'):#line:862
                _OOOOO0O00OO0O000O =(1 <<O0OO0O0O000OO00OO .data ["rows_count"])-1 #line:863
            O0OO0O0O000OO00OO ._genvar (O0OOO0OO0OO0O0OOO ,OO000OO0000000000 ,_OOO0O00OO00O00OOO ,_OO0000OO0OOOOO0O0 ,_OOOOO0O00OO0O000O ,OO000OO0000000000 ['defi'].get ('minlen'),OO000OO0000000000 ['defi'].get ('maxlen'))#line:864
    def _calc_all (O00O0O00OOO0O0O0O ,**OOOO0O00OOO000OO0 ):#line:867
        O00O0O00OOO0O0O0O ._prep_data (O00O0O00OOO0O0O0O .kwargs .get ("df"))#line:868
        O00O0O00OOO0O0O0O ._calculate (**OOOO0O00OOO000OO0 )#line:869
    def _check_cedents (OO0O0O000O00O0000 ,O000O0O0O0OO0O00O ,**O0OOO00O0O0OOO0O0 ):#line:871
        O0O0OO0OOO0OOO00O =True #line:872
        if (O0OOO00O0O0OOO0O0 .get ('quantifiers',None )==None ):#line:873
            print (f"Error: missing quantifiers.")#line:874
            O0O0OO0OOO0OOO00O =False #line:875
            return O0O0OO0OOO0OOO00O #line:876
        if (type (O0OOO00O0O0OOO0O0 .get ('quantifiers'))!=dict ):#line:877
            print (f"Error: quantifiers are not dictionary type.")#line:878
            O0O0OO0OOO0OOO00O =False #line:879
            return O0O0OO0OOO0OOO00O #line:880
        for OO00OOO0OOO0O0OOO in O000O0O0O0OO0O00O :#line:882
            if (O0OOO00O0O0OOO0O0 .get (OO00OOO0OOO0O0OOO ,None )==None ):#line:883
                print (f"Error: cedent {OO00OOO0OOO0O0OOO} is missing in parameters.")#line:884
                O0O0OO0OOO0OOO00O =False #line:885
                return O0O0OO0OOO0OOO00O #line:886
            OOOOOOOOO0OO0OO0O =O0OOO00O0O0OOO0O0 .get (OO00OOO0OOO0O0OOO )#line:887
            if (OOOOOOOOO0OO0OO0O .get ('minlen'),None )==None :#line:888
                print (f"Error: cedent {OO00OOO0OOO0O0OOO} has no minimal length specified.")#line:889
                O0O0OO0OOO0OOO00O =False #line:890
                return O0O0OO0OOO0OOO00O #line:891
            if not (type (OOOOOOOOO0OO0OO0O .get ('minlen'))is int ):#line:892
                print (f"Error: cedent {OO00OOO0OOO0O0OOO} has invalid type of minimal length ({type(OOOOOOOOO0OO0OO0O.get('minlen'))}).")#line:893
                O0O0OO0OOO0OOO00O =False #line:894
                return O0O0OO0OOO0OOO00O #line:895
            if (OOOOOOOOO0OO0OO0O .get ('maxlen'),None )==None :#line:896
                print (f"Error: cedent {OO00OOO0OOO0O0OOO} has no maximal length specified.")#line:897
                O0O0OO0OOO0OOO00O =False #line:898
                return O0O0OO0OOO0OOO00O #line:899
            if not (type (OOOOOOOOO0OO0OO0O .get ('maxlen'))is int ):#line:900
                print (f"Error: cedent {OO00OOO0OOO0O0OOO} has invalid type of maximal length.")#line:901
                O0O0OO0OOO0OOO00O =False #line:902
                return O0O0OO0OOO0OOO00O #line:903
            if (OOOOOOOOO0OO0OO0O .get ('type'),None )==None :#line:904
                print (f"Error: cedent {OO00OOO0OOO0O0OOO} has no type specified.")#line:905
                O0O0OO0OOO0OOO00O =False #line:906
                return O0O0OO0OOO0OOO00O #line:907
            if not ((OOOOOOOOO0OO0OO0O .get ('type'))in (['con','dis'])):#line:908
                print (f"Error: cedent {OO00OOO0OOO0O0OOO} has invalid type. Allowed values are 'con' and 'dis'.")#line:909
                O0O0OO0OOO0OOO00O =False #line:910
                return O0O0OO0OOO0OOO00O #line:911
            if (OOOOOOOOO0OO0OO0O .get ('attributes'),None )==None :#line:912
                print (f"Error: cedent {OO00OOO0OOO0O0OOO} has no attributes specified.")#line:913
                O0O0OO0OOO0OOO00O =False #line:914
                return O0O0OO0OOO0OOO00O #line:915
            for O0O000OOO0O00000O in OOOOOOOOO0OO0OO0O .get ('attributes'):#line:916
                if (O0O000OOO0O00000O .get ('name'),None )==None :#line:917
                    print (f"Error: cedent {OO00OOO0OOO0O0OOO} / attribute {O0O000OOO0O00000O} has no 'name' attribute specified.")#line:918
                    O0O0OO0OOO0OOO00O =False #line:919
                    return O0O0OO0OOO0OOO00O #line:920
                if not ((O0O000OOO0O00000O .get ('name'))in OO0O0O000O00O0000 .data ["varname"]):#line:921
                    print (f"Error: cedent {OO00OOO0OOO0O0OOO} / attribute {O0O000OOO0O00000O.get('name')} not in variable list. Please check spelling.")#line:922
                    O0O0OO0OOO0OOO00O =False #line:923
                    return O0O0OO0OOO0OOO00O #line:924
                if (O0O000OOO0O00000O .get ('type'),None )==None :#line:925
                    print (f"Error: cedent {OO00OOO0OOO0O0OOO} / attribute {O0O000OOO0O00000O.get('name')} has no 'type' attribute specified.")#line:926
                    O0O0OO0OOO0OOO00O =False #line:927
                    return O0O0OO0OOO0OOO00O #line:928
                if not ((O0O000OOO0O00000O .get ('type'))in (['rcut','lcut','seq','subset'])):#line:929
                    print (f"Error: cedent {OO00OOO0OOO0O0OOO} / attribute {O0O000OOO0O00000O.get('name')} has unsupported type {O0O000OOO0O00000O.get('type')}. Supported types are 'subset','seq','lcut','rcut'.")#line:930
                    O0O0OO0OOO0OOO00O =False #line:931
                    return O0O0OO0OOO0OOO00O #line:932
                if (O0O000OOO0O00000O .get ('minlen'),None )==None :#line:933
                    print (f"Error: cedent {OO00OOO0OOO0O0OOO} / attribute {O0O000OOO0O00000O.get('name')} has no minimal length specified.")#line:934
                    O0O0OO0OOO0OOO00O =False #line:935
                    return O0O0OO0OOO0OOO00O #line:936
                if not (type (O0O000OOO0O00000O .get ('minlen'))is int ):#line:937
                    print (f"Error: cedent {OO00OOO0OOO0O0OOO} / attribute {O0O000OOO0O00000O.get('name')} has invalid type of minimal length.")#line:938
                    O0O0OO0OOO0OOO00O =False #line:939
                    return O0O0OO0OOO0OOO00O #line:940
                if (O0O000OOO0O00000O .get ('maxlen'),None )==None :#line:941
                    print (f"Error: cedent {OO00OOO0OOO0O0OOO} / attribute {O0O000OOO0O00000O.get('name')} has no maximal length specified.")#line:942
                    O0O0OO0OOO0OOO00O =False #line:943
                    return O0O0OO0OOO0OOO00O #line:944
                if not (type (O0O000OOO0O00000O .get ('maxlen'))is int ):#line:945
                    print (f"Error: cedent {OO00OOO0OOO0O0OOO} / attribute {O0O000OOO0O00000O.get('name')} has invalid type of maximal length.")#line:946
                    O0O0OO0OOO0OOO00O =False #line:947
                    return O0O0OO0OOO0OOO00O #line:948
        return O0O0OO0OOO0OOO00O #line:949
    def _calculate (OO0OO00OO0O0OOOO0 ,**O00000OO00O0OOO0O ):#line:951
        if OO0OO00OO0O0OOOO0 .data ["data_prepared"]==0 :#line:952
            print ("Error: data not prepared")#line:953
            return #line:954
        OO0OO00OO0O0OOOO0 .kwargs =O00000OO00O0OOO0O #line:955
        OO0OO00OO0O0OOOO0 .proc =O00000OO00O0OOO0O .get ('proc')#line:956
        OO0OO00OO0O0OOOO0 .quantifiers =O00000OO00O0OOO0O .get ('quantifiers')#line:957
        OO0OO00OO0O0OOOO0 ._init_task ()#line:959
        OO0OO00OO0O0OOOO0 .stats ['start_proc_time']=time .time ()#line:960
        OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do']=[]#line:961
        OO0OO00OO0O0OOOO0 .task_actinfo ['cedents']=[]#line:962
        if O00000OO00O0OOO0O .get ("proc")=='CFMiner':#line:965
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do']=['cond']#line:966
            if O00000OO00O0OOO0O .get ('target',None )==None :#line:967
                print ("ERROR: no target variable defined for CF Miner")#line:968
                return #line:969
            if not (OO0OO00OO0O0OOOO0 ._check_cedents (['cond'],**O00000OO00O0OOO0O )):#line:970
                return #line:971
            if not (O00000OO00O0OOO0O .get ('target')in OO0OO00OO0O0OOOO0 .data ["varname"]):#line:972
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:973
                return #line:974
        elif O00000OO00O0OOO0O .get ("proc")=='4ftMiner':#line:976
            if not (OO0OO00OO0O0OOOO0 ._check_cedents (['ante','succ'],**O00000OO00O0OOO0O )):#line:977
                return #line:978
            _OOO00O0OO000O00O0 =O00000OO00O0OOO0O .get ("cond")#line:980
            if _OOO00O0OO000O00O0 !=None :#line:981
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:982
            else :#line:983
                OOOOOO0OO00O0OO0O =OO0OO00OO0O0OOOO0 .cedent #line:984
                OOOOOO0OO00O0OO0O ['cedent_type']='cond'#line:985
                OOOOOO0OO00O0OO0O ['filter_value']=(1 <<OO0OO00OO0O0OOOO0 .data ["rows_count"])-1 #line:986
                OOOOOO0OO00O0OO0O ['generated_string']='---'#line:987
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:989
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents'].append (OOOOOO0OO00O0OO0O )#line:990
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:994
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:995
        elif O00000OO00O0OOO0O .get ("proc")=='NewAct4ftMiner':#line:996
            _OOO00O0OO000O00O0 =O00000OO00O0OOO0O .get ("cond")#line:999
            if _OOO00O0OO000O00O0 !=None :#line:1000
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1001
            else :#line:1002
                OOOOOO0OO00O0OO0O =OO0OO00OO0O0OOOO0 .cedent #line:1003
                OOOOOO0OO00O0OO0O ['cedent_type']='cond'#line:1004
                OOOOOO0OO00O0OO0O ['filter_value']=(1 <<OO0OO00OO0O0OOOO0 .data ["rows_count"])-1 #line:1005
                OOOOOO0OO00O0OO0O ['generated_string']='---'#line:1006
                print (OOOOOO0OO00O0OO0O ['filter_value'])#line:1007
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1008
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents'].append (OOOOOO0OO00O0OO0O )#line:1009
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('antv')#line:1010
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1011
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1012
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1013
        elif O00000OO00O0OOO0O .get ("proc")=='Act4ftMiner':#line:1014
            _OOO00O0OO000O00O0 =O00000OO00O0OOO0O .get ("cond")#line:1017
            if _OOO00O0OO000O00O0 !=None :#line:1018
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1019
            else :#line:1020
                OOOOOO0OO00O0OO0O =OO0OO00OO0O0OOOO0 .cedent #line:1021
                OOOOOO0OO00O0OO0O ['cedent_type']='cond'#line:1022
                OOOOOO0OO00O0OO0O ['filter_value']=(1 <<OO0OO00OO0O0OOOO0 .data ["rows_count"])-1 #line:1023
                OOOOOO0OO00O0OO0O ['generated_string']='---'#line:1024
                print (OOOOOO0OO00O0OO0O ['filter_value'])#line:1025
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1026
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents'].append (OOOOOO0OO00O0OO0O )#line:1027
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1028
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1029
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1030
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1031
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1032
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1033
        elif O00000OO00O0OOO0O .get ("proc")=='SD4ftMiner':#line:1034
            if not (OO0OO00OO0O0OOOO0 ._check_cedents (['ante','succ','frst','scnd'],**O00000OO00O0OOO0O )):#line:1037
                return #line:1038
            _OOO00O0OO000O00O0 =O00000OO00O0OOO0O .get ("cond")#line:1039
            if _OOO00O0OO000O00O0 !=None :#line:1040
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1041
            else :#line:1042
                OOOOOO0OO00O0OO0O =OO0OO00OO0O0OOOO0 .cedent #line:1043
                OOOOOO0OO00O0OO0O ['cedent_type']='cond'#line:1044
                OOOOOO0OO00O0OO0O ['filter_value']=(1 <<OO0OO00OO0O0OOOO0 .data ["rows_count"])-1 #line:1045
                OOOOOO0OO00O0OO0O ['generated_string']='---'#line:1046
                print (OOOOOO0OO00O0OO0O ['filter_value'])#line:1047
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1048
                OO0OO00OO0O0OOOO0 .task_actinfo ['cedents'].append (OOOOOO0OO00O0OO0O )#line:1049
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('frst')#line:1050
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1051
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1052
            OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1053
        else :#line:1054
            print ("Unsupported procedure")#line:1055
            return #line:1056
        print ("Will go for ",O00000OO00O0OOO0O .get ("proc"))#line:1057
        OO0OO00OO0O0OOOO0 .task_actinfo ['optim']={}#line:1060
        OO0OOO0O000OOOO0O =True #line:1061
        for OO0O00OO0OOO0O0OO in OO0OO00OO0O0OOOO0 .task_actinfo ['cedents_to_do']:#line:1062
            try :#line:1063
                O0OOO00OO000O0OO0 =OO0OO00OO0O0OOOO0 .kwargs .get (OO0O00OO0OOO0O0OO )#line:1064
                if O0OOO00OO000O0OO0 .get ('type')!='con':#line:1067
                    OO0OOO0O000OOOO0O =False #line:1068
            except :#line:1069
                O00O00000O0O0O000 =1 <2 #line:1070
        if "opts"in O00000OO00O0OOO0O :#line:1072
            if "no_optimizations"in O00000OO00O0OOO0O .get ('opts'):#line:1073
                OO0OOO0O000OOOO0O =False #line:1074
                print ("No optimization will be made.")#line:1075
        OOO00O00OO000OOO0 ={}#line:1077
        OOO00O00OO000OOO0 ['only_con']=OO0OOO0O000OOOO0O #line:1078
        OO0OO00OO0O0OOOO0 .task_actinfo ['optim']=OOO00O00OO000OOO0 #line:1079
        print ("Starting to mine rules.")#line:1087
        OO0OO00OO0O0OOOO0 ._start_cedent (OO0OO00OO0O0OOOO0 .task_actinfo )#line:1088
        OO0OO00OO0O0OOOO0 .stats ['end_proc_time']=time .time ()#line:1090
        print ("Done. Total verifications : "+str (OO0OO00OO0O0OOOO0 .stats ['total_cnt'])+", hypotheses "+str (OO0OO00OO0O0OOOO0 .stats ['total_valid'])+",control number:"+str (OO0OO00OO0O0OOOO0 .stats ['control_number'])+", times: prep "+str (OO0OO00OO0O0OOOO0 .stats ['end_prep_time']-OO0OO00OO0O0OOOO0 .stats ['start_prep_time'])+", processing "+str (OO0OO00OO0O0OOOO0 .stats ['end_proc_time']-OO0OO00OO0O0OOOO0 .stats ['start_proc_time']))#line:1093
        O00O000O000O00OOO ={}#line:1094
        O0OOO000O0O000OOO ={}#line:1095
        O0OOO000O0O000OOO ["task_type"]=O00000OO00O0OOO0O .get ('proc')#line:1096
        O0OOO000O0O000OOO ["target"]=O00000OO00O0OOO0O .get ('target')#line:1098
        O0OOO000O0O000OOO ["self.quantifiers"]=OO0OO00OO0O0OOOO0 .quantifiers #line:1099
        if O00000OO00O0OOO0O .get ('cond')!=None :#line:1101
            O0OOO000O0O000OOO ['cond']=O00000OO00O0OOO0O .get ('cond')#line:1102
        if O00000OO00O0OOO0O .get ('ante')!=None :#line:1103
            O0OOO000O0O000OOO ['ante']=O00000OO00O0OOO0O .get ('ante')#line:1104
        if O00000OO00O0OOO0O .get ('succ')!=None :#line:1105
            O0OOO000O0O000OOO ['succ']=O00000OO00O0OOO0O .get ('succ')#line:1106
        if O00000OO00O0OOO0O .get ('opts')!=None :#line:1107
            O0OOO000O0O000OOO ['opts']=O00000OO00O0OOO0O .get ('opts')#line:1108
        O00O000O000O00OOO ["taskinfo"]=O0OOO000O0O000OOO #line:1109
        OOOO0O0O0OO0000O0 ={}#line:1110
        OOOO0O0O0OO0000O0 ["total_verifications"]=OO0OO00OO0O0OOOO0 .stats ['total_cnt']#line:1111
        OOOO0O0O0OO0000O0 ["valid_hypotheses"]=OO0OO00OO0O0OOOO0 .stats ['total_valid']#line:1112
        OOOO0O0O0OO0000O0 ["time_prep"]=OO0OO00OO0O0OOOO0 .stats ['end_prep_time']-OO0OO00OO0O0OOOO0 .stats ['start_prep_time']#line:1113
        OOOO0O0O0OO0000O0 ["time_processing"]=OO0OO00OO0O0OOOO0 .stats ['end_proc_time']-OO0OO00OO0O0OOOO0 .stats ['start_proc_time']#line:1114
        OOOO0O0O0OO0000O0 ["time_total"]=OO0OO00OO0O0OOOO0 .stats ['end_prep_time']-OO0OO00OO0O0OOOO0 .stats ['start_prep_time']+OO0OO00OO0O0OOOO0 .stats ['end_proc_time']-OO0OO00OO0O0OOOO0 .stats ['start_proc_time']#line:1115
        O00O000O000O00OOO ["summary_statistics"]=OOOO0O0O0OO0000O0 #line:1116
        O00O000O000O00OOO ["hypotheses"]=OO0OO00OO0O0OOOO0 .hypolist #line:1117
        O0OO00000OO00OO00 ={}#line:1118
        O0OO00000OO00OO00 ["varname"]=OO0OO00OO0O0OOOO0 .data ["varname"]#line:1119
        O0OO00000OO00OO00 ["catnames"]=OO0OO00OO0O0OOOO0 .data ["catnames"]#line:1120
        O00O000O000O00OOO ["datalabels"]=O0OO00000OO00OO00 #line:1121
        OO0OO00OO0O0OOOO0 .result =O00O000O000O00OOO #line:1123
