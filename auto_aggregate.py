# name: James Millar Mejino
# date: 2025 03 18
# email: localgeography@proton.me
# title: python automation project
# desc: calculate shape area of buildings by category
# input: coordinates (lon, lat)
# input: radius (metres)
# output: CSV file containing place categories and aggregated areas (in square meters)

# print welcome message
print("*** Welcome to the place area auto aggregator. ***")

# call UserInput function
UserInput()

# call CreatePoint function
CreatePoint(lon, lat)

# call SelectArea function
SelectArea(rad)

# call PlaceAreaCSV function
PlaceAreaCSV()