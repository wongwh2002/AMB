from xml.etree.ElementTree import TreeBuilder


def findIncr(dataDict, finding):
    incre = 0
    for i in dataDict:
        if i[finding] == '':
            incre += 1 
        else: 
            break
    return incre

def findMe(dataDict ,finding ,name):
    counter = 0
    for i in dataDict:
        counter+=1
        if i[finding] == name:
            return counter



