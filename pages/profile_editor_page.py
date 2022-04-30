import os

from flask import Flask, url_for, render_template
from werkzeug.utils import redirect

from data.user import BlacklandUser
from form.user_form import UserForm
from pages.page import Page
from sqlalchemy.orm import Session


class ProfileEditorPage(Page):

    def __init__(self, app: Flask, db_sess: Session, user: BlacklandUser):
        self.app = app
        self.db_sess = db_sess
        self.user = user

    def response(self):
        form = UserForm()

        if form.validate_on_submit():
            if form.new_name.data:
                self.user.name = form.new_name.data
                print(form.new_name.data)

            if form.new_password.data:
                self.user.set_password(form.new_password.data)

            if form.new_avatar.data:
                print(form.new_avatar.data)
                self.save_avatar(form.new_avatar.data)

            if form.new_description.data:
                self.user.description = form.new_description.data
            self.db_sess.merge(self.user)
            self.db_sess.commit()
            return redirect("/my_profile")

        return render_template("profile_editor.html", user=self.user, form=form)

    def save_avatar(self, data):
        path = os.path.join('static', 'cdn', 'profile', str(self.user.id))
        os.makedirs(path, exist_ok=True)
        filename = f'avatar{os.path.splitext(data.filename)[1]}'
        data.save(os.path.join(path, filename))
        self.user.avatar_url = url_for('static', filename=f'cdn/profile/{self.user.id}/{filename}')
