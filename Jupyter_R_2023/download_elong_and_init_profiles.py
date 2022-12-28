from sqlitedict import SqliteDict
import numpy as np
import pandas as pd
import subprocess 
from subprocess import call

def build_profile(infile, tr_id, tr_len, ambig=False):   
    profile = {}
    if tr_id in infile:
        minreadlen = 15
        maxreadlen = 150
        profile = {}
        try:
            unambig_trancounts = infile[tr_id]["unambig"]
        except:
            unambig_trancounts = {}
        try:
            ambig_trancounts = infile[tr_id]["ambig"]
        except:
            ambig_trancounts = {}    
        for readlen in unambig_trancounts:
            if readlen < minreadlen or readlen > maxreadlen:
                continue
            try:
                offset = offsets[readlen]
            except:
                offset = 15            
            for pos in unambig_trancounts[readlen]:
                count = unambig_trancounts[readlen][pos]
                offset_pos = pos + offset + 1 ##############??????????????????
                try:
                    profile[offset_pos]  += count # for each readlength we will add offseted count 
                except:
                    profile[offset_pos] = count                   
        if ambig == True:
            for readlen in ambig_trancounts:
                if readlen < minreadlen or readlen > maxreadlen:
                    continue
                try:
                    offset = offsets[readlen]
                except:
                    offset = 15
                for pos in ambig_trancounts[readlen]:
                    count = ambig_trancounts[readlen][pos]
                    offset_pos = pos + offset + 1 ###############????????????????????????
                    try:
                        profile[offset_pos]  += 0
                    except:
                        profile[offset_pos] = count                
        # add remaining positions = 0 counts 
        for position in range(1, tr_len+1):
            if position in profile:
                continue
            else:
                profile[position] = 0                
    else:
        profile=None        
    return profile

