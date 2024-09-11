
# Import necessary modules
from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from user_manage import *

from init_user import init_user_db
from init_library import init_library_db
from init_checked_out import *

from librarian_functions import *
from patron_functions import *




# Remove this
#from flask import render_template


# Initialize the Flask app and set a secret key
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

# Call the sys_init() function within the application context to initialize the user database
with app.app_context():
    init_user_db()
    init_library_db()
    init_checked_out_db()

# Routes for login and logout
@app.route('/')
def index():
    if request.args:
        messages = request.args.get('messages', '')
        return render_template('index.html', messages=messages)
    else:
        return render_template('index.html', messages='')
    
# Route for handling login requests
@app.route('/login', methods=['POST'])
def login_route():
    if request.method == 'POST':
        # Extract username and password from the form data
        username = request.form['username']
        password = request.form['password']
        
        # Attempt to authenticate the user
        user = authenticate_user(username, password)
        
        if user:
            # If authentication is successful, store user data in the session
            session['logged_in'] = True
            session['username'] = username
            session['user'] = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
            }
            # Check if the user has a user_type attribute
            if hasattr(user, 'user_type'):
                session['user']['user_type'] = user.user_type
                # Redirect to the appropriate profile page based on user type
                if user.user_type == 'patron':
                    return redirect(url_for('dashboard_patron'))
                elif user.user_type == 'librarian':
                    return redirect(url_for('dashboard_librarian'))
            else:
                # Handle the case where user_type is not present
                return redirect(url_for('index', messages='Invalid user account.'))

        # If authentication fails, redirect back to the login page with an error message
        return redirect(url_for('index', messages='Invalid credentials. Please try again.'))

    # If the request method is not POST, redirect to the login page
    return redirect(url_for('index'))




# Route for handling logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Route for rendering the librarian dashboard
@app.route('/dashboard_librarian')
def dashboard_librarian():
    user_data = session.get('user')
    if user_data and user_data['user_type'] == 'librarian':
        return render_template('dashboard_librarian.html')
    else:
        return redirect('/?messages=Unauthorized access.')

# Route for rendering the patron dashboard
@app.route('/dashboard_patron')
def dashboard_patron():
    user_data = session.get('user')
    if user_data and user_data['user_type'] == 'patron':
        return render_template('dashboard_patron.html')
    else:
        return redirect('/?messages=Unauthorized access.')

# Route for adding new items to the db
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'GET':
        return render_template('add_item.html')  # Render the add item form for GET requests

    elif request.method == 'POST':
        # Extract item information from the form
        
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        publication_year = request.form['publication_year']
        item_type = request.form['item_type']
        available_status = request.form['available_status']
        quantity = request.form['quantity']

        # Add the item to the library using the add_item function
        add_library_item(title, author, publisher, publication_year, item_type, available_status, quantity)
        
        # Redirect to a success page or another appropriate page
        return render_template('dashboard_librarian.html')


# Route for adding a new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    elif request.method == 'POST':
        # Check if the user is logged in and is a librarian
        user_data = session.get('user')
        if user_data and user_data['user_type'] == 'librarian':
            # Extract user information from the form
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            user_type = request.form['user_type']

            # Add the user to the system based on the user type
            if user_type == 'librarian':
                add_librarian(username, password, first_name, last_name, email, phone)
            elif user_type == 'patron':
                add_patron(username, password, first_name, last_name, email, phone)

            # Redirect to a success page or another appropriate page
            return redirect(url_for('dashboard_librarian'))
        else:
            # Redirect to the login page if the user is not logged in or is not a librarian
            return redirect(url_for('index'))

# Route for viewing all users (for librarians only)
@app.route('/view_all_users')
def view_all_users():
    user_data = session.get('user')
    if user_data and user_data['user_type'] == 'librarian':
        # Retrieve all users from the database
        users = display_all_users()
        return render_template('view_all_users.html', users=users)
    else:
        return redirect('/?messages=Unauthorized access.')

# Route for searching for specific users (by name/ID)
from flask import redirect, url_for, request

