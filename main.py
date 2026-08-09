# =======~~~~~--- Welcome to GWS core ---~~~~~=======
# ===~~-      Developer: Rian-Batista-Rx4n     -~~===
# ===~~-            Version: 0.9.8             -~~===
# =======~~~~~--- ................... ---~~~~~=======

# Imports
from flask import ( Flask, render_template, request, redirect, session, url_for, jsonify)
import json
import os
import shutil
from werkzeug.utils import secure_filename
from flask import send_file
from datetime import datetime

# Start Flask app
app=Flask(__name__)
app.config["SECRET_KEY"] = "gws_secret"

LOG_DIR = os.path.join("gwdata", "logs")
LOG_FILE = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} - graywolfsystem.log")

# ===== USERS =====
# Load Users data
def load_users():
    with open("gwdata/users/users.json", "r") as file:
        return json.load(file)


# Save new Users data
def save_users(data):
    with open("gwdata/users/users.json", "w") as file:
        json.dump(data, file, indent=4)


# Function to generate logs
### register_log("Route", session.get("username", "unknow"), "Action description")
def register_log(action, user="SYSTEM", description=""):
    time_log = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{time_log}] | [{user}]: {action} - {description}\n")


# Calculate user storage
def calculate_storage(path):
    total = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            full = os.path.join(root, file)

            total += os.path.getsize(full)

    return total


# Turn B >> KB >> MB >> GB in the front end
def format_storage(bytes_size):
    if bytes_size >= 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024 * 1024):,.3f} GB"
    elif bytes_size >= 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):,.3f} MB"
    elif bytes_size >= 1024:
        return f"{bytes_size / 1024:,.3f} KB"
    else:
        return f"{bytes_size:,} B"


# generate default folders for new users
def create_default_folders(username):
    base = f"gwhome/users/{username}"

    folders = [
        "videos",
        "audio",
        "images",
        "text",
        "documents"
    ]

    os.makedirs(base, exist_ok=True)

    for folder in folders:
        os.makedirs(os.path.join(base, folder), exist_ok=True)


# Root lock check
def root_locked(path):
    role = session["role"]
    if role == "admin":
        return False

    path = path.strip("/")

    return path == ""


# Verify user base
def get_user_base():
    username = session["username"]
    role = session["role"]

    if role == "admin":
        return "gwhome/users"

    return f"gwhome/users/{username}"


# Create first administrator if it is the first time starting GWS
def initialize_gws():
    users_file = "gwdata/users/users.json"

    os.makedirs("gwdata/users", exist_ok=True)

    if not os.path.exists(users_file):
        data = {
            "users": []
        }

        with open(users_file, "w") as file:
            json.dump(
                data,
                file,
                indent=4
            )

    data = load_users()

    if len(data["users"]) > 0:

        return

    print()
    print("========================================")
    print("       Welcome to Gray Wolf System")
    print("========================================")
    print()
    print("No users were found.")
    print("Create the first administrator account.")
    print()

    while True:
        username = input("Insert admin username: ").strip()

        if not username:
            print("Username cannot be empty.\n")
            continue

        password = input("Insert admin password: ")

        if not password:
            print("Password cannot be empty.\n")
            continue

        confirm_password = input("Confirm admin password: ")

        if password != confirm_password:
            print("Passwords do not match.\n")
            continue
        
        break

    data["users"].append({
        "username": username,
        "password": password,
        "role": "admin"
    })

    save_users(data)
    create_default_folders(username)

    print(f"\nAdministrator '{username}' created successfully.")
    print("Default folders created.\n")

# Create first administrator if it is the first time starting GWS
initialize_gws()

# Server Starter First Log
register_log("Starting", "System", "Starting GWS Server")

# ===== ROUTES =====
# Index and Login
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        data = load_users()

        for user in data["users"]:
            if (user["username"] == username and user["password"] == password):
                session["username"] = username
                session["role"] = user["role"]

                register_log("INDEX", session.get("username", "unknow"), "Authenticated")
                return redirect(url_for("home"))
            
    return render_template("index.html")


# Homepage and File Browser
@app.route("/home")
@app.route("/home/<path:subpath>")
def home(subpath = ""):

    if "username" not in session:
        return redirect(url_for("index"))

    base = get_user_base()
    current_path = os.path.join(base, subpath)

    if not os.path.exists(current_path):
        return redirect(url_for("home"))

    items = []

    for item in os.listdir(current_path):
        full = os.path.join(current_path, item)

        items.append({
            "name": item,
            "is_dir": os.path.isdir(full),
            "extension": os.path.splitext(item)[1],
            "path": os.path.join(subpath, item).replace("\\","/")
        })

    items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))

    return render_template("home.html", username=session["username"], files=items, current=subpath)


# ===== DELETE =====
@app.route("/action/delete", methods=["POST"])
def delete_item():
    path = request.form["path"]

    if root_locked(os.path.dirname(path)):
        return jsonify({
            "ok": False,
            "message": "Root protected"
        })

    full = os.path.join(get_user_base(), path)

    if os.path.isdir(full):
        shutil.rmtree(full)
    else:
        os.remove(full)

    return jsonify({
        "ok": True
    })


# ===== RENAME =====
@app.route("/action/rename", methods=["POST"])
def rename_item():
    old = request.form["old"]

    if root_locked(os.path.dirname(old)):
        return jsonify({
            "ok": False,
            "message": "Root protected"
        })

    new = request.form["new"]
    old_path = os.path.join(get_user_base(), old)
    new_path = os.path.join(os.path.dirname(old_path), new)

    os.rename(old_path, new_path)

    return jsonify({
        "ok":True
    })


