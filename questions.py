
QUESTIONS


- What to do in case of NO data (eg if the population 18-44 was 0, or if the Poverty level data was 0) 
	- Currently in ARCADIA - set the data to zero in dbo.census
	- Proposed - set it to null, as zero often indicates no data available

EG: "% Families w/ Incomes < 100% of Federal Poverty Level"

Example from current (2022) data
	860Z200US70402,70402,ZCTA5 70402,C17002_001E,Poverty Level | Total,0.0
	All other poverty data from this ZIP is also set to 0.0
	This seems unlikely that there is not a single individual is below the poverty line, although perhaps for this specific zip that is the case?


--------------------------------------------

LIST OF FIELDS IN ARCADIA THAT NEED CLARITY ABOUT THE FIELD DEFINITIONS

------------------------------------------


"% High School"		|	 "People Age 25+ w/ High School Degree"
	- Currently, these two Arcadia fields are exactly the same for all clients
	- They are supposed to represent anyone who has a high school degree (or lower)
	- They are a pair with another field, "% Bachelors" which represents bachelors degress and higher


- Current Arcadia Defition, based on guesswork and comparisons 
	- Bachelors = answered bachelor on form (B15003_022E)
	- High School = answered High school on form (B15003_017E)

AVAILABLE RELEVANT FIELDS WE COULD USE IN THESE FIELD DEFITIONS

# ['B15003_017E', 'Education | Regular high school diploma'],
# ['B15003_018E', 'Education | GED or alternative credential'],

# ['B15003_022E', 'Education | Bachelor\'s degree'],
# ['B15003_023E', 'Education | Master\'s degree'],
# ['B15003_024E', 'Education | Professional school degree'],
# ['B15003_025E', 'Education | Doctorate degree'],


Questions
- Should we include GED in the "% High School" and lower grouping?
- Should we include the masters, professional school and doctorate in teh "% bachelors" field?
- Should we add the following data points, which were not included in the past, to the high school grouping (this would require me to re-pull from the ACS Website)

# ['B15003_019E', 'Education | Some college, less than 1 year'],
# ['B15003_020E', 'Education | Some college, 1 or more years, no degree'],
# ['B15003_021E', 'Education | Associate's degree'],



------------------------------------------------------

Race - Currently, we use the following groupings
- Pro: Adding up all the groups gives the total count
- Con: there is no way to identify what the answers were for Two or more races

# ['B02001_001E', 'Race | Total'],

# ['B02001_002E', 'Race | White alone'],
# ['B02001_003E', 'Race | Black or African American alone'],
# ['B02001_004E', 'Race | American Indian and Alaska Native alone'],
# ['B02001_005E', 'Race | Asian alone'],
# ['B02001_006E', 'Race | Native Hawaiian and Other Pacific Islander alone'],
# ['B02001_007E', 'Race | Some other race alone'],
# ['B02001_008E', 'Race | Two or more races'],

--Vista does not use
--Add more fields?


Option:
- Use B02012_001E, Native Hawaiian and Other Pacific Islander Alone or in Combination With One or More Other Races	
- Pro: Get the actual count of individuals in the area who match this group
- con: double counts those who answer two or more, so the numbers don't add up
- con: different from how we have done it prior
- con: requires me to repull from the ACS website


-----------------------------------------------------

Female Earning Ratio

Questioning the best way to calculate this

Available relevant data points:

# ['B19326_001E', 'Median Income | Total'],
# ['B19326_002E', 'Median Income | Male'],
# ['B19326_003E', 'Median Income | Male | Works Fulltime'],
# ['B19326_005E', 'Median Income | Female'],
# ['B19326_006E', 'Median Income | Female | Works Fulltime'],

# Current example in Arcadia: 1.0121 
# Range from 2.7 to 0, mostly .8-1.3

# online suggests: (Median Income | Female) / (Median Income | Male)
# thats a pretty big change for this example - from 1.0121 down to .79
# could be (Median Income | Female) / (Median Income | Total) as well
# that would be .88 in this example

Example data from 2022 that I pulled recently

# Median Income | Total   10305
# Median Income | Male    11453
# Median Income | Male | Works Fulltime   19477
# Median Income | Female  9071
# Median Income | Female | Works Fulltime 21209


------------------------------------------------
Households with Children and a Single Parent

Should this be single male + single female / TOTAL, or single male + single female / Family

RELEVANT FIELDS

