from os import set_inheritable
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import apiFunc
import json

def main():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    client = gspread.authorize(creds)

    #sheet = client.open('AMB Memory Bank').sheet1
    sh = client.open_by_url('https://docs.google.com/spreadsheets/d/1cCWhhm2x2trjpReknfWsQ_4lDvN1smBknkUYjB2SICk/edit#gid=0')
    sheetName = datetime.now().strftime('%b %Y').upper()
    sheet = sh.worksheet(sheetName)

    dataDict = sheet.get_all_records()

    today = datetime.now().strftime('%#d/%#m/%y')
    myName = 'Wong Weng Hong'
    with open('selfInfo.json', 'r') as file:
        data = json.load(file)
        myName = data['name']
        row = data['row']
        col = int(datetime.now().strftime('%#d')) + 1

    def findRow(data, start):
        if start > 2:
            start -= 2
        else:
            start = 1
        for i in range(start,len(data)+2):
            if sheet.cell(i,2).value == myName:
                return i

    def findCol(data, start, item):
        if start > 2:
            start -= 2
        else:
            start = 1
        myList = list(dataDict[0])
        for i in range(start, len(myList)+2):
            if sheet.cell(1,i).value == item:
                return i

    #checks
    def checks(dataDict, myName, row, col):
        if sheet.cell(row,2).value != myName:
            print('fk u row')
            myRow = apiFunc.findMe(dataDict, 'NAME', myName)
            row = findRow(dataDict, myRow)
            with open('selfInfo.json', 'w') as file:
                data['row'] = row
                json.dump(data,file)

        if sheet.cell(1, col).value != today:
            col = findCol(dataDict, col, today)

        return row, col

    row, col = checks(dataDict, myName, row, col)
    sheet.update_cell(row, col, 'Y')
    print('DONE OUV GOOGLE SHEETS!')

if __name__ == '__main__':
    main()
