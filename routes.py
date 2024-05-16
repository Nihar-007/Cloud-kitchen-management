from flask import *
from __main__ import app
from models import *
import os

#customer

@app.route("/")
def HomePage():
    data = Categories.query.all()
    return render_template('home.html',data=data)


@app.route("/home", methods=['POST','GET']) #cus tracking
def home():
    count=1
    if('uname' in session):
        data = Categories.query.all()
        if(request.method=='POST'):
            user_dict = json.loads(request.form['user_dict'])
            ip=user_dict['ipv6']
            ip4=user_dict['ipv4']
            if(Ip.query.filter_by(ipv6=ip,ipv4=ip4).first()):
                count += 1
                return json.jsonify({'count':count})
            else:
                entry = Ip(ipv4=user_dict['ipv4'] ,ipv6=user_dict['ipv6'], country=user_dict['country'], state=user_dict['state'], city=user_dict['city'], time=user_dict['time'], isp=user_dict['isp'])
                db.session.add(entry)
                db.session.commit()
            # print(user_dict)
            
        return render_template('customer.html',data=data)
    else:
        return redirect('login')

@app.route("/contact", methods=['GET','POST'])
def ContactUs():
    if request.method == 'POST':
        uname = session['uname']
        email = session['email']
        msg = request.form['msg']
        entry = Contact(username=uname,email=email,message=msg)
        db.session.add(entry)
        db.session.commit()
        return redirect('home')
    return render_template('contact.html')

@app.route("/about")
def aboutUs():       
    return render_template('about.html')

@app.route("/menu")
def menu():
    data = Categories.query.all()
    return render_template('menu.html',data=data)

@app.route("/offer", methods=['GET','POST'])
def OfferPage():
    if('uname' in session):
        data = Offer.query.all()
        return render_template('offers.html',data=data) 

@app.route("/orderHistory", methods=['GET','POST'])
def orderHistory():
    user = session['uname']
    if request.method == "POST":
        req = request.get_json()
        title=[]
        price=[]
        quantity=[]
        for i in req:
            title.append(i['title'])
            price.append(i['price'])
            quantity.append(i['quantity'])
        total = req[0]['totalamount']
        # converting list into JSON
        tj=json.dumps(title)
        pj=json.dumps(price)
        qj=json.dumps(quantity)
        entry = Order_history(username=user, items=tj, quantity=qj, amount=pj, total=total)
        db.session.add(entry)
        db.session.commit()
    ud = Order_history.query.filter_by(username=user).all()
    return render_template('orderHistory.html',d1=ud,user=user)

@app.route('/admin', methods=['GET','POST'])
def admin():
    return render_template('admin.html')

@app.route('/admin/Add Manager', methods=['GET','POST'])
def addManager():
    if request.method == 'POST':
        name=request.form['name']
        uname=request.form['uname']
        email=request.form['email']
        phno=request.form['phno']
        password=request.form['password']
        cpassword=request.form['cpassword']
        desc=request.form['desc']
        if password==cpassword:
            entry = Signup(name=name, username=uname, email=email, phno=phno, passwd=password, description=desc)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('admin'))
    return render_template('addManager.html')

@app.route('/admin/Manager Details', methods=['GET','POST'])
def managerDetails():
    data = Signup.query.filter_by(description='manager').all()
    return render_template('managerDetails.html',data=data)

#live search      
@app.route("/livesearch", methods=['GET','POST'])
def liveSearch():
    if request.method == 'POST':
        tag = request.form['q']
        s = "%{}%".format(tag)
        print(s)
        search = Categories.query.filter(Categories.item.like(s)).all()
        res = [{"id": result.id,"item": result.item,"category": result.category,"price": result.price,"image":result.image} for result in search]
        return jsonify(res)
    return render_template('customer.html')

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name1 = request.form['name']
        uname1 = request.form['username']
        email1 = request.form['email']
        phno1 = request.form['phone']
        passwd1 = request.form['password']
        cpasswd = request.form['confirm-password']

        if passwd1==cpasswd:
            entry = Signup(name=name1 ,username=uname1 ,email=email1 ,phno=phno1 ,passwd=passwd1)
            db.session.add(entry)
            db.session.commit()
            flash(f"Registration Successful! hello {name1}!")
            return redirect('login')    
    return render_template('signup.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname = request.form['uname']
        passwd = request.form['password']

        try:
            user = Signup.query.filter_by(username=uname).first()
            pas = user.passwd

            if passwd == pas:
                session['uname'] = uname
                session['email'] = user.email
                session['phno'] = user.phno
                if user.description=="manager" :
                    return redirect(url_for('manager'))
                else:
                    return redirect(url_for('home'))
            else:
                flash("Incorrect username or password. Please try again.")
                return redirect('login')
        
        except:
            flash('Contact to admin for further details')
            return redirect(url_for('login'))
            
    
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('uname',None)
    session.pop('email',None)
    session.pop('phno',None)
    return redirect(url_for('HomePage'))

# Manager

@app.route("/manager")
def manager():
    return render_template('manager.html')

#  RESOURCE
@app.route("/manager/resource")
def resource():
    if 'uname' in session:
        uname=session['uname']
        data = Resource.query.all()
        name = Signup.query.filter_by(username=uname).first()
    return render_template('resource.html',data=data,name=name)

@app.route("/manager/resource/restock/<int:id>", methods=['GET','POST'])
def restock(id):
    data = Resource.query.filter_by(id=id).first()
    if request.method=='POST':
        # item = request.form['item']
        data.quantity = request.form['qty']
        db.session.commit()    
        return redirect(url_for('resource'))
    
    return render_template('restock.html',data=data)

@app.route("/manager/resource/Add-Items", methods=['GET','POST'])
def AddItem():
    if request.method == 'POST':
        item = request.form['item']
        qty = request.form['qty']
        entry = Resource(item=item,quantity=qty)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('resource'))

    return render_template('AddItem.html')

