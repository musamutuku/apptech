from flask import Flask, request, url_for, redirect
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.templating import render_template
import bcrypt
import os , datetime
from sqlalchemy.orm import backref
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:musa@localhost/akiba"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserAccount(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    pin = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    account_balance = db.Column(db.Float, default=0.0)
    float_balance = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=3)
    profile_pic = db.Column(db.String(100))

    def __init__(self, id, firstname, lastname, username, password, phone, pin, profile_pic):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.phone = phone
        self.pin = pin
        self.profile_pic = profile_pic

class RoleAccount(db.Model):   
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50))
    users = db.relationship('UserAccount', backref='role', lazy=True)


class TransactionAccount(db.Model):
    __tablename__ = "transactions"

    ref_no = db.Column(db.String(15), primary_key=True)
    id_no = db.Column(db.Integer)
    date = db.Column(db.String(100))
    deposit = db.Column(db.String(100))
    withdrawal = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __init__(self, ref_no, id_no, date, deposit, withdrawal, status):
        self.ref_no = ref_no
        self.id_no = id_no
        self.date = date
        self.deposit = deposit
        self.withdrawal = withdrawal
        self.status = status
    

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/admin/system_users')
def ViewUsers():
    if 'id' in session and 'role' in session:
        role_id = session.get('role')
        if role_id == 1:
            role_id = 3
            users = UserAccount.query.filter_by(role_id=role_id).all()
            return render_template('users.html', users = users)
    return redirect(url_for('Login'))


@app.route('/admin/system_agents')
def ViewAgents():
    if 'id' in session and 'role' in session:
        role_id = session.get('role')
        if role_id == 1:
            role_id = 2
            users = UserAccount.query.filter_by(role_id=role_id).all()
            return render_template('agents.html', users = users)
    return redirect(url_for('Login'))

    # user_id = 33771492
   # user_role = RoleAccount.query.get(role_id)
   # print(user_role.role_name)
   # user = user_role.users
   # print(user)
   
    # request_body = request.get_json()
    # user_id = request_body['user_id']
    # myrole = UserAccount.query.get(user_id).role
    # my_role= myrole.role_name
   # myrole_id = UserAccount.query.get(user_id)
   # print(myrole_id.role_id)
    # return f"my role is {my_role}"

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
            encrpted_pass =  bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
            encrpted_pin = bcrypt.hashpw(pin.encode(), bcrypt.gensalt(14))
            registered_user = UserAccount(id,firstname,lastname,username,encrpted_pass.decode(),phone,encrpted_pin.decode(),profile_pic='default.png')

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
                 session['id'] = current_user.id
                 session['role'] = current_user.role_id
                 # check if he/she is the admin 
                 if current_user.role_id == 1:
                    return render_template('admin_home.html', user = current_user)
                 else:
                    return render_template('user_home.html', user = current_user)
             else:
                 return render_template("login_error.html")
    return render_template('login.html')



@app.route('/logout')
def logout():
    if 'id' in session:
        session.pop('id', None)
        return redirect(url_for('index'))
    return redirect(url_for('Login'))


@app.route('/home')
def Home():
    if 'id' in session and 'role' in session:
        user_id = session.get('id')
        role_id = session.get('role')
        if role_id != 1:
            current_user = UserAccount.query.get(user_id)
            return render_template("user_home.html",user = current_user)
    return redirect(url_for('Login'))

@app.route('/admin')
def Admin():
    if 'id' in session and 'role' in session:
        role_id = session.get('role')
        if role_id == 1:
            return render_template("admin_home.html")
    return redirect(url_for('Login'))


@app.route('/admin/account')
def AdminAccount():
    if 'id' in session and 'role' in session:
        role_id = session.get('role')
        if role_id == 1:
            return render_template("admin.html")
    return redirect(url_for('Login'))


@app.route('/home/account')
def Account():
    if 'id' in session and 'role' in session:
        role_id = session.get('role')
        if role_id == 2:
            return render_template("account.html")
        elif role_id == 3:
            return render_template('user_account.html')
    return redirect(url_for('Login'))


