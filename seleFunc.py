from os import set_inheritable
from re import I
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

def findRow(sheet, data, start, name):
    if start > 8:
        start -= 8
    else:
        start = 1
    
    for i in range(start, len(data) + 2):
        current = sheet.cell(i,3).value
        if current:
            if name in current:
                return i
        print(sheet.cell(i,3).value, name)
        

def findCol(sheet, data, start, item):
    if start>5:
        start -= 5
    else:
        start = 1

    for i in range(start, len(data) + 4):
        if sheet.cell(1,i).value == item:
            return i

#print(sheet.cell(1,todate*4 + 1).value)
#row = findRow(dataDict, 50, myName)
#col = findCol(dataDict, 25*4, today)
#print(sheet.cell(row,col).value)

#check if person is present
def checkPresence(data, row, name, theDate):
    row = int(row)
    while True:
        currentData = data[row-2]
        if currentData['NAME'] != name:
            row = (row+1) % len(data)
        break

    if currentData[theDate].upper() == "P":
        return True
    return False




def main():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    client = gspread.authorize(creds)

    #sheet = client.open('AMB Memory Bank').sheet1
    sh= client.open_by_url('https://docs.google.com/spreadsheets/d/12kIg_INQLVE7osA7oP__khByITTgLm-abLJ5RDI1C74/edit#gid=1932046732')
    sheetName = datetime.now().strftime('%b %Y').upper()
    sheet = sh.worksheet(sheetName)

    dataDict = sheet.get_all_records()

    today = datetime.now().strftime('%#d/%#m/%y')
    todate = int(datetime.now().strftime('%#d'))

    with open('selfInfo.json', 'r') as file:
        data = json.load(file)
        myName = data['name']

    with open('rowAMB.json', 'r') as file:
        rowData = json.load(file)
        presentToday = []

    #checkRowData
    edit = False
    for i in rowData:
        currentData = sheet.cell(rowData[i],3).value
        if i not in currentData:
            print('fk u row')
            print(i, rowData[i])
            rowData[i] = findRow(sheet, dataDict, rowData[i], i)
            edit = True

    if edit:
        with open('rowAMB.json', 'w') as file:
            json.dump(rowData, file)
            print('edited')

    today = '4/1/22'
    #if user is present
    if checkPresence(dataDict, rowData[myName], myName, today):
        dataList = list(rowData.keys())
        for name in dataList:
            if name != myName:
                if checkPresence(dataDict, rowData[name], name, today):
                    presentToday.append(name)
    
    return presentToday
    
main()