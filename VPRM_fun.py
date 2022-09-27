import gdal
import numpy as np
import glob
import datetime
import pytz
from scipy import interpolate
from VPRM_params import xnew,delT_day,delT_nig,x_pt, y_pt # for get_UHI_deltT
from VPRM_input import NLCD_2D


def get_UHI_deltT(): 
    tck = interpolate.splrep(x_pt, y_pt, s=0)  
    ynew= interpolate.splev(xnew, tck, der=0) # The increase in temperature 
    return ynew

def get_Wscale(LSWI, LSWImax):
    '''LSWImax is the maximum for a given pixel during the growing season'''
    Wscale=(1+LSWI)/(1+LSWImax)
    return simpleQA_0_1(Wscale)


def get_Pscale(EVI, EVImin, EVImax):
    '''EVImin and EVImax are the minimum and maximum observed EVI 
       for each pixel during the growing season'''
    Pscale=(EVI-EVImin)/(EVImax-EVImin)
    return simpleQA_0_1(Pscale)


def get_Tscale(T, Tmin, Tmax):
    '''This function calculates Tscale 
       All temperatures are in Celsius
       
       Tmin is the minimum temperature for photosynthesis (0°C)
       Tmax is the maximum temperature for photosynthesis (40°C)
    '''
    LowerBound = 20.0
    UpperBound = 30.0
    tmp_1 = (T-Tmin)*(T-Tmax)
    
    if T<LowerBound:
        Tscale=tmp_1/(tmp_1-(T-LowerBound)**2)
    elif LowerBound<=T<=UpperBound:
        Tscale=1.0
    elif T>UpperBound:
        Tscale=tmp_1/(tmp_1-(T-UpperBound)**2)
    return Tscale

def get_RES_tot(Tair, Tlow, alpha, beta, ISA, EVI, EVIref, EVIrefmin):
    '''R_e: Ecosystem Resporation
       Tair is in Celsius'''
    Tair[Tair<Tlow] = Tlow   # account for winter soil respiration
    RES_e = Tair*alpha+beta
    RES_H = (1-ISA)*RES_e*0.5
    EVI_s = EVI/EVIref
    EVI_s[EVI_s>1.0] = 1.0
    EVI_s[EVI_s<0.0] = 0.0
    RES_A = EVI_s*RES_e*0.5
    return RES_H, RES_A, RES_H+RES_A

def get_GEE(lmbda,Tscale,Pscale,Wscale,EVI,PAR,PAR_0):
    '''This function calculates GEE
       Because lambda is a build-in function in Python,
       lmbda is used here to denote the parameter lambda in VPRM
    '''    
    return -1.0*lmbda*Tscale*Pscale*Wscale*EVI*PAR/(1+PAR/PAR_0)

def simpleQA_0_1(value):
    '''This simple function makes sure scalors are between 0-1'''
    value[value<0.0]=0.0
    value[value>1.0]=1.0      
    return value

def et_to_utc(dt_et):
    utc = pytz.timezone('UTC')
    est = pytz.timezone('US/Eastern')   
    outputfmt  = '%Y-%m-%d %H:%M:%S'
    dt_utc = est.localize(dt_et).astimezone(utc) #.strftime(outputfmt)
    return dt_utc

def get_HRRR_arr(dt_utc, band, NYC_bbox):
    '''dt is the Datetime format, band is a string'''
    
    # find the HRRR file
    HRRRDir    = '/data0/dwei/HRRR/2021/'
    fmt_met = '%Y%m%d'
    date_str=datetime.datetime.strftime(dt_utc, fmt_met)
    hr_str = str(dt_utc.hour).zfill(2)
    HRRRfolder = HRRRDir+'hrrr'+date_str+'/'
    filename = glob.glob(HRRRfolder+'*t'+hr_str+'*'+band+'*')
    
    if filename:   
        # resample to 30m resolution 
        xres=30.0
        yres=30.0
        resample_alg = 'near'
        bbox=NYC_bbox

        ds_in  = gdal.Open(filename[0])
        OutDir = '/data0/dwei/VPRMdata/HRRR/'
        Outfile= OutDir+date_str+'_t'+hr_str+'_B'+band+'.tif'
        ds_out = gdal.Warp(Outfile, ds_in, \
                xRes=xres, yRes=yres, resampleAlg=resample_alg,\
                outputBounds=bbox)
        arr2D_return = ds_out.GetRasterBand(1).ReadAsArray()
    else:
        print('No such file', filename)
        arr2D_return = np.empty(np.shape(NLCD_2D))
        arr2D_return[:] = np.nan
    return arr2D_return