@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    # Check if the user is logged in and is a librarian
    user_data = session.get('user')
    if user_data and user_data['user_type'] == 'librarian':
        if request.method == 'POST':
            user_id = request.form.get('user_id')  # Assuming you have a form field for user_id

            if user_id:
                # Redirect to the route for displaying checked out items
                return redirect(url_for('checked_out_items', user_id=user_id))

        # Get the search type and query from the request
        search_type = request.args.get('search_type')
        search_query = request.args.get('search_query')

        if search_type and search_query:
            # Perform the search based on the selected search type
            if search_type == 'username':
                # Search by username
                user = search_user_by_username(search_query)
            elif search_type == 'librarian_id':
                # Search by librarian ID
                user = search_user_by_librarian_id(search_query)

            if user:
                # If user is found, redirect to the user profile page
                return redirect(url_for('user_profile', username=user.username))
            else:
                # If user is not found, return a message
                return render_template('search_user.html', message='User not found.')
        else:
            # Render the search form page
            return render_template('search_user.html')
    else:
        # Redirect to unauthorized access page or login page
        return redirect(url_for('index', messages='Unauthorized access.'))


# Route for displaying user profile
@app.route('/user_profile/<username>', methods=['GET'])
def user_profile(username):
    # Get user profile data based on the username
    user_profile = get_user_profile(username)
    if user_profile:
        # Render the user profile template with the profile data
        return render_template('user_profile.html', user_profile=user_profile)
    else:
        # If user profile not found, return an error message
        return render_template('error.html', message='User profile not found.')

# Route for updating user profile
@app.route('/update_profile', methods=['POST'])
def update_profile():
    # Get user data from the request form
    user_id = request.form['user_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']

    # Retrieve the user object from the database or session
    user = get_user_by_id(user_id)

    # Check if the user exists
    if user:
        # Update the user profile
        user.update_profile(first_name=first_name, last_name=last_name, email=email, phone=phone)
        return redirect('/profile')  # Redirect to the profile page after successful update
    else:
        return 'User not found', 404  # Return a 404 error if user does not exist

    
# Route for viewing all items in the db    
@app.route('/view_all_items')
def view_all_items():
    # Retrieve all items from the database
    items = retrieve_all_items()  # Assuming you have a function to retrieve all items
    return render_template('view_all_items.html', items=items)

# Route for searching specific item in the db
@app.route('/search_item', methods=['GET'])
def search_item():
    # Get the title from the query string
    title = request.args.get('title')

    # If title is provided, perform the search
    if title:
        item = search_items(title)  # Assuming you have a function to search items by title
        if item:
            # If item is found, redirect to the item profile page with the item's title
            return redirect(url_for('item_profile', title=title))
        else:
            # If item is not found, return a message
            return render_template('search_item.html', message='Item not found.')
    # If no title is provided, render the search form page
    return render_template('search_item.html')


# Route for displaying an individual item's profile
@app.route('/item_profile/<title>')
def item_profile(title):
    # Get the item details by its title
    items = search_items(title)  # Assuming you have a function to search items by title

    if items:
        # If items are found, take the first item from the list
        item = items[0]
        # Render the item profile page with item details
        return render_template('item_profile.html', item=item)
    else:
        # If no items are found, render a message indicating that the item was not found
        return render_template('item_profile.html', message='Item not found.')


# Route for handling checkout requests
@app.route('/checkout_item', methods=['POST'])
def checkout_item():
    if request.method == 'POST':
        # Get user ID from session
        user_id = session.get('user').get('id')
        
        # Extract item ID from the form
        item_id = request.form.get('item_id')

        # Call the checkout_item function from patron_functions.py
        success = checkout_item(user_id, item_id)
        
        if success:
            # Redirect to a success page or another appropriate page
            return redirect(url_for('dashboard_patron'))
        else:
            # Handle the case where checkout failed, perhaps by showing an error message
            return redirect(url_for('dashboard_patron', messages='Checkout failed.'))
    else:
        # If the request method is not POST, redirect to the login page
        return redirect(url_for('index'))




# Route for displaying checked out items
@app.route('/checked_out_items/<int:user_id>')
def checked_out_items(user_id):
    checked_out_items = retrieve_checked_out_items(user_id)
    return render_template('checked_out_items.html', checked_out_items=checked_out_items)










if __name__ == '__main__':
    app.run(debug=True)