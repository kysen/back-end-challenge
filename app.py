# Create an api that contains an array of objects. 
# Each object should contain the following keys: 
#   first_name, 
#   last_name, 
#   birthday, 
#   special_skill

from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Info (db.Model):
    __tablename__="Info"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.String(20), nullable=False)
    special_skill = db.Column(db.String(20), nullable=False)


    def __init__(self, first_name, last_name, birthday, special_skill):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.special_skill = special_skill
        
class InfoSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "birthday", "special_skill")

info_schema = InfoSchema()
infos_schema = InfoSchema(many=True)


@app.route("/add-info", methods=["POST"])
def add_info():

    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    birthday = request.json["birthday"]
    special_skill = request.json["special_skill"]

    record = Info(first_name, last_name, birthday, special_skill)

    db.session.add(record)
    db.session.commit()

    info = Info.query.get(record.id)

    return info_schema.jsonify(info)


@app.route("/identity-theft", methods=["GET"])
def get_infos():
    all_infos = Info.query.all()
    result = infos_schema.dump(all_infos)
    return jsonify(result.data)

# @app.route("/info/<id>", methods=["PUT"])
# def update_info(id):

#     info = Info.query.get(id)

#     new_title = request.json["title"]
#     new_done = request.json["done"]

#     info.title = new_title
#     info.done = new_done

#     db.session.commit()
#     return info_schema.jsonify(info)


# @app.route("/info/<id>", methods=["DELETE"])
# def delete_info(id):
#     record = Info.query.get(id)
#     db.session.delete(record)
#     db.session.commit()

#     return jsonify("RECORD DELETED!")

if __name__ == "__main__":
    app.debug = True
    app.run()