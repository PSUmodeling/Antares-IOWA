# ### Potential Antares / EFC CSV files (ald_fname)
#                'CT_NCC_NF_00RH'#,'NT_RYE_NPS_30RH'
                 #,'CT_NCC_NF_30RH','CT_NCC_NF_45RH','CT_NCC_NF_70RH'
                 #,'RT_NCC_NF_00RH','RT_NCC_NF_30RH','RT_NCC_NF_45RH','RT_NCC_NF_70RH'
                 #,'NT_NCC_NF_00RH','NT_NCC_NF_30RH','NT_NCC_NF_45RH','NT_NCC_NF_70RH'
                 #,'CT_NCC_NPS_00RH','CT_NCC_NPS_30RH','CT_NCC_NPS_45RH','CT_NCC_NPS_70RH'
                 #,'RT_NCC_NPS_00RH','RT_NCC_NPS_30RH','RT_NCC_NPS_45RH','RT_NCC_NPS_70RH'
                 #,'NT_NCC_NPS_00RH','NT_NCC_NPS_30RH','NT_NCC_NPS_45RH','NT_NCC_NPS_70RH'
                 #,'CT_RYE_NF_00RH','CT_RYE_NF_30RH','CT_RYE_NF_45RH','CT_RYE_NF_70RH'
                 #,'RT_RYE_NF_00RH','RT_RYE_NF_30RH','RT_RYE_NF_45RH','RT_RYE_NF_70RH'
                 #,'NT_RYE_NF_00RH','NT_RYE_NF_30RH','NT_RYE_NF_45RH','NT_RYE_NF_70RH'
                 #,'CT_RYE_NPS_00RH','CT_RYE_NPS_30RH','CT_RYE_NPS_45RH','CT_RYE_NPS_70RH'
                 #,'RT_RYE_NPS_00RH','RT_RYE_NPS_30RH','RT_RYE_NPS_45RH','RT_RYE_NPS_70RH'
                 #,'NT_RYE_NPS_00RH','NT_RYE_NPS_30RH','NT_RYE_NPS_45RH','NT_RYE_NPS_70RH'
#!/usr/bin/env python3
import sys
import numpy as np
# import time
# startTime = time.time()
EFC_first_year = 2013
EFC_last_year = 2016

if len(sys.argv)!=2:
    raise ValueError('Provide scenario identifier')
scen_interest = sys.argv[1]#.strip("[]")).split(',')

ref_file = 'PSU_CT_00RH_NCC_NF_ref.csv' #'CLU_CT_00RH_NCC_NF_test.csv'
data = open(ref_file)
scen_interest = scen_interest.split('_')
scen = scen_interest[0]+'_'+scen_interest[3]+'_'+scen_interest[1]+'_'+scen_interest[2]
wfile_name = scen+'_cycles.csv'
scen_interest = '_'.join(scen_interest)

# create multimode files
r_type =['C','CS','CCS']
lenRot  =[1,2,3]

firstrun = True
C = []
M = []
S = []
L = []
P = []
A = []
N = []
W = []
WC= []
B = []
F = []
crop=[]

a_dict={}
n_data=[{}]*(EFC_last_year-EFC_first_year+1)
y_data=[{}]*(EFC_last_year-EFC_first_year+1)

#Use -1 to force a crash if index not found
cc = -1  # cycles id
mc = -1  # cafo id
sc = -1  # soil id
lc = -1  # landuse id
anc= -1  # animal id
nc = -1  # ammonium id
ac = -1  # acreage
wc = -1  # nldas weather file
fc = -1  # county (fips) id
wcc= -1  # nldas code id
rlen = -1  # rotation length

for row in data:
    row_copy = row
    row = row.split(',')

    if firstrun:
        #print(First!)
        firstrun = False
        for i in range(len(row)):
                #print(Saving vectors)
                if row[i] == 'cluid':
                    cc = i
                elif row[i] == 'fips':
                    fc = i
                elif row[i] == 'cluacres':
                    ac = i
                elif row[i] == 'gnatsgo_ma':
                    sc = i
                elif row[i] == 'EFC_ROTATE':
                    lc = i
                elif row[i] == 'NLDAS':
                    wc = i
                elif row[i] == 'NLDAS_CODE':
                    wcc = i
                elif row[i] == 'cafo_major':
                    mc = i
                elif row[i] == '_NH3ADJ':
                    nc = i

    else:
        try:
            L.append(row[lc])
            S.append(row[sc])
            C.append(row[cc])
            N.append(round(float(row[nc]),3))
            M.append(float(row[mc]))
            W.append(row[wc].strip())
            WC.append(row[wcc].strip())
            a_dict[row[cc]] = [row[fc],float(row[ac])]
        except ValueError:
            print(row_copy)
            quit()

data.close()

nrow=len(C)
YEAR= []
CLU = []
NO3 = []
CROP= []
NO3 = [] # nitrate leached
Vol = [] # volatilized
N2O = [] # N2O denitrification
Yld = [] # Annual yield
Crp = [] # Crops harvested each year
YR =  []

