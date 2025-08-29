from flask import Flask, render_template, request, jsonify, redirect, url_for
import datetime
import os
import csv

app = Flask(__name__)
# =====global variables =====
v_time = 1


# ====== Helper Files ======
PRODUCTS_FILE = "products/products.csv"
REQUESTS_FILE = "requests/request.txt"
NUMBER_STORED_FILE = "requests/number_stored.txt"
PASS_FILE = "requests/pass.txt"
VALID_CHK_FILE = "requests/valid.txt"
USER_FILE = "requests/user.txt"
CONSOLE_FILE = "requests/console.txt"


# ==== Starting Actions ====
valid_time = (v_time*60)

with open(CONSOLE_FILE, "w") as f:
    f.write("") # clear console file

# ====== Helper Functions ======
def load_products():
    os.makedirs("products", exist_ok=True)
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "product_info"])
            writer.writerow(["", "--Select Product--"])
        return [{"id": 1, "product_info": "--Select Product--"}]

    products = []
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({"id": row["id"], "product_info": row["product_info"]})
    return products

def stay_valid():
    with open(VALID_CHK_FILE,"r") as FILE:
        VALID_TIME = int(FILE.read())
    dt = datetime.datetime.now()
    nh = dt.hour
    nm = dt.minute
    ns = dt.second
    CURRENT_TIME = str((nh*3600) + (nm*60) + (ns*1))
    el = (int(CURRENT_TIME) - int(VALID_TIME))
    if el > valid_time:
        return render_template("login.html")
    else:
        return True

def save_product(product_info):
    products = load_products()
    new_id = 1
    if len(products) > 1:
        new_id = max(int(p["id"]) for p in products[1:]) + 1
    with open(PRODUCTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([new_id, product_info])

def delete_product(product_id):
    products = load_products()
    filtered = [p for p in products if p["id"] != str(product_id)]
    with open(PRODUCTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "product_info"])
        for p in filtered:
            writer.writerow([p["id"], p["product_info"]])

# ====== Routes ======
@app.route("/")
def index_page():
    result = stay_valid()
    if result is not True:
        return result
    return render_template("main.html")


@app.route("/temp_notes")
def temp_notes_page():
    result = stay_valid()
    if result is not True:
        return result    
    
    return render_template("temp_notes.html")

@app.route("/product_add")
def product_add_page():
    result = stay_valid()
    if result is not True:
        return result
    return render_template("product_add.html")

@app.route("/change_user")
def change_user_page():
    with open(PASS_FILE,"r") as FILE:
        PASS = str(FILE.read())
    return render_template("change_user.html",content=(PASS))

@app.route("/chng/<password>/<user>")
def chng_page(password,user):
    with open(PASS_FILE,"w") as FILE:
        FILE.write(str(password))
    with open(USER_FILE,"w") as FILE:
        FILE.write(str(user))
    return render_template("login.html")

@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/pass/<password>/<user>")
def pass_page(password,user):
    g_password = str(password)
    g_user = str(user)
    with open(PASS_FILE,"r") as FILE:
        IRL_PASS = str(FILE.read())
    if g_password == IRL_PASS:
        dt = datetime.datetime.now()
        nh = dt.hour
        nm = dt.minute
        ns = dt.second
        with open(USER_FILE,"r") as FILE:
            IRL_USER = str(FILE.read())
        if g_user == IRL_USER:
            FULLT = str((nh*3600) + (nm*60) + (ns*1))
            with open(VALID_CHK_FILE,"w") as FILE:
                FILE.write(FULLT)
            content = "True"
        else:
            content = "False"
            return render_template("pass.html", content=(content))
    else:
        content = "False"
    
    return render_template("pass.html", content=(content))


@app.route("/outputconsole")
def console_page():
    result = stay_valid()
    if result is not True:
        return result
    return render_template("console.html")

@app.route("/console_data")
def console_data():
    try:
        with open(CONSOLE_FILE, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return jsonify(lines)  # returns a JSON array of lines
    except Exception as e:
        print(f"Error reading {CONSOLE_FILE}", e)
        return jsonify(["No console data found."])


@app.route("/get_products")
def get_products():
    products = load_products()
    return jsonify([{"id": p["id"], "name": p["product_info"]} for p in products[1:]])

# ====== Delete request ======
@app.route("/delete_request/<int:index>", methods=["POST"])
def delete_request(index):
    requests_file = "requests/request.txt"
    
    # Check if the file exists
    if not os.path.exists(requests_file):
        return redirect(url_for("request_list"))  # Use the correct function name

    # Read all lines from the file
    with open(requests_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove the line at the given index if valid
    if 0 <= index < len(lines):
        del lines[index]

    # Write the updated lines back to the file
    with open(requests_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Redirect back to the request list page
    return redirect(url_for("request_list"))


@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.get_json()
    if not data:
        return "❌ No form data received"
    name = data.get("name", "").strip()
    price = data.get("price", "").strip()
    description = data.get("description", "").strip()
    if not all([name, price, description]):
        return "❌ All fields are required"
    product_info = f"{name} - price:- {price}tk . ---- {description}"
    save_product(product_info)
    return f"✅ Product added successfully: {product_info}"

@app.route("/number")
def number_page():
    result = stay_valid()
    if result is not True:
        return result
    products = load_products()
    formatted_products = [{"id": p["id"], "name": p["product_info"]} for p in products]
    return render_template("number.html", products=formatted_products)

@app.route("/store", methods=["POST"])
def store():
    data = request.get_json()
    if not data:
        return jsonify({"message": "❌ No data received"})
    number = data.get("number", "").strip()
    product = data.get("product", "").strip()
    if str(product) == "--Select Product--":
        return jsonify({"message": "❌ Select a product"})
    if not all([number, product]):
        return jsonify({"message": "❌ Number and product are required"})

    os.makedirs("requests", exist_ok=True)

    # Prevent repeated numbers
    if os.path.exists(NUMBER_STORED_FILE):
        with open(NUMBER_STORED_FILE, "r", encoding="utf-8") as f:
            stored_numbers = set(line.strip() for line in f)
        if number not in stored_numbers:
            with open(NUMBER_STORED_FILE, "a", encoding="utf-8") as f:
                f.write(f"{number}\n")

    with open(REQUESTS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{number},{product}\n")

    return jsonify({"message": f"✅ Stored number {number} for product {product}"})

@app.route("/product_ls")
def product_list():
    result = stay_valid()
    if result is not True:
        return result
    products = load_products()
    return render_template("product_ls.html", products=products[1:])

@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product_route(product_id):
    delete_product(product_id)
    return redirect(url_for("product_list"))

@app.route("/number_ls")
def number_list():
    result = stay_valid()
    if result is not True:
        return result
    numbers = []
    if os.path.exists(NUMBER_STORED_FILE):
        with open(NUMBER_STORED_FILE, "r", encoding="utf-8") as f:
            numbers = [line.strip() for line in f if line.strip()]
    return render_template("number_ls.html", numbers=numbers)

@app.route("/request_ls")
def request_list():
    result = stay_valid()
    if result is not True:
        return result
    requests_data = []
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",", 1)
                if len(parts) == 2:
                    requests_data.append({"number": parts[0], "product": parts[1]})
    return render_template("request_ls.html", requests=requests_data)

# ====== Run ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
