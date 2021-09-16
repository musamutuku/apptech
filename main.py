from flask import Flask, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.templating import render_template
import bcrypt

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import backref
import datetime


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret" 
jwt = JWTManager(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:musa@localhost/akiba"

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class UserAccount(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    pin = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    account_balance = db.Column(db.Integer, default=0)
    float_balance = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=3)

    def __init__(self, id, firstname, lastname, username, password, phone, pin):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.phone = phone
        self.pin = pin
        # self.account_balance = account_balance
        # self.float_balance = float_balance
        #self.role_id = role_id

class RoleAccount(db.Model):  
    
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50))
    users = db.relationship('UserAccount', backref='role', lazy=True)
    

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/checkrole', methods= ["POST"])
def CheckRole():
   # role_id = 3
   # user_role = RoleAccount.query.get(role_id)
   # print(user_role.role_name)
   # user = user_role.users
   # print(user)
   
    request_body = request.get_json()
    user_id = request_body['user_id']
    myrole = UserAccount.query.get(user_id).role
    my_role= myrole.role_name
   # myrole_id = UserAccount.query.get(user_id)
   # print(myrole_id.role_id)
    return f"my role is {my_role}"

@app.route('/register', methods = ["POST","GET"])
def Register():
    users = UserAccount.query.all()

    # getting form details from registration form
    if request.method == "POST":
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        id = request.form.get('id_no')
        phone = request.form.get('phone')
        pin = request.form.get('pin')
        confirm_pin = request.form.get('confirm_pin')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

    
        # get/check the entered user_id no and username in the users' table(database) (if any)
        user_ID = UserAccount.query.filter_by(id=id).first()
        new_user = UserAccount.query.filter_by(username=username).first()

        # check if the user_id and username are already used
        if user_ID is None:
            if new_user is not None:
                error_msg = "The username you entered is already taken!"
                error_msg2 = "Try again and use another username."
                return render_template("register_error2.html", username_error = error_msg, username_error2 = error_msg2)   
        else:
            idError = "The ID number you entered already exists!"
            idError2 = "Try again with another ID number."
            return render_template("register_error.html", id_error = idError, id_error2 = idError2)
        
        
        # encrypting the password and pin using hash function
        if confirm == password and pin == confirm_pin:
            encrpted_pass =  bcrypt.hashpw(password.encode(), bcrypt.gensalt(7))
            encrpted_pin = bcrypt.hashpw(pin.encode(), bcrypt.gensalt(7))
            registered_user = UserAccount(id,firstname,lastname,username,encrpted_pass.decode(),phone,encrpted_pin.decode())

        # add the details in the database
        db.session.add(registered_user)
        db.session.commit()
        return render_template('register_success.html')
    return render_template('register.html', users_list = users)
    

@app.route('/login', methods=['POST','GET'])
def Login():

    # getting form details from login form
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')

        # get/check the person with the entered username in the database
        current_user = UserAccount.query.filter_by(username=username).first()

        # check the existence of the person in the database
        # if current_user is not None:(opposite statement)
        if current_user is None:
             return render_template("login_error.html")
        else:
            # get the password and encrypt it and check the match with the one encrypted in the database(will be success or error)
             result = bcrypt.checkpw(password.encode(), current_user.password.encode())
             if result:
                 # check if he/she is the admin 
                 if current_user.role_id == 1:
                    return render_template('admin_home.html')
                 else:
                    return render_template('user_home.html', user = current_user)
             else:
                 return render_template("login_error.html")
    return render_template('login.html')


@app.route('/home')
def Home():
    return render_template("user_home.html")

@app.route('/admin')
def Admin():
    return render_template("admin_home.html")

@app.route('/admin/account')
def AdminAccount():
    return render_template("admin.html")

@app.route('/home/account')
def Account():
    return render_template("account.html")

@app.route('/account/deposit')
def Account1():
    return render_template("account.html")

@app.route('/account/withdraw')
def Account3():
    return render_template("account.html")


@app.route('/logout')
def Logout():
    return render_template("logout.html")


