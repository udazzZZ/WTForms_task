from flask import request, url_for, render_template, redirect, flash, Flask
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from models import User
from forms import SignUpForm, UpdateForm, DeleteForm


class UserList(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        users: list[User] = self.engine.session.execute(User.query).scalars()
        return render_template("user/list.html", users=users)


class UserView(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, user_id: int):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()
        if not user:
            return "wtf"
        return render_template("user/read.html", user=user)


class UserSignUp(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self):
        form = SignUpForm()
        return render_template("user/signup.html", form=form)

    def post(self):
        form = SignUpForm(request.form)
        if form.validate():
            user = User(name=form.name.data, email=form.email.data, age=form.age.data)
            self.engine.session.add(user)
            self.engine.session.commit()
            flash("User created successfully!", "success")
        else:
            print(form.errors)

        return redirect(url_for("user.list"))


class UserUpdate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, user_id: int):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()

        if not user:
            return "wtf"

        form = UpdateForm(name=user.name, email=user.email, age=user.age)

        return render_template("user/update.html", form=form)

    def post(self, user_id: int):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()

        if not user:
            return "wtf"

        form = UpdateForm(request.form)
        if form.validate():
            user.name = form.name.data
            user.email = form.email.data
            user.age = form.age.data
            self.engine.session.commit()
            flash("User updated successfully!", "success")
        else:
            print(form.errors)

        return redirect(url_for("user.view", user_id=user.id))


class UserDelete(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        self.engine = engine

    def get(self, user_id: int):
        form = DeleteForm()
        return render_template("user/delete.html", form=form)

    def post(self, user_id: int):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()

        if not user:
            return "wtf"

        self.engine.session.delete(user)
        self.engine.session.commit()

        return redirect(url_for("user.list"))


def add_user(app: Flask, engine: SQLAlchemy):
    common_func = UserList.as_view("user.list", engine=engine)
    app.add_url_rule("/", view_func=common_func)
    app.add_url_rule("/user/list", view_func=common_func)

    app.add_url_rule(
        "/user/<user_id>", view_func=UserView.as_view("user.view", engine=engine)
    )
    app.add_url_rule(
        "/signup", view_func=UserSignUp.as_view("user.signup", engine=engine)
    )
    app.add_url_rule(
        "/user/update/<user_id>",
        view_func=UserUpdate.as_view("user.update", engine=engine),
    )
    app.add_url_rule(
        "/user/delete/<user_id>",
        view_func=UserDelete.as_view("user.delete", engine=engine),
    )
