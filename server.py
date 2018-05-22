from flask import Flask, render_template, session, redirect, request
from models import connect_to_db, db, User

app = Flask(__name__)
app.secret_key = 'ABCD'


@app.route('/')
def landing_page():
    """Render landing page."""

    # check if user is already logged in and if they are render the index page
    if session.get('user_id'):
        return render_template('index.html')

    # if not render login page
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST'])
def register_user():
    """Add a user to the database."""

    user_name = request.form.get('usrname')
    password = request.form.get('psw')

    # check if user already exists in database. if the do redirect to login
    if User.query.filter(User.user_name == user_name).all():
        return redirect('/')

    # if not in the database add them and redirect to home page
    else:
        user = User(user_name=user_name,
                    password=password,
                    tokens=0,
                    completed=[])

        db.session.add(user)
        db.session.commit()
        user = User.query.filter(User.user_name == user_name).first()
        session['user_id'] = user.user_id

        return redirect('/')


@app.route('/login', methods=['POST'])
def login_user():
    """Login an already registered user."""

    user_name = request.form.get('usrname')
    password = request.form.get('psw')

    user = db.session.query(User).filter(User.user_name == user_name).first()

    # check password
    if user.password == password:
        session['user_id'] = user.user_id
        return render_template('index.html')

    else:
        return redirect('/')

@app.route('navigation', methods=['POST'])
def navigate_user():
    """ display a map with basic pins of each route """

    return render_template(navigation.html)

@app.route('route_info.json', methods=['POST'])
def route_info():
    """ forward route information to the google maps on the navigation route """

    #return jsonify(route_info)

@app.route('/logout')
def logout_user():
    """Logout a user"""

    session.clear()

    return redirect('/')



if __name__ == "__main__":

    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0', debug=True)
