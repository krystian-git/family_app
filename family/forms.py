from flask import request
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, StringField, SubmitField, BooleanField
from wtforms.validators import EqualTo, Email, DataRequired, Length, ValidationError, NumberRange
from family.models import Todolist, Buyitem, WhereItem, Room, User, Movie, Roombilgoraj


# todo.html
class TodoForm(FlaskForm):
    new_list = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    submit = SubmitField('Add List')

    def validate_new_list(self, new_list):
        check_name = Todolist.query.filter_by(name=request.form.get('new_list')).first()
        if check_name:
            raise ValidationError(' is already Your List')


# todo.html
class EventForm(FlaskForm):
    new_note = StringField('Name', validators=[DataRequired(), Length(min=3, max=200)])
    list_sellect = StringField(validators=[DataRequired()])
    submit_event = SubmitField()


# todo.html
class DeleteIsDoneForm(FlaskForm):
    is_done = BooleanField(default=False)
    delete_event = BooleanField(default=False)


# cost_calculator
class RoomForm(FlaskForm):
    new_room = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    submit_room = SubmitField('Add Room')

    def validate_new_room(self, new_room):
        check_room = Roomb.query.filter_by(name=request.form.get('new_room')).first()
        if check_room:
            raise ValidationError(f'You already have that room')


class RoomBilgorajForm(FlaskForm):
    new_room = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    submit_room = SubmitField('Add Room')

    def validate_new_room(self, new_room):
        check_room = Roombilgoraj.query.filter_by(name=request.form.get('new_room').upper()).first()
        if check_room:
            raise ValidationError(f'You already have that room')


# cost_calculator
class NewItemForm(FlaskForm):
    new_item = StringField('Name',validators=[DataRequired(), Length(min=3, max=200)])
    new_price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=1,max=50000) ])


# login.html
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField('Login')


# settings.html
class RegisterForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=60), Email(message='Not valid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords don't match")])
    submit = SubmitField('Register')

    def validate_email(self, email):
        email_check = User.query.filter_by(email=(email.data).lower()).first()
        if email_check:
            raise ValidationError(f'User with this email is already registered. Forgot password?')
    
    def validate_username(self, username):
        username_check = User.query.filter_by(name=(username.data).lower()).first()
        if username_check:
            raise ValidationError(f'This username is already registered. Choose another one')


# movie_to_watch.html
class MovieForm(FlaskForm):
    movie_name = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])

    def validate_movie_name(self, movie_name):
        check_title = Movie.query.filter_by(title=request.form.get('movie_name')).first()
        if check_title:
            raise ValidationError(f'This movie is already added')


# price_compare.html
class BuyitemForm(FlaskForm):
    new_item = StringField('Item', validators=[DataRequired(), Length(min=5, max=100)])
    
    def validate_name(self, name):
        item = Buyitem.query.filter_by(name=request.form.get('item')).first()
        if item:
            raise ValidationError(f'Item already listed')


# price_compare.html
class WhereItemForm(FlaskForm):
    shop = StringField('Shop', validators=[DataRequired(), Length(min=3, max=100)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=1, max=10000)])
