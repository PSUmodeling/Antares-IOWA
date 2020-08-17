#!/usr/bin/env python3

import numpy
import sys
#########################################################################################
## write multimode files
#########################################################################################


data = open("PSU_CT_00RH_NCC_NF_ref.csv") #'PSU_CT_00RH_NCC_NF_ref.csv'
 #IA_EFC_PSU_CGSB_20200622.csv

if len(sys.argv)!=2:
    raise ValueError('Provide scenario identifier')
scen_interest = (sys.argv[1].strip("[]")).split(',')

#scen_interest = ['CT_NCC_NF_00RH'#,'NT_RYE_NPS_30RH'
                 #,'CT_NCC_NF_30RH'#,'CT_NCC_NF_45RH','CT_NCC_NF_70RH'
                 #,'RT_NCC_NF_00RH','RT_NCC_NF_30RH','RT_NCC_NF_45RH','RT_NCC_NF_70RH'
                 #,'NT_NCC_NF_00RH'#,'NT_NCC_NF_30RH','NT_NCC_NF_45RH','NT_NCC_NF_70RH'
                 #,'CT_NCC_NPS_00RH','CT_NCC_NPS_30RH','CT_NCC_NPS_45RH','CT_NCC_NPS_70RH'
                 #,'RT_NCC_NPS_00RH','RT_NCC_NPS_30RH','RT_NCC_NPS_45RH','RT_NCC_NPS_70RH'
                 #,'NT_NCC_NPS_00RH','NT_NCC_NPS_30RH','NT_NCC_NPS_45RH','NT_NCC_NPS_70RH'
                 #,'CT_RYE_NF_00RH','CT_RYE_NF_30RH','CT_RYE_NF_45RH','CT_RYE_NF_70RH'
                 #,'RT_RYE_NF_00RH','RT_RYE_NF_30RH','RT_RYE_NF_45RH','RT_RYE_NF_70RH'
                 #,'NT_RYE_NF_00RH','NT_RYE_NF_30RH','NT_RYE_NF_45RH','NT_RYE_NF_70RH'
                 #,'CT_RYE_NPS_00RH','CT_RYE_NPS_30RH','CT_RYE_NPS_45RH','CT_RYE_NPS_70RH'
                 #,'RT_RYE_NPS_00RH','RT_RYE_NPS_30RH','RT_RYE_NPS_45RH','RT_RYE_NPS_70RH'
                 #,'NT_RYE_NPS_00RH','NT_RYE_NPS_30RH','NT_RYE_NPS_45RH','NT_RYE_NPS_70RH'
                 #]

# create multimode files
r_type = ['C','CS','CCS']                   # rotations
lenRot = [1,2,3]                            # length of rotation label
#tillage= ['RT','NT','CT']                  # reduced till, no till, conventional
#application=['NF','NPS']                   # fall UAN, preplant anhydrous w/ UAN side-dress
#covercrop = ['NCC','RYE']                  # no cover crop, rye cover crop
#resRemoval = ['00RH','30RH','45RH','75RH'] # percent of residue removed

# CRP scenarios

# Swithgrass scenarios
# MMfile = open('input\IA_SG_scenarios.txt', 'w' )
# MMfile.write('SIM_CODE \t\t\t\t\t\t ROTATION_YEARS START_YEAR END_YEAR USE_REINIT CROP_FILE \t OPERATION_FILE \t\t\t SOIL_FILE \
#     \t WEATHER_FILE \t REINIT_FILE HOURLY_INFILTRATION AUTOMATIC_NITROGEN \n')
# MMfile.close()

# Conventional crops scenarios
for j in range(len(scen_interest)):
    for i in range(len(r_type)):
        MMfile = open('input/IA_'+scen_interest[j]+'_'+r_type[i]+'_scenarios.txt', 'w' )
        MMfile.write('SIM_CODE \t\t\t\t ROTATION_YEARS START_YEAR END_YEAR USE_REINIT CROP_FILE \t OPERATION_FILE \t\t\t SOIL_FILE \
            \t WEATHER_FILE \t REINIT_FILE HOURLY_INFILTRATION AUTOMATIC_NITROGEN \n')
        MMfile.close()

# default parameter values
reinit   = 0
hour_inf = 1
auto_nit = 0
start    = 2010
end      = 2016
reinit_file = 'N/A'
crop_file   = 'GenCrops00RH.crop'

firstrun = True
C = []
M = []
S = []
L = []
P = []
A = []
W = []
WC= []
ON= []
TP= []
B = []
crop=[]

