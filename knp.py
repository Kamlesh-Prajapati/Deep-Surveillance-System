from random import choice
from redis import Redis
from rq import Queue
import requests
import boto3
import mysql.connector as mysql
from Deploy import *
from gmail import *

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "final_year"
)

s3=boto3.client('s3')

gmail = Queue('gmail',connection=Redis())

def get_video(link):
    print(link)
    temp=link.split('.')[0]
    s = "/home/kamlesh/Desktop/Downloaded_Videos/"+link
    #d = "/home/kamlesh/eclipse-workspace/WebApp/src/main/resources/public/images/"+temp
    d="/home/kamlesh/Desktop/WebFolder/videos/"+temp
    s3.download_file('videos151824-amplify','public/'+link,s)
    Solution(s,d)
    cursor = db.cursor()
    query = "INSERT INTO violence (url,date) VALUES (%s,CURDATE())"
    store = "videos/"+link
    values = (store,)
    cursor.execute(query, values)
    db.commit()
    print(cursor.rowcount, "record inserted")
    gmail.enqueue(send_mail,"/home/kamlesh/Desktop/WebFolder/videos/"+link)
    print("-----------------Work is Done---------------------")
    
