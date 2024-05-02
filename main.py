import uvicorn
from fastapi import FastAPI, Response
from pymongo import MongoClient
from config import DB_URL
from pydantic import BaseModel
from bson.objectid import ObjectId
from Method.getCaries import result_node,result_edge
import json
from fastapi.responses import JSONResponse
from Method.getCaries_search import formatForNodeToJson_HT
from Method.creatRdf import rdf_disease

client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")
db = client["dental_disease"]
app = FastAPI()

@app.get("/")
async def root():
    return {"root api"}

@app.get("/getnode")
async def getnode():
    return JSONResponse(result_node)

@app.get("/getedge")
async def getedge():
    return JSONResponse(result_edge)

@app.get("/getnode_search/{q}")
async def getnode_search(q:str):
    return JSONResponse(formatForNodeToJson_HT(q))

@app.get("/getrdf")
async def getrdf():
    return rdf_disease()

@app.get("/downloadrdf_caries")
async def downloadrdf_caries():
    response = Response(content=rdf_disease(), media_type="application/rdf+xml")
    response.headers["Content-Disposition"] = "attachment; filename=dental_caries.rdf"
    return response