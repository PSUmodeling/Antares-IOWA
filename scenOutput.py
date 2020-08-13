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

if len(sys.argv)!=2:
    raise ValueError('Provide scenario identifier')
scen_interest = sys.argv[1]#.strip("[]")).split(',')

ref_file = 'PSU_CT_00RH_NCC_NF_test.csv' #'CLU_CT_00RH_NCC_NF_test.csv'
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
W = []
WC= []
# ON= []
# TP= []
B = []
crop=[]
nOut = []
yOut = []
delta_C = []

SOC = [] # delta soil organic carbon
NO3 = [] # nitrate leached
Vol = [] # volatilized
N2O = [] # N2O denitrification

#Use -1 to force a crash if index not found
cc = -1  # cycles id
mc = -1  # cafo id
sc = -1  # soil id
lc = -1  # landuse id
anc= -1  # animal id
ac = -1  # ammonium id
# onc= -1  # organic nitrogen id
# tpc= -1  # total phosphorus id
wc = -1  # nldas weather file
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
                    ac = i
                elif row[i] == '_ONADJ':
                    onc = i
                elif row[i] == '_ANIMAL':
                    anc = i
                elif row[i] == '_PADJ':
                    tpc = i

    else:
        try:
            L.append(row[lc])
            S.append(row[sc])
            C.append(row[cc])
            A.append(float(row[ac]))
            M.append(float(row[mc]))
            B.append(row[anc])
            # ON.append(float(row[onc]))
            # TP.append(float(row[tpc]))
            W.append(row[wc].strip())
            WC.append(row[wcc].strip())
        except ValueError:
            print(row_copy)
            quit()

data.close()
nrow=len(C)

for i in range(nrow):
    SOC = [] # delta soil organic carbon
    NO3 = [] # nitrate leached
    Vol = [] # volatilized
    N2O = [] # N2O denitrification
    NO3_avg = 999 # nitrate leached
    Vol_avg = 999 # volatilized
    N2O_avg = 999 # N2O denitrification
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

    ctrl_file = 'W'+WC[i]+'_'+crop[i]+P[i]+'_'+S[i]+'_'+scen_interest

    n_path = 'output/'+ctrl_file+'/annualN.dat'
    y_path = 'output/'+ctrl_file+'/season.dat'
    s_path = 'output/'+ctrl_file+'/summary.dat'

    try:
        cycOut = open(n_path)

        NO3sum = 0
        N2Osum = 0
        Volsum = 0
        y0 = 0
        yf = 1
        nums = []
        nitrate = vol = nitrous = 'NA'
        for rownum, row in enumerate(cycOut):
            if rownum >= 2 and row[0:4] != '':
                if rownum == 2:
                    y0 = float(row[0:4])

                nums_str = row.split()
                nums = [float(n.strip()) for n in nums_str]
                NO3sum += nums[4]+nums[6]
                N2Osum += nums[11]
                Volsum += nums[10]
                yf = float(row[0:4])

                if float(row[0:4])>= 2013:
                    nums_str = row.split()
                    nums = [float(n.strip()) for n in nums_str]

                    nitrate = round(nums[4]+nums[6],3)
                    nitrous = round(nums[11],3)
                    vol = round(nums[10],3)
                    NO3.append(nitrate)
                    N2O.append(nitrous)
                    Vol.append(vol)
        NO3_avg = round(NO3sum/(yf - y0),3)
        N2O_avg = round(N2Osum/(yf - y0),3)
        Vol_avg = round(Volsum/(yf - y0),3)
        if nitrate == 'NA':
            nOut.append(',NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA')
        else:
            nOut.append(','+str(NO3)[1:-1]+','+str(N2O)[1:-1]+\
            ','+str(Vol)[1:-1]+','+str(NO3_avg)+','+str(N2O_avg)+','+str(Vol_avg))

        cycOut = open(y_path)
        crpOld = ''
        yldOld = 0
        yrOld = ''
        Yld = [] # Annual yield
        Crp = [] # Crops harvested each year
        for rownum, row in enumerate(cycOut):
            if rownum > 1 and float(row[0:4])>= 2013:
                row = row.split()
                crp = row[1][0:3]

                # Harvest may be grain or forage
                if float(row[5]) > 0:
                    if crpOld != crp and yrOld != row[0][0:4]:
                        yld = round(float(row[5]),3)
                    else: # Cycles may set harvest early, 2 harvests print
                        yld = round(float(row[5]),3) + float(yldOld)
                else: # forage
                    yld = round(float(row[6]),3)


                # There may be multiple harvests in 1 year
                # If this is not the first harvest of the year:
                if yrOld == row[0][0:4] and crp == ('Alf' or 'Rye'):
                    yld = str(yldOld)+'|'+str(yld)
                    crp = crpOld+'|'+crp

                # if the last crop isn't current crop, AND it's not 1st year:
                elif yldOld != crpOld != '' and yrOld != row[0][0:4]:
                        Yld.append(yldOld)
                        Crp.append(crpOld)

                yrOld = row[0][0:4]
                crpOld= crp
                yldOld= yld

        # Take care of the last row of data
        Yld.append(yld)
        Crp.append(crp)
        cycOut.close()

        if crpOld== '': # There's no crop data
            yOut.append(',NA,NA,NA,NA,NA,NA,NA,NA,')
        else:
            yOut.append(','+str(Crp)[1:-1]+','+str(Yld)[1:-1]+',')
        cycOut = open(s_path)
        dC = 'NA'
        for rownum,row in enumerate(cycOut):
            if rownum == 2:
                row = row.split()
                # change in soil C over the simulation
                # for default scenario, 1980-2016
                # for alternative scenarios, 2013-2016
                dC = round(float(row[2]),3)
        delta_C.append(dC)
        cycOut.close()

    except FileNotFoundError:
        nOut.append(',NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA')
        yOut.append(',NA,NA,NA,NA,NA,NA,NA,NA,')
        delta_C.append('NA')
data.close()

if nrow != len(delta_C) or nrow != len(nOut) or nrow != len(yOut):
    print('Length of output arrays are not equal')
    print('Number of rows is '+str(nrow))
    print('Length of delta_C: '+str(len(delta_C)))
    print('Length of N array: '+str(len(nOut)))
    print('Length of Y array '+str(len(yOut)))
    quit()
# print(nrow)
# print(len(delta_C))
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
        updated = ",".join(row)+str(',NO3_13, NO3_14, NO3_15, NO3_16, N2O_13, N2O_14, N2O_15, N2O_16, Vol_13, Vol_14, Vol_15, Vol_16 \
,NO3_avg, N2O_avg, Vol_avg, Crops13, Crops14, Crops15, Crops16, Yield13, Yield14, Yield15, Yield16, soilC_delta \n')
    else:
        updated = ",".join(row)+nOut[i]+yOut[i]+str(delta_C[i])+str('\n')

    newdata+=updated
wfile.close()
data2 = open(wfile_name,"w")
data2.write(newdata)
data2.close()
#########################################################################################
