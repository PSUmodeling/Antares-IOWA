#scen_interest = ['C_CT_RYE_NF','C_RT_RYE_NPS']
# data = open("CT_NCC_NF_30RH.csv") 

#### Potential Antares / EFC CSV files (ald_fname)
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
                 
#ald_fname = 'PSU_CT_00RH_NCC_NF.csv' # This will create a reference scenario                 
ald_fname = 'PSU_CT_00RH_NCC_NF.csv'
data = open(ald_fname) 
wfile_name = ald_fname[0:-4]+'_cycles.csv'

ald_fname = ald_fname.split('_')
scen = ald_fname[1]+'_'+ald_fname[3]+'_'+ald_fname[4]+'_'+ald_fname[2]
ald_fname = '_'.join(ald_fname)

# create multimode files
r_type =['C','CS','CCS','S',]
lenRot  =[1,1,2,1]

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
onc= -1  # organic nitrogen id
tpc= -1  # total phosphorus id 
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

for i in range(nrow):
    SOC = [] # delta soil organic carbon
    NO3 = [] # nitrate leached
    Vol = [] # volatilized
    N2O = [] # N2O denitrification
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
    
    ctrl_file = 'W'+WC[i]+'_'+crop[i]+P[i]+'_'+S[i]+'_'+scen 
    n_path = 'output/'+ctrl_file+'/annualN.dat'
    y_path = 'output/'+ctrl_file+'/season.dat'
    s_path = 'output/'+ctrl_file+'/summary.dat'
    try:
        #print(n_path)
        cycOut = open(n_path)
        nums = []
        for rownum, row in enumerate(cycOut):
            if rownum > 1 and float(row[0:4])>= 2013:
                #print(C[i])
                nums_str = row.split()
                nums = [float(n.strip()) for n in nums_str]
                NO3.append(round(nums[4]+nums[6],3))
                N2O.append(round(nums[11],3))
                Vol.append(round(nums[10],3))
        cycOut.close()  
        nOut.append(','+str(NO3)[1:-1]+','+str(N2O)[1:-1]+','+str(Vol)[1:-1])
        
        cycOut = open(y_path)
        crpOld = ''
        yldOld = ''
        yrOld = ''
        Yld = [] # Annual yield
        Crp = [] # Crops harvested each year
        for rownum, row in enumerate(cycOut):
            if rownum > 1 and float(row[0:4])>= 2013:
                row = row.split()
                
                # Harvest may be grain or forage
                if float(row[5]) > 0:
                    yld = round(float(row[5]),3)
                else: yld = round(float(row[6]),3)
                
                crp = row[1][0:3]
                # There may be multiple harvests in 1 year
                # If this is not the first harvest of the year:
                if yrOld == row[0][0:4]:
                    yld = str(yldOld)+'|'+str(yld)
                    crp = crpOld+'|'+crp
                    
                # if the last crop isn't the same as this year, AND it's not the first year:    
                elif yldOld !='': 
                    Yld.append(yldOld)
                    Crp.append(crpOld)
                    
                #elif yldOld !='': 
                    #pass
                
                #else:
                    #Yld.append(yld)
                    #Crp.append(crp)
                    
                yrOld = row[0][0:4]
                crpOld= crp
                yldOld= yld
                
        # Take care of the last row of data     
        Yld.append(yld)
        Crp.append(crp)

        cycOut.close()  
        yOut.append(','+str(Crp)[1:-1]+','+str(Yld)[1:-1]+',')
        cycOut = open(s_path)
        for rownum,row in enumerate(cycOut):
            if rownum == 2:
                row = row.split()
                # change in soil C over the simulation
                # for default scenario, 1980-2016
                # for alternative scenarios, 2013-2016
                delta_C.append(round(float(row[2]),3))
        cycOut.close()                
                
    except FileNotFoundError:
        nOut.append(',NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA')
        yOut.append(',NA,NA,NA,NA,NA,NA,NA,NA,')
        delta_C.append('NA')
data.close()

frstrun=True
newdata=''
updated = ''
add0n=' '
wfile = open(ald_fname)
for j,row in enumerate(wfile):
    row = [r.strip() for r in row.split(',')]
    i = j-1
    if frstrun:
        frstrun=False
        updated = ",".join(row)+str(',NO3_13, NO3_14, NO3_15, NO3_16, N2O_13, N2O_14, N2O_15, N2O_16, Vol_13, Vol_14, Vol_15, Vol_16 \
, Crops13, Crops14, Crops15, Crops16, Yield13, Yield14, Yield15, Yield16, soilC_delta \n')
    else:
        updated = ",".join(row)+nOut[i]+yOut[i]+str(delta_C[i])+str('\n')

    newdata+=updated
wfile.close()    
data2 = open(wfile_name,"w") 
data2.write(newdata)   
data2.close()
#########################################################################################
