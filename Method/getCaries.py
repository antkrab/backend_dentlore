from pymongo import MongoClient
client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")
db = client["dental_disease"]
collection = db["caries"]
node = []
relation = []
frequency = []
# passmongo QKUbcy3AH2ZL3P2


def queryData():
    lst = []
    data = collection.find()
    for obj in data:
        lst.append(obj.values())
    return lst

def cleanData(lst):
    tmp = []
    for dict in lst:
        tmp_lst = list(dict)
        head = tmp_lst[1]
        if tmp_lst[2][0] == " ":
            edge = tmp_lst[2][1:]
        else:
            edge = tmp_lst[2]
        
        if tmp_lst[3][0] == " ":
            tail = tmp_lst[3][1:]
        else:
            tail = tmp_lst[3]
        if head[-1] == " ":
            head = head[0:-1]
        elif tail[-1] == " ":
            tail = tail[0:-1]
        tmp.append([head.replace("_"," "), edge.replace("_"," "), tail.replace("_"," ")])
    return tmp


def countFrequency(lst):
    for row in lst:
        if row[0] not in node:
            node.append(row[0])
            frequency.append(1)
        else:
            frequency[node.index(row[0])] += 1
        if row[1] not in relation:
            relation.append(row[1])
        if row[2] not in node:
            node.append(row[2])
            frequency.append(1)
        else:
            frequency[node.index(row[2])] += 1

def formatForNodeToJson():
    result =[]
    for i in range(len(node)):
        data = {"id":node[i],"value": frequency[i],"label": node[i]}
        result.append(data)
    return result
def formatForRelationToJson(lst):
    result = []
    for row in lst:
        head = row[0][0].upper() + row[0][1:]
        tail = row[2][0].upper() + row[2][1:]
        data = {"from":head,"to":tail,"label":row[1]}
        result.append(data)
    return result



data_clean = cleanData(queryData())
countFrequency(data_clean)
result_node = formatForNodeToJson()
result_edge = formatForRelationToJson(data_clean)
