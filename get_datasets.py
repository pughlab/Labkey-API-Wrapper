#!/usr/bin/python2
import os, json, argparse, shutil

from labkey.utils import create_server_context
from labkey.exceptions import QueryNotFoundError
from labkey.query import select_rows

wordsToChangeDict = {"BEGINNING_DATE_OF_TREATMENT": "START_DATE", "END_DATE_OF_TREATMENT": "STOP_DATE",
                     "DATE": "DATE_OF_BIRTH", "PARTICIPANTID": "PATIENT_ID"}

metadataDict = {'METASTATIC_SITE': 'Override TUMOR_SITE (patient level attribute)',
                'AGE': 'Age at which the condition or disease was first diagnosed, in years (number)',
                'REGISTRATION_DATE': 'The date the patient was registered for treatment',
                'PATIENT_ID': 'Patient Identifier', 'PRIMARY_SITE': 'Override TUMOR_SITE (patient level attribute)',
                'DATE_OF_DEFINITIVE_DIAGNOSIS': 'Date of Diagnosis', 'SAMPLE_ID': 'Sample Identifier',
                'CANCER_TYPE_DETAILED': 'Cancer Type Detailed, a sub-type of the specified CANCER_TYPE',
                'OS_MONTHS': 'Overall Survival (Months)', 'GENDER': 'Gender or sex of the patient (string)',
                'DFS_MONTHS': 'Disease Free (Months)', 'DFS_STATUS': 'Disease Free Status',
                'OS_STATUS': 'Overall Survival Status'}

datasetsWithMetadata = ["patients", "samples", "treatments"]


def get_options():
    parser = argparse.ArgumentParser(description="Process the commandline arguments for labkey api")
    parser.add_argument("-p", "--project", type=str, required=True, help="input project name on Labkey")
    parser.add_argument("-j", "--json", type=str, help="output file name including path")
    parser.add_argument("-c", "--cbio", type=str, help="cbio output if needed")

    return parser.parse_args()


def createDirectory(dirName):
    if (os.path.isdir(dirName)):
        shutil.rmtree(dirName)

    os.mkdir(dirName)


def renameColumnNames(inputList):
    outputList = []

    for val in inputList:
        val = val.upper()

        if val in wordsToChangeDict.keys():
            val = wordsToChangeDict.get(val)
        outputList.append(val)

    return outputList


def main():
    args = get_options()
    dictionaryFromFile = []

    with open('data/dictionary.txt', 'r') as inf:
        for line in inf:
            dictionaryFromFile.append(eval(line))

    labkeyDictionary = dictionaryFromFile[0]

    labkeyServer = 'labkey.uhnresearch.ca'
    contextPath = 'labkey'
    schema = 'study'

    projectName = args.project.lower()

    if projectName not in labkeyDictionary:
        print('Caught bad project name. Please pass in a project name that is on labkey.')
        exit()
    projectDatasets = labkeyDictionary[projectName]

    outputFolder = args.project + "_results"

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)



    print("Create a server context")
    serverContext = create_server_context(labkeyServer, projectName, contextPath, use_ssl=True)

    if args.json:
        print("JSON output required.")
        outputFile = os.path.join(outputFolder, args.project.lower() + ".json")
        file = open(outputFile, "w")
        print("Created a " + outputFile + " file.")

    dict = {}

    if (args.cbio):
        print("Cbio output required.")
        outputCbioDir = args.project.lower()
        createDirectory(outputFolder + "/" + outputCbioDir)



    for table in projectDatasets:

        try:

            result = select_rows(serverContext, schema, table)

            if result is not None:
                row_to_add = result["rows"]

                if (args.cbio):
                    newFile = open(outputFolder + "/" + outputCbioDir + "/" + table + ".txt", "w")
                    header = True

                for idx in range(len(row_to_add)):

                    row_to_add[idx] = removeUnnecessaryColumns(row_to_add[idx])
                    row_to_add[idx] = convertUnicodeToASCII(row_to_add[idx])
                    row_to_add[idx] = removeTrailingSpacesInValues(row_to_add[idx])
                    row_to_add[idx] = changeDateTimeFormat(row_to_add[idx])
                    row_to_add[idx] = convertKeyToUpperCase(row_to_add[idx])
                    row_to_add[idx] = renameSpecificColumns(row_to_add[idx], table)


                    if (args.cbio):

                        rowDict = row_to_add[idx]
                        rowDictHeader = ""
                        rowDictHeaderValuesList = []
                        rowDictvalues = ""

                        if (header):
                            for key in rowDict.keys():
                                rowDictHeader += key + "\t"
                                rowDictHeaderValuesList.append(rowDict[key])

                            rowDictHeader.strip()
                            if table.lower() in datasetsWithMetadata:
                                # createMetadata(inputString, rowDictHeaderValuesList)
                                newFile.write(createMetadata(rowDictHeader, rowDictHeaderValuesList) + "\n")
                            newFile.write(rowDictHeader + "\n")
                            header = False

                        for key in rowDict.keys():

                            if (type(rowDict[key]) != str):
                                rowDictvalues += str(rowDict[key]) + "\t"
                            else:
                                rowDictvalues += rowDict[key] + "\t"
                        rowDictvalues.strip()
                        newFile.write(rowDictvalues + "\n")

                if (args.cbio):
                    newFile.close()

                dict[table] = row_to_add

                print("From the dataset " + table + ", the number of rows returned: " + str(result['rowCount']))
            else:
                print('select_rows: Failed to load results from ' + schema + '.' + table)
        except QueryNotFoundError:
            print('Error: The table ' + table + " was not found.")

    if args.json:
        file.write(json.dumps((dict), indent=4, sort_keys=True))
        file.close()


