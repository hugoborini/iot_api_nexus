from flask import Flask, jsonify, jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
import sys
import json

# sys.path is a list of absolute path strings
sys.path.append('../models')

from models import model


class getBookingByEmail (Resource):
    def get(self, email):
        
        data = model.getBookingByEmailModel(email)

        try:
            return {'data': data}
        except:
            return {'data': 'An Error Occurred during fetching Api'}

