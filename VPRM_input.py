import gdal
import numpy as np
import glob
import pandas as pd

DataDir = '/data0/dwei/VPRMdata/'  # input dir

##########################################################
#                                                        #
#                Read inputs data                        #
#                                                        #
##########################################################
# NLCD and ISA
ds_nlcd = gdal.Open(DataDir+'nlcd_epsg32618_cropped.tif')
ds_ipsa = gdal.Open(DataDir+'ipsa_epsg32618_cropped.tif')
NLCD_2D = ds_nlcd.GetRasterBand(1).ReadAsArray()
IPSA_2D = ds_ipsa.GetRasterBand(1).ReadAsArray()
NLCD    = NLCD_2D.reshape(np.size(NLCD_2D))   
IPSA    = IPSA_2D.reshape(np.size(IPSA_2D))
IPSA[IPSA==127] = 0.0      # 127 is the background value; assuming its zero
IPSA    = IPSA/100.0

# Coordinates X,Y (upper left conner of the pixel)
EVIDir    = "/data0/dwei/Landsat/2021/" 
EVITSfile = glob.glob(EVIDir+'TimeSeries/*')
EVITS     = pd.read_csv(EVITSfile[0])
X         = EVITS["X"]
Y         = EVITS["Y"]
X_2D = np.array(X).reshape(np.shape(NLCD_2D))
Y_2D = np.array(Y).reshape(np.shape(NLCD_2D))

# EVI and LSWI
EVI_df  = pd.read_csv(DataDir + 'EVI_all_intp_row2411760') 
LSWI_df = pd.read_csv(DataDir + 'LSWI_all_intp_row2411760') 
EVI     = EVI_df.iloc[:,1:].to_numpy()  # First column is the row index
LSWI    = LSWI_df.iloc[:,1:].to_numpy() # First column is the row index


##########################################################
#                                                        #
#               Secondary parameters                     #
#                                                        #
##########################################################
# EVImin,VImax: min and max for each pixel during the growing season
# LSWImax     : max for each pixel during the growing season
# EVIref      : EVI at a non-urban reference site 
# EVIref,min  : minimum of EVIref, a baseline leaf-off, woody biomass respiration

# Parameters
SOS = 80       # DOY of the start of growing season
EOS = 300      # DOY of the end of growing season
EVIref = 0.44  # 0.44 is yearly average for deciduous; 0.65 is the June-August average for deciduous forest
EVIrefmin = 0.18

# Calculation
EVImin  = np.nanmin(EVI[:,SOS:EOS], axis=1)
EVImax  = np.nanmax(EVI[:,SOS:EOS], axis=1)
LSWImax = np.nanmax(LSWI[:,SOS:EOS], axis=1)

