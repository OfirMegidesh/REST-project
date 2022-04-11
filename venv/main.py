import json
from flask import Flask
from flask import render_template, request, redirect, url_for
import logging
import sqlite3

# filename='page.log',
logging.basicConfig(level=logging.DEBUG)


def getconn():
    conn = sqlite3.connect(r'C:\Users\eliav\Downloads\data.db')
    return conn


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    logging.debug("opening home page")
    return render_template('homepage.html')


@app.route('/users_home', methods=['GET'])
def users():
    logging.debug("opening the users html")
    return render_template('theUsersSite.html')


@app.route('/users', methods=['GET', 'POST'])
def users_get_post():
    # request for all the users
    try:
        if request.method == 'GET':
            conn = getconn()
            users2 = conn.execute('SELECT * FROM users')
            variable = ""
            for row in users2:
                user = f'id_ai:{row[0]}, full_name:{row[1]}, password:{row[2]}, real_id:{row[3]}\n'
                variable = variable + user
            conn.close()
            return variable
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')
    try:
        # request to create a new user
        if request.method == 'POST':
            conn = getconn()
            full_name = request.form['full name']
            password = request.form['psw']
            user_id = request.form['id']
            print('post' + user_id)
            conn.execute(
                f'INSERT INTO users (full_name, password, real_id) VALUES ("{full_name}","{password}","{user_id}")')
            conn.commit()
            global id_ai
            id_ai = conn.execute(f'SELECT id_AI FROM users WHERE real_id =  "{user_id}"')
            conn.close()
            logging.debug(f"posting the new user {full_name} and opening the tickets page")
            return render_template('theTicketSite.html')
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/sign_in', methods=['POST'])
def user_sign():
    try:
        conn = getconn()
        user_id = request.form['id_g']
        password = request.form['psw_g']
        conn.execute(f'SELECT * FROM users WHERE real_id = {user_id} AND password = {password}')
        id = conn.execute(f'SELECT id_AI FROM users WHERE real_id = {user_id} AND password = {password}')
        global id_ai
        id_ai = ''
        for row in id:
            id = str(row)
            for i in range(len(id)):
                if id[i].isdigit():
                    id_ai += id[i]
        conn.close()
        logging.debug(f"returning the user where id={user_id} and password={password} and saving the id_AI {id_ai}")
        return render_template('theTicketSite.html')
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/users/<int:id>', methods=['GET', 'DELETE'])
def user_g_d(id):
    try:
        # request of a specific user
        if request.method == 'GET':
            logging.debug(f"returning user {id}")
            conn = getconn()
            user = conn.execute(f'SELECT * FROM users WHERE id_AI = {id}')
            variable = ""
            for row in user:
                a = f'id_ai:{row[0]}, full_name:{row[1]},password:{row[2]}, real_id:{row[3]}'
                variable = variable + a
            conn.close()
            return variable

    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')

    try:
        # request to delete a user according to a given id
        if request.method == 'DELETE':
            logging.debug(f"deleting the user {id}")
            conn = getconn()
            conn.execute(f'DELETE FROM users WHERE  id_AI = {id}')
            conn.commit()
            conn.close()
            return 'the ticket have been deleted'
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')

########### the first problem###########
@app.route('/users/put', methods=['PUT'])
def users_put():
    print('here')
    try:
        print(1)
        # request to update a user that's already exist
        full_name = request.form['fullname_p']
        print(2)
        password = request.form['psw_p']
        print(3)
        real_id = request.form['id_p']
        print(4)
        logging.debug(f"updating the user where the id is {real_id}")
        conn = getconn()
        id = f'SELECT id_AI FROM users WHERE real_id = "{real_id}"'
        id_ai = ''
        for row in id:
            id = str(row)
            for i in range(len(id)):
                if id[i].isdigit():
                    id_ai += id[i]
        conn.execute(
            f'UPDATE users SET full_name = "{full_name}", password = "{password}", real_id = "{real_id}" WHERE id_AI = {id_ai}')
        conn.commit()
        conn.close()
        return 'action completed'
    except:
        print(5)
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/home_tickets', methods=['GET'])
def tickets():
    try:
        logging.debug("entering the tickets html")
        return render_template('theTicketSite.html')
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/tickets/post', methods=['POST'])
def tickets_post():
    try:
        # request to create a new ticket
        if request.method == 'POST':
            flight_id = request.form['flight id']
            logging.debug(
                f"printing to the user {id_ai} all the available flights and adding the ticket to flight num {flight_id}")
            getconn().execute(f'INSERT INTO tickets (user_id, flight_id) VALUES ({id_ai},{flight_id})')
            getconn().commit()
            getconn().execute(
                f'UPDATE flights set remaining_seats = (SELECT remaining_seats FROM flights WHERE flight_id = {flight_id}) -1')
            getconn().commit()
            getconn().close()
            return 'the action completed'
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/tickets/get', methods=['GET'])
def tickets_get():
    try:
        # request for all the tickets
        logging.debug("returning all the tickets ")
        tickets = getconn().execute(f'SELECT * FROM tickets')
        variable = ""
        for row in tickets:
            a = f'ticket_id:{row[0]}, user_id:{row[1]}, flight_id:{row[2]}\n'
            variable = variable + a
        return variable
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/tickets/user', methods=['GET'])
def ticket_get():
    try:
        # request of a tickets of a specific user.
        if request.method == 'GET':
            logging.debug(f"returning the tickets of the user {id_ai}")
            ticket = getconn().execute(f'SELECT * FROM tickets WHERE user_id = {id_ai}')
            variable = ""
            for row in ticket:
                a = f'ticket_id:{row[0]}, user_id:{row[1]}, flight_id:{row[2]}|||||\n'
                variable = variable + a
            getconn().close()
            return variable
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/tickets/<int:t_id>', methods=['GET'])
def ticket_get1(t_id):
    try:
        # request of a specific ticket
        if request.method == 'GET':
            logging.debug(f"returning the ticket where the id={t_id}")
            ticket = getconn().execute(f'SELECT * FROM tickets WHERE ticket_id = {t_id}')
            getconn().close()
            variable = ""
            for row in ticket:
                a = f'ticket_id:{row[0]}, user_id:{row[1]}, flight_id:{row[2]}|||||\n'
                variable = variable + a
            return variable
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')