@app.route('/userDetails')
def UserEditing():
    if 'id' in session and 'role' in session:
        user_id = session.get('id')
        role_id = session.get('role')
        if role_id != 1:
            current_user = UserAccount.query.get(user_id)
            return render_template("user_details.html", user = current_user)
        else:
            current_user = UserAccount.query.get(user_id)
            return render_template("admin_details.html", user = current_user)
    return redirect(url_for('Login'))


@app.route('/userDetails/editData', methods = ['POST','GET'])
def UserSaving():
    if request.method == "POST":
        if 'id' in session:
            user_id = session.get('id')
            name1 = request.form.get('name1')
            name2 = request.form.get('name2')
            name3 = request.form.get('name3')
            name4 = request.form.get('name4')
            current_user = UserAccount.query.get(user_id)

            current_user.username = name1
            current_user.firstname = name2
            current_user.lastname = name3
            current_user.phone = name4
            db.session.add(current_user)
            db.session.commit()
                                
            one_user = UserAccount.query.get(user_id)
            role_id = session.get('role')
            if role_id != 1:
                return render_template("user_details.html", user = one_user)
            else:
                return render_template("admin_details.html", user = one_user)
    return redirect(url_for('Login'))


@app.route('/userDetails/editPhoto', methods = ['POST','GET'])
def PhotoUpload():
    if request.method == "POST":
        if 'id' in session:
            user_id = session.get('id')
            pic = request.files['pic']

            user = UserAccount.query.get(user_id)
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            user.profile_pic = filename
            db.session.add(user)
            db.session.commit()

            one_user = UserAccount.query.get(user_id)
            role_id = session.get('role')
            if role_id != 1:
                return render_template("user_details.html", user= one_user)
            else:
                return render_template("admin_details.html", user= one_user)
    return redirect(url_for('Login'))


@app.route('/account/check_balance', methods=['POST','GET'])
def CheckBalance():
    if request.method == "POST":
        if 'id' in session:
            user_id = session.get('id')
            id = int(request.form.get('id_no'))
            pin = request.form.get('pin_no')
            if user_id == id:
                current_user = UserAccount.query.filter_by(id=id).first()
                if current_user is not None:
                    if current_user.role_id != 1:
                        result = bcrypt.checkpw(pin.encode(), current_user.pin.encode())
                        if result:
                            if current_user.role_id == 3:
                                time = datetime.datetime.now().strftime("%d/%m/%Y at %I:%M %p")
                                return render_template('user_balance.html', user = current_user, the_time = time)
                            elif current_user.role_id == 2:
                                time = datetime.datetime.now().strftime("%d/%m/%Y at %I:%M %p")
                                return render_template('user_balance.html', agent = current_user, the_time = time)
                        else:
                            pin_mismatch = "Sorry! You have entered wrong PIN. Try again."
                            return render_template('user_balance.html', errored_pin_msg = pin_mismatch)
                else:
                    not_found_msg = "Invalid ID! Please confirm your ID number and try again."
                    return render_template('user_balance.html', not_found = not_found_msg )
            else:
                not_found_msg = "Invalid ID! Please confirm your ID number and try again."
                return render_template('user_balance.html', not_found = not_found_msg )
    return redirect(url_for('Login'))


@app.route('/admin/check_balance', methods=['POST','GET'])
def CheckBalanceAdmin():
    if request.method == "POST":
        if 'id' in session:
            user_id = session.get('id')
            id = int(request.form.get('id_no'))
            pin = request.form.get('pin_no')
            current_admin = UserAccount.query.filter_by(id=id).first()
            if user_id == id:
                if current_admin is not None:
                    if current_admin.role_id == 1:
                        result = bcrypt.checkpw(pin.encode(), current_admin.pin.encode())
                        if result:
                            time = datetime.datetime.now().strftime("%d/%m/%Y at %I:%M %p")
                            return render_template('admin_balance.html', admin = current_admin, the_time = time)
                        else:
                            pin_mismatch = "Sorry! You have entered wrong PIN. Try again."
                            return render_template('admin_balance.html', errored_pin_msg = pin_mismatch)
                else:
                    not_found_msg = "Invalid ID! Please confirm your ID number and try again."
                    return render_template('admin_balance.html', not_found = not_found_msg)
            else:
                not_found_msg = "Invalid ID! Please confirm your ID number and try again."
                return render_template('admin_balance.html', not_found = not_found_msg)
    return redirect(url_for('Login'))


