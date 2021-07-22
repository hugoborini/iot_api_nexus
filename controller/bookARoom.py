from flask import Flask, jsonify, jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
import sys
import json

# sys.path is a list of absolute path strings
sys.path.append('../models')

from models import model

class bookARoom (Resource):
    def get(self):
        try:
            return {'status': "this route is for post"}
        except:
            return {'data': 'An Error Occurred during fetching Api'}

    def post(self):
        data = request.get_json()
        #data = json.dumps(data, separators=(',', ':'))
        #print(data["nameRoom"])
        returnMsg = model.bookARoom(data["nameRoom"], data["start"], data["end"],  data["studentEmail"])

        try:
            return {'status':  returnMsg}
        except :
            return{ 'data': 'An Error Occurred during fetching Api'}
            