@app.route('/account/check_balance', methods=['POST','GET'])
def CheckBalance():
    if request.method == "POST":
        id = request.form.get('id_no')
        pin = request.form.get('pin_no')
        current_user = UserAccount.query.filter_by(id=id).first()

        if current_user is not None:
            if current_user.role_id != 1:
                result = bcrypt.checkpw(pin.encode(), current_user.pin.encode())
                if result:
                    if current_user.role_id == 3:
                        return render_template('user_balance.html', user = current_user)
                    elif current_user.role_id == 2:
                        return render_template('user_balance.html', agent = current_user)
                else:
                    pin_mismatch = "You have entered wrong PIN. Try again"
                    return render_template('user_balance.html', errored_pin_msg = pin_mismatch)
            else:
                try_check = "Confirm if the ID you entered is yours"
                return render_template('user_balance.html', check_msg = try_check)
        else:
             not_found_msg = "invalid ID number. Try again"
             return render_template('user_balance.html', not_found = not_found_msg )
    return render_template("account.html")


@app.route('/admin/check_balance', methods=['POST','GET'])
def CheckBalanceAdmin():
    if request.method == "POST":
        id = request.form.get('id_no')
        pin = request.form.get('pin_no')
        current_admin = UserAccount.query.filter_by(id=id).first()

        if current_admin is not None:
            if current_admin.role_id == 1:
                result = bcrypt.checkpw(pin.encode(), current_admin.pin.encode())
                if result:
                    return render_template('admin_balance.html', admin = current_admin)
                else:
                    pin_mismatch = "You have entered wrong PIN. Try again"
                    return render_template('admin_balance.html', errored_pin_msg = pin_mismatch)
            else:
                try_check = "Confirm if the ID you entered is yours"
                return render_template('admin_balance.html', check_msg = try_check)
        else:
             not_found_msg = "invalid ID number. Try again"
             return render_template('admin_balance.html', not_found = not_found_msg )
    return render_template("admin.html")


@app.route('/deposit', methods= ['POST'])
def Deposit():
    request_body = request.get_json()

    # variable to get an agent
    agent_id = request_body['agentId']

    # variable to store the agent by (get) to obtain one
    # to get more than one agent use (filter_by()) 
    agent = UserAccount.query.get(agent_id)

    # varible to define the amount to deposit
    amount = request_body['amount']

    if agent is not None:

        # to check if the float is enough to deposit the amount
        if agent.float_balance >= amount:

            # go find a user
            user_id = request_body['userID']
            user = UserAccount.query.get(user_id)

            # deposit the amount to their account
            # return the user object as a json object, return the agent account with the updated float balance
            user.account_balance += amount
            db.session.add(user)
            db.session.commit()

            agent.float_balance -= amount
            db.session.add(agent)
            db.session.commit()
            
            one_user = UserAccount.query.get(user_id)
            one_agent = UserAccount.query.get(agent_id)
            user_data = {
                "account_balance": one_user.account_balance,
                "firstname": one_user.firstname
            }
            agent_data = {
                "username": one_agent.username,
                "float_balance": one_agent.float_balance
            }
            return jsonify(user_data, agent_data)
        else:
            # the agent account has no enough money to deposit
            # user goes away
            error_message = 'no enough funds to deposit {}'.format(amount)
            return error_message
    else:
        return {"error": "agent not found, confirm your id"}

    

@app.route('/withdraw', methods= ['GET'])
def WithdrawCash():
    request_body = request.get_json()
    user_id = request_body['userID']
    user = UserAccount.query.get(user_id)
    amount = request_body['amount']
    if user is not None:
        if user.account_balance >= amount:
            user.account_balance -= amount
            db.session.add(user)
            db.session.commit()
            return 'Your have successfully withdrawn {0}.Your new balance is {1}'.format(amount,user.account_balance)
        else:
            error_message = 'You have insufficient balance to withdraw such amount'
            return error_message
        
    else:
        return {"error": "user not found, confirm your id"}


if __name__ == "__main__":
    app.run()