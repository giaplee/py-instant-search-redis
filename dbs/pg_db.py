#code for postgres database implementation
import psycopg2 #we use postgres for python lib here

#This function will create a connection to the database
def connect():
    try:
        connection = psycopg2.connect("user = demo_user",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      password = "pc209e66f47c905fe557d97af03103fabb",
                                      database = "book_db")

    except (Exception, psycopg2.Error) as error :
        print('Error while connecting to PostgreSQL', error)
    finally:
            if(connection):
                print("PostgreSQL connection is connected")
                return connection
    return None

'''
This function will get all item in the database
'''
def getAllDataItems(connection):
    items = [] #we get all data items from the database by connection
    return items