from random import sample, randint
from urllib import request

from flask import Flask, abort, jsonify, request
from sqlalchemy.orm import sessionmaker

from db_engine import engine
from models import Animal, Specie

app = Flask(__name__)


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


def insert_data(json_data):
    try:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        animal_name = json_data.get('animals')
        new_animal = Animal(name=animal_name)
        session.add(new_animal)
        session.commit()

        specie_name = json_data.get('species')
        new_specie = Specie(name=specie_name, animal_id=new_animal.id)
        session.add(new_specie)
        session.commit()

    except Exception as e:
        abort(500, description=f"Database error: {e}")

    return {'action': "data inserted"}


@app.route('/insert', methods=['POST'])
def insert_animals():
    data = {}
    if request.method == 'POST':
        data = insert_data(request.json)
    else:
        data['action'] = "you request something weird..."

    return data


@app.route('/animals/<animal>', methods=['GET'])
def random_remote_animals(animal):
    data = {'species': []}
    if request.method == 'GET':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        for animal_row in session.query(Animal).filter_by(name=animal):
            for specie in session.query(Specie).filter_by(animal_id=animal_row.id):
                data['species'].append(specie.name)
    else:
        data['action'] = "you request something weird..."

    return data
