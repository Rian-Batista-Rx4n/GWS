# =============================================================
# --------------------- IMPORTS -------------------------------
# =============================================================
from flask import Flask, render_template, request, redirect, flash, session, send_from_directory, url_for, abort
from werkzeug.utils import secure_filename
from urllib.parse import quote
from datetime import datetime
import getpass
import os, json
import json
import time
import psutil

# =============================================================
# --------------------- FUNCTIONS -----------------------------
# =============================================================

# Function to generate logs
def registrar_log(acao, usuario="SYSTEM", detalhes=""):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{agora}] [{usuario}] {acao} - {detalhes}\n")


#Funtion to create the first ADMIN of the system
def garantir_usuario_admin():
    if not os.path.exists(users_json_path):
        print("⚠️ No users data! please create a ADMIN user now!")

        os.makedirs(os.path.dirname(users_json_path), exist_ok=True)

        username = input("→ Username: ").strip()
        while not username:
            username = input("→ Username can't be empty: ").strip()

        password = getpass.getpass("→ Password: ").strip()
        while not password:
            password = getpass.getpass("→ Password can't be empty: ").strip()

        criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        users_data = {
            username: {
                "senha": password,
                "nivel": "admin",
                "criado_em": criado_em,
                "armazenamento_usado": 0
            }
        }
        with open(users_json_path, "w") as f:
            json.dump(users_data, f, indent=4, ensure_ascii=False)

        print(f"✅ ADMIN '{username}' is an admin now!")

# Load all users in the system to verify if then exist
def carregar_usuarios():
    registrar_log("USERS", session.get("usuario_logado", "unknow"), "Loading Users")
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save the new users data
def salvar_usuarios(usuarios):
    registrar_log("USERS", session.get("usuario_logado", "unknow"), "User Saved")
    with open(USERS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

# Function to verify if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Turn B >> KB >> MB >> GB in the front end
def formatar_tamanho(bytes_size):
    if bytes_size >= 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024 * 1024):,.3f} GB"
    elif bytes_size >= 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):,.3f} MB"
    elif bytes_size >= 1024:
        return f"{bytes_size / 1024:,.3f} KB"
    else:
        return f"{bytes_size:,} B"

# PATHs
users_json_path = os.path.join("GWData", "GWS_Users", "users.json")
LOG_DIR = "GWLogs"
LOG_FILE = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - GrayWolf.log")
os.makedirs(LOG_DIR, exist_ok=True)
USERS_FILE = "GWData/GWS_Users/users.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "GWFiles", "document")
BASE_DIR_GWF = os.path.abspath(os.path.dirname(__file__))
GWFILES_DIR = os.path.join(BASE_DIR, "GWFiles")
UPLOAD_FOLDER = 'GWFiles/geral/no_subcategory'

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'ico',
    'zip', 'rar', '7z', 'tar', 'gz', 'xz',
    'doc', 'docx', 'odt', 'xls', 'xlsx', 'ods', 'ppt', 'pptx', 'csv', 'rtf',
    'mp4', 'mkv', 'avi', 'mov', 'webm',
    'mp3', 'wav', 'ogg', 'flac', 'm4a',
    'py', 'js', 'html', 'css', 'json', 'xml', 'sql', 'md', 'sh'
}

# First User Creation be admin
registrar_log("Start", "SYSTEM", "Server Started")
garantir_usuario_admin()

# First Folders Maker
# Verify if folder are created
pastas_criadas = False
estrutura = {
        "video": ["movie", "serie", "video_no_category"],
        "image": ["photo", "screenshot", "image_no_category"],
        "audio": ["music", "podcast", "audio_no_category"],
        "document": ["excel", "pdf", "powerpoint", "word", "document_no_category"],
        "text": ["list", "note", "script", "text_no_category"],
        "trash": [],
        "geral": ["sem_categoria"]
    }

# For each category, create a folder for category and its subfolders based on category, subcategory folder
for categoria, subcategorias in estrutura.items():
    if subcategorias:
        for sub in subcategorias:
            caminho = os.path.join("GWFiles", categoria, sub)
            os.makedirs(caminho, exist_ok=True)
    else:
        caminho = os.path.join("GWFiles", categoria)
        os.makedirs(caminho, exist_ok=True)

