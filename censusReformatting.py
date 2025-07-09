# census reformatting

import csv
import math
import datetime

class censusReformatting():
    file_path = ''
    geography_type = ''
    printLogging = False;

    def csv_to_array(self, file_path):
        # Initialize an empty array to hold the data
        raw_census_data = []

        # Open the CSV file
        with open(file_path, mode='r', newline='', encoding='utf-8',  errors='ignore') as csvfile:
            # Use csv.reader to read the file
            csv_reader = csv.reader(csvfile)

            # Iterate over each row and append it to the array, skipping header
            next(csv_reader)
            for row in csv_reader:
                raw_census_data.append(row)
        
        return raw_census_data

    def outputData(self, reformattedData):
        print('Beginning output of ' + str(len(reformattedData)) + ' reformattedData')
        
        fileTag = self.file_path[self.file_path.find('/')+1:]
        # time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fileName = 'rf-' + fileTag + '.csv'
        with open('dataOutput/'+fileName, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(reformattedData)

    def get_distinct_geo_ids(self, data_array):
        # Use a set to store distinct values (sets automatically handle duplicates)
        distinct_values = set()

        for row in data_array:
            if row:  # Ensure the row is not empty
                distinct_values.add(row[0])  # Add the first field to the set

        # Convert the set back to a list
        return list(distinct_values)

    def reformat_blockgroup_geo_id(self, string_list):
        transformed_list = []

        for entry in string_list:
            transformed_entry = entry[9:]
            transformed_entry = transformed_entry[:5] + '.' + transformed_entry[5:11] + '.' + transformed_entry[11]
            transformed_list.append([entry, transformed_entry])
        return transformed_list

    def reformat_zip_geo_id(self, string_list):
        transformed_list = []

        for entry in string_list:
            transformed_entry = entry[9:]
            transformed_list.append([entry, transformed_entry])
        return transformed_list

    def turn_list_to_dictionary(self, censusdata):
        # Initialize an empty dictionary
        nested_dict = {}
        censusdata
        if self.geography_type == 'Census Block Group':
            # block group header: GEO_ID,state,county,tract,block group,NAME,Var ID,Var Name,Var Value
            for row in censusdata:
                geo_id = row[0]  # using provided geo id as first nested key
                variable_id = row[6] 
                variable_name = row[7]
                try:
                    variable_value = float(row[8]) if row[8].strip() != '' else None
                except (ValueError, TypeError):
                    print('value parse error:')
                    print(row[8])
                    variable_value = None

                # Check if the key exists in the dictionary
                if geo_id not in nested_dict:
                    nested_dict[geo_id] = {}
                
                nested_dict[geo_id].update({variable_id: variable_value ,variable_name: variable_value})
        else:
            # zip header: GEO_ID,zip code tabulation area,NAME,Var ID,Var Name,Var Value
            for row in censusdata:
                geo_id = row[0]  # using provided geo id as first nested key
                variable_id = row[3] 
                variable_name = row[4]
                variable_value = float(row[5])

                # Check if the key exists in the dictionary
                if geo_id not in nested_dict:
                    nested_dict[geo_id] = {}
                
                nested_dict[geo_id].update({variable_id: variable_value ,variable_name: variable_value})

        return nested_dict

    def printIfLogging(self, string):
        if self.printLogging:
            print(string)


    def runReformatting(self):
        raw_census_data = self.csv_to_array(self.file_path)
        distinct_geo_ids = self.get_distinct_geo_ids(raw_census_data)
        distinct_geo_id_pairs = [];
        #contains a list, each entry is an original geo_id and a 

        if self.geography_type == 'Census Block Group':
            distinct_geo_id_pairs = self.reformat_blockgroup_geo_id(distinct_geo_ids)
        else:
            distinct_geo_id_pairs = self.reformat_zip_geo_id(distinct_geo_ids)

        census_dictionary = self.turn_list_to_dictionary(raw_census_data)

        # print(census_dictionary['860Z200US00601'])
        # print(distinct_geo_id_pairs[0])

        # 29 items in the list
        arcadia_census_data = [[
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
        ]]

        for geo_pair in distinct_geo_id_pairs:
            geo_id = geo_pair[0]
            reformatted_geo_id = geo_pair[1]
            new_census_entry = [reformatted_geo_id, self.geography_type]

            self.printIfLogging ('geo_id: ' + geo_id)

            # Step 1: Ages
            self.printIfLogging ('Subsection 1: Ages')

            totalAge = census_dictionary[geo_id]['B01001_001E']

            if totalAge is not None and totalAge != 0:

                # "% 18 to 44"
                self.printIfLogging('Step 1: 18 to 44')

                lowerMiddleAgeBracket = sum([census_dictionary[geo_id]['B01001_007E'], census_dictionary[geo_id]['B01001_008E'],
                    census_dictionary[geo_id]['B01001_009E'],census_dictionary[geo_id]['B01001_010E'],
                    census_dictionary[geo_id]['B01001_011E'],census_dictionary[geo_id]['B01001_012E'],
                    census_dictionary[geo_id]['B01001_013E'],census_dictionary[geo_id]['B01001_014E'],
                    census_dictionary[geo_id]['B01001_031E'],census_dictionary[geo_id]['B01001_032E'],
                    census_dictionary[geo_id]['B01001_033E'],census_dictionary[geo_id]['B01001_034E'],
                    census_dictionary[geo_id]['B01001_035E'],census_dictionary[geo_id]['B01001_036E'],
                    census_dictionary[geo_id]['B01001_037E'],census_dictionary[geo_id]['B01001_038E']])

                percentLowerMiddleAgeBracket = round(lowerMiddleAgeBracket  / totalAge, 4)

                new_census_entry.append(percentLowerMiddleAgeBracket)


                # ['B01001_001E', 'Sex Age Total'],
                # ['B01001_007E', 'Sex Age | Male | 18 and 19 years'],
                # ['B01001_008E', 'Sex Age | Male | 20 years'],
                # ['B01001_009E', 'Sex Age | Male | 21 years'],
                # ['B01001_010E', 'Sex Age | Male | 22 to 24 years'],
                # ['B01001_011E', 'Sex Age | Male | 25 to 29 years'],
                # ['B01001_012E', 'Sex Age | Male | 30 to 34 years'],
                # ['B01001_013E', 'Sex Age | Male | 35 to 39 years'],
                # ['B01001_014E', 'Sex Age | Male | 40 to 44 years'],
                # ['B01001_031E', 'Sex Age | Female | 18 and 19 years'],
                # ['B01001_032E', 'Sex Age | Female | 20 years'],
                # ['B01001_033E', 'Sex Age | Female | 21 years'],
                # ['B01001_034E', 'Sex Age | Female | 22 to 24 years'],
                # ['B01001_035E', 'Sex Age | Female | 25 to 29 years'],
                # ['B01001_036E', 'Sex Age | Female | 30 to 34 years'],
                # ['B01001_037E', 'Sex Age | Female | 35 to 39 years'],
                # ['B01001_038E', 'Sex Age | Female | 40 to 44 years'],


                # "% 45 - 64"
                self.printIfLogging('Step 2: 45 - 64')

            
                upperMiddleAgeBracket = sum([census_dictionary[geo_id]['B01001_015E'], census_dictionary[geo_id]['B01001_016E'],
                    census_dictionary[geo_id]['B01001_017E'],census_dictionary[geo_id]['B01001_018E'],
                    census_dictionary[geo_id]['B01001_019E'],census_dictionary[geo_id]['B01001_039E'],
                    census_dictionary[geo_id]['B01001_040E'],census_dictionary[geo_id]['B01001_041E'],
                    census_dictionary[geo_id]['B01001_042E'],census_dictionary[geo_id]['B01001_043E']])

                percentUpperMiddleAgeBracket = round( upperMiddleAgeBracket  / totalAge, 4)
                new_census_entry.append(percentUpperMiddleAgeBracket)
             
                # ['B01001_015E', 'Sex Age | Male | 45 to 49 years'],
                # ['B01001_016E', 'Sex Age | Male | 50 to 54 years'],
                # ['B01001_017E', 'Sex Age | Male | 55 to 59 years'],
                # ['B01001_018E', 'Sex Age | Male | 60 and 61 years'],
                # ['B01001_019E', 'Sex Age | Male | 62 to 64 years'],
                # ['B01001_039E', 'Sex Age | Female | 45 to 49 years'],
                # ['B01001_040E', 'Sex Age | Female | 50 to 54 years'],
                # ['B01001_041E', 'Sex Age | Female | 55 to 59 years'],
                # ['B01001_042E', 'Sex Age | Female | 60 and 61 years'],
                # ['B01001_043E', 'Sex Age | Female | 62 to 64 years'],

                # "% 65 and Up"
                self.printIfLogging('Step 3: 65 and Up')

                uppermostAgeBracket = sum([census_dictionary[geo_id]['B01001_020E'], census_dictionary[geo_id]['B01001_021E'],
                    census_dictionary[geo_id]['B01001_022E'],census_dictionary[geo_id]['B01001_023E'],
                    census_dictionary[geo_id]['B01001_024E'],census_dictionary[geo_id]['B01001_025E'],
                    census_dictionary[geo_id]['B01001_044E'],census_dictionary[geo_id]['B01001_045E'],
                    census_dictionary[geo_id]['B01001_046E'],census_dictionary[geo_id]['B01001_047E'],
                    census_dictionary[geo_id]['B01001_048E'],census_dictionary[geo_id]['B01001_049E']
                    ])

                percentUppermostAgeBracket = round(uppermostAgeBracket / totalAge, 4)
                new_census_entry.append(percentUppermostAgeBracket)

                # ['B01001_020E', 'Sex Age | Male | 65 and 66 years'],
                # ['B01001_021E', 'Sex Age | Male | 67 to 69 years'],
                # ['B01001_022E', 'Sex Age | Male | 70 to 74 years'],
                # ['B01001_023E', 'Sex Age | Male | 75 to 79 years'],
                # ['B01001_024E', 'Sex Age | Male | 80 to 84 years'],
                # ['B01001_025E', 'Sex Age | Male | 85 years and over'],
                #  ['B01001_044E', 'Sex Age | Female | 65 and 66 years'],
                # ['B01001_045E', 'Sex Age | Female | 67 to 69 years'],
                # ['B01001_046E', 'Sex Age | Female | 70 to 74 years'],
                # ['B01001_047E', 'Sex Age | Female | 75 to 79 years'],
                # ['B01001_048E', 'Sex Age | Female | 80 to 84 years'],
                # ['B01001_049E', 'Sex Age | Female | 85 years and over'


            else:
                # total age is zero, append several
                new_census_entry.append(None)
                new_census_entry.append(None)
                new_census_entry.append(None)





            # "% Adults who are Unemployed"
            self.printIfLogging('Step 4: Adults who are Unemployed')
            
            totalEmployment = census_dictionary[geo_id]['B23025_001E']

            if totalEmployment is not None and totalEmployment != 0: 
                percentUnemployment = round(census_dictionary[geo_id]['B23025_005E'] / totalEmployment, 4)
                new_census_entry.append(percentUnemployment)
            else:
                new_census_entry.append(None)




            # "% Bachelors"
            self.printIfLogging('Step 5: Bachelors')

            totalEducation = census_dictionary[geo_id]['B15003_001E']

            if totalEducation is not None and totalEducation != 0: 
                percentBachelors = round((census_dictionary[geo_id]['B15003_022E'] + census_dictionary[geo_id]['B15003_023E']
                    + census_dictionary[geo_id]['B15003_024E'] + census_dictionary[geo_id]['B15003_025E'])
                    / totalEducation, 4)
                new_census_entry.append(percentBachelors)
            else:
                new_census_entry.append(None)

            # bachelors degree or higher

            # ['B15003_022E', 'Education | Bachelor\'s degree'],
            # ['B15003_023E', 'Education | Master\'s degree'],
            # ['B15003_024E', 'Education | Professional school degree'],
            # ['B15003_025E', 'Education | Doctorate degree'],
            # ['B15003_001E', 'Education | Total'],


            self.printIfLogging('Step 6: Families w/ Incomes < 100% of Federal Poverty Level')
            self.printIfLogging('Step 7: Families w/ Incomes < 200% of Federal Poverty Level')


            totalPovertyLevel = census_dictionary[geo_id]['C17002_001E']

            if totalPovertyLevel is not None and totalPovertyLevel != 0: 

                # "% Families w/ Incomes < 100% of Federal Poverty Level"

                underPovertyLevel = round(
                    (census_dictionary[geo_id]['C17002_002E'] + census_dictionary[geo_id]['C17002_003E'])
                    / totalPovertyLevel, 4)
                
                new_census_entry.append(underPovertyLevel)


                # "% Families w/ Incomes < 200% of Federal Poverty Level"

                underTwicePovertyLevel = round(
                    (census_dictionary[geo_id]['C17002_002E'] + census_dictionary[geo_id]['C17002_003E']
                    + census_dictionary[geo_id]['C17002_004E'] + census_dictionary[geo_id]['C17002_005E']
                    + census_dictionary[geo_id]['C17002_006E'] + census_dictionary[geo_id]['C17002_007E'])
                    / totalPovertyLevel, 4)
                new_census_entry.append(underTwicePovertyLevel)

                          # ['C17002_001E', 'Poverty Level | Total'],
                # ['C17002_002E', 'Poverty Level | Under .50'],
                # ['C17002_003E', 'Poverty Level | .50 to .99'],
                # ['C17002_004E', 'Poverty Level | 1.00 to 1.24'],
                # ['C17002_005E', 'Poverty Level | 1.25 to 1.49'],
                # ['C17002_006E', 'Poverty Level | 1.50 to 1.84'],
                # ['C17002_007E', 'Poverty Level | 1.85 to 1.99'],
                # ['C17002_008E', 'Poverty Level | 2.00 and over'],


            else:
                new_census_entry.append(None)
                new_census_entry.append(None)


            # "% Female"
            self.printIfLogging('Step 8: Female')

            totalGender = census_dictionary[geo_id]['B01001_001E']

            if totalGender is not None and totalGender != 0: 
                percentFemale = round(census_dictionary[geo_id]['B01001_026E'] / totalGender, 4)
                new_census_entry.append(percentFemale)
            else:
                new_census_entry.append(0.0)

            # ['B01001_026E', 'Sex Age | Female'],
            # ['B01001_001E', 'Sex Age Total'],



            # "% High School"
            self.printIfLogging('Step 9: High School')

            # TODO: Fix this

            # Supposed to be everyone with a highschool degree or lower. THat would either mean summing 17 and 18, or taking the total,
            # repulling data with the extra and subtracting everything else:fro total

            totalEducation = census_dictionary[geo_id]['B15003_001E']
            
            if totalEducation is not None and totalEducation != 0: 
                percentHighSchoolOrLower = round(  (census_dictionary[geo_id]['B15003_017E'] + census_dictionary[geo_id]['B15003_018E'])
                    / totalEducation, 4)
                new_census_entry.append(percentHighSchoolOrLower)

            else:
                new_census_entry.append(None)

                # Add to list for repulling -

            # List this as a changed defition - additional data, grouping all degrees and above, rather than just a single row

            #difference between this and Step 14

            # ['B15003_017E', 'Education | Regular high school diploma'],
            # ['B15003_018E', 'Education | GED or alternative credential'],
            # ['B15003_001E', 'Education | Total'],





            # "% Households Receiving Public Assistance"
            self.printIfLogging('Step 10: Households Receiving Public Assistance')

            totalPublicAssistance = census_dictionary[geo_id]['B19057_001E']

            if totalPublicAssistance is not None and totalPublicAssistance != 0: 
                percentPublicAssistance = round(census_dictionary[geo_id]['B19057_002E'] / totalPublicAssistance, 4)
                new_census_entry.append(percentPublicAssistance)
            else:
                new_census_entry.append(None)

            # ['B19057_001E', 'Public Assistance | Total'],
            # ['B19057_002E', 'Public Assistance | With Public Assistance'],



            # "% Households w/ No Car"
            self.printIfLogging('Step 11: Households w/ No Car')

            totalTransportation = census_dictionary[geo_id]['B08141_001E']

            if totalTransportation is not None and totalTransportation != 0: 
                percentNoCar = round(census_dictionary[geo_id]['B08141_002E'] / totalTransportation, 4)
                new_census_entry.append(percentNoCar)
            else:
                new_census_entry.append(None)


            # ['B08141_001E', 'Transportation | Total'],
            # ['B08141_002E', 'Transportation | No Vehicles']



            # "% Households with Children and a Single Parent"
            self.printIfLogging('Step 12: Households with Children and a Single Parent')


            totalFamily = census_dictionary[geo_id]['B09005_002E']

            if totalFamily is not None and totalFamily != 0: 
                percentSingleParent = round((census_dictionary[geo_id]['B09005_004E'] + census_dictionary[geo_id]['B09005_005E'])
                 / totalFamily, 4)
                new_census_entry.append(percentSingleParent)
            else:
                new_census_entry.append(None)

            # ['B09005_001E', 'Child Households | Total'],
            # ['B09005_002E', 'Child Households | Family'],
            # ['B09005_003E', 'Child Households | Family | Couple'],
            # ['B09005_004E', 'Child Households | Family | Single Male'],
            # ['B09005_005E', 'Child Households | Family | Single Female'],
            # #does not exist in the 2022 data, which is the most recent acs5 data set as of Dec 2024 when this was run
            # #['B09005_006E', 'Child Households | Nonfamily'],
            # Use family as denominator per JH


            # "% Male"
            self.printIfLogging('Step 13: Male')

            if totalGender is not None and totalGender != 0: 
                percentMale = round(census_dictionary[geo_id]['B01001_002E']  / totalGender, 4)
                new_census_entry.append(percentMale)
            else:
                new_census_entry.append(None)

            # ['B01001_002E', 'Sex Age | Male'],
            # Created totalGender above


            # "% People Age 25+ w/ High School Degree"
            self.printIfLogging('Step 14: People Age 25+ w/ High School Degree')
                
            # Exact Sme as "high school" above
            
            if totalEducation is not None and totalEducation != 0: 
                new_census_entry.append(percentHighSchoolOrLower)
            else:
                new_census_entry.append(None)


            # Part Q - Race

            # ['B02001_001E', 'Race | Total'],
            # ['B02001_002E', 'Race | White alone'],
            # ['B02001_003E', 'Race | Black or African American alone'],
            # ['B02001_004E', 'Race | American Indian and Alaska Native alone'],
            # ['B02001_005E', 'Race | Asian alone'],
            # ['B02001_006E', 'Race | Native Hawaiian and Other Pacific Islander alone'],
            # ['B02001_007E', 'Race | Some other race alone'],
            # ['B02001_008E', 'Race | Two or more races'],

            self.printIfLogging ('Subsection 2: Race')

            totalRace = census_dictionary[geo_id]['B02001_001E']

            if totalRace is not None and totalRace != 0:
                # "% Population by Race - Native Hawaiian or Pacific Islander"
                self.printIfLogging('Step 15: Population by Race - Native Hawaiian or Pacific Islander')
                percentNHPI = round(census_dictionary[geo_id]['B02001_006E'] / totalRace, 4)
                new_census_entry.append(percentNHPI)


                # "% Population by Race - American Indian or Alaskan Native"
                self.printIfLogging('Step 16: Population by Race - American Indian or Alaskan Native')
                percentA = round(census_dictionary[geo_id]['B02001_004E'] / totalRace, 4)
                new_census_entry.append(percentA)


                # "% Population by Race - Asian"
                self.printIfLogging('Step 17: Population by Race - Asian')
                percentAsian = round(census_dictionary[geo_id]['B02001_005E'] / totalRace, 4)
                new_census_entry.append(percentAsian)


                # "% Population by Race - Black or African American"
                self.printIfLogging('Step 18: Population by Race - Black or African American')
                percentBAA = round(census_dictionary[geo_id]['B02001_003E'] / totalRace, 4)
                new_census_entry.append(percentBAA)


                # "% Population by Race - White"
                self.printIfLogging('Step 19: Population by Race - White')
                percentW = round(census_dictionary[geo_id]['B02001_002E'] / totalRace, 4)
                new_census_entry.append(percentW)

            else:
                self.printIfLogging ('Total Race field empty')
                new_census_entry.append(None)
                new_census_entry.append(None)
                new_census_entry.append(None)
                new_census_entry.append(None)
                new_census_entry.append(None)



            # "% Under 18"
            self.printIfLogging('Step 20: Under 18')

            if totalAge is not None and totalAge != 0:
                lowestAgeBracket = sum([census_dictionary[geo_id]['B01001_003E'], census_dictionary[geo_id]['B01001_004E'],
                    census_dictionary[geo_id]['B01001_005E'],census_dictionary[geo_id]['B01001_006E'],
                    census_dictionary[geo_id]['B01001_027E'],census_dictionary[geo_id]['B01001_028E'],
                    census_dictionary[geo_id]['B01001_029E'],census_dictionary[geo_id]['B01001_030E']
                    ])

                percentLowestAgeBracket = round(lowestAgeBracket / totalAge, 4)
                new_census_entry.append(percentLowestAgeBracket)
            else:
                new_census_entry.append(None)


            #             ['B01001_001E', 'Sex Age Total'],
            # ['B01001_002E', 'Sex Age | Male'],
            # ['B01001_003E', 'Sex Age | Male | Under 5 years'],
            # ['B01001_004E', 'Sex Age | Male | 5 to 9 years'],
            # ['B01001_005E', 'Sex Age | Male | 10 to 14 years'],
            # ['B01001_006E', 'Sex Age | Male | 15 to 17 years'],
            # ['B01001_026E', 'Sex Age | Female'],
            # ['B01001_027E', 'Sex Age | Female | Under 5 years'],
            # ['B01001_028E', 'Sex Age | Female | 5 to 9 years'],
            # ['B01001_029E', 'Sex Age | Female | 10 to 14 years'],
            # ['B01001_030E', 'Sex Age | Female | 15 to 17 years'],
            # ['B01001_031E', 'Sex Age | Female | 18 and 19 years'],

            # "Female Earning Ratio"
            self.printIfLogging('Step 21: Female Earning Ratio')

            maleMedianIncome = census_dictionary[geo_id]['B19326_002E']

            if maleMedianIncome is not None and maleMedianIncome != 0: 
                femaleEarningRatio = round(census_dictionary[geo_id]['B19326_005E'] 
                 / maleMedianIncome, 4)
                new_census_entry.append(femaleEarningRatio)
            else:
                new_census_entry.append(None)

            #Per jh: (Median Income | Female) / (Median Income | Male)

            # ['B19326_001E', 'Median Income | Total'],
            # ['B19326_002E', 'Median Income | Male'],
            # ['B19326_003E', 'Median Income | Male | Works Fulltime'],
            # ['B19326_005E', 'Median Income | Female'],
            # ['B19326_006E', 'Median Income | Female | Works Fulltime'],


            # "Median Earnings"
            self.printIfLogging('Step 22: Median Earnings')

            medianEarnings = census_dictionary[geo_id]['B19326_001E']
            if medianEarnings is not None and medianEarnings != 0: 
                new_census_entry.append(medianEarnings)
            else:
                new_census_entry.append(None)


            # ['B19326_001E', 'Median Income | Total'],
            # 10095 from 2017
            # Median Income | Total   10305 in recent pull


            # "Persons Per Housing Unit"
            self.printIfLogging('Step 23: Persons Per Housing Unit')

            population = census_dictionary[geo_id]['B01003_001E']
            housingUnits = census_dictionary[geo_id]['B25001_001E']
            if population is not None and population != 0 and housingUnits is not None and housingUnits != 0: 
                personsPerHousing = round(housingUnits / population, 4)
                new_census_entry.append(personsPerHousing)
            else:
                new_census_entry.append(None)

            # ['B01003_001E', 'Population'],
            # ['B25001_001E', 'Housing Units | Total'],


            # "Total Population"
            self.printIfLogging('Step 24: Total Population')


            if population is not None and population != 0: 
                new_census_entry.append(population)
            else:
                new_census_entry.append(None)

            # ['B01003_001E', 'Population'],


            if totalRace is not None and totalRace != 0:
                # "% Population by Race - Other"
                self.printIfLogging('Step 25: Population by Race - Other')

                percentSORA = round(census_dictionary[geo_id]['B02001_007E'] / totalRace, 4)
                new_census_entry.append(percentSORA)
                # ['B02001_007E', 'Race | Some other race alone'],


                # "% Population by Race - Two or More Races"
                self.printIfLogging('Step 26: Population by Race - Two or More Races')

                percentTOMR = round(census_dictionary[geo_id]['B02001_008E'] / totalRace, 4)
                new_census_entry.append(percentTOMR)                
                # ['B02001_008E', 'Race | Two or more races'],
            else:
                self.printIfLogging ('Total Race field empty')
                new_census_entry.append(None)
                new_census_entry.append(None)

            # "Housing Vacancy Rate"
            self.printIfLogging('Step 27: Housing Vacancy Rate')

            if housingUnits is not None and housingUnits != 0:
                vacancyRate = round(census_dictionary[geo_id]['B25002_003E'] / housingUnits, 4)
                new_census_entry.append(vacancyRate)

            # eg 2017 0.1839
            #2023 - 0.255
            # Housing Units | Total   7173
            # Housing Units | Vacant  1832

            # ['B25001_001E', 'Housing Units | Total'],
            # ['B25002_003E', 'Housing Units | Vacant'],


            # final append
            arcadia_census_data.append(new_census_entry)
            if self.printLogging:
                print('break')
                break;

        # Final output
        self.outputData(arcadia_census_data)


        # averages