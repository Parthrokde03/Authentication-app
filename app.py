from flask import Flask,render_template,redirect , request, session
import psycopg2

app = Flask(__name__)
app.secret_key = '@abc123DEF456#'

def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="psql123",
        host="localhost",
        port="5433"
    )


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = user[1]
            return redirect('/confirm')
        else:
            msg = "Invalid username or password"

    return render_template('login.html',message = msg)

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        phonenumber = request.form['phonenumber']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']        
        
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, password, address, phonenumber, city, state, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name,email, password,address,phonenumber,city,state,pincode))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/')
    return render_template('registration.html')

@app.route('/confirm')
def confirm():
    if not session.get('logged_in'):
        return redirect('/')
    username = session.get('username') 
    return render_template('validuser.html',username = username)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)