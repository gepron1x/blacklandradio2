import os

import flask
from flask import jsonify, request, url_for
from flask_restful import Resource, abort

from data import db_session

from marshmallow import Schema, fields

from data.user import BlacklandUser


class LoginAndPasswordSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)


def user_to_dict(user: BlacklandUser):
    user_dict = user.to_dict(only=(
        'id',
        'name')
    )

    user_dict['avatar_url'] = url_for('useravatarresource', user_id=user.id)
    return user_dict


class UsersByIdResource(Resource):

    def get(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(BlacklandUser).filter(BlacklandUser.id == user_id).first()
        if not user:
            abort(404)

        return jsonify(
            {
                'user': user_to_dict(user)
            }
        )

    def delete(self, user_id):
        schema = LoginAndPasswordSchema()
        errors = schema.validate(request.args)
        if errors:
            abort(400)
        result = schema.dump(request.args)
        login = result['login']
        password = result['password']
        db_sess = db_session.create_session()
        user = db_sess.query(BlacklandUser).filter(BlacklandUser.email == login).first()
        if not user or not user.check_password(password):
            abort(401)

        user = db_sess.query(BlacklandUser).get(user_id)

        if not user:
            abort(404)

        if not user:
            return jsonify({'error': 'Not found'})
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersResource(Resource):

    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(BlacklandUser).all()

        return jsonify(
            {'users': [user_to_dict(a) for a in users]}
        )


class SearchSchema(Schema):
    value = fields.Str(required=True)


class UsersByNameResource(Resource):

    def get(self):
        schema = SearchSchema()
        errors = schema.validate(request.args)
        if errors:
            abort(400)
        result = schema.dump(request.args)

        db_sess = db_session.create_session()

        users = db_sess.query(BlacklandUser).filter(BlacklandUser.name.like(f"%{result.value}%")).all()

        return jsonify({'users': [user_to_dict(a) for a in users]})


class UserAvatarResource(Resource):

    def get(self, user_id):
        db_sess = db_session.create_session()

        user = db_sess.query(BlacklandUser).filter(BlacklandUser.id == user_id).first()
        if not user:
            abort(404)

        filename = user.cover_url.split('/')[-1]

        return flask.send_file(os.path.join("static", "cdn", "profile", str(user_id), filename))