#Use -1 to force a crash if index not found
cc = -1  # cycles id
mc = -1  # cafo id
sc = -1  # soil id
lc = -1  # landuse id
anc= -1  # animal id
ac = -1  # ammonium id
onc= -1  # organic nitrogen id
tpc= -1  # total phosphorus id
wc = -1  # nldas weather file
wcc= -1  # nldas sim ID
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
                elif row[i] == '_ANIMAAL':
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
            ON.append(float(row[onc]))
            TP.append(float(row[tpc]))
            W.append(row[wc].strip())
            WC.append(row[wcc].strip())
        except ValueError:
            print(row_copy)
            quit()

data.close()
nrow=len(C)

sim_seen = set() # Keep track of unique simulation names
for i in range(nrow):
    if L[i]== "CG|CG|CG|CG":
        crop.append('C')
        rlen = 1
        P.append(1)
    elif L[i] == "SB|SB|SB|SB":
        crop.append('S')
        rlen = 1
        P.append(1)
    elif L[i] == "CG|SB|CG|SB" or L[i] == "SB|CG|SB|CG":
        crop.append('CS')
        rlen = 2
        if L[i] == "SB|CG|SB|CG":
            P.append(1)
        else:
            P.append(2)
    elif L[i] == "SB|CG|CG|SB" or L[i] == "CG|CG|SB|CG" or L[i] == "CG|SB|CG|CG" or L[i] == "SB|CG|CG|CG":
        crop.append('CCS')
        rlen = 3

        if L[i][0:2] == 'SB':
            P.append(1)
        elif L[i][3:5] == 'SB':
            P.append(2)
        elif L[i][6:8] == 'SB':
            P.append(3)
        else: P.append(4)
    else:
        crop.append('CS')
        rlen = 2
        if L[i][0:2] == 'SB':
            P.append(1)
        else: P.append(2)

    if B[i] == 'fert':
        A[i] = 0.75
    else: A[i] = round(A[i],3)


    # ctrl_SG = 'W'+WC[i]+'_'+crop[i]+'_'+S[i]+'_SG'
    soil_file = 'soils/'+S[i]+'.soil'
    wthr_file = 'weather/'+W[i]

    # oper_fileSG = 'operations/ALD_SG1_NH'+str(A[i])+'_CT_00RH.operation'
    # MMfileSG = open( 'input/IA_SG_scenarios.txt', 'a' )
    # MMfileSG.write('%s \t %i \t\t\t %i \t\t %i \t %i \t %s \t %s \t %s \t %s \t %s \t %i \t %i \n' %
    # (C[i]+'SG', 1, 2010, 2016, reinit, crop_file, oper_fileSG, ctrl_SG[0:-2]+'CT_NCC_NF_00RH_ss.soil', wthr_file, reinit_file, hour_inf, auto_nit))
    # MMfileSG.close()

    for k in range(len(scen_interest)):
         #unique simulation ID
            ctrl_file = 'W'+WC[i]+'_'+crop[i]+str(P[i])+'_'+S[i]+'_NH'+str(A[i])+'_'+scen_interest[k]
            soil_file_alt = 'W'+WC[i]+'_'+crop[i]+str(P[i])+'_'+S[i]+'_NH'+str(A[i])+'_CT_NCC_NF_00RH_ss.soil'
            if ctrl_file not in sim_seen:
                pass
            else: continue # skip repeat simulations

            # Pick operation file, fields with manure will receive manure in all scenarios
            if M[i] == -1:
                oper_file = 'operations/ALD_'+crop[i]+str(P[i])+'_NH'+str(A[i])+'_'+scen_interest[k][0:-5]+'.operation'
                #print(oper_file)
            else:
                oper_file = 'operations/ALD_'+crop[i]+str(P[i])+'_NH'+str(A[i])+'_'+scen_interest[k][0:6]+'_MAN'+'.operation'


            MMfile = open('input/IA_'+scen_interest[k]+'_'+crop[i]+'_scenarios.txt', 'a' )

            # scenarios should have a soil from default business-as-usual scenario, fertilizer scenarios will still have areas w/ manure
            if 'CT_NCC_NF_00RH' not in ctrl_file:
                # start= 2010
                MMfile.write('%s \t %i \t\t\t %i \t\t %i \t %i \t %s \t %s \t %s \t %s \t %s \t %i \t %i \n' %
                (ctrl_file, rlen, start, end, reinit, 'GenCrops'+scen_interest[k][-4:]+'.crop', oper_file, soil_file_alt, wthr_file, reinit_file, hour_inf, auto_nit))
                MMfile.close()
            else:
                start= 1980
                MMfile.write('%s \t %i \t\t\t %i \t\t %i \t %i \t %s \t %s \t %s \t %s \t %s \t %i \t %i \n' %
                (ctrl_file, rlen, start, end, reinit, crop_file, oper_file, soil_file, wthr_file, reinit_file, hour_inf, auto_nit))
                MMfile.close()

            sim_seen.add(ctrl_file)

