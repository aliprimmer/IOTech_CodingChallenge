import json
import re

# open JSON file

def openFile(fileName):
    #Used to open files and parse JSON   
    file = open(fileName)
    file = json.load(file)
    return file

def extractData(data):
    #used to store all data to be returned
    uuid = []
    payloads = []
    newStructure = []
    #temporary store to be updated on each loop and add data in the desired format    
    adder = {'Name': '', 'Type': '', 'Info': '', 'Uuid': '', 'PayloadTotal': 0}
    for element in data:
        #call function to add payloads and store them in payloads array
        tempPayload = calcPayloads(element)
        payloads.append(tempPayload)
          
        #use uuid regular expression found online to identitfy uuids with strings and store the Uuids
        uuid_extract_pattern = "[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}"
        tempUuid = re.findall(uuid_extract_pattern, element['Info'])[0]
        uuid.append(tempUuid)
        
        #edit adder to include updated fields and add these as an element in with newStructure array   
        adder['Name'] = element['Name']
        adder['Type'] = element['Type']
        adder['Info'] = element['Info']
        adder['Uuid'] = tempUuid
        adder['PayloadTotal'] = tempPayload
        newStructure.append(adder.copy())
        
        #return data to be used later
    return uuid, payloads, newStructure

def calcPayloads(data):
    #add all payloads and return results 
    payload = 0 
    for pay in data['Sensors']:
        payload += pay['Payload']  
    return payload

def orderData(data):
    orderedData = []
    names = []
    #sort all names alphabetically then use names to add in elements in the correct order to storage array 
    for element in data:
        names.append(element['Name'])
    sortedNames = sorted(names, key=str.casefold)
    for name in sortedNames:
        for element in data:
            if(element['Name'] == name):
                orderedData.append(element)
    return orderedData 

parsedData = openFile('data\devices.json')
data = parsedData['Devices']
        
extractedIDs, payloads, reformattedData = extractData(data)
#print(data)
#print(extractedIDs)
#print(payloads)
#print(reformattedData)

sortedData = orderData(reformattedData)

formattedData = {'Devices': sortedData}

outputJSON = json.dumps(formattedData)

# write to json
with open("solution.json", "w") as outfile:
    json.dump(formattedData, outfile, indent=4)


