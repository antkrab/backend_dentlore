from pymongo import MongoClient
client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")
db = client["dental_disease"]
node = []
relation = []
frequency = []
all_node = []


def queryData(collection):
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
        elif row[0] in node:
            frequency[node.index(row[0])] += 1
        if row[1] not in relation:
            relation.append(row[1])
        if row[2] not in node:
            node.append(row[2])
            frequency.append(1)
        elif row[2] in node:
            frequency[node.index(row[2])] += 1


def search_collection(hn):
    for collec_list in db.list_collection_names():
        collection = db[collec_list]
        data_clean = cleanData(queryData(collection))
        tmp_node = []
        for data in data_clean:
            if data[0] not in tmp_node:
                tmp_node.append(data[0])
            if data[2] not in tmp_node:
                tmp_node.append(data[2])
        if hn in tmp_node:
            return collec_list
        
def formatForNodeToJson_HT(highlight_node):
    result =[]
    highlight_node = highlight_node.split(",")
    highlight_node = [word.lower() for word in highlight_node]
    for word in highlight_node:
        collection = search_collection(word)
        break
    countFrequency(cleanData(queryData(db[collection])))
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

def formatForRelationToJson(highlight_node):
    highlight_node = highlight_node.split(",")
    highlight_node = [word.lower() for word in highlight_node]
    for word in highlight_node:
        collection = search_collection(word)
        break
    lst = cleanData(queryData(db[collection]))
    result = []
    for row in lst:
        data = {"from":row[0],"to":row[2],"label":row[1]}
        result.append(data)
    return result
 

        
# HTresult = formatForNodeToJson_HT("EnameL,operative treatment")
# print(HTresult)
# print(formatForRelationToJson("enamel,dentin"))
    