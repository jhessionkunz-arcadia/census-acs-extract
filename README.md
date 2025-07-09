# census-acs-extract
Simple method to query Census API for multiple ACS variables, multiple geographies.

See first example for how to extract the data. See second example for how to reformat the data into the Arcadia format

### Example 1 - Extract

Requires a Census API Key: https://www.census.gov/developers/
Also requires DataMade's Census tool: https://github.com/datamade/census

```python
import censusAcsExtract
e=censusAcsExtract.censusAcsExtract()
e.apiKey = "<MY API KEY>"
```
Set states to be included in the extract. Requires 2-digit abbreviations. Use "All" to extract for all US States.
```python
e.states = ['MA', 'NH'] 
```
Set ACS Variables and provide a friendly name for export. The \DataInput\ directory has the list of variables in an Excel sheet for reference.
```python
e.stats = [
    ['B25034_010E', 'Built 1940 to 1949'],
    ['B25034_011E', 'Built 1939 or earlier']
]
```
Call an extract function either by Zip, Tract or Block Group. Note: When calling Zip Codes, you cannot filter by State. All states will be returned regardless.
```python
e.extractByTract()
e.extractByZip()
e.extractByBlockGroup()
```
Results are exported to \DataOutput\ directory as a CSV file.

### Example 2 - Reformat

Once you have the data extracted, you will need to edit and run the python script "runReformatting.py" once for each data file. This will run the censusReformatting.py file with the proper variables, and takes the data and combines it into one row per zip/block, as well as calculates the arcadia fields based on data points.

You can then take the rf versions of the output for Arcadia use.

In runReformatting, update the file name to be the name of the output file you want to reformat, including the .csv on the end

Also change the geography type based on which file you are using.

Finally, you can turn on printlogging to process only a single zip/block with some logging, then you can examine the output.