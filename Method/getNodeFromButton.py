from pymongo import MongoClient
client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")
db = client["dental_disease"]
from Method.getSearch import search_collection, cleanData
from Method.getCaries import formatForRelationToJson_normal

def getEdgeFromDb(node):
    lst = []
    node = node.lower()
    collection = db[search_collection(node)]
    result = collection.find({"$or": [{"head": node}, {"tail": " " + node}]})
    for i in result:
        lst.append(i.values())
    return formatForRelationToJson_normal(cleanData(lst))

