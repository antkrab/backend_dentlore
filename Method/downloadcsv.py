from pymongo import MongoClient
from Method.getSearch import search_collection, cleanData, queryData
import csv
import io
client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")
db = client["dental_disease"]


def createDataForCsv(collection_input: str):
    collection = db[collection_input]
    data = cleanData(queryData(collection))
    data.insert(0, ["head", "relation", "tail"])
    return data

def generate_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    output.seek(0)
    return output