import uvicorn
from fastapi import FastAPI, Response, UploadFile, File, HTTPException
from pymongo import MongoClient
from config import DB_URL
from pydantic import BaseModel
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse, StreamingResponse
from Method.creatRdf import rdf_disease
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO
from Method.getSearch import formatForNodeToJson_HT, formatForRelationToJson, search_collection, cleanData, queryData
from Method.getNodeFromButton import getEdgeFromDb
from bson.objectid import ObjectId
from Method.getDataForUpdate import getDocId,formatDataToUpdate
from Method.downloadcsv import generate_csv, createDataForCsv
from Method.getCaries import formatForRelationToJson_normal

client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")
db = client["dental_disease"]
password_admin = "ajarnart"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
async def root():
    return {"root api"}

@app.get("/getnode_search")
async def getnode_search(q:str):
    return JSONResponse(formatForNodeToJson_HT(q))

@app.get("/getedge_search")
async def getedge_search(q:str):
    return JSONResponse(formatForRelationToJson(q))

@app.get("/getrdf")
async def getrdf(topic: str):
    try:
        return rdf_disease(topic)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/downloadrdf")
async def downloadrdf_caries(topic: str):
    try:
        if topic not in db.list_collection_names():
            return {"message":"not found"}
        else:
            response = Response(content=rdf_disease(topic), media_type="application/rdf+xml")
            response.headers["Content-Disposition"] = f"attachment; filename={topic}.rdf"
            return response
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/add_data_from_csv")
async def add_data_from_csv(collection_name: str, password:str, file: UploadFile = File(...)):
    if password != password_admin:
        return {"message": "admin only"}
    if collection_name in db.list_collection_names():
        return {"message": "Collection already exists"}
    db.create_collection(collection_name)


    collection = db[collection_name]

    try:
        content = await file.read()
        csv_content = content.decode("utf-8")
        csv_data = pd.read_csv(StringIO(csv_content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(e)}")

    inserted_ids = []
    try:
        for index, row in csv_data.iterrows():
            data = row.to_dict()
            inserted_data = collection.insert_one(data)
            inserted_ids.append(str(inserted_data.inserted_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting data into MongoDB: {str(e)}")

    return {"message": "Data from CSV added successfully", "inserted_ids": inserted_ids}


@app.get("/collections")
async def get_collections():
    return db.list_collection_names()

@app.get("/getedgeSearch")
async def getedgeSearch(node:str):
    try:
        return JSONResponse(getEdgeFromDb(node))
    except:
        return {"message": "not found"}

@app.put("/update_data")
async def update_document(old_h: str, old_r: str, old_t: str, new_h: str, new_r: str, new_t: str, password:str):
    if password != password_admin:
        return {"message": "admin only"}
    old_h = old_h.lower()
    old_r = old_r.lower()
    old_t = old_t.lower()
    new_h = new_h.lower()
    new_r = new_r.lower()
    new_t = new_t.lower()
    collection = db[search_collection(old_h)]
    document_id = getDocId(old_h,old_r,old_t)
    new_data = formatDataToUpdate(new_h,new_r,new_t)
    result = collection.update_one({"_id": ObjectId(document_id)}, {"$set": new_data})
    if result.modified_count == 1:
        return {"message": "success"}
    else:
        return {"message": "not found"}


@app.post("/add_data")
async def addData(topic: str,head: str, relation: str, tail: str, password:str):
    if password != password_admin:
        return {"message": "admin only"}
    if topic in db.list_collection_names():
        colletion = db[db.list_collection_names()[db.list_collection_names().index(topic)]]
        result = colletion.insert_one({"head":head, "relation": " " + relation, "tail": " " + tail})
    else:
        return {"message": "not found"}
    if result.inserted_id:
        return {"message": "success"}
    else:
        raise HTTPException(status_code=400, detail="Item could not be added")
    
@app.delete("/delete_data")
async def deleteData(head: str, relation: str, tail: str, password:str):
    if password != password_admin:
        return {"message": "admin only"}
    
    try:
        head = head.lower()
        relation = relation.lower()
        tail = tail.lower()
        collection = db[search_collection(head)]
    except :
        return {"message": "not found"}
    document_id = getDocId(head,relation,tail)
    print(document_id)
    result = collection.delete_one({"_id": ObjectId(document_id)})
    if result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/delete_topic")
async def dropcollection(collection_name:str, password:str):
    if password != password_admin:
        return {"message": "admin only"}
    
    if collection_name in db.list_collection_names():
        collection = db[db.list_collection_names()[db.list_collection_names().index(collection_name)]]
    else:
        return {"message": "not found"}
    try:
        collection.drop()
        return {"message": "Collection dropped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/isAdmin")
async def isAdmin(password: str):
    if password == password_admin:
        return JSONResponse(True)
    else:
        return JSONResponse(False)

@app.get("/downloadCsv")
async def downloadCSV(topic: str):
    csv_data = generate_csv(createDataForCsv(topic))
    response = StreamingResponse(
        csv_data,
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = f"attachment; filename={topic}.csv"
    return response

@app.get("/getEdit")
async def getEdit(topic: str):
    try:
        if topic in db.list_collection_names():
            data = cleanData(queryData(db[topic]))
            return JSONResponse(formatForRelationToJson_normal(data))
        else:
            {"message": "not found"}


    except Exception as e:
        return {"message": str(e)}