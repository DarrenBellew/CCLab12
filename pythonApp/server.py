import boto.sqs
import boto.sqs.queue
import requests
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys
import json
from flask import Flask, request, redirect, url_for, Response

app = Flask(__name__)
# curl -s -X GET -H 'Accept: application/json'
# http://localhost:5000/queues | python	-mjson.tool



def get_conn():
	res = requests.get('http://ec2-52-30-7-5.eu-west-1.compute.amazonaws.com:81/key')
	keyId, key = res.text.split(":")
	conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id=keyId, aws_secret_access_key=key)
	return conn

@app.route("/")
def index():
    return """
	Available API endpoints:

	GET /containers                     List all containers
	GET /containers?state=running      List running containers (only)
	GET /containers/<id>                Inspect a specific container
	GET /containers/<id>/logs           Dump specific container logs
	GET /images                         List all images


	POST /images                        Create a new image
	POST /containers                    Create a new container

	PATCH /containers/<id>              Change a container's state
	PATCH /images/<id>                  Change a specific image's attributes

	DELETE /containers/<id>             Delete a specific container
	DELETE /containers                  Delete all containers (including running)
	DELETE /images/<id>                 Delete a specific image
	DELETE /images                      Delete all images
	"""


# List all queues
@app.route("/queues", methods=["GET"])
def ListAllQueues():
	rs = get_conn().get_all_queues()
	all = []
	for q in rs:
		all.append(q.name)
	resp = json.dumps(all)
	return Response(response=resp, mimetype="application/json")

@app.route("/queues", methods=["POST"])
def CreateAQueue():
	body = request.get_json(force=True)
	name = body["name"]

	name = "C13729611_" + name
	conn = get_conn()	
	conn.create_queue(name)
	resp = "queue '" + name + "'' is now created."
	resp = {"response": resp}
	resp = json.dumps(resp)
	return Response(response=resp, mimetype="application/json")


@app.route("/queues/<name>", methods=["DELETE"])
def DeleteAQueue(name):
	conn = get_conn()
	name = "C13729611_" + name
	rs=conn.get_queue(name)
	resp = "failed"
	if rs is not None:
		conn.delete_queue(conn.get_queue(name))
		resp = "queue '" + name + "' is now deleted."
	else:
		resp = "queue '" + name + "' is not deleted."

	resp = {"response": resp}
	resp = json.dumps(resp)
	return Response(response=resp, mimetype="application/json")

@app.route("/queues/<name>/msgs/count", methods=["GET"])
def CountQueues(name):
	name = "C13729611_"+name
	conn = get_conn()
	rs = conn.get_queue(name)
	resp = str(rs.count())
	resp = {"response":resp}
	resp = json.dumps(resp)
	return Response(response = resp, mimetype="application/json")

@app.route("/queues/<name>/msgs", methods=["POST"])
def WriteMessage(name):
	name = "C13729611_"+name
	conn = get_conn()
	rs = conn.get_queue(name)

	body = request.get_json(force=True)
	message = body["content"]

	m = Message()
	m.set_body(message)
	resp = "Failed to write message"
	if rs is not None:
		rs.write(m)
		resp = "Message '" + m.get_body() + "' is written to queue: " + name

	resp = {"Response": resp}
	resp = json.dumps(resp)
	return Response(response=resp,mimetype="application/json")

@app.route("/queues/<name>/msgs", methods=["GET"])
def ReadMessage(name):
	name = "C13729611_"+name
	conn = get_conn()
	rs = conn.get_queue(name)

	m = []
	for i in range(0, rs.count()):
		m.append(rs.read(60).get_body())

	resp = json.dumps(m)
	return Response(response=resp, mimetype="application/json")

@app.route("/queues/<name>/msgs", methods=["DELETE"])
def ConsumeMessage(name):
	name = "C13729611_" + name
	conn = get_conn()
	rs = conn.get_queue(name)

	m = rs.read(60)
	rs.delete_message(m)

	resp = {"Response": "Remove message " + str(m.get_body())}
	resp = json.dumps(resp)


	q = conn.get_queue(queueName)
	m = q.read(60)
	q.delete_message(m)
	return m.get_body()

# Get the keys from a specific url and then use them to connect to AWS Service

# Set up a connection to the AWS service.

# Get a list of the queues that exists and then print the list out

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)