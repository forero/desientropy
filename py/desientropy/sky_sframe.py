import desientropy.compute
import fitsio
import glob
import numpy as np
import pandas as pd

def list_exps(release,date):
    exps_daily = pd.read_csv("/global/cfs/cdirs/desi/spectro/redux/{}/exposures-{}.csv".format(release, release))
    ii = (exps_daily["NIGHT"]==date)
    exps_daily = exps_daily[ii]
    return exps_daily
    
def read_sky_sframe(sframe_file):
    try:
        h = fitsio.FITS(sframe_file)
        sel = h["FIBERMAP"]["OBJTYPE"].read() == "SKY"
        sky = h["FLUX"].read()[sel,:]
    except:
        sky = None
    return sky

def summary_entropy_expid(release, date, expid, program, survey):
    n_petals = 10
    bands = ['b', 'r', 'z']
    summary = {}
    summary['BAND'] = []
    summary['PETAL'] = []
    summary['H'] = []
    summary['EXPID'] = []
    summary['NIGHT'] = []
    summary['PROGRAM'] = []
    summary['SURVEY'] = []
    release_path = '/global/cfs/cdirs/desi/spectro/redux/{}/exposures/'.format(release)
    for i in range(n_petals):
        for band in bands:
            filename = '{}/{}/{:08d}/sframe-{}{}-{:08d}.fits'.format(release_path, date, expid, band, i, expid)
            sky_petal = read_sky_sframe(filename)
            if sky_petal is not None:
                entropy =  desientropy.compute.entropy_2d(sky_petal)
                summary['BAND'].append(band)
                summary['PETAL'].append(i)
                summary['H'].append(entropy)
                summary['EXPID'].append(expid)
                summary['NIGHT'].append(date)
                summary['PROGRAM'].append(program)
                summary['SURVEY'].append(survey)
                print(date, expid, band, i, entropy, program, survey)
    entropy_df = pd.DataFrame.from_dict(summary)
    filename = 'entropy_sky_sframe_{}_{:08d}.csv'.format(date, expid)
    
    #os.makedirs(output_path, exist_ok=True) 
    entropy_df.to_csv(filename)
    return 
    #print(summary)
    
def summary_entropy_night(release, date):
    exps_night = list_exps(release, date)
    n = len(exps_night)
    for i in range(n):
        summary_entropy_expid(release, date, 
                              exps_night['EXPID'].iloc[i], 
                              exps_night['PROGRAM'].iloc[i],
                              exps_night['SURVEY'].iloc[i])
    
