from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import sys

# sys.path is a list of absolute path strings
sys.path.append('../models')

from models import model

class getRoomInfoByIdRoom (Resource):
    def get(self, idRoom):
        data = model.getInfoOfARoomBYIdRoom(int(idRoom))
        try:
            return {'data': data}
        except:
            return {'data': 'An Error Occurred during fetching Api'}