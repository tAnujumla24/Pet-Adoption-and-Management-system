from flask import Flask,render_template,request,redirect,url_for,session, flash
from  flask_mysqldb import MySQL
import bcrypt


app = Flask(__name__)

app.secret_key = 'secret'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin@00'
app.config['MYSQL_DB'] = 'pet_shop'

mysql = MySQL(app)

def get_db_connection():
    return mysql.connection



@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/about')
def aboutus_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT GetTotalOrders()")
    ans = cur.fetchone()
    cur.close()

    return render_template("about_us.html",ans=ans)





@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = get_db_connection().cursor()

        cur.execute("SELECT * FROM users1 WHERE username = %s", (username,))
        user = cur.fetchone()

        cur.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]

            flash('Login successful!', 'success')
            return redirect(url_for('home_page'))

        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template("login.html")

@app.route("/services")
def service_page():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM services")
    services = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        service_id = request.form.get('service_id')
        user_id = get_current_user_id()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Cart (user_id, service_id) VALUES (%s, %s)", (user_id, service_id))
        mysql.connection.commit()
        cur.close()


    return render_template('services.html',services=services)


    

@app.route('/pets',methods=['GET','POST'])
def pet_page():
    images = [{'img':'Cat.jpg'},{'img':'Dog.jpg'},{'img':'Hamster.jpg'},{'img':'Parrot.jpg'},{'img':'Rabbit.jpg'}]

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Pet")
    pets = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        pet_id = request.form.get('pet_id')
        user_id = get_current_user_id()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Cart (user_id, pet_id) VALUES (%s, %s)", (user_id, pet_id))
        mysql.connection.commit()
        cur.close()

    

    return render_template('pet.html', pets=pets,images=images)