samples_dict = {'Park16': ["SRR3306583.sqlite", "SRR3306584.sqlite", "SRR3306585.sqlite", "SRR3306586.sqlite", "SRR3306587.sqlite", "SRR3306588.sqlite", "SRR3306589.sqlite"],
                'Liu13': ["SRR619082.sqlite", "SRR619083.sqlite", "SRR619084.sqlite", "SRR619085.sqlite", "SRR619086.sqlite", "SRR619087.sqlite", "SRR619088.sqlite", "SRR619089.sqlite", "SRR619090.sqlite", "SRR619091.sqlite", "SRR619092.sqlite", "SRR619093.sqlite", "SRR619094.sqlite", "SRR619095.sqlite", "SRR619096.sqlite", "SRR619097.sqlite", "SRR619098.sqlite", "SRR619099.sqlite", "SRR619100.sqlite"], 
                'Gameiro18':["SRR7207259.sqlite", "SRR7207260.sqlite", "SRR7207261.sqlite", "SRR7207262.sqlite", "SRR7207263.sqlite", "SRR7207264.sqlite", "SRR7207265.sqlite", "SRR7207266.sqlite", "SRR7207268.sqlite", "SRR7207269.sqlite", "SRR7207270.sqlite", "SRR7207271.sqlite", "SRR7207272.sqlite", "SRR7207273.sqlite", "SRR7207274.sqlite", "SRR7207275.sqlite", "SRR7207276.sqlite", "SRR7207277.sqlite", "SRR7207278.sqlite", "SRR7207279.sqlite", "SRR7207280.sqlite", "SRR7207281.sqlite", "SRR7207282.sqlite", "SRR7207283.sqlite", "SRR7207284.sqlite"],
                 'Werner15': ["SRR1610244.sqlite", "SRR1610245.sqlite", "SRR1610246.sqlite", "SRR1610247.sqlite", "SRR1610248.sqlite", "SRR1610249.sqlite", "SRR1610250.sqlite", "SRR1610251.sqlite", "SRR1610252.sqlite", "SRR1610253.sqlite", "SRR1610254.sqlite", "SRR1610255.sqlite", "SRR1610256.sqlite", "SRR1610257.sqlite", "SRR1610258.sqlite", "SRR1610259.sqlite", "SRR2086025.sqlite", "SRR2086026.sqlite", "SRR2086027.sqlite", "SRR2086028.sqlite", "SRR2086029.sqlite", "SRR2086030.sqlite", "SRR2086031.sqlite"],
                'Goodarzi16':["SRR3129148.sqlite", "SRR3129153.sqlite", "SRR3129940.sqlite", "SRR3130941.sqlite", "SRR3131003.sqlite", "SRR3131008.sqlite", "SRR3131015.sqlite", "SRR3131021.sqlite", "SRR3129149.sqlite", "SRR3129936.sqlite", "SRR3129941.sqlite", "SRR3130944.sqlite", "SRR3131004.sqlite", "SRR3131011.sqlite", "SRR3131016.sqlite", "SRR3131023.sqlite", "SRR3129152.sqlite", "SRR3129937.sqlite", "SRR3130940.sqlite", "SRR3130945.sqlite", "SRR3131007.sqlite", "SRR3131012.sqlite", "SRR3131019.sqlite", "SRR3131025.sqlite"],
                'Calviello16': ['SRR2433794.sqlite'], 
                'Guo14':['SRR1598971.sqlite', 'SRR1598975.sqlite', 'SRR1598981.sqlite'],
                'Iwasaki19': ["SRR5937640.sqlite", " SRR5937643.sqlite", "SRR5937641.sqlite", "SRR5937644.sqlite", "SRR5937642.sqlite", "SRR5937645.sqlite"],
                'Zhang17':['SRR5227449.sqlite', 'SRR5227448.sqlite'],
                'Xu16':["SRR403883.sqlite", "SRR403889.sqlite", "SRR403885.sqlite", "SRR403891.sqlite", "SRR403887.sqlite", "SRR403893.sqlite"], 
                "Hsieh12":["SRR403883.sqlite", "SRR403889.sqlite", "SRR403885.sqlite", "SRR403891.sqlite", "SRR403887.sqlite", "SRR403893.sqlite"],
                "Wolfe14":["SRR1248252.sqlite", "SRR1248255.sqlite", "SRR1248253.sqlite", "SRR1248254.sqlite"],
                'Lauria18':['SRR6838651.sqlite'], 
                'Iwasaki16':["SRR2075925.sqlite", "SRR2075928.sqlite", "SRR2075936.sqlite", "SRR2075939.sqlite", "SRR2075926.sqlite", "SRR2075929.sqlite", "SRR2075937.sqlite", "SRR2075927.sqlite", "SRR2075935.sqlite", "SRR2075938.sqlite"], 
                'Ji16':['SRR1802129.sqlite", " SRR1802132.sqlite", " SRR1802138.sqlite", " SRR1802141.sqlite", "SRR1802147.sqlite", "SRR1802153.sqlite", "SRR1802130.sqlite", "SRR1802139.sqlite", "SRR1802142.sqlite", "SRR1802148.sqlite", "SRR1802154.sqlite", "SRR1802131.sqlite", "SRR1802137.sqlite", "SRR1802140.sqlite", "SRR1802146.sqlite", "SRR1802152.sqlite'], 
                'Crappe15': ['SRR1333393.sqlite'], 
                'Fijalkowska17':['SRR4293696.sqlite', 'SRR4293694.sqlite']  
                }

samples_dict_init = {
    'Fijalkowska17':['SRR4293695.sqlite', 'SRR4293693.sqlite'], 
    'Crappe15':['SRR1333394.sqlite'], 
    'Ji16':["SRR1802135.sqlite", "SRR1802150.sqlite", "SRR1802156.sqlite", "SRR1802133.sqlite", "SRR1802136.sqlite", "SRR1802151.sqlite", "SRR1802157.sqlite", "SRR1802134.sqlite", "SRR1802149.sqlite", "SRR1802155.sqlite"], 
    'Zhang17':['SRR6327777.sqlite'], 
    'Gawron16':['SRR2732970.sqlite'],
    'Chen20':['SRR9113062.sqlite', 'SRR9113063.sqlite']
}

            
    
#############################################################
################## CREATE RIBO-SEQ PROFILES #################
#############################################################

print ('start ELONG Ribo-seq profile sqlites')
f = open('ribofiles_elong_opened.txt', 'w')

infile_d = {}

