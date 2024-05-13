from pymongo import MongoClient
from Method.getSearch import search_collection
client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")
db = client["dental_disease"]

def getDocId(h: str, r: str, t: str):
    lst = []
    collection = db[search_collection(h)]
    result = collection.find({"$and": [{"head": h}, {"relation": " " + r}, {"tail": " " + t}]})
    for i in result:
        lst.append(i.values())
    return str(list(lst[0])[0])

def formatDataToUpdate(h: str, r: str, t: str):
    return {"head":h, "relation":" " + r, "tail":" " + t}
