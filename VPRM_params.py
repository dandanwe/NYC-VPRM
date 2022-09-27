##########################################################
#                                                        #
#                   Domain information                   #
#                                                        #
##########################################################
# EPSG:32618
bbox=[563086.4981809029, 4483346.578300821, 609468.3374729961, 4530140.279354534]
# lat,lon
ul = (40.91994359299865, -74.25078580367983)
ll = (40.498429317593086, -74.25549540873544)
ur = (40.915050108690444, -73.70006247106176)
lr = (40.493607634923094, -73.70823210074099)
Domname = 'DEVasGRS_2021_apr_oct'

##########################################################
#                                                        #
#                   Urban heat island                    #
#                                                        #
##########################################################
xnew = range(0, 24) # can be used as hour or index 
delT_day = 4.0   
delT_nig = 2.0 
x_pt = [0, 6, 12, 20, 23]  # start hour, sunrise, max, sunset, end hour
y_pt = [delT_nig, delT_nig, delT_day, delT_nig*1.333, delT_nig]  

##########################################################
#                                                        #
#          Land cover and parameters                     #
#                                                        #
##########################################################
# ENF: Evergreen forest
# DBF: Deciduous forest
# MXF: Mixed forest
# SHB: Shrub
# CRP: Crop
# GRS: Grassland
# WET: Woody wetland
# OTH: 0 fluxes (here used for water)
# DEVL: Developed, low intensity or open space
# DEVM: Developed, medium intensity
# DEVH: Developed, high intensity
LC_types    = ["EVF", "DBF", "MXF", "SHB", "CRP", "GRS", "WET",\
               "DEO", "DEL", "DEM", "DEH", "BRL", "OTH"]

# Define parameters (Winbourne et al. 2021)
# Tmin, Topt, Tmax, Tlow, PAR_0, lambda, alpha, beta
# Harvard forest (Mahadevan et al. 2008) VPRM_DBF= (0, 20, 40, 5, 570, 0.127, 0.271, 0.25)   
# Duke forest (Winbourne et al. 2021)    VPRM_DBF= (0, 30, 40, 5, 863, 0.09355, 0.1379, 1.09)
EVF= (0, 20, 40, 1, 446, 0.128, 0.250, 0.17)  # 0, 20, 40, 1, 446, 0.128, 0.250, 0.17
DBF= (0, 20, 40, 5, 570, 0.127, 0.271, 0.25)  # 0, 30, 40, 5, 863, 0.09355, 0.1379, 1.09
MXF= (0, 20, 40, 2, 629, 0.123, 0.244, -0.24) # 0, 20, 40, 2, 629, 0.123, 0.244, -0.24
SHB= (2, 20, 40, 1, 321, 0.122, 0.028, 0.48)  # 2, 20, 40, 1, 321, 0.122, 0.028, 0.48
CRP= (5, 22, 40, 2, 1250, 0.075, 0.173, 0.82) # 5, 22, 40, 2, 1250, 0.075, 0.173, 0.82
GRS= (2, 18, 40, 1, 542, 0.213, 0.028, 0.72)  # 2, 18, 40, 1, 542, 0.213, 0.028, 0.72
WET= (0, 20, 40, 3, 558, 0.051, 0.081, 0.24)  # 0, 20, 40, 3, 558, 0.051, 0.081, 0.24
DEO= (2, 18, 40, 1, 542, 0.213, 0.028, 0.72) 
BRL= (0, 0, 0, 0, 0, 0, 0, 0)    # Ice/snow
OTH= (0, 0, 0, 0, 0, 0, 0, 0)    # Water, ice, snow

DEL= (2, 18, 40, 1, 542, 0.213, 0.028, 0.72)
DEM= (2, 18, 40, 1, 542, 0.213, 0.028, 0.72)
DEH= (2, 18, 40, 1, 542, 0.213, 0.028, 0.72)

# Link parameters to land cover type
LC_dict = {'EVF':EVF, 'DBF':DBF, 'MXF':MXF, 'SHB':SHB, 'CRP':CRP,\
               'GRS':GRS, 'WET':WET, 'DEO':DEO, 'DEL':DEL, 'DEM':DEM,\
               'DEH':DEH, 'BRL':BRL, 'OTH':OTH}
LC_codes = {"EVF":42, "DBF":41, "MXF":43, "SHB":52, "CRP":82, 
            "GRS":[71,81], "WET":[90,95],\
            "DEO":21, "DEL":22, "DEM":23, "DEH":24, "BRL":31, "OTH":[0,11,12]}
NLCD_def = {"OTH":11, "SNW":12, \
            "DEO":21, "DEL":22, "DEM":23, "DEH":24,"BRL":31,\
            "DBF":41, "EVF":42, "MXF":43, "SHB":52,\
            "GRS":71, "PST":81, "CRP":82, "WDW":90, "EHW":95}