# ['B09005_001E', 'Child Households | Total'],
# ['B09005_002E', 'Child Households | Family'],
# ['B09005_003E', 'Child Households | Family | Couple'],
# ['B09005_004E', 'Child Households | Family | Single Male'],
# ['B09005_005E', 'Child Households | Family | Single Female'],
# #does not exist in the 2022 data, which is the most recent acs5 data set as of Dec 2024 when this was run
# #['B09005_006E', 'Child Households | Nonfamily'],


EXAMPLE DATASET

860Z200US00601,00601,ZCTA5 00601,B09005_001E,Child Households | Total,3070.0
860Z200US00601,00601,ZCTA5 00601,B09005_002E,Child Households | Family,1274.0
860Z200US00601,00601,ZCTA5 00601,B09005_003E,Child Households | Family | Couple,789.0
860Z200US00601,00601,ZCTA5 00601,B09005_004E,Child Households | Family | Single Male,23.0
860Z200US00601,00601,ZCTA5 00601,B09005_005E,Child Households | Family | Single Female,984.0



--------------------------------------------------------------------------------


LIST OF FIELDS IN ARCADIA


"GeographyId", "GeographyType",
"% 18 to 44", "% 45 - 64", "% 65 and Up", 
"% Adults who are Unemployed", "% Bachelors", "% Families w/ Incomes < 100% of Federal Poverty Level", 
"% Families w/ Incomes < 200% of Federal Poverty Level", "% Female", "% High School", "% Households Receiving Public Assistance", 
"% Households w/ No Car", "% Households with Children and a Single Parent", "% Male", 
"% People Age 25+ w/ High School Degree", "% Population by Race - Native Hawaiian or Pacific Islander", 
"% Population by Race - American Indian or Alaskan Native", "% Population by Race - Asian", 
"% Population by Race - Black or African American", "% Population by Race - White", "% Under 18",
"Female Earning Ratio", "Median Earnings", "Persons Per Housing Unit", "Total Population", 
"% Population by Race - Other", "% Population by Race - Two or More Races", "Housing Vacancy Rate"



LIST OF AVAILABLE FIELDS (this could be expanded but this is what we used previously)