sim_seen = set()
for i in range(nrow):
    crp = [] # yield

    if L[i]== "CG|CG|CG|CG":
        crop.append('C')
        rlen = 1
        P.append('1')
    elif L[i] == "SB|SB|SB|SB":
        crop.append('S')
        rlen = 1
        P.append('1')
    elif L[i] == "CG|SB|CG|SB" or L[i] == "SB|CG|SB|CG":
        crop.append('CS')
        rlen = 2
        if L[i] == "SB|CG|SB|CG":
            P.append('1')
        else:
            P.append('2')
    elif L[i] == "SB|CG|CG|SB" or L[i] == "CG|CG|SB|CG" or L[i] == "CG|SB|CG|CG" or L[i] == "SB|CG|CG|CG":
        crop.append('CCS')
        rlen = 3

        if L[i][0:2] == 'SB':
            P.append('1')
        elif L[i][3:5] == 'SB':
            P.append('2')
        elif L[i][6:8] == 'SB':
            P.append('3')
        else: P.append('4')
    else:
        crop.append('CS')
        rlen = 2
        if L[i][0:2] == 'SB':
            P.append('1')
        else: P.append('2')

    ctrl_file = 'W'+WC[i]+'_'+crop[i]+P[i]+'_'+S[i]+'_NH'+str(N[i])+'_'+scen_interest

    if ctrl_file in sim_seen: continue

    n_path = 'output/'+ctrl_file+'/annualN.dat'
    y_path = 'output/'+ctrl_file+'/season.dat'
    s_path = 'output/'+ctrl_file+'/summary.dat'

    try:
        cycOut = open(n_path)

        for rownum, row in enumerate(cycOut):
            if rownum >= 2 and row[0:4] != '':
                nums_str = row.split()
                nums = [float(n.strip()) for n in nums_str]
                NO3 = nums[4]+nums[6]
                N2O = nums[11]
                Vol = nums[10]
                YEAR = int(row[0:4])

                if YEAR >= EFC_first_year:
                    n_data[YEAR-EFC_first_year][ctrl_file] = [NO3,N2O,Vol]

        cycOut.close()
        cycOut = open(y_path)
        crpOld = ''
        yldOld = 0
        yrOld = ''
        yld = np.nan
        crp = 'NA'
        for rownum, row in enumerate(cycOut):
            if rownum > 1 :

                row = row.split()
                crp = row[1][0:3]
                yr = int(row[0][0:4])
                # if grain, then yield is column 5
                if float(row[5]) > 0:
                    yld = round(float(row[5]),3)
                # otherwise, forage; use column 6 for yield
                else:
                    yld = round(float(row[6]),3)

                # There may be multiple harvests in 1 year
                # if the last crop isn't current crop, AND it's not 1st year:
                if (len(YR) > 0 and len(Crp) > 0 and len(CLU) > 0 and
                    crp in ('Alf', 'Rye') and
                    crp == Crp[-1] and yr == YR[-1] and CLU[-1] == C[i]):

                    Yld[-1] += yld
                else:
                    CLU.append(C[i])
                    Yld.append(yld)
                    Crp.append(crp)
                    YR.append(yr)
                    y_data[YEAR-EFC_first_year][ctrl_file] = [crp,yld]
        cycOut.close()
        sim_seen.add(ctrl_file)
    except FileNotFoundError:
        continue

data.close()

# Calculate weighted average yield for year, crop, and county
WA = [np.nan]*len(Yld)
yr_cty_crp_inds = {}
for i in range(len(Yld)):
    yr = YR[i]
    cty = a_dict[CLU[i]][0]
    crp = Crp[i]
    cty_yr_crp = cty+'_'+str(yr)+'_'+crp
    if cty_yr_crp in yr_cty_crp_inds:
        yr_cty_crp_inds[cty_yr_crp].append(i)
    else:
        yr_cty_crp_inds[cty_yr_crp] = [i]

WAD = {}
#YTD = {}
for i in range(len(Yld)):
    yr = YR[i]
    cty = a_dict[CLU[i]][0]
    crp = Crp[i]
    cty_yr_crp = cty+'_'+str(yr)+'_'+crp
    if cty_yr_crp not in WAD:
        weighted_yields = [Yld[j]*a_dict[CLU[j]][1] for j in yr_cty_crp_inds[cty_yr_crp]]
        total_area = sum([ a_dict[CLU[j]][1] for j in yr_cty_crp_inds[cty_yr_crp]])
        #YTD[cty_yr_crp] = round(np.nansum(weighted_yields) ,3)
        WAD[cty_yr_crp] = round(np.nansum(weighted_yields) / total_area,3)


text = 'CTY_YEAR_CROP, WA_CTY \n'
for key,value in WAD.items():
    text +=  key+','+str(value)+'\n'

data2 = open(scen+'_WA_cty_booneV.csv',"w")
data2.write(text)
data2.close()

frstrun=True
newdata=''
updated = ''
add0n=' '
wfile = open(ref_file)
for j,row in enumerate(wfile):
    row = [r.strip() for r in row.split(',')]
    i = j-1
    if frstrun:
        frstrun=False
        updated = ",".join(row)+str(', NO3_13, N2O_13, Vol_13, NO3_14, N2O_14,\
Vol_14, NO3_15, N2O_15, Vol_15, NO3_16, NO_16, Vol_16,\
Crops13, Yld13, Crp14, Yld14, Crp15, Yld15, Crp16, Yld16 \n')
    else:
        ctrl_file = 'W'+WC[i]+'_'+crop[i]+P[i]+'_'+S[i]+'_NH'+str(N[i])+'_'+scen_interest

        if ctrl_file in n_data[0].keys():
            updated = ",".join(row)+\
            ','+','.join([','.join(map(str,n[ctrl_file])) for n in n_data]) +\
            ','+','.join([','.join(map(str,y[ctrl_file])) for y in y_data]) +\
            '\n'
        else:
            updated = ','.join(row)+ ','.join(['NA']*20)+'\n'
            print(ctrl_file)

    newdata+=updated
wfile.close()
data3 = open(wfile_name,"w")
data3.write(newdata)
data3.close()
################################################################################
# executionTime = (time.time() - startTime)
# print('Execution time in seconds: ' + str(executionTime))
