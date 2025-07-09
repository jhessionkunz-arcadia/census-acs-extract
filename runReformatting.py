import censusReformatting

r = censusReformatting.censusReformatting()

#  update path for file to transform, you will need the four different files, three blockGroup and one ZIP file
r.file_path = "dataOutput/blockGroup-99vars-export-3-20241217-193739.csv" 

# Switch to ZTCA for Zipcode file
r.geography_type = 'Census Block Group'
#r.geography_type = 'ZCTA';

# turn logging on, and limit to only one single zip/block for testing
r.printLogging = False;

r.runReformatting()
