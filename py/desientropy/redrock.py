import desientropy.compute
import pandas as pd
import numpy as np
import os
import glob
import fitsio

def summary_tile_entropy(release_path, tile_id):
    n_gal_list = []
    n_star_list = []
    n_qso_list = []
    n_good_z_list = []
    z_entropy = []
    petal_list = [] 
    for petal_id in range(10):
        search_path = "{}/tiles/cumulative/{}/*/redrock-*-{}-thru*.fits".format(release_path, tile_id, tile_id)
        #print(search_path)
        try:
            file_in = glob.glob(search_path)[0]
            #print(file_in)
            #print(file_in.split('/')[-1].split('-')[-3])
            this_petal_id = file_in.split('/')[-1].split('-')[-3]
            tile_file = file_in.replace("redrock-{}".format(this_petal_id), "redrock-{}".format(petal_id))
            #tile_file = "{}/tiles/cumulative/{}/{}/redrock-{}-{}-thru{}.fits".format(
            #    fuji_path, tile_id, last_night, petal_id, tile_id, last_night)
            print(tile_file)
            try:
                z_tile_per_exp = fitsio.read(tile_file, ext="REDSHIFTS")
                fmap_tile_per_exp = fitsio.read(tile_file, ext="FIBERMAP")
                exp_fmap_tile_per_exp = fitsio.read(tile_file, ext="EXP_FIBERMAP")
            except:
                pass
            try:
                ii = (z_tile_per_exp['ZWARN']==0) #& (exp_fmap_tile_per_exp['FIBERSTATUS']==0)
                n_good_z = np.count_nonzero(ii)
                h = desientropy.compute.entropy_1d(z_tile_per_exp['Z'][ii])
                n_gal = np.count_nonzero(z_tile_per_exp['SPECTYPE'][ii]=='GALAXY')
                n_star = np.count_nonzero(z_tile_per_exp['SPECTYPE'][ii]=='STAR')
                n_qso = np.count_nonzero(z_tile_per_exp['SPECTYPE'][ii]=='QSO')
        
                petal_list.append(petal_id)
                z_entropy.append(h)
                n_gal_list.append(n_gal)
                n_star_list.append(n_star)
                n_qso_list.append(n_qso)
                n_good_z_list.append(n_good_z)
            except:
                pass
        except:
            pass
    return {'petal_id':petal_list, 'z_entropy':z_entropy, 'n_gal':n_gal_list, 'n_star':n_star_list, 'n_qso':n_qso_list, 
           'n_good_z':n_good_z_list}


def summary_release_entropy(release, n_tiles_max=None, lastnight=None):
    release_path = "/global/cfs/cdirs/desi/spectro/redux/{}/".format(release)
    data_tiles_release = pd.read_csv(os.path.join(release_path, "tiles-{}.csv".format(release)))
    
    if lastnight is not None:
        print('Selecting tiles for lastnight:'.format(lastnight))
        ii = data_tiles_release['LASTNIGHT']==lastnight
        data_tiles_release = data_tiles_release[ii]
    
    n_tiles = len(data_tiles_release)
    print('Release {} has {} tiles'.format(release, n_tiles))
    
    if n_tiles==0:
        return 
    
    #return data_tiles_release
    
    filename = 'summary_rr_entropy_{}.csv'.format(release)
    if lastnight is not None:
        filename = 'summary_rr_entropy_{}_{}.csv'.format(release,lastnight)
    print(filename)
    out = open(filename, 'w')
    h = 'TILEID,PROGRAM,SURVEY,LASTNIGHT,PETALID,H,N_GAL,N_STAR,N_QSO,N_GOOD_Z\n'
    out.write(h)
    out.close()
    
    if n_tiles_max is None:
        n_max = n_tiles
    else:
        n_max = n_tiles_max
        
    for i in range(n_max):
        print('computing {} over {}. tileid {}'.format(i+1, n_max, data_tiles_release['TILEID'].iloc[i]))
        a = summary_tile_entropy(release_path, data_tiles_release['TILEID'].iloc[i])
        if len(a['petal_id']):
            n_p = len(a['petal_id'])
            for j in range(n_p):
                s = '{},{},{},{},{},{},{},{},{},{}\n'.format(data_tiles_release['TILEID'].iloc[i], 
                                                    data_tiles_release['FAPRGRM'].iloc[i],
                                                    data_tiles_release['SURVEY'].iloc[i],
                                                    data_tiles_release['LASTNIGHT'].iloc[i],
                                                 a['petal_id'][j],a['z_entropy'][j],
                                     a['n_gal'][j], a['n_star'][j], a['n_qso'][j], a['n_good_z'][j])
                out = open(filename, 'a')
                out.write(s)
                out.close()
    return