# make list of unique operation files
for k in range(len(scen_interest)):
    opfile = open('input/IA_ops_'+scen_interest[k]+'.txt', 'w')
    opfile.close()

    for i in range(len(r_type)):
        lines_seen = set() # holds lines already seen
        scenfile = open('input/IA_'+scen_interest[k]+'_'+r_type[i]+'_scenarios.txt', 'r')
        outfile2 = open('input/IA_ops_'+scen_interest[k]+'.txt', 'a')

        for line in scenfile:
            line = line.split()

            if line[0][0:2] != 'SI':
                op_line = line[6][11:]+str('\n')
                if op_line not in lines_seen: # not a duplicate
                    outfile2.write(op_line)
                    lines_seen.add(op_line)
        scenfile.close()
        outfile2.close()

#########################################################################################
### Create operation files
#########################################################################################
amndsT  = ['swine','cattle','poultry','fert','mixed']
amndsF  = [0.80,0.60,0.500,1.0,0.5]  # fall fraction
amndsS  = [0.20,0.40,0.500,1.0,0.5]  # spring fraction
amndsN  = [0.32,0.32,0.375,1.0,0.4]  # Nitrogen available fraction
amndsA  = [0.056,0.001,0.022,0.75,0] # Ammonia fraction
amndsNO = [0,0,0,0.25,0]             # NO3 fraction
amndsO  = [0.022,0.016,0.024,0,1] # Organic N fraction
amndsP  = [0.026,0.007,0.030,0,1] # P fraction
newApp  = 0
TNdef   = 0.078 # total nitrogen in swine manure, swine reference value
def editFile(rotfile,newfile,amends,perm):
    for i in range(nrow):

        # if application or year need to be changed
        #if A[i] == amends or perm != 1:
        nf = str(newfile)
        try:
            outfile = open('input/operations/'+rotfile,'r')
            newfile = newfile.split('_')
            ofile = outfile.read()
            ofile = ofile.split('\n\n')
            text = ''
            newline = ''
            for op in range(len(ofile)):
                ofile[op] = ofile[op].strip()

                # If year needs permutation (e.g. CCS vs CSC)
                if 'YEAR' in ofile[op] and perm!= 1:
                    row = ofile[op].split('\n')

                    for j in range(len(r_type)):
                            if rotfile[4:(4+len(r_type[j]))] == newfile[1][:-1]:
                                Yr_i = float(row[1].strip()[-1])
                                Yr_f = int( (Yr_i + perm - 1) % lenRot[j] )
                                if Yr_f == 0:
                                    Yr_f = lenRot[j]
                                row[1] = str(row[1][0:20])+str(Yr_f)

                            # recreate the operation text
                            ofile[op] = '\n'.join(row)

                # Remove tillage operations if not conventional tillage
                if 'CT' not in nf:
                   # print(nf)
                    # Reduced tillage case
                    if 'Antares_disk' in ofile[op]:
                        row = ofile[op].split('\n')
                        row[4] = row[4][:-3]
                        row[5] = row[5][:-5]+str('0')
                        row[6] = row[6][:-3]
                        ofile[op] = '\n'.join(row)

                    if 'NT' in nf:
                        #print(nf)
                    # No tillage case, but we want to keep mixing
                        if 'Chisel' in ofile[op] or 'chisel' in ofile[op]:
                            row = ofile[op].split('\n')
                            row[4] = row[4][:-3]
                            ofile[op] = '\n'.join(row)

                        if 'Cultivator' in ofile[op]or 'cultivator' in ofile[op]:
                            row = ofile[op].split('\n')
                            row[4] = row[4][:-3]
                            ofile[op] = '\n'.join(row)

                # Remove rye if no cover crop is planted
                if 'NCC' in nf:
                    if 'Rye' in ofile[op]:
                        ofile[op] = ''

                    if 'FORAGE_HARVEST' in ofile[op]:
                        ofile[op] = ''

                # if nutrient amendment isn't standard composition (swine or fertilizer is default)
                if A[i]==amends and (amends != 0.056 and amends != 0.75):

                    if 'FIXED_FERTILIZATION' in ofile[op] and 'UAN' not in ofile[op]:
                        row = ofile[op].split('\n')

                        for j in range(len(amndsT)):
                            if B[i] == amndsT[j]:

                                # change name of nutrient amendment
                                row[3] = str(row[3][0:20])+str(amndsT[j])+str(' source')

                        # change mass of manure
                        if '/' in row[4]:
                            app = float(row[4][20:24])

                            if '*' in row[4]:
                                frac = float(row[4].split("*")[-1])
                                if frac!= 0.8 and frac!=0.2:
                                    print('manure fraction error')
                            else:
                                frac = 1.0
                                newApp = 0

                            # frac=0.2 for spring manure, 0.8 means fall manure, else its fertilizer
                            if frac == 0.2:
                                for j in range(len(amndsT)):
                                    if B[i] == amndsT[j]:
                                        newApp = (app/frac*TNdef)/(A[i]+ON[i]+amndsNO[j]) * amndsS[j]
                                    else:
                                        newApp = (app/frac*TNdef)/(A[i]+ON[i]) * amndsS[4]

                            elif frac == 0.8:
                                for j in range(len(amndsT)):
                                    if B[i] == amndsT[j]:
                                        newApp = (app/frac*TNdef)/(A[i]+ON[i]+amndsNO[j]) * amndsF[j]
                                    else:
                                        newApp = (app/frac*TNdef)/(A[i]+ON[i]) * amndsF[4]

                            elif frac == 1.0:
                                for j in range(len(amndsT)):
                                    if B[i] == amndsT[j]:
                                        newApp = (app/frac*TNdef)/(A[i]+ON[i]+amndsNO[j])
                                    else:
                                        if newfile[1][:] == 'SG1' and amends == amndsA[3]:
                                            newApp = '67' # apply 60lbsN/ac of fertilizer
                                        else: newApp = (app/frac*TNdef)/(A[i]+ON[i])

                            else:
                                newApp = (app*TNdef)/(A[i]+ON[i])
                                print('manure fraction is undefined')

                            row[4] = str(row[4][0:20])+str(newApp)

                        # Change values for amendment composition
                        row[10] = str(row[10][0:20])+str(ON[i]) # N organic
                        row[12] = str(row[12][0:20])+str(A[i])  # NH4
                        row[14] = str(row[14][0:20])+str(TP[i]) # P organic

                        if amends==amndsA[3]:
                            row[8] = str(row[8][0:20])+str('0')        # C organic
                            row[13] = str(row[13][0:20])+str('0.25')   # NO3

                        # recreate the operation text
                        ofile[op] = '\n'.join(row)

            ofile = '\n\n'.join(ofile)

            if perm!=1:
                #print(nf)
                nfile = ofile.split('\n###\n')
                sfile = numpy.sort(nfile)
                ofile = '\n###\n'.join(sfile)

            newOpFile = open( 'input/operations/'+nf, "w" )
            newOpFile.write(ofile)
            newOpFile.close()
            return
        except FileNotFoundError:
            print('no op file')
            print('input/operations/'+rotfile)
            # outfile = open('input/operations/'+nf,"w")
            # outfile.close()
            quit()
            return

for j in range(len(scen_interest)):
    linefile = open('input/IA_ops_'+scen_interest[j][:]+'.txt', 'r')
    for line in linefile:
        #print(line)
        line = line.split('_')
        rotStr =''.join([i for i in line[1] if not i.isdigit()])

        for i in range(len(r_type)):
            if rotStr == r_type[i]:
                try:
                    amends = round(float(line[2][2:]),3)

                except ValueError:
                    amends = amndsA[3]
                    print(line[2][2:])
                    print(line[:])
                    print('amendment error')
                    quit()
                if amends == 0.75:
                    rotfile = 'ALD_'+r_type[i]+'1_NH0.75_CT_RYE_'+line[-1][:]
                    rotfile = rotfile.strip()
                else:
                    rotfile = 'ALD_'+r_type[i]+'1_NH0.056_CT_RYE_MAN'+line[-1][-11:]
                    rotfile = rotfile.strip()

                perm = int(line[1][len(r_type[i]):])
                newfile = ("_".join(line)).strip('\n')
                # print(newfile)
                # print(rotfile)
                # print()
                if newfile not in lines_seen and newfile != rotfile:
                    editFile(rotfile,newfile,amends,perm)
    linefile.close()
