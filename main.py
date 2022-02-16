#main code here
#Includes: connect to to redis server, read database items and then index it into redis server, 
#search function (single condition query and multiple condition query) 

import json
import re
import time
from dbs import pg_db #import database implementation here (maybe is mongo / postgres or mysql ?)
from flask import Flask, jsonify, Response
from redisearch import Client, TextField, IndexDefinition, Query

app = Flask(__name__) #init flask server instance

#setting up the routers logic

#Handle request to root of domain (or http://localhost:5000)
@app.route("/")
def index():
    return "Welcome to Redis Search Example"

#api endpoint: /api/v1/search/
'''
/api/
/v1 >> version 1.0
/search >> action to do
'''
@app.route("/api/v1/search/<path:query>") #handle request for shipmet indexing from client
def search(query):
    # Creating a client with a given index name (the index must be existing)
    client  = Client("IdxBooks")  #point to book index on the redis server
    q       = Query(queryNormalize(query) + "*").verbatim() #we add "*" to end of query string to search everything with start string from query string
    res     = client.search(q) #execute query

    result = []
    # check the results
    if res.total > 0:
        result = res.docs #redis search results is docs (it includes all result items in it's list')
    
    response = Response(response=searchResultRender(result), status=200, mimetype="application/json")
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

#api endpoint: /api/v1/index/start
'''
We connect to the database server and get data then insert into the redis server
/api/
/v1/ >> version 1.0
/index/start >> action to do
'''
@app.route("/api/v1/index/start")
def indexData():
    # Creating a client with a given index name
    client  = Client("IdxBooks")  #point to book index on the redis server
    try: 
        client.info() #this method will get index information from the redis server
    except Exception: #if we got an exception that means the index is not available so we must create a new index else we don't need create anymore
        # IndexDefinition is avaliable for RediSearch 2.0+
        definition = IndexDefinition(prefix=['doc:', 'article:'])

        #first of all, we need to create the index with a specific index definition like below
        #TextField is type of field (string), weight=5.0 means we focus on title or author than more other fields
        client.create_index((TextField("title", weight=5.0), 
                                                            TextField("isbn"), 
                                                            TextField("category"), 
                                                            TextField("author")), definition = definition)

    db_conn = pg_db.connect() #connect to database
    items = db_conn.getAllDataItems(); #suppose we have about 1K book items in database
    db_conn.close();

    #loop on each item and insert it into the redis memory (we can use thread if the total of items is greater ~ 100k -> 1M)
    try:
        for item in items:
            #we use .hset to insert the item into the index stack, we have to set a document id by combine 'doc:' with book_id (eg: 'doc:12345')
            client.redis.hset('doc:' + str(item['book_id']),
                                mapping={'title': item['book_title'], 
                                'isbn': item['book_isbn'], 'author': item['book_author'], 
                                'category': item['book_category']})
    except Exception as e:
        print("Error message") # print error message in console or terminal
        return "Error message" # return error message to client
    finally:
        print("Completed") # print message in console or terminal
        
    return "Completed" # return message to client


#Ultiliti functions here ==============================================================================>
'''
Clean some special characters from the query string
'''
def queryNormalize(query):
    # Suppose: want to clean some special characters from the query string
    # Further: we can use regex (regular expression) instead
    return query.replace("-","").replace("*","").replace("//","")
'''
This is a simple function
'''
def searchResultRender(results):
    #TODO:we can format results here before reponse to the client in json format or any type you want 
    json_data = json.dump(results)
    return json_data

#EOF of ultiliti functions ============================================================================<



#Server running functions =================================================================>
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)