@app.route("/manager/CustomerDetails")
def customerDetails():
    data = Signup.query.filter_by(description='customer').all()
    return render_template('customerDetails.html',data=data)

@app.route("/manager/Chef")
def chef():
    return render_template('chef.html')

# Add cuisine
@app.route("/manager/Cuisine", methods=['GET','POST'])
def CuisineManager():
    data = Categories().query.all()
    return render_template('CuisineManager.html',data=data)

@app.route("/manager/Cuisine/AddCusine", methods=['GET','POST'])
def AddCuisine():
    if request.method=='POST':
        name = request.form['name']
        cat = request.form['cat']
        price = request.form['price']
        file = request.files['img'] #importing file from form data which will be stored in 'file variable in form of array'
        
        #File storing
        img = file.filename # taking filename in 'img' variable from 'file' array which is taking file data from 'form'
        extension = os.path.splitext(file.filename)[1] # splitting extension of file from file name 
        if extension not in app.config['ALLOWED_EXTENSIONS']: #checking if extension is not there in the given file
            return 'File type is not allowed'
        file.save(os.path.join(
            'static/restimg/',file.filename # storing image on given location
        ))
        
        entry = Categories(category=cat,item=name,price=price,image=img)
        db.session.add(entry)
        db.session.commit()
        # print(file) --> <FileStorage: 'Idli Sambar.jpeg' ('image/jpeg')> this is the format of file which is taken from HTML FORM
        return redirect(url_for('CuisineManager'))
    return render_template('AddCuisine.html')

@app.route("/manager/cuisine/delete/<int:id>", methods=['GET','POST'])
def DeleteCuisine(id):
    df = Categories.query.filter_by(id=id).first()
    db.session.delete(df)
    db.session.commit()
    return redirect(url_for('CuisineManager'))

@app.route("/manager/cuisine/edit/<int:id>", methods=['GET','POST'])
def EditCuisine(id):
    data = Categories.query.filter_by(id=id).first()
    if request.method=='POST':
        data.item = request.form['name']
        data.category = request.form['cat']
        data.price = request.form['price']

        db.session.commit()

        return redirect(url_for('CuisineManager'))

    return render_template('EditCuisine.html',data=data)

# order_details
@app.route("/manager/order details", methods=['GET','POST'])
def OrderPending():
    if "uname" in session:
        user = session['uname']
        data = Order_pending.query.all()
    return render_template('order_pending.html',data=data,user=user)

@app.route("/manager/order details/completed/<int:id>", methods=['GET','POST'])
def OrderCompleted(id):
    data = Order_pending.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('OrderPending'))

#  OFFERS
@app.route("/manager/offer", methods=['GET','POST'])
def OfferManager():
    data = Offer.query.all()
    return render_template('ManagerOffer.html',data=data)

@app.route("/manager/offer/add", methods=['GET','POST'])
def AddOffer():
    if request.method == 'POST':
        name=request.form['name']
        code=request.form['code']
        # start=request.form['start']
        valid=request.form['valid']
        entry = Offer(code=code, offer_on=name, valid=valid)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('OfferManager'))
        
    return render_template('AddOffer.html')

@app.route("/manager/offer/delete/<int:id>", methods=['GET','POST'])
def DeleteOffer(id):
    df = Offer.query.filter_by(id=id).first()
    db.session.delete(df)
    db.session.commit()
    return redirect(url_for('OfferManager'))

@app.route("/manager/offer/edit/<int:id>", methods=['GET','POST'])
def EditOffer(id):
    data = Offer.query.filter_by(id=id).first()
    if request.method=='POST':
        data.offer_on = request.form['name']
        data.code = request.form['code']
        data.valid = request.form['valid']
        db.session.commit()
        return redirect(url_for('OfferManager'))

    return render_template('EditOffer.html',data=data)