# Update the verify of then category folders
pastas_criadas = True

# =============================================================
# ------------------------- GWS SYSTEM BACKEND ----------------
# =============================================================
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

# Make a UPLOAD FOLDER if don't exist
if not os.path.exists(UPLOAD_FOLDER):
    registrar_log("PATH", "SYSTEM", "Upload Path Created")
    os.makedirs(UPLOAD_FOLDER)

# First page, index, load the LOGIN page
@app.route("/")
def home():
    registrar_log("Login", session.get("usuario_logado", "unknow"), "Login Accessed")
    return render_template("index.html")

#===================== ERROR 404 PAGE ========================
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("404_page.html"), 404

# ===================== Back Button =======================
@app.route("/graywolf-back", methods=["GET"])
def graywolf_back():
    registrar_log("Back Button", session.get("usuario_logado", "unknow"), "Back to the HomePage")
    return render_template("homepage.html")

# ===================== Info Button =======================
@app.route('/graywolf-info-file', methods=['GET'])
def graywolf_info_file():
    file_path = request.args.get('file_path')
    
    if not file_path or not os.path.exists(file_path):
        return "Arquivo não encontrado", 404

    info = {
        "path": file_path,
        "size_kb": round(os.path.getsize(file_path) / 1024, 2),
        "created": time.ctime(os.path.getctime(file_path)),
        "modified": time.ctime(os.path.getmtime(file_path)),
        "absolute_path": os.path.abspath(file_path),
        "is_readable": os.access(file_path, os.R_OK),
        "is_writable": os.access(file_path, os.W_OK),
    }

    return render_template('info_file.html', info=info)

# ========================================== Do Logout ====================================
@app.route("/graywolf-logout")
def logout():
    usuario = session.get('usuario_logado')
    session.pop('usuario_logado', None)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    registrar_log("LOGOUT", session.get("usuario_logado", "unknow"), f"{usuario} left the game")
    return redirect("/")

