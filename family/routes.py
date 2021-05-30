from family import db, bcrypt
from flask import render_template, url_for, flash, redirect, request, session,\
                    current_app as app
from family.models import User, Role, Room, Movie, ItemOrService, Todolist, Event,\
                    Buyitem, WhereItem, Roombilgoraj, ItemOrServiceBilgoraj
from family.forms import TodoForm, EventForm, DeleteIsDoneForm, NewItemForm, MovieForm,\
                    WhereItemForm, BuyitemForm, RoomForm, RegisterForm, LoginForm, RoomBilgorajForm
from flask_login import login_required, login_user, logout_user, current_user
from family.libs.filmweb import Filmweb
from family.utils import bitcoin, pln


MOVIES_QUANTITY = 10 # number of movies being scraped from filmweb.pl to display
                     # the bigger the number slower loading optimal ~10

""" Login route """
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'danger')
        return redirect(url_for('todo'))
    
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, duration=5)
            flash(f'You have successfully logged in as {user.name}', 'success')            
            return redirect(url_for('todo'))

        flash(f'Check Credentials', 'danger')

    return render_template('login.html', form=form)


""" Route for quick adding tasks for family members """
@app.route('/', methods=['GET', 'POST'])
@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    form_is_done = DeleteIsDoneForm() # form for getting value true/false from done/undone button
    form_todo = TodoForm() # form for adding new list to todo
    form_event = EventForm() # form for adding new event to todo list 
    if request.method == 'POST' and form_todo.validate_on_submit() and "submit" in request.form:
        """ Adding new list (name) to todo.html page"""
        todolist = Todolist(name=request.form.get('new_list').upper())
        db.session.add(todolist)
        db.session.commit()
        flash(f'You have successfully added {request.form.get("new_list")}', 'success')
        return redirect(url_for('todo'))

    elif request.method == 'POST' and form_event.validate_on_submit() and "submit_event" in request.form:
        """ Adding new event to todo list """
        list_object = Todolist.query.filter_by(name=request.form.get('list_sellect')).first()
        event = Event(name=request.form.get('new_note'), todolist=list_object)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('todo'))
    
    elif request.method == "POST" and "submit_delete" in request.form:
        """ Deleting event from list  """        
        event_to_delete = Event.query.get(int(request.form.get('submit_delete')))
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect(url_for('todo'))

    elif request.method == 'POST' and "submit_is_done" in request.form:
        """ Mark events/items in list as done """
        event_to_update = Event.query.get(int(request.form.get('submit_is_done')))
        if event_to_update.is_done:
            event_to_update.is_done = False
        else:
            event_to_update.is_done = True
        db.session.commit()
        return redirect(url_for('todo'))
    
    todo_lists = Todolist.query.all() # Get all todo lists objects
    return render_template('todo.html', todo_lists=todo_lists,form_is_done=form_is_done, form_todo=form_todo, form_event=form_event)
    

""" Route to calculate your total cost renovating Rzeszow """
@app.route('/rzeszow_cost', methods=['GET', 'POST'])
@login_required
def rzeszow_cost():
    form_room = RoomForm() # form for adding new room to cost route
    form_item = NewItemForm() # form for adding new service/item and price to cost route

    if request.method == 'POST' and form_room.validate_on_submit() and 'submit_room' in request.form:
        """ Adding new room """
        room = Room(name=request.form.get('new_room'), total_cost=0)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('rzeszow_cost'))

    elif request.method == 'POST' and form_item.validate_on_submit() and 'submit_item' in request.form:
        """ Adding new item/service and price to sellected room """
        room_sellected = Room.query.filter_by(name=request.form.get('room_sellect')).first()
        item = ItemOrService(name=request.form.get('new_item'), price=request.form.get('new_price'),
                            area=room_sellected)
        room_sellected.total_cost += int(request.form.get('new_price'))
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('rzeszow_cost'))

    elif request.method == "POST" and "submit_delete" in request.form:
        """ Deleting item from list  """        
        item_to_delete = ItemOrService.query.get(int(request.form.get('submit_delete')))
        item_to_delete.area.total_cost -= item_to_delete.price # calculate total cost for room
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('rzeszow_cost'))

    room_list = Room.query.all()     
    return render_template('rzeszow_cost.html', form_room=form_room, form_item=form_item,
                             room_list=room_list)


""" Route - Calculating cost for renovating in Biłgoraj """
@app.route('/bilgoraj_cost', methods=['GET', 'POST'])
@login_required
def bilgoraj_cost():
    form_room = RoomBilgorajForm()
    form_item = NewItemForm()

    # Add new room to Bilgoraj_cost
    if request.method == 'POST' and form_room.validate_on_submit() and 'submit_room' in request.form:
        room = Roombilgoraj(name=request.form.get('new_room').upper(), total_cost=0)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('bilgoraj_cost'))

    # Add new item/service to room in Bilgoraj
    elif request.method == 'POST' and form_item.validate_on_submit() and 'submit_item' in request.form:
        room_sellected = Roombilgoraj.query.filter_by(name=request.form.get('room_sellect')).first()
        item = ItemOrServiceBilgoraj(name=request.form.get('new_item'), price=request.form.get('new_price'),
                            area=room_sellected)
        room_sellected.total_cost += int(request.form.get('new_price'))
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('bilgoraj_cost'))

    # Delete item/service from romm by item.id
    elif request.method == "POST" and "submit_delete" in request.form:
        item_to_delete = ItemOrServiceBilgoraj.query.get(int(request.form.get('submit_delete')))
        item_to_delete.area.total_cost -= item_to_delete.price
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('bilgoraj_cost'))

    room_list = Roombilgoraj.query.all()
    return render_template('bilgoraj_cost.html', form_room=form_room, form_item=form_item,
                             room_list=room_list)