@app.route('/Petshop')
def shop_page():
    product_images = [{'img':'catp.jpeg'},{'img':'dogp.jpeg'},{'img':'hamsterp.jpeg'},{'img':'parrotp.jpeg'},{'img':'rabbitp.jpeg'}]

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Pet_product")
    products = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        user_id = get_current_user_id()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Cart (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
        mysql.connection.commit()
        cur.close()

    return render_template('productpage.html',products=products,product_images=product_images)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    user_id = get_current_user_id()
    pet_id = request.form.get('pet_id')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Cart (user_id, pet_id) VALUES (%s, %s)", (user_id, pet_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('view_cart'))

@app.route('/add_to_cart1', methods=['POST'])
def add_to_cart1():
    user_id = get_current_user_id()
    product_id = request.form.get('product_id')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Cart (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('view_cart1'))

@app.route('/add_to_cart2', methods=['POST'])
def add_to_cart2():
    user_id = get_current_user_id()
    service_id = request.form.get('service_id')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Cart (user_id, service_id) VALUES (%s, %s)", (user_id, service_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('view_cart2'))


@app.route('/cart')
def view_cart():
    user_id = get_current_user_id()
    cur = mysql.connection.cursor()
    cur.execute("SELECT Pet.* FROM Pet JOIN Cart ON Pet.pet_id = Cart.pet_id WHERE Cart.user_id = %s", (user_id,))
    cart_contents = cur.fetchall()
    cur.close()

    return render_template('cart.html', cart_contents=cart_contents)

@app.route('/cart1')
def view_cart1():
    user_id = get_current_user_id()
    cur = mysql.connection.cursor()
    cur.execute("SELECT Pet_product.* FROM Pet_product JOIN Cart ON Pet_product.product_id = Cart.product_id WHERE Cart.user_id = %s", (user_id,))
    cart_contents1 = cur.fetchall()
    cur.close()

    return render_template('cart.html', cart_contents1=cart_contents1)

@app.route('/cart2')
def view_cart2():
    user_id = get_current_user_id()
    cur = mysql.connection.cursor()
    cur.execute("SELECT services.* FROM services JOIN Cart ON services.service_id = Cart.service_id WHERE Cart.user_id = %s", (user_id,))
    cart_contents1 = cur.fetchall()
    cur.close()

    return render_template('cart.html', cart_contents1=cart_contents1)

@app.route('/checkout')
def checkout():
    user_id = get_current_user_id()
    cur = mysql.connection.cursor()
    total_amount = 165
    cur.execute("SELECT Pet.* FROM Pet JOIN Cart ON Pet.pet_id = Cart.pet_id WHERE Cart.user_id = %s", (user_id,))
    cart_contents = cur.fetchall()

    cur.execute("SELECT Pet_product.* FROM Pet_product JOIN Cart ON Pet_product.product_id = Cart.product_id WHERE Cart.user_id = %s", (user_id,))
    cart_contents1 = cur.fetchall()

    cur.execute("SELECT services.* FROM services JOIN Cart ON services.service_id = Cart.service_id WHERE Cart.user_id = %s", (user_id,))
    cart_contents3 = cur.fetchall()

    cart_contents2 = len(cart_contents) + len(cart_contents1) + len(cart_contents3)

    # pet_price = 100
    # product_price = sum(item['product_price'] for item in cart_contents1)
    # service_fee = sum(item['service_fees'] for item in cart_contents3)
    

    cur.execute("""
        INSERT INTO orders (order_quantity, total_amount, order_date, exp_date, order_status, user_id)
        VALUES (%s, %s, NOW(), NOW() + INTERVAL 7 DAY, 'Pending', %s)
    """, (cart_contents2, total_amount, user_id))
    ans = cur.lastrowid

    cur.execute("""
        SELECT order_id, order_quantity, total_amount, order_date,exp_date,order_status
        FROM orders
        WHERE user_id = %s
        ORDER BY orders.order_id DESC
        LIMIT 1
    """, (user_id,))
    
    order_details = cur.fetchall()
    
    for item in cart_contents:
        cur.execute("""
    INSERT INTO order_items (order_id, pet_id, quantity, price)
    VALUES (%s, %s, %s, %s)
    """, (ans, item[0], 1, total_amount))
        
    
    
    cur.execute("DELETE FROM Cart WHERE user_id = %s", (user_id,))

    mysql.connection.commit()
    cur.close()

    return render_template('checkout.html', order_details=order_details, cart_contents=cart_contents,cart_contents1=cart_contents1,cart_contents3=cart_contents3,ans=ans)

def get_current_user_id():
    if 'user_id' in session:
        return session['user_id']
    else:
        # If the user is not logged in, you might want to handle this case accordingly
        # For simplicity, return None here, and handle it in your actual implementation
        return None
    


@app.route('/checkout/<int:order_id>/payment', methods=['GET', 'POST'])
def payment(order_id):
    if request.method == 'POST':
        paid_by = request.form.get('paid_by')
        amount_paid = request.form.get('amount_paid')
        payment_status = 'Paid'  

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO payment (paid_by, amount_paid, payment_status, user_id, order_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (paid_by, amount_paid, payment_status, get_current_user_id(), order_id))
        mysql.connection.commit()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("UPDATE orders SET order_status = 'Paid' WHERE order_id = %s", (order_id,))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('payment_success', order_id=order_id))

    return render_template('payment.html', order_id=order_id)

@app.route('/payment_success/<int:order_id>')
def payment_success(order_id):
    return render_template('payment_success.html', order_id=order_id)