# ===== DOCUMENT =====
@app.route("/action/create_document", methods=["POST"])
def create_document():
    current = request.form["current"]

    if root_locked(current):
        return jsonify({
            "ok": False
        })

    path = os.path.join(get_user_base(), current)

    i = 0

    while True:
        name = f"document{i if i else ''}.txt"
        full = os.path.join(path, name)

        if not os.path.exists(full):
            open(full, "w").close()
            break

        i += 1

    return jsonify({
        "ok": True
    })


# ===== FOLDER =====
@app.route("/action/create_folder", methods=["POST"])
def create_folder():
    current = request.form["current"]

    if root_locked(current):
        return jsonify({
            "ok": False
        })

    path  = os.path.join(get_user_base(), current)

    i=0

    while True:
        name = f"folder{i if i else ''}"
        full = os.path.join(path, name)

        if not os.path.exists(full):
            os.mkdir(full)
            break

        i += 1

    return jsonify({
        "ok": True
    })


# ===== UPLOAD PAGE =====
@app.route("/upload")
def upload():
    current = request.args.get("current", "")
    base = get_user_base()
    folders = []

    categories=[
        "audio",
        "images",
        "videos",
        "text",
        "documents"
    ]

    for category in categories:
        path = os.path.join(base, category)

        if os.path.exists(path):
            folders.append({
                "category": category,
                "subfolders": [
                    f
                    for f in os.listdir(path)
                    if os.path.isdir(os.path.join(path, f))
                ]
            })

    return render_template("upload.html", folders=folders, current=current)


# ===== UPLOAD FILE =====
@app.route("/upload_file", methods=["POST"])
def upload_file():
    files = request.files.getlist("files")
    mode = request.form.get("mode")
    base = get_user_base()

    if mode == "current":
        current = request.form.get("current", "")
        destination = os.path.join(base, current)
    else:
        category = request.form.get("category")
        subfolder = request.form.get("subfolder")
        destination = os.path.join(base, category, subfolder)

    os.makedirs(destination, exist_ok=True)

    for file in files:
        if file.filename == "":
            continue

        name = secure_filename(file.filename)

        file.save(os.path.join(destination, name))

    return jsonify(
        {"ok": True}
    )


# Open text files
@app.route("/open/<path:file>")
def open_file(file):
    full = os.path.join(get_user_base(), file)
    ext = os.path.splitext(file)[1].lower()
    text_ext = [
        ".txt",
        ".py",
        ".js",
        ".html",
        ".css",
        ".json"
    ]

    image_ext = [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp"
    ]

    video_ext = [
        ".mp4",
        ".webm",
        ".avi"
    ]

    audio_ext = [
        ".mp3",
        ".ogg",
        ".wav"
    ]

    if ext in text_ext:
        with open(full, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return render_template("textviewer.html", filename=os.path.basename(file), content=content, path=file)

    if(ext in image_ext or ext in video_ext or ext in audio_ext):
        return send_file(full)

    return redirect(url_for("home"))


# Save text edited by textviewer.html
@app.route("/save_text", methods=["POST"])
def save_text():
    path = request.form["path"]
    content = request.form.get("content", "")
    content = content.replace("\r\n", "\n")
    content = content.rstrip("\n")
    full = os.path.join(get_user_base(), path)

    with open(full, "w", encoding="utf-8") as file:
        file.write(content)

    return redirect(
        url_for("open_file", file=path))


# download file
@app.route("/download/<path:file>")
def download(file):
    full = os.path.join(get_user_base(), file)

    return send_file(full, as_attachment=True)


# file info
@app.route("/info/<path:file>")
def info(file):
    full = os.path.join(get_user_base(), file)
    size = os.path.getsize(full)
    units = [
        "B",
        "KB",
        "MB",
        "GB"
    ]

    i=0

    while(size > 1024 and i < 3):
        size /= 1024
        i += 1

    return render_template("info.html", name=os.path.basename(file), size=f"{size:.2f} {units[i]}", ext=os.path.splitext(file)[1])


# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ===== SETTINGS =====
@app.route("/settings")
def settings():
    if "username" not in session:
        return redirect(url_for("index"))

    role = session["role"]
    data = load_users()
    users = []

    for user in data["users"]:
            folder = f"gwhome/users/{user['username']}"
            size = calculate_storage(folder)
            users.append({
                "username": user["username"],
                "role": user["role"],
                "storage": format_storage(size)
            })


    if role == "admin":
        data = load_users()

        return render_template("settings_admin.html", users=users)

    return render_template("settings_user.html")


# ===== CREATE USER =====
@app.route("/create_user", methods=["POST"])
def create_user():
    if session["role"] != "admin":
        return redirect(url_for("home"))

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]
    data = load_users()

    for user in data["users"]:
        if(user["username"] == username):
            return "User exists"

    data["users"].append({
        "username": username,
        "password": password,
        "role": role
    })

    save_users(data)
    create_default_folders(username)

    return redirect(url_for("settings"))


# ===== DELETE USER =====
@app.route("/delete_user/<username>")
def delete_user(username):
    if session["role"] != "admin":
        return redirect(url_for("home"))

    data = load_users()
    data["users"] = [
        u for u in data["users"]
        if u["username"] != username
    ]

    save_users(data)

    folder = f"gwhome/users/{username}"

    if os.path.exists(folder):
        shutil.rmtree(folder)

    return redirect(url_for("settings"))


# ===== REGISTER PAGE =====
@app.route("/register")
def register():
    if session["role"] != "admin":
        return redirect(url_for("home"))

    return render_template("register.html")


# ===== CORE =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777, debug=True)