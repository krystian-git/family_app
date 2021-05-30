from family import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import event



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


""" relation table for User and Role models """
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    )


@event.listens_for(roles_users, 'after_create')
def conect_user_admin(*args, **kwargs):
    """ After creating ralational table between User and Role we add Admin role to ADMIN user  """
    role = Role.query.filter_by(name='Admin').first()
    print(role.name)
    user = User.query.first()
    user.roles.append(role)
    print(user.name, user.roles)
    db.session.commit()
    

class Role(db.Model):
    """ Role of user in app """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False,unique=True)

    def __repr__(self):
        return f'{self.name} - {self.description}'


@event.listens_for(Role.__table__,'after_create')
def create_role(*args, **kwargs):
    """ Create 3 roles after creating Role table """
    db.session.add(
        Role(
            name='Admin',
            description='Access to every endpoint, can manage users, manage todo lists, cost of renowations etc.')
            )
    db.session.add( 
        Role(
            name = 'Parent',
            description='Restricted view. No access to settings. Can not add Lists, Rooms')
            )
    db.session.add(
        Role(
            name='Child',
            description='Resctricted view. Can go todo.html and news. Can not add lists etc...')
            )
    db.session.commit()


class User(db.Model, UserMixin):
    """ User to Sign in and Log in to app """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False,nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=roles_users, backref='users', lazy='select')

    def __repr__(self):
        return f'{self.name}, and its email {self.email}' 

    def has_role(self, role):
        return role in (role.name for role in self.roles) 


@event.listens_for(User.__table__,'after_create')
def create_user(*args, **kwargs):
    """ Create first user ADMIN """
    user = User(
        name='ADMIN',
        password=bcrypt.generate_password_hash('ADMIN').decode('utf-8'),
        email='admin@admin.com'
    )
    db.session.add(user)
    db.session.commit()
  

class Todolist(db.Model):
    """ List for Todo.html """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    events = db.relationship('Event', backref='todolist', lazy=True)

    def __repr__(self):
        return f'{self.name}'


class Event(db.Model):
    """ Event for Todo lists """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    is_done = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    todolist_id = db.Column(db.Integer, db.ForeignKey('todolist.id'))

    def __repr__(self):
        return f'{self.name} - is done: {self.is_done}'
 

class Room(db.Model):
    """ Room for Cost Calculate nav item """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    total_cost = db.Column(db.Integer, unique=False, nullable=True)
    item_or_service = db.relationship('ItemOrService', backref='area', lazy=True)
    
    def __repr__(self):
        return f'{self.name}'


class ItemOrService(db.Model):
    """ New Item or Service and its cost """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return f'{self.name} - {self.price}'


class Roombilgoraj(db.Model):
    """ Room for Cost Calculate nav item """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    total_cost = db.Column(db.Integer, unique=False, nullable=True)
    item_or_service = db.relationship('ItemOrServiceBilgoraj', backref='area', lazy=True)
    
    def __repr__(self):
        return f'{self.name}'


class ItemOrServiceBilgoraj(db.Model):
    """ New Item or Service and its cost """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('roombilgoraj.id'))

    def __repr__(self):
        return f'{self.name} - {self.price}'


class Movie(db.Model):
    """ New movie to be watched """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)

    def __repr__ (self):
        return f'{self.title}' 


class Buyitem(db.Model):
    """ Item for Price compare """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    item_or_service = db.relationship('WhereItem', backref='buyitem', lazy=True)
    
    def __repr__(self):
        return f'{self.name}'


class WhereItem(db.Model):
    """ Shop and price for item """
    id = db.Column(db.Integer, primary_key=True)
    shop = db.Column(db.String(300), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('buyitem.id'))

    def __repr__(self):
        return f'{self.name} - {self.price}'