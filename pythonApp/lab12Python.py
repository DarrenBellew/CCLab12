import boto.sqs
import boto.sqs.queue
import requests
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys


# curl -s -X GET -H 'Accept: application/json'
# http://localhost:5000/queues | python	-mjson.tool

def get_conn():
	res = requests.get('http://ec2-52-30-7-5.eu-west-1.compute.amazonaws.com:81/key')
	keyId, key = res.text.split(":")
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id=keyId, aws_secret_access_key=key)
	return conn

# @app.route('/images', methods=['GET'])

# GET /queues List all queues
# POST /queues Create a new queue
# DELETE /queues/<qid>	Delete a specific queue
# GET /queues/<qid>/msgs Get a message, return it to the user	
# GET /queues/<qid>/msgs/count Return the number of messages in a queue
# POST /queues/<qid>/msgs Write a new message to a queue
# DELETE /queues/<qid>/msgs Get	and	delete a message from the queue

# List all queues
@app.route("/queues", methods=["GET"])
def ListAllQueues():
	rs = get_conn().get_all_queues()
	all[]
	for q in rs:
		all.append(q.name)
	resp = json.dumps(all)
	return Response(response=resp, mimetype="application/json")

@app.route("/queues", methods["POST"])
def CreateAQueue(queueName):
	queueName = "C13729611_" + queueName
	conn = get_conn()
	rs = conn.get_all_queues()
	conn.create_queue(queueName)
	resp = "queue '" + queueName + "'' is now created."
	resp = {"response": resp}
	resp = json.dumps(resp)
	return Response(response=resp, mimetype="application/json")


@app.route("/queues", methods["DELETE"])
def DeleteAQueue(queueName):
	conn = get_conn()
	rs = conn.get_all_queues()
	resp = ""
	if "/747210654827/"+queueName in rs:
		conn.delete_queue(conn.get_queue('queueName'))
		resp = "queue '" + queueName + "' is now deleted."
	else:
		resp = "queue '" + queueName + "' is not deleted."

	resp = {"response": resp}

@app.route("/queues/<name>/msgs/count", methods["GET"])
def CountQueues(name):
	name = "C13729611_"+name
	conn = get_conn()
	rs = conn.get_all_queues()
	resp = str(rs.count())
	resp = {"response":resp}
	resp = json.dumps(resp)
	return Response(response = resp, mimetype="application/json")

@app.route("/queues/<name>/msgs", methods["POST"])
def WriteMessage(name, message):
	name = "C13729611_"+name
	conn = get_conn()
	rs = conn.get_queue(queueName)

	m = Message()
	m.set_body(message)
	resp = "Failed to write message"
	if rs is not None:
		q.write(m)
		resp = "Message '" + m.get_body() + "' is written to queue: " + name

	resp = {"Response": resp}
	resp = json.dumps(resp)
	return Response(response=resp,mimetype="application/json")

@app.route("/queues/<name>/msgs", methods["GET"])
def ReadMessage(name):
	name = "C13729611_"+name 
	conn = get_conn()
	rs = conn.get_conn()

	m = []
	for i in range(0, q.count()):
		m.append(rs.read(60).get_body())

	resp = json.dumps(m)
	return Response(response=resp, mimetype="application/json")

@app.route("/queues/<name>/msgs", methods["DELETE"])
def ConsumeMessage(name):
	name = "C13729611_" + name
	conn = get_conn()
	rs = conn.get_conn()
	resp = {"Response": "Remove message " + str(deleteMessage(rs, name))}
	resp = json.dumps(resp)

# Get the keys from a specific url and then use them to connect to AWS Service

# Set up a connection to the AWS service.

# Get a list of the queues that exists and then print the list out
