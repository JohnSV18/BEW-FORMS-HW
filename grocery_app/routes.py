from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User
# from grocery_app.forms import BookForm, AuthorForm, GenreForm
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
# Import app and db from events_app package so that we can run app
from grocery_app import app, db
from grocery_app import bcrypt


main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    # TODO: Create a GroceryStoreForm
    form = GroceryStoreForm()

    # TODO: If form was submitted and was valid:
    if form.validate_on_submit():
    # - create a new GroceryStore object and save it to the database,
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data
        )
        db.session.add(new_store)
        de.session.commit()
    # - flash a success message, and
    # - redirect the user to the store detail page.
        flash('New Grocery Store was created successfully.')
        return redirect(url_for('main.store_detail', store_id=new_store.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()

    # TODO: If form was submitted and was valid:
    if form.validate_on_submit():
    # - create a new GroceryItem object and save it to the database,
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data
        )
        db.session.add(new_item)
        db.session.commit()
    # - flash a success message, and
    # - redirect the user to the item detail page.
        flash('New Grocery Store Item was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_item.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html' ,form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)

    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    if form.validate_on_submit():
        store(
            title = form.title.data,
            address = form.address.data
        )
        db.session.add(store)
        db.commit()


    # - flash a success message, and
    # - redirect the user to the store detail page.
        flash('New Store was updated successfully.')
        return redirect(url_for('main.store_detail', store_id = store.id))
    # TODO: Send the form to the template and use it to render the form fields
    store = GroceryStore.query.get(store_id)
    return render_template('store_detail.html', store=store)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form= GroceryItemForm(obj=item)

    # TODO: If form was submitted and was valid:
    if form.validate_on_submit():
    # - update the GroceryItem object and save it to the database,
        item(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data
        )
        db.session.add(item)
        db.session.commit()
   

    # - flash a success message, and
        flash('item was updated successfully.')
    # - redirect the user to the item detail page.
        return redirect(url_for('main.item_detail', item_id=new_item.id))

    # TODO: Send the form to the template and use it to render the form fields
    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item)
# --------------------------------------------------------------------------------------------------
auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