@app.route('/register',methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password'].encode('utf-8')
            confirm_password = request.form['confirm_password'].encode('utf-8')

            if password != confirm_password:
                flash('Password and confirmation password do not match.', 'error')
                return redirect(url_for('register_page'))

            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            cur = get_db_connection().cursor()

            cur.execute("SELECT * FROM users1 WHERE username = %s", (username,))
            existing_user = cur.fetchone()

            if existing_user:
                
                return redirect(url_for('register_page'))

            cur.execute("INSERT INTO users1 (username, password) VALUES (%s, %s)", (username, hashed_password))
            get_db_connection().commit()

            cur.close()

            
            return redirect(url_for('login', success_message='Registration successful! You can now log in.'))

        except Exception as e:
            
            return redirect(url_for('register_page'))
        
    return render_template('register.html')


@app.route('/tables')
def index():
    return render_template('index.html')

@app.route('/changes_page')
def changes_page():
    return render_template('change.html')


@app.route('/table/<table_name>')
def get_table_data(table_name):
    cur = mysql.connection.cursor()
    cur.callproc('GetTableData', [table_name])
    data = cur.fetchall()

    cur.close()

    return render_template('table_content.html', data=data)


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = get_db_connection().cursor()

        cur.execute("SELECT * FROM admins WHERE username = %s", (username,))
        user = cur.fetchone()

        cur.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]

            flash('Login successful!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('admin.html')


@app.route('/insert_pet', methods=['GET', 'POST'])
def insert_pet():
    if request.method == 'POST':
        try:
            pet_id = request.form['pet_id']
            descriptions = request.form['descriptions']
            category = request.form['category']
            pet_status = request.form['pet_status']

            cur = mysql.connection.cursor()

            sql = "INSERT INTO Pet (pet_id, descriptions, category, pet_status) VALUES (%s, %s, %s, %s)"
            values = (pet_id, descriptions, category, pet_status)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()
            return render_template('index.html', success=True)

        except Exception as e:
            return render_template('index.html', success=False, error=str(e))

    return render_template('index.html', success=None)

@app.route('/insert_vendor', methods=['GET', 'POST'])
def insert_vendor():
    if request.method == 'POST':
        try:
            vendor_id = request.form['vendor_id']
            vendor_name = request.form['vendor_name']
            vendor_email = request.form['vendor_email']
            company_name = request.form['company_name']
            vendor_contact = request.form['vendor_contact']

            cur = mysql.connection.cursor()

            sql = "INSERT INTO vendor (vendor_id, vendor_name, vendor_email, company_name,vendor_contact) VALUES (%s, %s, %s, %s, %s)"
            values = (vendor_id, vendor_name, vendor_email, company_name, vendor_contact)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()
            return render_template('index.html', success=True)

        except Exception as e:
            return render_template('index.html', success=False, error=str(e))

    return render_template('index.html', success=None)

@app.route('/update_pet', methods=['GET', 'POST'])
def update_pet():
    if request.method == 'POST':
        try:
            pet_id = request.form['pet_id']
            pet_status = request.form['pet_status']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Pet WHERE pet_id = %s", (pet_id,))
            before_update = cur.fetchone()

            sql = "UPDATE Pet SET pet_status = %s WHERE pet_id = %s"
            values = (pet_status, pet_id)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()

            return render_template('index.html', before_update=before_update)

        except Exception as e:
            return "Error"

    return render_template('index.html')

@app.route('/update_petproduct', methods=['GET', 'POST'])
def update_petproduct():
    if request.method == 'POST':
        try:
            product_id = request.form['product_id']
            product_price = request.form['product_price']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Pet_product WHERE product_id = %s", (product_id,))
            before_update = cur.fetchone()

            sql = "UPDATE Pet_product SET product_price = %s WHERE product_id = %s"
            values = (product_price, product_id)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()

            return render_template('index.html', before_update=before_update)

        except Exception as e:
            return "Error"

    return render_template('index.html')

@app.route('/update_services', methods=['GET', 'POST'])
def update_services():
    if request.method == 'POST':
        try:
            service_id = request.form['service_id']
            service_fees = request.form['service_fees']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM services WHERE service_id = %s", (service_id,))
            before_update = cur.fetchone()

            sql = "UPDATE services SET service_fees = %s WHERE service_id = %s"
            values = (service_fees, service_id)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()

            return render_template('index.html', before_update=before_update)

        except Exception as e:
            return "Error"

    return render_template('index.html')

@app.route('/delete_vendor', methods=['GET', 'POST'])
def delete_vendor():
    if request.method == 'POST':
        try:
            vendor_id = request.form['vendor_id']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM vendor WHERE vendor_id = %s", (vendor_id,))
            before_delete = cur.fetchone()

            sql = "DELETE FROM vendor WHERE vendor_id = %s"
            values = (vendor_id,)
            cur.execute(sql, values)
            mysql.connection.commit()
            
            cur.close()
            
            return render_template('index.html', before_delete=before_delete)

        except Exception as e:
            return "Error"

    return render_template('index.html')


@app.route('/vendor')
def vendor_page():
    return render_template('vendor.html')
