from osgeo import ogr
from osgeo import osr  
import numpy as np
from netCDF4 import Dataset 

def Read_VPRMout(filepath):
    nc_fid = Dataset(filepath, 'r')  
    #nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)
    GEE    = nc_fid.variables['GEE'][:,:,:]  # GEE   [mol m^-2 hr^-1']
    Res_H  = nc_fid.variables['RESH'][:,:,:] # Res_H [mol m^-2 hr^-1']
    Res_A  = nc_fid.variables['RESA'][:,:,:] # Res_A [mol m^-2 hr^-1']
    time   = nc_fid.variables['time'][:]
    Xdim   = nc_fid.variables['Xdim'][:] 
    Ydim   = nc_fid.variables['Ydim'][:] 
    Res_t  = Res_H + Res_A
    NEE    = GEE+Res_t
    TMP    = nc_fid.variables['TEMP'][:,:,:] 
    PAR    = nc_fid.variables['PAR'][:,:,:] 
    nc_fid.close()
    return GEE, Res_H, Res_A, NEE, time, Xdim, Ydim, TMP

def get_first_dimension_ave(arr_3D):
    ss = np.zeros(np.shape(arr_3D[0,:,:]))
    for i in range(0, np.shape(arr_3D)[0]):  
        ss=ss+arr_3D[i,:,:]
    return ss/np.shape(arr_3D)[0]

def latlon_to_EPSG32618(latlon_lst):
    # Convert lat,lon to projected meters
    # Spatial Reference System
    inputEPSG = 4326
    outputEPSG = 32618

    # create a geometry from coordinates
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(latlon_lst[0], latlon_lst[1])

    # create coordinate transformation
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(inputEPSG)

    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(outputEPSG)

    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    # transform point
    point.Transform(coordTransform)

    # print point in EPSG 32618
    x = point.GetX()
    y = point.GetY()   
    return x, y

def EPSG32618_to_latlon(coords):
    # Convert projection to lat,lon
    # Spatial Reference System
    inputEPSG = 32618 
    outputEPSG = 4326

    # create a geometry from coordinates
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(coords[0], coords[1])

    # create coordinate transformation
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(inputEPSG)

    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(outputEPSG)

    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    # transform point
    point.Transform(coordTransform)

    # print point in lat, lon
    x = point.GetX()
    y = point.GetY()   
    return x, y

def find_a_point_in_grids(x, y, Xdim, Ydim):

    X_2D, Y_2D  = np.meshgrid(Xdim, Ydim)
    X_1D = X_2D.reshape(np.size(Y_2D))
    Y_1D = Y_2D.reshape(np.size(Y_2D))

    Pixel = [X<x<=X+30.0 and Y-30.0<y<=Y for X,Y in zip(X_1D, Y_1D)]
    the_ind = Pixel.index(True)
    x_ind = np.where(Xdim==X_1D[the_ind])
    y_ind = np.where(Ydim==Y_1D[the_ind])
    
    return x_ind[0],y_ind[0]

# # Get the center lat and lon of each small pixel
# Xdim_nyc, Ydim_nyc = np.meshgrid(Xdim, Ydim) 
# print(np.shape(Xdim_nyc)) # corresponds to Lon  
# print(np.shape(Ydim_nyc)) # corresponds to Lat  
# Xdim_1D = Xdim_nyc.reshape(np.size(Xdim_nyc))
# Ydim_1D = Ydim_nyc.reshape(np.size(Ydim_nyc))
# print(np.shape(Xdim_1D),np.shape(Ydim_1D))

# res = 30
# center_latlon = [EPSG32618_to_latlon([x+res/2.0, y-res/2.0])for x,y in zip(Xdim_1D,Ydim_1D)]
# center_lat = np.array([x for x,y in center_latlon])
# center_lon = np.array([y for x,y in center_latlon])

# # To create a dataframe with time, coordinates (X, Y), and EVI   
# Data = pd.DataFrame({"Center_lat":center_lat, "Center_lon":center_lon})
# Data.to_csv('/data0/dwei/VPRMout/NYC_domain_center_latlon')
# print(Data.head())
