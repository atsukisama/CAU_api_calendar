from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from datetime import datetime
from dateutil import parser as dateparser
import binascii
import os

db_connect = create_engine('sqlite:///database.sqlt')
app = Flask(__name__)
api = Api(app)

class Calendar(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from calendar")
        result = []
        for elem in query.cursor.fetchall():
            result.append({"id" : elem[0], "keylink" : elem[1]})
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        query = conn.execute("select keylink from calendar")
        new_key = binascii.b2a_hex(os.urandom(8))
        while new_key in query:
            new_key = binascii.b2a_hex(os.urandom(8))
        conn.execute("insert into calendar (keylink) values (?)", new_key)
        return jsonify({"keylink" : new_key})

    def delete(self):
        conn = db_connect.connect()
        conn.execute("delete from event where keylink=?", request.form['keylink'])
        conn.execute("delete from calendar where keylink=?", request.form['keylink'])
        return ({"result" : "ok"})

class CalendarEvent(Resource):
    def get(self, keylink):
        conn = db_connect.connect()
        query = conn.execute("select * from event where keylink=?", keylink)
        result = []
        for elem in query.cursor.fetchall():
            result.append({"id" : elem[0], "name" : elem[2], "color" : elem[3], "start" : elem[4], "end" : elem[5]})
        return jsonify(result)

    def post(self, keylink):
        name = request.form['name']
        color = request.form['color']
        start = dateparser.parse(request.form['start'])
        end = dateparser.parse(request.form['end'])
        conn = db_connect.connect()
        conn.execute("insert into event (keylink, name, color, start, end) values (?, ?, ?, ?, ?)", keylink, name, color, unicode(start), unicode(end))
        return ({"result" : "ok"})

    def delete(self, keylink):
        conn = db_connect.connect()
        conn.execute("delete from event where id=?", request.form['id'])
        return ({"result" : "ok"})

api.add_resource(Calendar, '/calendar')
api.add_resource(CalendarEvent, '/calendar/<string:keylink>')

if __name__ == '__main__':
     app.run(port=5002, host='0.0.0.0')