@app.route('/account/deposit', methods= ['GET','POST'])
def Deposit():
    # a varible to get agent
    if request.method == 'POST':
        if 'id' in session:
            agent_id = request.form.get('agent_id') 

            # variable to store the agent by (get) to obtain one
            # to get more than one agent use (filter_by()) 
            agent = UserAccount.query.get(agent_id)

            # variable to define the agent_pin and the amount to deposit
            pin = request.form.get('pin_no')
            amount = int(request.form.get('amount'))

            if agent is not None:
                if agent.role_id == 2:
                    result = bcrypt.checkpw(pin.encode(), agent.pin.encode())
                    if result:
                        # to check if the float is enough to deposit the amount
                        if agent.float_balance >= amount:

                            # go find a user
                            user_id = request.form.get('user_id')
                            user = UserAccount.query.get(user_id)
                            if user:
                                # deposit the amount to their account and update agent float_balance
                                user.account_balance += amount
                                db.session.add(user)
                                db.session.commit()

                                agent.float_balance -= amount
                                db.session.add(agent)
                                db.session.commit()
                                
                                one_user = UserAccount.query.get(user_id)
                            
                                time = datetime.datetime.now().strftime("%d/%m/%Y at %I:%M %p")
                                ref = datetime.datetime.now().strftime("%H%M%S")
                                refNo = 'TX{}'.format(ref)
                                theID = user.id
                                theAgent = agent.id
                                transaction = TransactionAccount(refNo,theID,time,amount,withdrawal='',status='SUCCESS')

                                db.session.add(transaction)
                                db.session.commit()
                                return render_template('user_balance.html', the_user=one_user, time=time, amount=amount, refNo=refNo, theID=theID, theAgent=theAgent)
                            else:
                                no_user = "Invalid user ID! Please confirm the user ID number and try again."
                                return render_template('user_balance.html', no_user_found = no_user)
                        else:
                            # the agent account has no enough money to deposit
                            no_float_msg= 'Sorry! You have no enough funds to deposit Ksh {}.'.format(amount)
                            return render_template("user_balance.html", no_float = no_float_msg)
                    else:
                        agent_pin_error = "Sorry! You have entered wrong PIN. Try again."
                        return render_template('user_balance.html', agent_pinerror = agent_pin_error)
                else:
                    no_agent = "Agent not found! Confirm your ID number and try again."
                    return render_template('user_balance.html', no_agent_found = no_agent)
            else:
                no_agent = "Agent not found! Confirm your ID number and try again."
                return render_template('user_balance.html', no_agent_found = no_agent)
    return redirect(url_for('Login'))
    

