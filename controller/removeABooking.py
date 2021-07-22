from flask import Flask, jsonify, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
import sys

# sys.path is a list of absolute path strings
sys.path.append('../models')

from models import model


class removeABooking(Resource):
    def get(self):
        try:
            return {'status': "this route is for post"}
        except:
            return {'data': 'An Error Occurred during fetching Api'}
    
    def post(self):

        data = request.get_json()

        data = model.removeABookingModel(int(data["idBooking"]))

        try:
            return {'data': data}
        except:
            return {'data': 'An Error Occurred during fetching Api'}

