from flask import Flask, render_template, request, redirect, flash, session, send_from_directory, url_for
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "GWFiles", "document")

pastas_criadas = False

UPLOAD_FOLDER = 'GWUpload'
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'ico',
    'zip', 'rar', '7z', 'tar', 'gz', 'xz',
    'doc', 'docx', 'odt', 'xls', 'xlsx', 'ods', 'ppt', 'pptx', 'csv', 'rtf',
    'mp4', 'mkv', 'avi', 'mov', 'webm',
    'mp3', 'wav', 'ogg', 'flac', 'm4a',
    'py', 'js', 'html', 'css', 'json', 'xml', 'sql', 'md', 'sh'
}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'RX4NRX4N'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/graywolf-back", methods=["GET"])
def graywolf_back():
    return render_template("homepage.html")

@app.route("/graywolf-register", methods=["GET"])
def graywolf_register():
    if session.get("usuario_logado") == "rx4n":
        return render_template("register.html")
    else:
        return render_template("homepage.html")

@app.route("/graywolf-homepage", methods=["POST"])
def graywolf_homepage():
    usuario = request.form.get("nome_usuario")
    senha = request.form.get("senha_usuario")
    if usuario == "rx4n" and senha == "rx4n":
        session['usuario_logado'] = usuario
        session['login_time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{session['login_time']} - Usuario: {usuario}, entrou.")
        return render_template("homepage.html")
    else:
        flash("Usuário ou senha incorretos.")
        return redirect("/")

def print_log_page(page_name):
    if 'usuario_logado' in session:
        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Usuario: {session['usuario_logado']}, Acessou {page_name}.")

@app.route("/graywolf-document", methods=["GET"])
def show_document_page():
    if 'usuario_logado' not in session:
        return redirect("/")
    print_log_page("Documentos")
    return render_template("document.html")

@app.route("/graywolf-text", methods=["GET"])
def show_text_page():
    if 'usuario_logado' not in session:
        return redirect("/")
    print_log_page("Texto")
    return render_template("text.html")

@app.route("/graywolf-audio", methods=["GET"])
def show_audio_page():
    if 'usuario_logado' not in session:
        return redirect("/")
    print_log_page("Áudio")
    return render_template("audio.html")

@app.route("/graywolf-image", methods=["GET"])
def show_image_page():
    if 'usuario_logado' not in session:
        return redirect("/")
    print_log_page("Imagem")
    return render_template("image.html")

@app.route("/graywolf-video", methods=["GET"])
def show_video_page():
    if 'usuario_logado' not in session:
        return redirect("/")
    print_log_page("Vídeo")
    return render_template("video.html")

@app.route("/graywolf-upload", methods=["GET"])
def show_upload_page():
    if 'usuario_logado' not in session:
        return redirect("/")
    print_log_page("Upload")
    return render_template("upload.html")

@app.route("/graywolf-upload-file", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect(request.referrer)

    files = request.files.getlist("file")
    main_category = request.form.get("chooseFile")
    sub_category = request.form.get("subCategory")

    if not files or not main_category or not sub_category:
        flash("Todos os campos são obrigatórios.")
        return redirect(request.referrer)

    folder_path = os.path.join("GWFiles", main_category, sub_category)
    os.makedirs(folder_path, exist_ok=True)

    agora = datetime.now()
    for file in files:
        if file.filename == '':
            continue  # Ignora arquivos sem nome

        if not allowed_file(file.filename):
            continue  # Ignora arquivos com extensões inválidas

        timestamp = agora.strftime("%Y%m%d_%H%M%S")
        filename = f"{file.filename}"
        filepath = os.path.join(folder_path, filename)
        file.save(filepath)
        print(f"{agora.strftime('%d/%m/%Y %H:%M:%S')} - Arquivo {file.filename} salvo em {filepath}")

    flash('Arquivos enviados com sucesso!')
    return redirect("/graywolf-upload")

@app.route('/graywolf-uploadFiles')
def upload_files_page():
    arquivos = []
    for root, dirs, files in os.walk("GWFiles"):
        for file in files:
            caminho = os.path.relpath(os.path.join(root, file), start="GWFiles")
            arquivos.append(caminho)
    return render_template('uploadFiles.html', arquivos=arquivos)

@app.route('/download/<path:nome_arquivo>')
def download_arquivo(nome_arquivo):
    diretorio = os.path.join("GWFiles", os.path.dirname(nome_arquivo))
    return send_from_directory(diretorio, os.path.basename(nome_arquivo), as_attachment=True)

@app.route("/logout")
def logout():
    usuario = session.get('usuario_logado')
    session.pop('usuario_logado', None)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{agora} - Usuario {usuario} saiu.")
    flash("Você saiu da sessão.")
    return redirect("/")

# ===================================== VER VIDEOS ==================================
@app.route("/graywolf-video/<subcategoria>")
def exibir_videos(subcategoria):
    caminho_pasta = os.path.join("GWFiles", "video", subcategoria)

    if not os.path.exists(caminho_pasta):
        flash("Subcategoria não encontrada.")
        return redirect("/graywolf-upload")

    arquivos = [
        f for f in os.listdir(caminho_pasta)
        if os.path.isfile(os.path.join(caminho_pasta, f)) and allowed_file(f)
    ]

    return render_template("videos.html", subcategoria=subcategoria, arquivos=arquivos)

@app.route('/videos/<subcategoria>/<nome_arquivo>')
def servir_video(subcategoria, nome_arquivo):
    caminho = os.path.join("GWFiles", "video", subcategoria)
    return send_from_directory(caminho, nome_arquivo)
# ====================================== OUVIR AUDIO ======================================
@app.route("/graywolf-audio/<subcategoria>")
def exibir_audios(subcategoria):
    caminho_pasta = os.path.join("GWFiles", "audio", subcategoria)

    if not os.path.exists(caminho_pasta):
        flash("Subcategoria não encontrada.")
        return redirect("/graywolf-upload")

    arquivos = [
        f for f in os.listdir(caminho_pasta)
        if os.path.isfile(os.path.join(caminho_pasta, f)) and allowed_file(f)
    ]

    return render_template("audios.html", subcategoria=subcategoria, arquivos=arquivos)

@app.route('/audios/<subcategoria>/<nome_arquivo>')
def servir_audio(subcategoria, nome_arquivo):
    caminho = os.path.join("GWFiles", "audio", subcategoria)
    return send_from_directory(caminho, nome_arquivo)

# ================================ VER IMAGENS ==============================
@app.route("/graywolf-photo")
def exibir_fotos():
    return exibir_imagens_por_subcategoria("photo")

@app.route("/graywolf-screenshot")
def exibir_capturas():
    return exibir_imagens_por_subcategoria("screenshot")

@app.route("/graywolf-image-no-category")
def exibir_imagens_gerais():
    return exibir_imagens_por_subcategoria("image_no_category")

def exibir_imagens_por_subcategoria(subcategoria):
    caminho = os.path.join("GWFiles", "image", subcategoria)
    if not os.path.exists(caminho):
        flash("Subcategoria não encontrada.")
        return redirect("/graywolf-upload")
    
    imagens = [
        f for f in os.listdir(caminho)
        if os.path.isfile(os.path.join(caminho, f)) and allowed_file(f)
    ]
    return render_template("images.html", imagens=imagens, subcategoria=subcategoria)

@app.route('/imagem/<subcategoria>/<nome_arquivo>')
def servir_imagem(subcategoria, nome_arquivo):
    caminho = os.path.join("GWFiles", "image", subcategoria)
    return send_from_directory(caminho, nome_arquivo)

# ================================= VER DOCUMENTS =================================
@app.route("/graywolf-<categoria>", methods=["GET"])
def exibir_documentos_categoria(categoria):
    categoria_map = {
        "excel": "excel",
        "pdf": "pdf",
        "powerpoint": "powerpoint",
        "word": "word",
        "document-no-category": "document_no_category"
    }

    if categoria in categoria_map:
        pasta = os.path.join(BASE_DIR, "GWFiles", "document", categoria_map[categoria])
        arquivos = [
            arquivo for arquivo in os.listdir(pasta)
            if os.path.isfile(os.path.join(pasta, arquivo))
        ]
        return render_template(
            "documents.html",                # ✅ o template correto
            arquivos=arquivos,
            categoria=categoria,
            categoria_titulo=categoria_map[categoria]
        )
    else:
        return redirect(url_for('document_page'))

@app.route("/document/<categoria>/<nome_arquivo>")
def download_documento(categoria, nome_arquivo):
    categoria_map = {
        "excel": "excel",
        "pdf": "pdf",
        "powerpoint": "powerpoint",
        "word": "word",
        "document-no-category": "document_no_category"
    }

    pasta = categoria_map.get(categoria)
    if not pasta:
        flash("Categoria inválida.")
        return redirect("/graywolf-document")

    caminho = os.path.join("GWFiles", "document", pasta)
    return send_from_directory(caminho, nome_arquivo, as_attachment=True)

# ==================== CRIAR PASTAS NESCESSARIAS =====================
@app.before_request
def criar_pastas_necessarias():
    estrutura = {
        "video": ["movie", "serie", "video_no_category"],
        "image": ["photo", "screenshot", "image_no_category"],
        "audio": ["music", "podcast", "audio_no_category"],
        "document": ["excel", "pdf", "powerpoint", "word", "document_no_category"],
        "text": ["list", "note", "script", "text_no_category"],
        "trash": [],
        "geral": ["sem_categoria"]
    }

    for categoria, subcategorias in estrutura.items():
        if subcategorias:
            for sub in subcategorias:
                caminho = os.path.join("GWFiles", categoria, sub)
                os.makedirs(caminho, exist_ok=True)
        else:
            caminho = os.path.join("GWFiles", categoria)
            os.makedirs(caminho, exist_ok=True)

    print("✅ Todas as pastas necessárias foram verificadas/criadas.")
    pastas_criadas = True

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
