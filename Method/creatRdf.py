import csv
from rdflib import Graph, Literal, URIRef, Namespace, RDF
from rdflib.namespace import RDF, RDFS, Namespace
from pymongo import MongoClient
from Method.getSearch import cleanData, queryData
client = MongoClient("mongodb+srv://dentlore:Lv8uNUt5u08nZLUI@cluster0.zq9fxeg.mongodb.net/")

db = client["dental_disease"]
collection = db["caries"]
node = []
relation = []
frequency = []
result = []

def create_rdf(data,topic):
    g = Graph()
    ns = Namespace(f"http://dentlore.online/{topic}/")
    for row in data:
        subject = URIRef(ns[row[0].replace(" ","_")])
        predicate = URIRef(ns[row[1].replace(" ","_")])
        obj = Literal(ns[row[2].replace(" ","_")])
        g.add((subject, predicate, obj))
    return g

def rdf_disease(topic):
    data = cleanData(queryData(db[topic]))
    g = create_rdf(data,topic)
    print(g.serialize(format='pretty-xml'))
    return g.serialize(format='pretty-xml')

# def write_rdf(graph, file_path):
#     with open(file_path, 'wb') as f:
#         f.write(graph.serialize(format='pretty-xml'))

# data = cleanData(queryData())
# print()
# print(data)
# g = create_rdf(data)
# print(g.serialize(format='pretty-xml'))

# g.serialize(destination='example.rdf', format='pretty-xml')
# write_rdf(g, "firstrdf.rdf")


# rdf_disease("caries")