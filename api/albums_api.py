import os
import shutil

import flask
from flask import jsonify, request, url_for
from flask_restful import Resource, abort

from data import db_session
from data.album import Album

from marshmallow import Schema, fields

from data.comment import Comment
from data.song import Song
from data.user import BlacklandUser


class LoginAndPasswordSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)

class ContentSchema(Schema):
    content = fields.Str(required=True)

class IdSchema(Schema):
    id = fields.Int(required=True)


def album_to_dict(album: Album):
    album_dict = album.to_dict(only=(
        'name',
        'year',
        'description',
        'genre.name',
        'author_id')
    )

    album_dict['cover'] = url_for('albumcoverresource', album_id=album.id)
    songs = list()
    for song in album.songs:
        songs.append(url_for(f'songfileresource', song_id=song.id))
    album_dict['songs'] = songs
    return album_dict


class AlbumsByIdResource(Resource):

    def get(self, album_id):
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(Album.id == album_id).first()
        if not album:
            abort(404)

        return jsonify(
            {
                'album': album_to_dict(album)
            }
        )

    def delete(self, album_id):
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

        album = db_sess.query(Album).filter(Album.id == album_id).first()

        if not album:
            abort(404)

        if album.author != user:
            abort(401)

        db_sess.delete(album)
        shutil.rmtree(f"static/cdn/albums/{album.id}")
        db_sess.commit()

        return jsonify({'Success': 'Ok'})


class AlbumsResource(Resource):

    def get(self):
        db_sess = db_session.create_session()
        albums = db_sess.query(Album).all()

        return jsonify(
            {'albums': [album_to_dict(a) for a in albums]}
        )


class SearchSchema(Schema):
    value = fields.Str(required=True)


class AlbumsSearchResource(Resource):

    def get(self):
        schema = SearchSchema()
        errors = schema.validate(request.args)
        if errors:
            abort(400)
        result = schema.dump(request.args)

        db_sess = db_session.create_session()

        albums = db_sess.query(Album).filter(Album.name.like(f"%{result.value}%")).all()

        return jsonify({'albums': [album_to_dict(a) for a in albums]})


class SongFileResource(Resource):

    def get(self, song_id):
        db_sess = db_session.create_session()

        song = db_sess.query(Song).filter(Song.id == song_id).first()
        if not song:
            abort(404)

        filename = song.url.split('/')[-1]
        return flask.send_file(os.path.join("static", "cdn", "albums", str(song.album_id), filename))


class AlbumCoverResource(Resource):

    def get(self, album_id):
        db_sess = db_session.create_session()

        album = db_sess.query(Album).filter(Album.id == album_id).first()
        if not album:
            abort(404)

        filename = album.cover_url.split('/')[-1]

        return flask.send_file(os.path.join("static", "cdn", "albums", str(album_id), filename))


class FavoriteAlbumsResource(Resource):

    def get(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(BlacklandUser).filter(BlacklandUser.id == user_id)
        if not user:
            abort(404)

        return jsonify({'users': [album_to_dict(a) for a in user.favorites]})


class FavoriteAlbumResource(Resource):

    def post(self, album_id):
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

        album = db_sess.query(Album).filter(Album.id == album_id).first()

        if not album:
            abort(404)

        user.favorites.append(album)
        db_sess.merge(user)
        db_sess.commit()

    def delete(self, album_id):
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

        album = db_sess.query(Album).filter(Album.id == album_id).first()

        if not album:
            abort(404)

        user.favorites.remove(album)
        db_sess.merge(user)
        db_sess.commit()


class CommentResource(Resource):

    def get(self, album_id):

        db_sess = db_session.create_session()

        album = db_sess.query(Album).filter(Album.id == album_id).first()

        if not album:
            abort(404)

        return [c.to_dict('author_id', 'content') for c in album.comments]

    def post(self, album_id):
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

        album = db_sess.query(Album).filter(Album.id == album_id).first()

        content_schema = ContentSchema()
        if schema.validate(request.args):
            abort(400)

        content = content_schema.dump(request.args)['content']

        if not album:
            abort(404)

        album.comments.append(Comment(author_id=user.id, album_id=album_id, content=content))

    def delete(self, album_id):
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

        album = db_sess.query(Album).filter(Album.id == album_id).first()
        if not album:
            abort(404)

        id_schema = IdSchema()

        if id_schema.validate(request.args):
            abort(400)

        comment_id = id_schema.dump(request.args)['id']

        comment = db_sess.query(Comment).filter(Comment.id == comment_id).first()

        if not comment:
            abort(404)

        db_sess.delete(comment)

        return jsonify({'Success': 'Ok'})