@app.route('/admin/deposit', methods= ['GET','POST'])
def DepositAdmin():
    if request.method == 'POST':
        if 'id' in session:
            admin_id = request.form.get('admin_id')  
            admin = UserAccount.query.get(admin_id)

            # variable to define the admin_pin and the amount to deposit
            pin = request.form.get('pin_no')
            amount = int(request.form.get('amount'))

            if admin is not None:
                if admin.role_id == 1:
                    result = bcrypt.checkpw(pin.encode(), admin.pin.encode())
                    if result:
                        # to check if the float is enough to deposit the amount
                        if admin.float_balance >= amount:

                            # go find a user
                            user_id = request.form.get('user_id')
                            user = UserAccount.query.get(user_id)
                            if user:
                                # deposit the amount to their account and update admin float_balance
                                user.account_balance += amount
                                db.session.add(user)
                                db.session.commit()

                                admin.float_balance -= amount
                                db.session.add(admin)
                                db.session.commit()
                                
                                one_user = UserAccount.query.get(user_id)
                                time = datetime.datetime.now().strftime("%d/%m/%Y at %I:%M %p")
                                ref = datetime.datetime.now().strftime("%H%M%S")
                                refNo = 'TX{}'.format(ref)
                                theID = user.id
                                theAdmin = admin.id
                                transaction = TransactionAccount(refNo,theID,time,amount,withdrawal='',status='SUCCESS')

                                db.session.add(transaction)
                                db.session.commit()
                                return render_template('admin_balance.html', the_user=one_user, time=time, amount=amount, refNo=refNo, theID=theID, theAdmin=theAdmin)
                            else:
                                no_user = "Invalid user ID! Please confirm the user ID number and try again."
                                return render_template('admin_balance.html', no_user_found = no_user)
                        else:
                            no_float_msg= 'Sorry! You have no enough funds to deposit Ksh {}.'.format(amount)
                            return render_template("admin_balance.html", no_float = no_float_msg)
                    else:
                        admin_pin_error = "Sorry! You have entered wrong PIN. Try again."
                        return render_template('admin_balance.html', admin_pinerror = admin_pin_error)
                else:
                    no_admin = "Admin not found! Confirm your ID number and try again."
                    return render_template('admin_balance.html', no_admin_found = no_admin)
            else:
                no_admin = "Admin not found! Confirm your ID number and try again."
                return render_template('admin_balance.html', no_admin_found = no_admin)
    return redirect(url_for('Login'))


@app.route('/account/withdraw', methods= ['GET','POST'])
def Withdraw():
    if request.method == 'POST':
        if 'id' in session:
            logged_user = session.get('id')
            agent_id = request.form.get('agent_id')
            user_id = int(request.form.get('user_id'))
            pin = request.form.get('pin_no')
            amount = int(request.form.get('amount'))
            agent = UserAccount.query.get(agent_id)

            if agent is not None:
                if agent.role_id == 2:
                    if logged_user == user_id:
                        user = UserAccount.query.get(user_id)
                        if user is not None:
                            result = bcrypt.checkpw(pin.encode(), user.pin.encode()) 
                            if result:
                                if user.account_balance > amount:
                                    user.account_balance = user.account_balance - (amount + (0.03*amount))
                                    user.account_balance = "{:.2f}".format(user.account_balance)
                                    db.session.add(user)
                                    db.session.commit()

                                    agent.float_balance += amount
                                    db.session.add(agent)
                                    db.session.commit()

                                    one_user = UserAccount.query.get(user_id)
                                    time = datetime.datetime.now().strftime("%d/%m/%Y at %I:%M %p")
                                    new_balance = one_user.account_balance
                                    theID = user.id
                                    theAgent = agent.id
                                    ref = datetime.datetime.now().strftime("%H%M%S")
                                    refNo = 'TX{}'.format(ref)
                                    transaction = TransactionAccount(refNo,theID,time,deposit='',withdrawal=amount,status='SUCCESS')
                                    db.session.add(transaction)
                                    db.session.commit()
                                    return render_template('user_balance.html', that_user=one_user, time=time, amount=amount, new_balance=new_balance, refNo=refNo, theID=theID, theAgent=theAgent)
                                else:
                                    withdraw_error_message = 'Sorry! You have insufficient balance to withdraw such amount.'
                                    return render_template('user_balance.html', withdraw_error_msg = withdraw_error_message)  
                            else:
                                pin_occured_err = "Sorry! You have entered wrong PIN. Try again"
                                return render_template('user_balance.html', pin_err = pin_occured_err) 
                        else:
                            userID_error = "Invalid ID! Please confirm your ID number and try again."
                            return render_template('user_balance.html', user_id_error = userID_error)
                    else:
                        userID_error = "Invalid ID! Please confirm your ID number and try again."
                        return render_template('user_balance.html', user_id_error = userID_error)
                else:
                    agentID_error = "Agent not found! Confirm the Agent ID and try again."
                    return render_template('user_balance.html', agentID_err = agentID_error)
            else:
                agentID_error = "Agent not found! Confirm the Agent ID and try again."
                return render_template('user_balance.html', agentID_err = agentID_error)
    return redirect(url_for('Login'))