for study, samples in samples_dict.items():
    print ('attempt to open samples %s from a study %s' % (study, samples))
    
    if study not in infile_d:
        infile_d[study] = {}
        
    for sample in samples:
        print ('attempt to find sample %s' % sample)
        try:
            infile = SqliteDict('/home/DATA/www/tripsviz/tripsviz/uploads/%s/%s' % (study, sample) )
            infile_d[study][sample] = infile
        except: 
            infile = SqliteDict('/home/DATA/www/tripsviz/tripsviz/trips_shelves/riboseq/homo_sapiens/%s/%s' % (study, sample))
            infile_d[study][sample] = infile
        
print ('number of studies opened: ', len(list(infile_d.keys())))


# use only transcripts with 5'UTRs 
metadata_pc_g25_5utr = pd.read_csv('10k_RiboSET.txt', sep='\t')
dict_of_transcripts = dict(zip(metadata_pc_g25_5utr.tr_id.tolist(), metadata_pc_g25_5utr.tr_len.tolist()))

i = 0

for tr_id1, tr_len in dict_of_transcripts.items():
    tr_id = tr_id1.split('.')[0]
    print ('transcript %s is being processed; %s' %(tr_id, i))
    list_of_profiles = []
    d = {}
    # get a transcript profile per sample per study in a dtaframe format 
    for study, samples_infiles in infile_d.items(): 
        for sample, infile in samples_infiles.items():
            if tr_id not in infile:
                continue
            else:
                profile = build_profile(infile, tr_id, tr_len, ambig=False) 
                list_of_profiles.append(profile)
                #df.to_csv("profiles_sample_study/profile_%s_%s_%s.txt" % (tr_id, study, sample), sep='\t', index=False)
    if len(list_of_profiles) != 0:    
        for profile_ in list_of_profiles:
            for pos, count in profile_.items():
                if pos not in d:
                    d[pos] = count
                else:
                    d[pos] += count 
        df = pd.DataFrame(d.items())
        df.columns = ['Position', 'Count']
        df.to_csv('/home/DATA2/alla/SOLE_nonAUG/ELONG_PROFILES/%s.txt' % tr_id, sep='\t', index=False)
    
    i += 1


f.close()
                                

print ('start INIT Ribo-seq profile sqlites')
f = open('ribofiles_init_opened.txt', 'w')

infile_d = {}

for study, samples in samples_dict_init.items():
    print ('attempt to open samples %s from a study %s' % (study, samples))
    
    if study not in infile_d:
        infile_d[study] = {}
        
    for sample in samples:
        print ('attempt to find sample %s' % sample)
        try:
            infile = SqliteDict('/home/DATA/www/tripsviz/tripsviz/uploads/%s/%s' % (study, sample) )
            infile_d[study][sample] = infile
        except: 
            infile = SqliteDict('/home/DATA/www/tripsviz/tripsviz/trips_shelves/riboseq/homo_sapiens/%s/%s' % (study, sample))
            infile_d[study][sample] = infile
        
print ('number of studies opened: ', len(list(infile_d.keys())))


# use only transcripts with 5'UTRs 
metadata_pc_g25_5utr = pd.read_csv('10k_RiboSET.txt', sep='\t')
dict_of_transcripts = dict(zip(metadata_pc_g25_5utr.tr_id.tolist(), metadata_pc_g25_5utr.tr_len.tolist()))

i = 0

for tr_id1, tr_len in dict_of_transcripts.items():
    tr_id = tr_id1.split('.')[0]
    print ('transcript %s is being processed; %s' %(tr_id, i))
    list_of_profiles = []
    d = {}
    # get a transcript profile per sample per study in a dtaframe format 
    for study, samples_infiles in infile_d.items(): 
        for sample, infile in samples_infiles.items():
            if tr_id not in infile:
                continue
            else:
                profile = build_profile(infile, tr_id, tr_len, ambig=False) 
                list_of_profiles.append(profile)
                #df.to_csv("profiles_sample_study/profile_%s_%s_%s.txt" % (tr_id, study, sample), sep='\t', index=False)
    if len(list_of_profiles) != 0:    
        for profile_ in list_of_profiles:
            for pos, count in profile_.items():
                if pos not in d:
                    d[pos] = count
                else:
                    d[pos] += count 
        df = pd.DataFrame(d.items())
        df.columns = ['Position', 'Count']
        df.to_csv('/home/DATA2/alla/SOLE_nonAUG/INIT_PROFILES/%s.txt' % tr_id, sep='\t', index=False)
    
    i += 1


f.close()




             
                
 