function verSenha(){
    let campo = document.getElementById("password")

    if (campo.type == "password") {
        campo.type = "text"
    } else {
        campo.type = "password"
    }
}