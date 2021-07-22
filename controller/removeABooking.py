from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import sys

# sys.path is a list of absolute path strings
sys.path.append('../models')

from models import model


class removeABooking(Resource):
    def get(self, idBooking):

       

        data = model.removeABookingModel(int(idBooking))

        try:
            return {'data': data}
        except:
            return {'data': 'An Error Occurred during fetching Api'}

