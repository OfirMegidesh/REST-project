from flask import Flask
from flask import render_template, request, redirect, url_for
import logging
import sqlite3

filename='page.log',
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


@app.route('/users/put', methods=['POST'])
def users_put():
    try:
        real_id = request.form['real_id']
        full_name = request.form['full_name']
        password = request.form['password']
        conn = getconn()
        id = conn.execute(f'SELECT id_AI FROM users WHERE real_id = {real_id}')
        id_ai = ''
        for row in id:
            id = str(row)
            for i in range(len(id)):
                if id[i].isdigit():
                    id_ai += id[i]
        conn.execute(f'UPDATE users SET full_name = "{full_name}", password = "{password}" WHERE id_AI = {id_ai}')
        conn.commit()
        logging.debug(f'updating the user with the id {real_id}')
        conn.close()
        return 'the update succeeded'
    except:
        logging.debug('oh no something went wrong')
        return render_template('error.html')


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
            conn = getconn()
            flight_id = request.form['flight id']
            logging.debug(
                f"printing to the user {id_ai} all the available flights and adding the ticket to flight num {flight_id}")
            conn.execute(f'INSERT INTO tickets (user_id, flight_id) VALUES ({id_ai},{flight_id})')
            conn.commit()
            conn.execute(
                f'UPDATE flights set remaining_seats = (SELECT remaining_seats FROM flights WHERE flight_id = {flight_id}) -1')
            conn.commit()
            conn.close()
            return 'the action completed'
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')



# request to delete a ticket according to a given id
@app.route('/tickets/delete', methods=['POST'])
def delete_ticket():
    try:
        conn = getconn()
        ticket_id = request.form['ticket_id']
        logging.debug(f'deleting the ticket where the id = {ticket_id}')
        fli_id = getconn().execute(f'SELECT flight_id FROM tickets WHERE ticket_id = {ticket_id}')
        flight_id = ''
        for row in fli_id:
            id = str(row)
            for i in range(len(id)):
                if id[i].isdigit():
                    flight_id += id[i]
        conn.execute(f'DELETE FROM tickets WHERE ticket_id  = {ticket_id}')
        conn.commit()
        conn.execute(
            f'UPDATE flights set remaining_seats = (SELECT remaining_seats FROM flights WHERE flight_id = {flight_id}) +1')
        conn.commit()
        conn.close()
        return 'the action completed'

    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/tickets/get', methods=['GET'])
def tickets_get():
    try:
        # request for all the tickets
        logging.debug("returning all the tickets ")
        conn = getconn()
        tickets = conn.execute(f'SELECT * FROM tickets')
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
            conn = getconn()
            logging.debug(f"returning the tickets of the user {id_ai}")
            ticket = conn.execute(f'SELECT * FROM tickets WHERE user_id = {id_ai}')
            variable = ""
            for row in ticket:
                a = f'ticket_id:{row[0]}, user_id:{row[1]}, flight_id:{row[2]}|||||\n'
                variable = variable + a
            conn.close()
            return variable
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


@app.route('/tickets/<int:t_id>', methods=['GET'])
def ticket_get1(t_id):
    try:
        # request of a specific ticket
        if request.method == 'GET':
            conn = getconn()
            logging.debug(f"returning the ticket where the id={t_id}")
            ticket = conn.execute(f'SELECT * FROM tickets WHERE ticket_id = {t_id}')
            variable = ""
            for row in ticket:
                a = f'ticket_id:{row[0]}, user_id:{row[1]}, flight_id:{row[2]}|||||\n'
                variable = variable + a
            conn.close()
            return variable
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


# request to update a flight that's already exist
@app.route('/flights/put', methods=['POST'])
def flights_put():
    try:
        conn = getconn()
        flight_id = request.form['flight_id']
        timestamp = request.form['timestamp']
        remaining_seats = request.form['remaining_seats']
        origin_country_id = request.form['origin_country_id']
        dest_country_id = request.form['dest_country_id']
        conn.execute(f'UPDATE flights SET timestamp = \'{timestamp}\', remaining_seats = {remaining_seats}, origin_country_id = {origin_country_id}, dest_country_id = {dest_country_id} WHERE flight_id = {flight_id}')
        conn.commit()
        conn.close()
        logging.debug(f'updating the flight where the id = {flight_id}')
        return 'the update succeeded'
    except:
        logging.debug('oh no something went wrong')
        return render_template('error.html')


@app.route('/flights/get_post', methods=['GET', 'POST'])
def flights_get_post():
    try:
        # request for all the flights
        if request.method == 'GET':
            conn = getconn()
            logging.debug("returning all the flights that's available")
            flights = conn.execute(f'SELECT * FROM flights WHERE remaining_seats > 0')
            conn.close()
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
            conn = getconn()
            timestamp = request.form['time']
            remaining_seats = request.form['remaining seats']
            origin_country_id = request.form['original country id']
            dest_country_id = request.form['destination country id']
            conn.execute(f'INSERT INTO flights(timestamp, origin_country_id, dest_country_id, remaining_seats) VALUES(\'{timestamp}\',{origin_country_id},{dest_country_id}, {remaining_seats})')
            conn.commit()
            conn.close()
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
            conn = getconn()
            logging.debug(f"getting the flights with the id {flight_id}")
            flight = conn.execute(f'SELECT * FROM flights WHERE flight_id = {flight_id}')
            variable = ""
            for row in flight:
                a = f'flight_id:{row[0]}, timestamp:{row[1]}, remaining_seats:{row[2]}, original_country_id:{row[3]}, dest_country_id:{row[4]}|||\n'
                variable = variable + a
            conn.close()
            return variable
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')
    try:
        # request to delete a flight according to a given id
        if request.method == 'DELETE':
            conn = getconn()
            logging.debug(f"deleting the flights with the id {flight_id}")
            conn.execute(f'DELETE FROM flights WHERE flight_id = {flight_id}')
            conn.commit()
            conn.close()
            return 'the action completed'
    except:
        logging.debug("oh no something went wrong")
        return render_template('error.html')


app.run()