""" Endpoint for settings - available only for Admin (check navbar -> layout.html) """
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    role_list = Role.query.all()
    user_list = User.query.all()
    todo_list = Todolist.query.all()
    room_list_bilgoraj = Roombilgoraj.query.all()
    room_list_rzeszow = Room.query.all()
    form = RegisterForm()
    
    # Registering new user
    if request.method == 'POST' and form.validate_on_submit():
        user_role = Role()
        user = User(
            name=(form.username.data).lower(),
            email=(form.email.data).lower(),
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        flash(f'You have added new user:{form.username.data}','success')
        return redirect(url_for('settings'))

    # Delete user
    elif request.method == "POST" and "submit_delete_user" in request.form:
        user_to_delete = User.query.get(int(request.form.get('submit_delete_user')))
        print(user_to_delete)
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('settings'))

    # Adding new roles to user
    elif request.method == 'POST' and 'submit_roles' in request.form:
        for user_ in user_list:
            user = User.query.filter_by(name=user_.name).first()
            user.roles.clear()
            for role_ in role_list:
                if str(user_.name + role_.name) in request.form:
                    role = Role.query.filter_by(name=role_.name).first()
                    user.roles.append(role)
            db.session.commit()
        return redirect(url_for('settings'))

    # Deleting list from todo.html
    elif request.method == 'POST' and 'submit_todo' in request.form:
        for todo_l in todo_list:
            if todo_l.name in request.form:
                db.session.delete(todo_l)        
        db.session.commit()
        return redirect(url_for('settings'))
    
    # Deleting room in bilgoraj_cost.html
    elif request.method == 'POST' and 'submit_bilgoraj' in request.form:
        for room in room_list_bilgoraj:
            if room.name in request.form:
                db.session.delete(room)        
        db.session.commit()
        return redirect(url_for('settings'))

    # Deleting room in rzeszow_cost.html
    elif request.method == 'POST' and 'submit_rzeszow' in request.form:
        for room in room_list_rzeszow:
            if room.name in request.form:
                db.session.delete(room)        
        db.session.commit()
        return redirect(url_for('settings'))

    return render_template('settings.html', todo_list=todo_list, room_list_rzeszow=room_list_rzeszow,
                            room_list_bilgoraj=room_list_bilgoraj, form=form, role_list=role_list, user_list=user_list)


""" Logout """
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


"""Endpoint to Movies to Watch"""
@app.route('/movies_to_watch', methods=['POST', 'GET'])
@login_required
def movies_to_watch():
    movies_from_filmweb = Filmweb()
    movie_list = Movie.query.all() # Getting all movies from Database
    form_movie = MovieForm() # Form for adding new movie to watch
    movies = movies_from_filmweb.movie_filmweb(limit=MOVIES_QUANTITY) # List of movies objects
    form_delete_is_done = DeleteIsDoneForm() # form for deleting movie from list
    
    # Adding new movies 
    if form_movie.validate_on_submit():
        movie = Movie(title=form_movie.movie_name.data)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('movies_to_watch'))
   
    # Deleting movie from list
    elif request.method == "POST" and 'submit_delete' in request.form :
        movie_to_delete = Movie.query.filter_by(title=request.form.get('submit_delete')).first()
        db.session.delete(movie_to_delete)
        db.session.commit()
        flash(f'Deleted {request.form.get("submit_delete")}','danger')
        return redirect('movies_to_watch')

    return render_template('movies_to_watch.html', movies=movies, form_movie=form_movie, movie_list=movie_list, form_delete_is_done=form_delete_is_done)


""" Endpoint for PLN exchange & other news """
@app.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    pln_rate = pln()
    bitcoins = bitcoin()
    return render_template('news.html', pln_rate=pln_rate, bitcoins=bitcoins)


""" Price Compare """
@app.route('/price_compare', methods=['GET', 'POST'])
@login_required
def price_compare():
    form_buy_item = BuyitemForm()
    form_where_buy = WhereItemForm()

    if request.method == 'POST' and form_buy_item.validate_on_submit() and 'submit_buy_item' in request.form:
        item = Buyitem(name=request.form.get('new_item'))
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('price_compare'))

    elif request.method == 'POST' and form_where_buy.validate_on_submit() and 'submit_where_buy' in request.form:
        item_sellected = Buyitem.query.filter_by(name=request.form.get('item_sellect')).first()
        item = WhereItem(shop=request.form.get('shop'), price=request.form.get('price'),
                            buyitem=item_sellected)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('price_compare'))

    elif request.method == "POST" and "submit_delete" in request.form:
        """ Deleting shop from list  """        
        item_to_delete = WhereItem.query.get(int(request.form.get('submit_delete')))
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('price_compare'))

    item_list = Buyitem.query.all()
    return render_template('price_compare.html', form_buy_item=form_buy_item, form_where_buy=form_where_buy,
                             item_list=item_list)
