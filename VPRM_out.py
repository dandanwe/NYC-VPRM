from netCDF4 import Dataset 
import numpy as np
import datetime

##########################################################
#                                                        #
#                  Output set up                         #
#                                                        #
##########################################################
OutDir  = '/data0/dwei/VPRMout/'   # output dir
Domname = 'test'

try: ncfile.close()  # just to be safe, make sure dataset is not already open.
except: pass

str_today = datetime.datetime.strftime(datetime.date.today(), '%Y%m%d') # string type
outfile = OutDir+Domname+'_'+str_today+'.nc'

# Opening a file, creating a new Dataset
ncfile = Dataset(outfile,mode='w',format='NETCDF4') 

# Creating dimensions
x_dim = ncfile.createDimension('Xdim', np.shape(NLCD_2D)[1])      # cols, equivalent to lon 
y_dim = ncfile.createDimension('Ydim', np.shape(NLCD_2D)[0])      # rows, equivalent to lat
time_dim = ncfile.createDimension('time', None) # unlimited axis (can be appended to).
#for dim in ncfile.dimensions.items():
#   print(dim)

# Creating attributes
#ncfile.title='NYC domain 2021'
#print(ncfile.title)

# Creating variables
# Define two variables with the same names as dimensions,
# a conventional way to define "coordinate variables".
x = ncfile.createVariable('Xdim', np.float32, ('Xdim',))
x.units = 'meter'
x.long_name = 'Projected meters east-west'

y = ncfile.createVariable('Ydim', np.float32, ('Ydim',))
y.units = 'meter'
y.long_name = 'Projected meters north-south'

time = ncfile.createVariable('time', np.float64, ('time',))
time.units = 'seconds since 00:00:00 UTC on 1 January 1970'
time.long_name = 'seconds since 00:00:00 UTC on 1 January 1970'
#print(time)

# Define a 3D variable to hold the data
GEE = ncfile.createVariable('GEE',np.float64,('time','Ydim','Xdim')) # note: unlimited dimension is leftmost
GEE.units = '\u03BCmoles m-2 s-1'
GEE.standard_name = 'Gross Ecosystem Exchange'

RES_H = ncfile.createVariable('RESH',np.float64,('time','Ydim','Xdim')) # note: unlimited dimension is leftmost
RES_H.units = '\u03BCmoles m-2 s-1'
RES_H.standard_name = 'Heterotrophic respiration'

RES_A = ncfile.createVariable('RESA',np.float64,('time','Ydim','Xdim')) # note: unlimited dimension is leftmost
RES_A.units = '\u03BCmoles m-2 s-1'
RES_A.standard_name = 'autotrophic respiration'

# ncfile= create_vprm_output('test3', np.shape(NLCD_2D)[1], np.shape(NLCD_2D)[0], X_cord[0,:], Y_cord[:,0])   
#print(ncfile)
#print('------------- nc file created --------------')