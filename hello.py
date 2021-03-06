import sys
import database
import mock
from bson import json_util
import flask
import requests
from flask import Flask, Response, request
from flask.ext.restful import reqparse, abort, Api, Resource
import urllib2, json
import numpy
import Pycluster
from collections import Counter

app = Flask(__name__)
api = Api(app)

generator_url = "http://immense-refuge-2812.herokuapp.com/push/test?config=2"

def abort_if_doesnt_exist(data_id):
	if database.find(data_id) is None:
		abort(404, message = "Data {} doesn't exist".format(data_id))

def json_dump(obj):
	return Response(flask.json.dumps(obj, default=json_util.default), mimetype='application/json')

class Data(Resource):
	def get(self, data_id):
		abort_if_doesnt_exist(data_id)
		return json_dump(database.find(data_id))

class DataList(Resource):
	def get(self):
		dataList = list(database.find_all())
		return json_dump(dataList)

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('data', type = str)
		args = parser.parse_args()
		data_id = database.insert(args['data'])
		return flask.json.dumps(data_id, default=json_util.default), 201

class Mock(Resource):
	def get(self):
		return json_dump(json_util.loads(mock.getData()))


class Consume(Resource):
	def post(self):
		print 'im here'
		print request.data
		database.insertEvents(json.loads(request.data))
		print "po request"
		req = requests.post("http://immense-refuge-2812.herokuapp.com/results", data=json.dumps(k_means()))
		return {}, 201

	def get(self):
		request = requests.post("http://immense-refuge-2812.herokuapp.com/sample/test?config=2&timespan=10")
		host = [{"host" : "flask-ztis.herokuapp.com", "path" : "/consume"}]
		headers = {'content-type': 'application/json'}
		request = requests.post(generator_url, data=json.dumps(host), headers=headers)
		return {}, 200

class Result(Resource):
	def get(self):
		return json_dump(k_means())

def k_means():
	dataList = list(database.find_all())
	vectors = []
	uuids = []
	for data in dataList:
		counter = Counter()
		uuids.append(data['uuid'])
		for event in data['events']:
				counter[event['name']] += 1
		vector = []
		for typ in counter:
			vector.append(counter[typ])
		vectors.append(vector)

	result = vectors
	labels, error, nfound = Pycluster.kcluster(vectors, 3)

	classes = []
	for label in labels:
		classes.append(numpy.asscalar(label))
	result = dict(zip(uuids,classes))
	return result

api.add_resource(Data, '/data/<string:data_id>')
api.add_resource(DataList, '/', '/data')
api.add_resource(Mock, '/mock')
api.add_resource(Consume, '/consume')
api.add_resource(Result, '/result')

if __name__ == '__main__':
    app.run(debug=True)