def convertUnicodeToASCII(input):
    if isinstance(input, dict):
        return {convertUnicodeToASCII(key): convertUnicodeToASCII(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convertUnicodeToASCII(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def removeUnnecessaryColumns(row_to_add):
    row_to_add.pop(u'_labkeyurl_PATIENT_ID', None)
    row_to_add.pop(u'_labkeyurl_ParticipantId', None)
    row_to_add.pop(u'lsid', None)

    return row_to_add


def changeDateTimeFormat(myDict):
    for key in myDict.keys():
        if (((type(myDict[key]) == str) and ("00:00:00" in myDict[key])) or (
                (isinstance(myDict[key], unicode) and (u'00:00:00' in myDict[key])))):
            myDict[key] = myDict[key].split(" ")[0]

    return myDict


def convertKeyToUpperCase(rowDict):
    result = {}
    for key, value in rowDict.items():
        newKey = '_'.join(key.split()).upper()
        result[newKey] = value

    return result


def renameSpecificColumns(rowDict, datasetName):
    if datasetName == "Patients":
        rowDict["DATE_OF_BIRTH"] = rowDict.pop("DATE")

    return rowDict


def removeTrailingSpacesInValues(rowDict):
    for key in rowDict.keys():
        val = rowDict[key]

        if (type(val) == str):
            rowDict[key] = val.strip()

        if (type(val) is not int) and (type(val) is not float) and (val != None):
            if val.strip().isdigit():
                rowDict[key] = int(val)

    return rowDict


def createMetadata(inputString, rowDictHeaderValuesList):
    rowDictHeader = inputString.strip().split()
    # print(rowDictHeaderValuesList)

    # print(rowDictHeader)
    newStr = "#"
    inputStrOfTypes = "#"
    onesStr = "#"

    for i in rowDictHeader:
        # print(i, type(i))

        if i in metadataDict:

            newStr += metadataDict[i] + "\t"
        elif i not in metadataDict:
            newStr += i + "\t"

    for i in rowDictHeaderValuesList:
        # print(i, type(i))
        if type(i) == int:

            inputStrOfTypes += "NUMBER" + "\t"
        elif type(i) == str:
            # print("String")
            inputStrOfTypes += "STRING" + "\t"
        onesStr += "1" + "\t"

    # print(inputStrOfTypes)
    newStr.strip()
    inputStrOfTypes.strip()
    onesStr.strip()

    # print("onesStr" + onesStr)
    # print(inputStrOfTypes)

    outputStr = newStr + "\n" + newStr + "\n" + inputStrOfTypes + "\n" + onesStr
    # print(inputList)
    # print(newStr)
    # print("-------------------\n")
    # print(outputStr)

    return outputStr


if __name__ == "__main__":
    main()
    myDict = {'DATE': '2018/06/25   ', 'TIME_POINT': 'Post-Op  ', 'TEST_RESULT': 1, 'END_DATE_OF_TREATMENT': 'NA',
              'BEGINNING_DATE_OF_TREATMENT': 455, 'EVENT_TYPE': 'CTDNA BLOOD DRAW', 'COLLECTION_DATE': '2018/06/25',
              'PATIENT_ID': 'CMP-02-01'}

    str = "OS_MONTHS       REGISTRATION_DATE       GENDER  AGE     MALIGNANCY      HISTOLOGY_CYTOLOGY_DIAGNOSIS    DFS_MONTHS      YEAR_OF_BIRTH   RACE    DFS_STATUS      DATE_OF_DEFINITIVE_DIAGNOSIS   SLIDE_ID        PATIENT_ID      DATE_OF_BIRTH   OS_STATUS       ETHNICITY"

    # createMetadata(str)

    # result  = removeTrailingSpacesInValues(myDict)
