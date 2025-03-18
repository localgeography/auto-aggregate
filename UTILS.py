# name: James Millar Mejino
# date: 2025 03 18
# email: localgeography@proton.me
# title: python automation project
# desc: calculate shape area of buildings by category
# input: coordinates (in lon, lat)
# input: radius (in metres)
# output: CSV file containing place categories and aggregated areas (in square meters)

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
env.workspace = "FILEPATH HERE"

# set overwrite option to true
env.overwriteOutput = True

# setup variables to be filled by user-input
radius = ""
lon = ""
lat = ""

# set up list of place categories for later use
categories = ['bakery', 'bank', 'bar', 'cafe', 'convenience', 'fast_food', 'hairdresser', 'pharmacy', 'restaurant', 'supermarket']

# set up empty list of place areas for later use
places = []

# now we're gonna define our helper functions

# create a function that takes and validates user-specified radius and geographic coordinates and stores them as variables
def UserInput():
    
    # while loop to ask user for radius and validate input
    while True:
        try:
            # ask user for radius
            radius = int(raw_input("Please enter a search radius in meters: "))

            # check if radius is positive
            if 0 < radius:
                # if positive, exit loop
                break

            # if not positive, ask user to retry input
            else:
                print("Invalid radius. Try again")
                continue

        # raise exceptions for invalid user inputs
        except ValueError:
            print("Oops! Invalid number!")
        except TypeError:
            print("Oops! That's not a number!")
    
    
    # while loop to ask user for geographic coordinates and validate input
    while True:
        try:
            # ask user for geographic coordinates
            coord = raw_input("Please enter the longitude and latitude as floats split by a space: ")
            
            # split user-specified coordinates into long and lat, convert into floats
            lon = float(coord.split()[0])
            lat = float(coord.split()[1])
            
            # check if coordinates are in Montreal
            if (-74 <= lon < -73) and (45 <= lat < 46):

                # if they're in Montreal, exit loop
                break

            # if they're not in Montreal, ask user to retry input
            else:
                print("Coordinates out of range. Try again.")
                continue
            
        # raise exception for invalid user inputs
        except ValueError:
            print("Oops! Those coordinates are outside Montreal!")
        except TypeError:
            print("Oops! That's not a number!")

# create a function that takes user-specified coordinates and outputs a point shapefile
def CreatePoint(x, y):
    
    # set up coordinates of point using user-specified coordinates
    point = (x, y)

    # create point geometry
    pt = Point(point)
    geom = [pt]
    
    # create dictionary to store attributes
    attributes = {'name': ['point'], 'id':[0], 'longitude': [x], 'latitude': [y]}

    # set up spatial reference system
    crs = {"init": "epsg:4326"}
    
    # create geodataframe
    df = GeoDataFrame(crs = crs, geometry = geom, data = attributes)

    # save geodataframe as a shapefile
    df.to_file("FILEPATH/point.shp")

# create function that takes user-specified search radius and outputs a feature layer of the selected area
def SelectArea(x):

    # reproject point from GCS WGS to WGS 1984
    infc = "point.shp"
    outfc = "ptProject"
    sr = arcpy.SpatialReference(3857)
    
    # execute Project tool
    try:
        arcpy.Project_management(infc, outfc, sr)
        # if executed 
        print("Projected point shapefile")
        
    # if unsuccessful
    except arcpy.ExecuteError:
        # print error message
        print(arcpy.GetMessages(2))

    # buffer by user-specified radius
    infc = "ptProject.shp"
    outfc = "ptBuffer"
    buffer_distance = x
    
    #execute Buffer tool
    try:
        arcpy.Buffer_analysis(infc, outfc, buffer_distance)
        # if executed
        print("Buffered point by {}m".format(x))

    # if unsuccessful
    except arcpy.ExecuteError:
        # print error message
        print(arcpy.GetMessages(2))


    # make a feature layer from the buffered point shapefile
    infc = "ptBuffer.shp"
    outlyr = "buffer_lyr"
    
    # execute Make Feature Layer tool
    try:
        buffer_lyr = arcpy.MakeFeatureLayer_management(infc, outlyr)
        # if executed
        print("Created selected area feature layer")

    # if unsuccessful
    except arcpy.ExecuteError:
        # print error message
        print(arcpy.GetMessages(2))

    # make a feature layer for the MTL buildings shapefile
    infc = "MTL_buildings_sample.shp"
    outlyr = "MTL_lyr"
    
    # where clause to filter out '' category
    where_clause = "category <> ''"
    
    # execute Make Feature Layer tool
    try:
        mtl_lyr = arcpy.MakeFeatureLayer_management(infc, outlyr, where_clause)
        # if executed
        print("Created MTL buildings feature layer")

    # if unsuccessful
    except arcpy.ExecuteError:
        # print error message
        print(arcpy.GetMessages(2))


    # select by location to intersect the two layers 
    inlyr = mtl_lyr
    overlap_type = "INTERSECT"
    select_features = buffer_lyr

    # execute Select Layer By Location tool
    try:
        select_location = arcpy.SelectLayerByLocation_management(inlyr, overlap_type, select_features)
        # if executed
        print("Selected layer by location")

    # if unsuccessful
    except arcpy.ExecuteError:
        # print error message
        print(arcpy.GetMessages(2))


    # make a feature layer of the intersected layers
    infc = select_location
    outlyr = "Location_lyr"
    
    # execute Make Feature Layer tool
    try:
        arcpy.MakeFeatureLayer_management(infc, outlyr)
        # if executed
        print("Created selected area feature layer")

    # if unsuccessful
    except arcpy.ExecuteError:
        # print error message
        print(arcpy.GetMessages(2))

# create a function that takes a selected area feature layer and returns 
# a csv file of total areas (in square meters) by place category
def PlaceAreaCSV()

    # for loop to iterate through each place category
    for category in categories:
        infc = "Select_Location_Layer.shp"
        outlyr = category + "_Layer"
        
        # where clause to select place category
        where_clause = "category = '" + category + "'"
        
        # execute Make Feature Layer tool 
        try:
            arcpy.MakeFeatureLayer_management(infc, outlyr, where_clause)
            # if executed
            print("Made layer of selected features")

        # if unsuccessful
        except arcpy.ExecuteError:
            # print error message
            print(arcpy.GetMessages(2))

        # set selected features as input
        fc = outlyr
        rows = arcpy.SearchCursor(fc)
        area = 0.0
        
        # for loop to iterate through each selected feature
        for row in rows:
            # add all shape areas together
            area += row.Shape.area

        # round results to nearest 1.0
        result = round(area, 0)

        # store place category and corresponding area as a tuple
        tup = (category, result)

        # append tuple to list of place areas
        places.append(tup)

    # using pandas module, convert list of place areas into a dataframe 
    df = pd.DataFrame(places, columns=["place category", "total area"])

    # convert dataframe into a csv file
    df.to_csv('FILEPATH HERE/places.csv', index=False)

    # sanity check
##    print("done")