@app.route('/admin/withdraw', methods= ['GET','POST'])
def WithdrawAdmin():

    agent_id = request.form.get('agent_id')
    user_id = int(request.form.get('user_id'))
    pin = request.form.get('pin_no')
    amount = int(request.form.get('amount'))
    agent = UserAccount.query.get(agent_id)

    if request.method == 'POST':
        if 'id' in session:
            logged_user = session.get('id')
            if agent is not None:
                if agent.role_id == 2:
                    if logged_user == user_id:
                        user = UserAccount.query.get(user_id)
                        if user is not None:
                            result = bcrypt.checkpw(pin.encode(), user.pin.encode()) 
                            if result:
                                if user.account_balance > amount:
                                    user.account_balance = user.account_balance - (amount + (0.03*amount))
                                    user.account_balance = "{:.2f}".format(user.account_balance)
                                    db.session.add(user)
                                    db.session.commit()

                                    agent.float_balance += amount
                                    db.session.add(agent)
                                    db.session.commit()

                                    one_user = UserAccount.query.get(user_id)
                                    time = datetime.datetime.now().strftime("%d/%m/%Y at %I:%M %p")
                                    new_balance = one_user.account_balance
                                    theID = user.id
                                    theAgent = agent.id
                                    ref = datetime.datetime.now().strftime("%H%M%S")
                                    refNo = 'TX{}'.format(ref)
                                    transaction = TransactionAccount(refNo,theID,time,deposit='',withdrawal=amount,status='SUCCESS')
                                    db.session.add(transaction)
                                    db.session.commit()
                                    return render_template('admin_balance.html', that_user=one_user, time=time, amount=amount, refNo=refNo, new_balance=new_balance, theID=theID, theAdmin=theAgent)
                                else:
                                    withdraw_error_message = 'Sorry! You have insufficient balance to withdraw such amount'
                                    return render_template('admin_balance.html', withdraw_error_msg = withdraw_error_message)  
                            else:
                                pin_occured_err = "Sorry! You have entered wrong PIN. Try again"
                                return render_template('admin_balance.html', pin_err = pin_occured_err) 
                        else:
                            userID_error = "Invalid ID! Please confirm your ID number and try again."
                            return render_template('admin_balance.html', user_id_error = userID_error)
                    else:
                        userID_error = "Invalid ID! Please confirm your ID number and try again."
                        return render_template('admin_balance.html', user_id_error = userID_error)
                else:
                    agentID_error = "Agent not found! Confirm the Agent ID and try again."
                    return render_template('admin_balance.html', agentID_err = agentID_error)
            else:
                agentID_error = "Agent not found! Confirm the Agent ID and try again."
                return render_template('admin_balance.html', agentID_err = agentID_error)
    return redirect(url_for('Login'))


@app.route('/admin/system_info')
def SystemInfo():
    if 'id' in session and 'role' in session:
        role_id = session.get('role')
        if role_id == 1:
            return render_template('system_info.html')
    return redirect(url_for('Login'))


@app.route('/account/statement')
def ViewStatement():
    if 'id' in session and 'role' in session:
        role_id = session.get('role')
        user_id = session.get('id')
        if role_id != 1:
            transactions = TransactionAccount.query.filter_by(id_no=user_id).all()
            if(len(transactions)< 1):
                no_tx = "You have zero transaction!"
                return render_template('account_statement.html', no_tx = no_tx)
            download = "download"
            return render_template('account_statement.html', transactions = transactions, download=download)
    return redirect(url_for('Login'))
    

if __name__ == "__main__":
    app.run(host="0.0.0.0")