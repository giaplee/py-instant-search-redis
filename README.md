# py-instant-search-redis
**Source code example for how to build an instant search (or real-time search) function with Redis in python.**

>This short source code will helps you understand about Redis Search feature and how to implement it into your
project ideas (eg: use real-time search function for any ecommerce website like Book/Movie/Product/etc..) helps
the user can search a product by tite/name/price/origin/category/... very quickly. 
Especially, this function can combine multiple search condition together which helps the system return the result with high accuracy.

**Technical stack:**
1. Programming language: Python
2. Backend server: Flask
3. Redis (use redis cli and Redis server + Redisearch lib):
4. Data source: you can access data source from MongoDB, MySQL, Postgres, etc and then index it into redis memory (I don't demo it here with this version)

**Deploy/Running environment**
1. OS: Linux (Ubuntu or CentOS or other)
2. If you want to use/try it on Windows, you can use Docker (with a linux image)


**Prerequisite**
1. Install python environment
2. Install Flask (https://flask.palletsprojects.com/en/2.0.x/installation/)
3. Install Docker Engine on your development host if you want to run code or redis server by Docker container
- Withow Docker engine desktop (on MacOS):
```python
# Install hyperkit and minikube
brew install hyperkit
brew install minikube

# Install Docker CLI
brew install docker
brew install docker-compose

# Start minikube
minikube start

# Tell Docker CLI to talk to minikube's VM
eval $(minikube docker-env)

# Save IP to a hostname
echo "`minikube ip` docker.local" | sudo tee -a /etc/hosts > /dev/null

# Test
docker run hello-world
```

- With Docker Engine Desktop app (on MacOS):
Read this article (https://docs.docker.com/desktop/mac/install/)

4. Install Redis client and Redis server:
- Redis Server (includes RedisSearch library)
 >You can run Redis server in a Docker container instead of run in on your host (this method help you install Redis quickly)
 >Redis server docker here (includes redis search library): `docker run -p 6379:6379 redislabs/redisearch:latest`
- Redis client for Python: (https://oss.redis.com/redisearch/1.4/python_client.html#installing) 
or just used this command with pip: `$ pip install redisearch`
 >Example code after installed Redis Client library 
 >>[More about redisearch API here](https://oss.redis.com/redisearch/1.4/python_client.html)
 >>[More about redis command/synctax here](https://oss.redis.com/redisearch/1.4/Commands.html)
 ```python
 from redisearch import Client, TextField, NumericField, Query

# Creating a client with a given index name
client = Client('myIndex')  #you can set any index name you want

# Creating the index definition and schema
client.create_index([TextField('title', weight=5.0), TextField('body')])

# Indexing a document
client.add_document('doc1', title = 'RediSearch', body = 'Redisearch implements a search engine on top of redis')

# Simple search
res = client.search("search engine")

# the result has the total number of results, and a list of documents
print res.total # "1"
print res.docs[0].title

# Searching with snippets
res = client.search("search engine", snippet_sizes = {'body': 50})

# Searching with complex parameters:
q = Query("search engine").verbatim().no_content().paging(0,5)
res = client.search(q)
```


**My development environment:**
1. Laptop/PC: MacOS BigSur
2. Python version: python3.8
3. Install Redis Cli for Mac
- Redis cli helps we can connect and interact with Redis server from command-line
>we can use `FT._LIST` to list all existing indexs on the Redis server (or create, delete, view an index information)
- Install steps on MacOS's terminal
```python
brew update
brew install redis

//To check
redis-cli ping
//if you are getting PONG Then you are good to go
```

**Now is time to start to code**
- Getting started >>
