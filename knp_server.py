from redis import Redis
from rq import Queue
from socket import *
from codecs import decode
from knp import get_video

server = socket(AF_INET, SOCK_STREAM)
server.bind(('192.168.43.147',7005))
server.listen(5)
video = Queue('video',connection=Redis())


while True: 
	print("Waiting for connection...")
	client, address = server.accept()
	print("connected")
	msg = decode(client.recv(1024),'ascii')
	print(msg)
	video.enqueue(get_video, msg)
	client.close()