['B01001_002E', 'Males'],
['B01001_026E', 'Females'],
['B01003_001E', 'Population'],
['B02001_001E', 'Race | Total'],
['B02001_002E', 'Race | White alone'],
['B02001_003E', 'Race | Black or African American alone'],
['B02001_004E', 'Race | American Indian and Alaska Native alone'],
['B02001_005E', 'Race | Asian alone'],
['B02001_006E', 'Race | Native Hawaiian and Other Pacific Islander alone'],
['B02001_007E', 'Race | Some other race alone'],
['B02001_008E', 'Race | Two or more races'],
['B09005_001E', 'Child Households | Total'],
['B09005_002E', 'Child Households | Family'],
['B09005_003E', 'Child Households | Family | Couple'],
['B09005_004E', 'Child Households | Family | Single Male'],
['B09005_005E', 'Child Households | Family | Single Female'],
#does not exist in the 2022 data, which is the most recent acs5 data set as of Dec 2024 when this was run
#['B09005_006E', 'Child Households | Nonfamily'],
['B15003_001E', 'Education | Total'],
['B15003_017E', 'Education | Regular high school diploma'],
['B15003_018E', 'Education | GED or alternative credential'],
['B15003_022E', 'Education | Bachelor\'s degree'],
['B15003_023E', 'Education | Master\'s degree'],
['B15003_024E', 'Education | Professional school degree'],
['B15003_025E', 'Education | Doctorate degree'],
['B19057_001E', 'Public Assistance | Total'],
['B19057_002E', 'Public Assistance | With Public Assistance'],
['B25001_001E', 'Housing Units | Total'],
['B25002_003E', 'Housing Units | Vacant'],
['B25031_001E', 'Median Rent | Total'],
['B25031_003E', 'Median Rent | 1 Bed'],
['B25031_004E', 'Median Rent | 2 Bed'],
['B25031_005E', 'Median Rent | 3 Bed'],
['C17002_001E', 'Poverty Level | Total'],
['C17002_002E', 'Poverty Level | Under .50'],
['C17002_003E', 'Poverty Level | .50 to .99'],
['C17002_004E', 'Poverty Level | 1.00 to 1.24'],
['C17002_005E', 'Poverty Level | 1.25 to 1.49'],
['C17002_006E', 'Poverty Level | 1.50 to 1.84'],
['C17002_007E', 'Poverty Level | 1.85 to 1.99'],
['C17002_008E', 'Poverty Level | 2.00 and over'],
['B01001_001E', 'Sex Age Total'],
['B01001_002E', 'Sex Age | Male'],
['B01001_003E', 'Sex Age | Male | Under 5 years'],
['B01001_004E', 'Sex Age | Male | 5 to 9 years'],
['B01001_005E', 'Sex Age | Male | 10 to 14 years'],
['B01001_006E', 'Sex Age | Male | 15 to 17 years'],
['B01001_007E', 'Sex Age | Male | 18 and 19 years'],
['B01001_008E', 'Sex Age | Male | 20 years'],
['B01001_009E', 'Sex Age | Male | 21 years'],
['B01001_010E', 'Sex Age | Male | 22 to 24 years'],
['B01001_011E', 'Sex Age | Male | 25 to 29 years'],
['B01001_012E', 'Sex Age | Male | 30 to 34 years'],
['B01001_013E', 'Sex Age | Male | 35 to 39 years'],
['B01001_014E', 'Sex Age | Male | 40 to 44 years'],
['B01001_015E', 'Sex Age | Male | 45 to 49 years'],
['B01001_016E', 'Sex Age | Male | 50 to 54 years'],
['B01001_017E', 'Sex Age | Male | 55 to 59 years'],
['B01001_018E', 'Sex Age | Male | 60 and 61 years'],
['B01001_019E', 'Sex Age | Male | 62 to 64 years'],
['B01001_020E', 'Sex Age | Male | 65 and 66 years'],
['B01001_021E', 'Sex Age | Male | 67 to 69 years'],
['B01001_022E', 'Sex Age | Male | 70 to 74 years'],
['B01001_023E', 'Sex Age | Male | 75 to 79 years'],
['B01001_024E', 'Sex Age | Male | 80 to 84 years'],
['B01001_025E', 'Sex Age | Male | 85 years and over'],
['B01001_026E', 'Sex Age | Female'],
['B01001_027E', 'Sex Age | Female | Under 5 years'],
['B01001_028E', 'Sex Age | Female | 5 to 9 years'],
['B01001_029E', 'Sex Age | Female | 10 to 14 years'],
['B01001_030E', 'Sex Age | Female | 15 to 17 years'],
['B01001_031E', 'Sex Age | Female | 18 and 19 years'],
['B01001_032E', 'Sex Age | Female | 20 years'],
['B01001_033E', 'Sex Age | Female | 21 years'],
['B01001_034E', 'Sex Age | Female | 22 to 24 years'],
['B01001_035E', 'Sex Age | Female | 25 to 29 years'],
['B01001_036E', 'Sex Age | Female | 30 to 34 years'],
['B01001_037E', 'Sex Age | Female | 35 to 39 years'],
['B01001_038E', 'Sex Age | Female | 40 to 44 years'],
['B01001_039E', 'Sex Age | Female | 45 to 49 years'],
['B01001_040E', 'Sex Age | Female | 50 to 54 years'],
['B01001_041E', 'Sex Age | Female | 55 to 59 years'],
['B01001_042E', 'Sex Age | Female | 60 and 61 years'],
['B01001_043E', 'Sex Age | Female | 62 to 64 years'],
['B01001_044E', 'Sex Age | Female | 65 and 66 years'],
['B01001_045E', 'Sex Age | Female | 67 to 69 years'],
['B01001_046E', 'Sex Age | Female | 70 to 74 years'],
['B01001_047E', 'Sex Age | Female | 75 to 79 years'],
['B01001_048E', 'Sex Age | Female | 80 to 84 years'],
['B01001_049E', 'Sex Age | Female | 85 years and over'],
['B19326_001E', 'Median Income | Total'],
['B19326_002E', 'Median Income | Male'],
['B19326_003E', 'Median Income | Male | Works Fulltime'],
['B19326_005E', 'Median Income | Female'],
['B19326_006E', 'Median Income | Female | Works Fulltime'],
['B23025_001E', 'Employment | Total'],
['B23025_002E', 'Employment | In Labor Force'],
['B23025_005E', 'Employment | Unemployed'],
['B23025_006E', 'Employment | Armed Forces'],
['B08141_001E', 'Transportation | Total'],
['B08141_002E', 'Transportation | No Vehicles']