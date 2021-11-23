from flask import jsonify
from flask import request

from models import Flaskuser, db
from . import api


@api.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')

        if not (userid and username and password and re_password):
            return jsonify({'error': 'No arguments'}), 400

        if password != re_password:
            return jsonify({'error': 'Password Incorrect'}), 400

        fcuser = Flaskuser()
        fcuser.userid = userid
        fcuser.username = username
        fcuser.password = password

        db.session.add(fcuser)
        db.session.commit()

        return jsonify(), 201

    users = Flaskuser.query.all()
    return jsonify([user.serialize for user in users])


@api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(uid):
    if request.method == 'GET':
        user = Flaskuser.query.filter(Flaskuser.id == uid).first()
        return jsonify(user.serialize)

    elif request.method == 'DELETE':
        Flaskuser.query.delete(Flaskuser.id == uid)
        return jsonify(), 204

    data = request.get_json()

    Flaskuser.query.filter(Flaskuser.id == uid).update(data)
    user = Flaskuser.query.filter(Flaskuser == uid).first()
    return jsonify(user.serialize)
