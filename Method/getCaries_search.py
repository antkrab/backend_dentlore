from pymongo import MongoClient
client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")
db = client["dental_disease"]
collection = db["caries"]
node = []
relation = []
frequency = []


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

def formatForNodeToJson_HT(highlight_node):
    result =[]
    highlight_node = highlight_node.split(",")
    highlight_node = [word.lower() for word in highlight_node]

    #for debuging
    # for i in highlight_node:
    #     print(i) 
    
    for i in range(len(node)):
        if node[i] in highlight_node:
            data = {"id":node[i],"value": frequency[i],"label": node[i],"color":"red"}
            result.append(data)
        else:
            data = {"id":node[i],"value": frequency[i],"label": node[i]}
            result.append(data)
    return result
def formatForRelationToJson(lst):
    result = []
    for row in lst:
        data = {"from":row[0],"to":row[2],"label":row[1]}
        result.append(data)
    return result

data_clean = cleanData(queryData())
countFrequency(data_clean)
HTresult = formatForNodeToJson_HT("EnameL,operative treatment")
result_edge = formatForRelationToJson(data_clean)
# print(HTresult)

    