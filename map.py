# name: James Millar Mejino
# date: 2025 03 18
# email: localgeography@proton.me
# title: python automation project
# desc: calculate shape area of buildings by category
# input: coordinates (lon, lat)
# input: radius (metres)
# output: an example map (jpg)

# install modules
pip install geopandas
pip install pandas 
pip install shapely

# import modules
import arcpy
from arcpy import env
from geopandas import GeoDataFrame
import pandas as pd
from shapely.geometry import Point
import matplotlib as plt

# set workspace environemnt
env.workspace = "FILEPATH"

# set overwrite option to true
env.overwriteOutput = True

# set up variables for example map
testlon = -73.621
testlat = 45.481
testrad = 1000

# we're gonna preprocess our data with our helper functions

# first, we're gonna create our starting location using our helper functions
CreatePoint(testlon, testlat)

# then, create our search area using our helper functions
SelectArea(testrad)

# now we can plot our example map

# define file paths for MTL buildings and point buffer shapefiles
MTL = "FILEPATH/MTLProject.shp"
ptBuffer = "FILEPATH/ptReproj.shp"

# read files into geodataframes
mtl_df = gpd.read_file(MTL)
buffer_df = gpd.read_file(ptBuffer)

# set up figure
fig, ax = plt.pyplot.subplots(figsize = (11, 9))

# plot MTL buildings gdf
mtl_df.plot(ax = ax,
            # set symbology by "category" field
            column = "category", categorical = True,
            # create a legend
            legend = True)

# plot point buffer gdf
buffer_df.plot(color = "lightgrey", edgecolor = "black", ax = ax,
               # set opacity to 60% 
               alpha = 0.6)

# create title
ax.set_title("Example Search Area in Montreal")

# sanity check: display plot
plt.pyplot.show()

# save plot as jpg
plt.pyplot.savefig("FILEPATH/Example_Map.jpg", dpi = "figure")