########### this is the second problem###########
@app.route('/tickets/delete', methods=['DELETE'])
def ticket_delete():
    try:
        # request to delete a ticket according to a given id
        if request.method == 'DELETE':
            id = request.form['id']
            logging.debug(f"deleting the ticket where id={id}")
            flight_id = getconn().execute(f'SELECT flight_id FROM tickets WHERE ticket_id = {id}')
            getconn().execute(f'DELETE FROM tickets WHERE ticket_id  = {id}')
            getconn().commit()
            getconn().execute(
                f'UPDATE flights set remaining_seats = (SELECT remaining_seats FROM flights WHERE flight_id = {flight_id}) +1')
            getconn().commit()
            getconn().close()
            return 'the action completed'
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/flights_home', methods=['GET'])
def flights_page():
    try:
        logging.debug("opening the flights html")
        return render_template('theFlightSite.html')
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/flights/get_post', methods=['GET', 'POST'])
def flights_get_post():
    try:
        # request for all the flights
        if request.method == 'GET':
            logging.debug("returning all the flights that's available")
            flights = getconn().execute(f'SELECT * FROM flights WHERE remaining_seats > 0')
            getconn().close()
            variable = ""
            for row in flights:
                a = f'flight_id:{row[0]}, timestamp:{row[1]}, remaining_seats:{row[2]}, original_country_id:{row[3]}, dest_country_id:{row[4]}|||\n'
                variable = variable + a
            return variable
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')
    try:
        # request to create a new flight
        if request.method == 'POST':
            timestamp = request.form['time']
            remaining_seats = request.form['remaining seats']
            origin_country_id = request.form['original country id']
            dest_country_id = request.form['destination country id']
            getconn().execute(
                f'INSERT INTO flights(timestamp, origin_country_id, dest_country_id, remaining_seats) VALUES(\'{timestamp}\',{origin_country_id},{dest_country_id}, {remaining_seats})')
            getconn().commit()
            getconn().close()
            logging.debug(f"posting a new flight")
            return 'the action completed'

    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/flights/<int:flight_id>', methods=['GET', 'DELETE'])
def flights_get_delete(flight_id):
    try:
        # request of a specific flight
        if request.method == 'GET':
            logging.debug(f"getting the flights with the id {flight_id}")
            flight = getconn().execute(f'SELECT * FROM flights WHERE flight_id = {flight_id}')
            variable = ""
            for row in flight:
                a = f'flight_id:{row[0]}, timestamp:{row[1]}, remaining_seats:{row[2]}, original_country_id:{row[3]}, dest_country_id:{row[4]}|||\n'
                variable = variable + a
            getconn().close()
            return variable
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')
    try:
        # request to delete a flight according to a given id
        if request.method == 'DELETE':
            logging.debug(f"deleting the flights with the id {flight_id}")
            getconn().execute(f'DELETE FROM flights WHERE flight_id = {flight_id}')
            getconn().commit()
            getconn().close()
            return 'the action completed'
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


###########this is the last problem###########
@app.route('/flights/put', methods=['PUT'])
def flights_put():
    try:
        # request to update a flight that's already exist
        if request.method == 'PUT':
            flight_id = request.form['id']
            timestamp = request.form['time']
            remaining_seats = request.form['remaining seats']
            origin_country_id = request.form['original country id']
            dest_country_id = request.form['destination country id']
            getconn().execute(
                f'UPDATE flights SET timestamp = {timestamp}, origin_country_id = {origin_country_id}, dest_country_id = {dest_country_id}, remaining_seats = {remaining_seats} WHERE flight_id = {flight_id}')
            getconn().commit()
            getconn().close()
            logging.debug(f"updating the flight where the id = {flight_id}")
            return 'the update succeeded'
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


app.run()