# ========================== Make a Register =================================
@app.route("/graywolf-register", methods=["GET", "POST"])
def graywolf_register():
    usuario_logado = session.get("usuario_logado")
    
    registrar_log("Register", session.get("usuario_logado", "unknow"), "Register Accessed")

    if not usuario_logado:
        registrar_log("Register", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")

    usuarios = carregar_usuarios()

    if usuarios.get(usuario_logado, {}).get("nivel") != "admin":
        registrar_log("Register", session.get("usuario_logado", "unknow"), "Not Admin")
        return render_template("homepage.html")

    if request.method == "POST":
        usuario = request.form.get("nome_usuario")
        senha = request.form.get("senha_usuario")
        is_admin = request.form.get("beAdmin") == "beAdmin"

        if usuario in usuarios or usuario == "SYSTEM" or usuario == "public" or usuario == "public_" or usuario == "system":   
            registrar_log("Register", session.get("usuario_logado", "unknow"), "User already exists or DENIED")
            return redirect("/graywolf-register")

        usuarios[usuario] = {
            "senha": senha,
            "nivel": "admin" if is_admin else "normal",
            "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        salvar_usuarios(usuarios)
        registrar_log("Register", session.get("usuario_logado", "unknow"), f"User: {usuario} created; Pass: {senha}; Nivel: {is_admin}")
        return redirect("/graywolf-register")

    return render_template("register.html")

# ========================= Load HomePage ===================
@app.route("/graywolf-homepage", methods=["POST"])
def graywolf_homepage():
    usuario = request.form.get("nome_usuario")
    senha = request.form.get("senha_usuario")

    usuarios = carregar_usuarios()

    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        session['usuario_logado'] = usuario
        session['login_time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        registrar_log("Login", session.get("usuario_logado", "unknow"), "Login Successful")
        return render_template("homepage.html")
    else:
        registrar_log("Login", session.get("usuario_logado", "unknow"), "Login Failed")
        return redirect("/")

# Go to: Category - document
@app.route("/graywolf-document", methods=["GET"])
def show_document_page():
    if 'usuario_logado' not in session:
        registrar_log("Document", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")
    registrar_log("Document", session.get("usuario_logado", "unknow"), "Document Accessed")
    return render_template("document.html")

# =========================== Text ==========================
@app.route("/graywolf-text", methods=["GET"])
def show_text_page():
    if 'usuario_logado' not in session:
        registrar_log("Text", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")
    registrar_log("Text", session.get("usuario_logado", "unknow"), "Text Accessed")
    return render_template("text.html")

def listar_arquivos_por_categoria(categoria):
    if 'usuario_logado' not in session:
        registrar_log(categoria, session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")

    usuario = session.get('usuario_logado')
    base_path = 'GWFiles/text'
    extensoes_script = ['.py', '.js', '.ts', '.html', '.css', '.sh']
    extensoes_txt = ['.txt']

    if categoria == 'script':
        extensoes_permitidas = extensoes_script
    else:
        extensoes_permitidas = extensoes_txt

    pasta_categoria = os.path.join(base_path, categoria)
    files = []

    if os.path.exists(pasta_categoria):
        for file in os.listdir(pasta_categoria):
            _, ext = os.path.splitext(file)
            if ext.lower() in extensoes_permitidas:
                if file.startswith(f"{usuario}_") or file.startswith("public_"):
                    files.append(file)

    registrar_log("TextList", session["usuario_logado"], f"Accessed {categoria} files")

    return render_template(
        'texts.html',
        files=files,
        categoria=categoria,
        categoria_pasta=categoria
    )

@app.route("/graywolf-list", methods=["GET"])
def graywolf_list():
    return listar_arquivos_por_categoria('list')

@app.route("/graywolf-note", methods=["GET"])
def graywolf_note():
    return listar_arquivos_por_categoria('note')

@app.route("/graywolf-script", methods=["GET"])
def graywolf_script():
    return listar_arquivos_por_categoria('script')

@app.route("/graywolf-text-no-category", methods=["GET"])
def graywolf_text_no_category():
    return listar_arquivos_por_categoria('text_no_category')

# =============================== Render Text =========================
@app.route("/graywolf-read-text/<categoria>/<nome_arquivo>", methods=["GET"])
def graywolf_read_text(categoria, nome_arquivo):
    if 'usuario_logado' not in session:
        registrar_log("ReadText", "unknown", "Not in Session")
        return redirect("/")

    usuario = session.get("usuario_logado")
    base_path = os.path.join("GWFiles", "text", categoria)
    file_path = os.path.join(base_path, nome_arquivo)

    # Segurança: impede acesso fora da pasta
    if not os.path.abspath(file_path).startswith(os.path.abspath(base_path)):
        registrar_log("ReadText", usuario, "Access Denied (Path traversal)")
        return abort(403)

    # Verifica se o arquivo é permitido ao usuário
    if not (nome_arquivo.startswith(f"{usuario}_") or nome_arquivo.startswith("public_")):
        registrar_log("ReadText", usuario, f"Not permitted: {nome_arquivo}")
        return abort(403)

    # Verifica se o arquivo existe
    if not os.path.isfile(file_path):
        registrar_log("ReadText", usuario, f"File not found: {file_path}")
        return abort(404)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        registrar_log("ReadText", usuario, f"Error reading file: {e}")
        conteudo = "[Erro ao ler o arquivo]"

    registrar_log("ReadText", usuario, f"Read {nome_arquivo} of {categoria}")

    return render_template(
        "read_text.html",
        file_name=nome_arquivo,
        categoria_pasta=categoria,
        arquivo=nome_arquivo,
        conteudo=conteudo
    )

# Go to: Category - audio
@app.route("/graywolf-audio", methods=["GET"])
def show_audio_page():
    if 'usuario_logado' not in session:
        registrar_log("Audio", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")
    registrar_log("Audio", session.get("usuario_logado", "unknow"), "Audio Accessed")
    return render_template("audio.html")

# Go to: Category - image
@app.route("/graywolf-image", methods=["GET"])
def show_image_page():
    if 'usuario_logado' not in session:
        registrar_log("Image", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")
    registrar_log("Image", session.get("usuario_logado", "unknow"), "Image Accessed")
    return render_template("image.html")

# Go to: Category - video
@app.route("/graywolf-video", methods=["GET"])
def show_video_page():
    if 'usuario_logado' not in session:
        registrar_log("Video", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")
    registrar_log("Video", session.get("usuario_logado", "unknow"), "Video Accessed")
    return render_template("video.html")

# ==================================== EDIT Text ==================================
@app.route("/graywolf-edit-text", methods=["POST"])
def graywolf_edit_text():
    file_path = request.form.get("file_path")
    if not file_path or not os.path.exists(file_path):
        flash("File not found or invalid path.")
        return redirect(url_for("graywolf-homapage"))
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return render_template("edit_text.html", file_path=file_path, content=content)

@app.route("/graywolf-save-text", methods=["POST"])
def graywolf_save_text():
    file_path = request.form.get("file_path")
    new_content = request.form.get("new_content")

    if not file_path or not os.path.exists(file_path):
        flash("Error: file not found.")
        return redirect(url_for("graywolf_homepage"))  # corrigido underline

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        flash("Text saved successfully.")
    except Exception as e:
        flash(f"Error saving file: {e}")
        return redirect(url_for("graywolf_homepage"))

    # 🧠 Aqui você extrai categoria e nome_arquivo a partir do path completo
    # Exemplo de path: GWFiles/text/note/arquivo.txt
    partes = file_path.split("/")
    if len(partes) >= 4:
        categoria = partes[2]
        nome_arquivo = partes[3]
    else:
        flash("Invalid file path format.")
        return redirect(url_for("graywolf_homepage"))

    return redirect(url_for("graywolf_read_text", categoria=categoria, nome_arquivo=nome_arquivo))

# ======================================= Do Upload ===========================
@app.route("/graywolf-upload", methods=["GET"])
def show_upload_page():
    if 'usuario_logado' not in session:
        registrar_log("Upload", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")
    
    usuario_logado = session.get('usuario_logado')
    usuarios = carregar_usuarios()
    admin = usuarios.get(usuario_logado, {}).get("nivel") == "admin"

    registrar_log("Upload", session.get("usuario_logado", "unknow"), "Upload Accessed")
    return render_template("upload.html", admin=admin)


@app.route("/graywolf-upload-file", methods=["POST", "GET"])
def upload_file():
    usuario_logado = session.get('usuario_logado')
    usuarios = carregar_usuarios()
    admin = usuarios.get(usuario_logado, {}).get("nivel") == "admin"

    if 'file' not in request.files:
        registrar_log("Upload", session.get("usuario_logado", "unknow"), "No file selected")
        return redirect(request.referrer)

    files = request.files.getlist("file")
    main_category = request.form.get("chooseFile")
    sub_category = request.form.get("subCategory")

    if not files or not main_category or not sub_category:
        registrar_log("Upload", session.get("usuario_logado", "unknow"), "Fill in all required fields")
        return redirect(request.referrer)

    folder_path = os.path.join("GWFiles", main_category, sub_category)
    os.makedirs(folder_path, exist_ok=True)
    agora = datetime.now()
    usuario = session.get("usuario_logado", "unknown")
    publico = request.form.get("public") == "yes"

    for file in files:
        if file.filename == '':
            continue

        if not allowed_file(file.filename):
            registrar_log("Upload", session.get("usuario_logado", "unknow"), f"File not permitted: {file.filename}")
            continue

        filename_base = secure_filename(file.filename)

        usuario_logado = session.get("usuario_logado", "unknow")
        usuarios = carregar_usuarios()

        if publico:
            if usuarios.get(usuario_logado, {}).get("nivel") == "admin":
                filename = f"public_{usuario}_{filename_base}"
            else:
                filename = f"{usuario}_{filename_base}"
        else:
            filename = f"{usuario}_{filename_base}"

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if "armazenamento_usado" not in usuarios[usuario_logado]:
            usuarios[usuario_logado]["armazenamento_usado"] = 0
        usuarios[usuario_logado]["armazenamento_usado"] += file_size

        with open("GWData/GWS_Users/users.json", "w") as f:
            json.dump(usuarios, f, indent=4)

        registrar_log("Upload", session.get("usuario_logado", "unknow"), f"Uploaded: {filename_base} ({file_size} bytes)")

        filepath = os.path.join(folder_path, filename)
        file.save(filepath)

    flash('Files uploaded successful!')
    registrar_log("Upload", session.get("usuario_logado", "unknow"), "Upload Complete")
    return redirect("/graywolf-upload")


# ======================================== Show Uploads files ===============================
@app.route('/download/<path:nome_arquivo>')
def download_arquivo(nome_arquivo):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    GWFILES_DIR = os.path.join(BASE_DIR, "GWFiles")
    return send_from_directory(GWFILES_DIR, nome_arquivo, as_attachment=True)

@app.route('/graywolf-uploadFiles')
def upload_files_page():
    registrar_log("Uploads", session.get("usuario_logado", "unknow"), "Uploads Accessed")
    
    usuario = session.get('usuario_logado')
    if not usuario:
        registrar_log("Uploads", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")

    usuarios = carregar_usuarios()
    is_admin = usuarios.get(usuario, {}).get("nivel") == "admin"

    arquivos = []

    for root, dirs, files in os.walk(GWFILES_DIR):
        for file in files:
            if not allowed_file(file):
                registrar_log("Uploads", usuario, "Not Permitted")
                continue

            relative_path = os.path.relpath(os.path.join(root, file), start=GWFILES_DIR)

            if is_admin:
                arquivos.append(relative_path)
            else:
                if file.startswith(f"{usuario}_") or file.startswith("public_"):
                    arquivos.append(relative_path)


    registrar_log("Uploads", usuario, "Uploads Rendered")
    return render_template('uploadFiles.html', arquivos=arquivos)
# ======================================= RENAME Files ===================================
@app.route("/graywolf-rename-form", methods=["GET"])
def graywolf_rename_file_form():
    if 'usuario_logado' not in session:
        return redirect("/")

    arquivo_path = request.args.get("file_path")
    nome_arquivo = os.path.basename(arquivo_path)

    return render_template("rename_file.html", arquivo_path=arquivo_path, nome_arquivo=nome_arquivo)

@app.route("/graywolf-rename-file", methods=["POST"])
def graywolf_rename_file():
    if 'usuario_logado' not in session:
        return redirect("/")

    usuario = session["usuario_logado"]
    arquivo_antigo_path = request.form.get("arquivo_antigo_path")
    novo_nome = request.form.get("novo_nome")

    if not arquivo_antigo_path or not os.path.exists(arquivo_antigo_path):
        return render_template("texts.html")

    nome_arquivo_antigo = os.path.basename(arquivo_antigo_path)
    pasta = os.path.dirname(arquivo_antigo_path)
    novo_caminho = os.path.join(pasta, novo_nome)

    # Verificações
    if os.path.exists(novo_caminho):
    
        return render_template("texts.html")

    if not (nome_arquivo_antigo.startswith(f"{usuario}_") or nome_arquivo_antigo.startswith("public_")):
        return "Você não tem permissão para renomear esse arquivo", 403
    extensao_antiga = os.path.splitext(nome_arquivo_antigo)[1]
    extensao_nova = os.path.splitext(novo_nome)[1]

    # Impede troca de extensão
    if extensao_antiga != extensao_nova:
        return render_template("texts.html")

    # Impede troca de prefixo
    if nome_arquivo_antigo.startswith("public_"):
        prefixo = "public_"
    elif nome_arquivo_antigo.startswith(f"{usuario}_"):
        prefixo = f"{usuario}_"
    else:
        return render_template("texts.html")

    novo_nome_limpo = prefixo + novo_nome.split(prefixo)[-1]  # garante prefixo

    novo_caminho = os.path.join(pasta, novo_nome_limpo)


    os.rename(arquivo_antigo_path, novo_caminho)
    registrar_log("RenameFile", usuario, f"{nome_arquivo_antigo} -> {novo_nome}")

    return redirect(request.referrer)

# ========================================== Delete Files ================================
@app.route("/graywolf-delete-file", methods=["GET", "POST"])
def delete_file():
    usuario_logado = session.get('usuario_logado')
    usuarios = carregar_usuarios()

    if not usuario_logado:
        return redirect('/graywolf-login')

    if request.method == "POST":
        file_path = request.form.get('file_path')
    else:
        file_path = request.args.get('file_path')

    if not file_path or not os.path.exists(file_path):
        nome_arquivo = os.path.basename(file_path)

        is_admin = usuarios.get(usuario_logado, {}).get("nivel") == "admin"
        is_dono_do_arquivo = (
            nome_arquivo.startswith(f"public_{usuario_logado}_") or
            nome_arquivo.startswith(f"{usuario_logado}_")
        )
        file_path = request.form.get('file_path')
        if is_admin or is_dono_do_arquivo:
            file_size = os.path.getsize(f"GWFiles/{file_path}")

            os.remove(f"GWFiles/{file_path}")
            registrar_log("Delete", usuario_logado, f"Deleted: {file_path} ({file_size} bytes)")

            if nome_arquivo.startswith("public_"):
                dono_arquivo = nome_arquivo.split("_")[1]
            else:
                dono_arquivo = nome_arquivo.split("_")[0]

            if dono_arquivo in usuarios:
                if "armazenamento_usado" not in usuarios[dono_arquivo]:
                    usuarios[dono_arquivo]["armazenamento_usado"] = 0
                usuarios[dono_arquivo]["armazenamento_usado"] -= file_size
                if usuarios[dono_arquivo]["armazenamento_usado"] < 0:
                    usuarios[dono_arquivo]["armazenamento_usado"] = 0


            with open("GWData/GWS_Users/users.json", "w") as f:
                json.dump(usuarios, f, indent=4)
        else:
            registrar_log("Delete", usuario_logado, f"Tried to delete unauthorized: {file_path}")
        return redirect(request.referrer)

    nome_arquivo = os.path.basename(file_path)

    is_admin = usuarios.get(usuario_logado, {}).get("nivel") == "admin"
    is_dono_do_arquivo = (
        nome_arquivo.startswith(f"public_{usuario_logado}_") or
        nome_arquivo.startswith(f"{usuario_logado}_")
    )

    if is_admin or is_dono_do_arquivo:
        file_size = os.path.getsize(file_path)

        os.remove(file_path)
        registrar_log("Delete", usuario_logado, f"Deleted: {file_path} ({file_size} bytes)")

        if nome_arquivo.startswith("public_"):
            dono_arquivo = nome_arquivo.split("_")[1]
        else:
            dono_arquivo = nome_arquivo.split("_")[0]

        if dono_arquivo in usuarios:
            if "armazenamento_usado" not in usuarios[dono_arquivo]:
                usuarios[dono_arquivo]["armazenamento_usado"] = 0
            usuarios[dono_arquivo]["armazenamento_usado"] -= file_size
            if usuarios[dono_arquivo]["armazenamento_usado"] < 0:
                usuarios[dono_arquivo]["armazenamento_usado"] = 0

        with open("GWData/GWS_Users/users.json", "w") as f:
            json.dump(usuarios, f, indent=4)
    else:
        registrar_log("Delete", usuario_logado, f"Tried to delete unauthorized: {file_path}")

    return redirect(request.referrer)

# ===================================== Show Videos ==================================
@app.route("/graywolf-video/<subcategoria>")
def exibir_videos(subcategoria):
    registrar_log("Video", session.get("usuario_logado", "unknow"), f"Video: {subcategoria} Accessed")
    caminho_pasta = os.path.join("GWFiles", "video", subcategoria)

    if not os.path.exists(caminho_pasta):
        return redirect("/graywolf-upload")

    usuario = session['usuario_logado']
    
    with open(USERS_FILE) as f:
        usuarios = json.load(f)
        user_info = usuarios.get(usuario)
        is_admin = user_info and user_info.get("nivel") == "admin"

    arquivos = [
        f for f in os.listdir(caminho_pasta)
        if os.path.isfile(os.path.join(caminho_pasta, f))
        and allowed_file(f)
        and (f.startswith(f'{usuario}_') or f.startswith('public_') or is_admin)
    ]
    registrar_log("Video", session.get("usuario_logado", "unknow"), f"Video: {subcategoria} Rendered")
    return render_template("videos.html", subcategoria=subcategoria, arquivos=arquivos)

@app.route('/videos/<subcategoria>/<nome_arquivo>')
def servir_video(subcategoria, nome_arquivo):
    caminho = os.path.join("GWFiles", "video", subcategoria)
    registrar_log("Video", session.get("usuario_logado", "unknow"), f"Video: {subcategoria}. {nome_arquivo}")
    return send_from_directory(caminho, nome_arquivo)
# ====================================== Listen Audio ======================================
@app.route("/graywolf-audio/<subcategoria>")
def exibir_audios(subcategoria):
    registrar_log("Audio", session.get("usuario_logado", "unknow"), f"Audio: {subcategoria} Accessed")
    caminho_pasta = os.path.join("GWFiles", "audio", subcategoria)
    usuario = session['usuario_logado']
    if not os.path.exists(caminho_pasta):
        return redirect("/graywolf-upload")
    
    with open(USERS_FILE) as f:
        usuarios = json.load(f)
        user_info = usuarios.get(usuario)
        is_admin = user_info and user_info.get("nivel") == "admin"

    arquivos = [
        f for f in os.listdir(caminho_pasta)
        if os.path.isfile(os.path.join(caminho_pasta, f))
        and allowed_file(f)
        and (f.startswith(f'{usuario}_') or f.startswith('public_') or is_admin)
    ]
    registrar_log("Audio", session.get("usuario_logado", "unknow"), f"Audio: {subcategoria} Rendered")
    return render_template("audios.html", subcategoria=subcategoria, arquivos=arquivos)

@app.route('/audios/<subcategoria>/<nome_arquivo>')
def servir_audio(subcategoria, nome_arquivo):
    caminho = os.path.join("GWFiles", "audio", subcategoria)
    registrar_log("Audio", session.get("usuario_logado", "unknow"), f"Audio: {subcategoria}. Downloading... {nome_arquivo}")
    return send_from_directory(caminho, nome_arquivo)

# ================================ Show Image ==============================
@app.route("/graywolf-photo")
def exibir_fotos():
    registrar_log("Image", session.get("usuario_logado", "unknow"), "Image: Photo Accessed")
    return exibir_imagens_por_subcategoria("photo")

@app.route("/graywolf-screenshot")
def exibir_capturas():
    registrar_log("Image", session.get("usuario_logado", "unknow"), "Image: Screenshot Accessed")
    return exibir_imagens_por_subcategoria("screenshot")

@app.route("/graywolf-image-no-category")
def exibir_imagens_gerais():
    registrar_log("Image", session.get("usuario_logado", "unknow"), "Image: image_no_category Accessed")
    return exibir_imagens_por_subcategoria("image_no_category")

def exibir_imagens_por_subcategoria(subcategoria):
    usuario = session.get('usuario_logado', 'unknown')
    registrar_log("Image", usuario, f"Image: {subcategoria} Accessed")
    
    caminho = os.path.join("GWFiles", "image", subcategoria)
    if not os.path.exists(caminho):
        return redirect("/graywolf-upload")

    with open(USERS_FILE) as f:
        usuarios = json.load(f)
    user_info = usuarios.get(usuario)
    is_admin = user_info and user_info.get("nivel") == "admin"

    imagens = [
        f for f in os.listdir(caminho)
        if os.path.isfile(os.path.join(caminho, f))
        and allowed_file(f)
        and (f.startswith(f'{usuario}_') or f.startswith('public_') or is_admin)
    ]

    registrar_log("Image", usuario, f"Image: {subcategoria} Rendered")
    return render_template(
        "images.html",
        imagens=imagens,
        subcategoria=subcategoria,
        usuario_logado=usuario,
        is_admin=is_admin
    )

@app.route('/imagem/<subcategoria>/<nome_arquivo>')
def servir_imagem(subcategoria, nome_arquivo):
    caminho = os.path.join("GWFiles", "image", subcategoria)
    registrar_log("Image", session.get("usuario_logado", "unknow"), f"Image: {subcategoria}. Downloading... {nome_arquivo}")
    return send_from_directory(caminho, nome_arquivo)

# =============================== Show Document ========================
@app.route("/graywolf-<categoria>", methods=["GET"])
def exibir_documentos_categoria(categoria):
    registrar_log("Document", session.get("usuario_logado", "unknow"), f"Document: {categoria} Accessed")
    
    categoria_map = {
        "excel": "excel",
        "pdf": "pdf",
        "powerpoint": "powerpoint",
        "word": "word",
        "document-no-category": "document_no_category"
    }

    if categoria in categoria_map:
        pasta = os.path.join(BASE_DIR, "GWFiles", "document", categoria_map[categoria])
        usuario = session['usuario_logado']
        usuarios = carregar_usuarios()
        nivel_usuario = usuarios.get(usuario, {}).get("nivel", "user")

        if nivel_usuario == "admin":
            arquivos = [
                arquivo for arquivo in os.listdir(pasta)
                if os.path.isfile(os.path.join(pasta, arquivo))
                and allowed_file(arquivo)
            ]
        else:
            arquivos = [
                arquivo for arquivo in os.listdir(pasta)
                if os.path.isfile(os.path.join(pasta, arquivo))
                and allowed_file(arquivo)
                and (arquivo.startswith(f'{usuario}_') or arquivo.startswith('public_'))
            ]

        registrar_log("Document", session.get("usuario_logado", "unknow"), f"Document: {categoria} Rendered")
        return render_template(
            "documents.html",
            arquivos=arquivos,
            categoria=categoria,
            categoria_pasta=categoria_map[categoria],
            categoria_titulo=categoria_map[categoria]
        )

    else:
        return redirect(url_for('document_page'))
    
# ============================ See Stats =================================
@app.route("/graywolf-stats", methods=["GET"])
def graywolf_stats():
    usuario_logado = session.get("usuario_logado")
    
    registrar_log("Stats", session.get("usuario_logado", "unknow"), "Stats Accessed")

    if not usuario_logado:
        registrar_log("Stats", session.get("usuario_logado", "unknow"), "Not in Session")
        return redirect("/")

    usuarios = carregar_usuarios()

    if usuarios.get(usuario_logado, {}).get("nivel") == "admin":
        registrar_log("Stats", session.get("usuario_logado", "unknow"), "Not Admin")
        lista_usuarios = []
        for nome, dados in usuarios.items():
            lista_usuarios.append({
                "nome": nome,
                "nivel": dados.get("nivel", "???"),
                "criado_em": dados.get("criado_em", "???"),
                "armazenamento_usado": dados.get("armazenamento_usado", 0)
            })
        
            # === CPU ===
            cpu_percent = psutil.cpu_percent(interval=1)
            load_avg = psutil.getloadavg()  # (1min, 5min, 15min)

            # === RAM ===
            mem = psutil.virtual_memory()
            ram_total = mem.total
            ram_usado = mem.used
            ram_livre = mem.available
            ram_percent = mem.percent

            # === Disco ===
            disco = psutil.disk_usage('/')
            disco_total = disco.total
            disco_usado = disco.used
            disco_livre = disco.free
            disco_percent = disco.percent

            # === Uptime ===
            uptime_segundos = int(psutil.boot_time())
            uptime = datetime.now() - datetime.fromtimestamp(uptime_segundos)

        

        registrar_log("Stats", session.get("usuario_logado", "unknow"), "Admin Access")
        return render_template(
            "stats.html",
            usuarios=lista_usuarios,
            formatar_tamanho=formatar_tamanho,
            cpu_percent=cpu_percent,
            load_avg=load_avg,
            ram_total=ram_total,
            ram_usado=ram_usado,
            ram_livre=ram_livre,
            ram_percent=ram_percent,
            disco_total=disco_total,
            disco_usado=disco_usado,
            disco_livre=disco_livre,
            disco_percent=disco_percent,
            uptime=str(uptime).split('.')[0]  # remove microsegundos
        )
    else:
        return render_template("homepage.html")

# ==================== LOGS PAGE ===========================
@app.route("/graywolf-logs", methods=["GET"])
def graywolf_logs():
    try:
        arquivos_log = [f for f in os.listdir(LOG_DIR) if f.endswith(".log")]

        # Ordena os arquivos do mais recente para o mais antigo com base na modificação
        arquivos_log.sort(key=lambda f: os.path.getmtime(os.path.join(LOG_DIR, f)), reverse=True)

        return render_template("logs.html", arquivos_log=arquivos_log)
    except Exception as e:
        return redirect(url_for("graywolf_stats"))

@app.route("/graywolf-log-view", methods=["GET"])
def graywolf_log_view():
    nome_arquivo = request.args.get("file")
    caminho_log = os.path.join(LOG_DIR, nome_arquivo)

    if not os.path.exists(caminho_log):
        return redirect(url_for("graywolf_logs"))

    try:
        with open(caminho_log, "r", encoding="utf-8") as f:
            conteudo = f.read()
        return render_template("log_view.html", nome_arquivo=nome_arquivo, conteudo=conteudo)
    except Exception as e:
        return redirect(url_for("graywolf_logs"))

# ==================== End ============================

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
