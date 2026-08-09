let menu_button = document.getElementById("menu-button")
let menu = document.getElementById("menu")
let delete_btn = document.getElementById("delete")
let rename_btn = document.getElementById("rename")
let document_btn = document.getElementById("create-document")
let folder_btn = document.getElementById("create-folder")
let upload_btn = document.getElementById("upload")

var menuIsOpen = false

menu_button.addEventListener("click", toggleMenu)

let buttons = [
    delete_btn,
    rename_btn,
    document_btn,
    folder_btn,
    upload_btn
]

function toggleMenu(){
    menuIsOpen =! menuIsOpen

    if(menuIsOpen){
        menu.style.width = "48px"
        menu.style.height = "240px"
        menu.style.background = "#60a5fa"

        buttons.forEach(btn => {

            btn.style.width="48px"
            btn.style.height="48px"
            btn.style.fontSize="24px"

        })
    } else {
        menu.style.width = "0"
        menu.style.height = "0"
        menu.style.background = "transparent"

        buttons.forEach(btn => {
            btn.style.width = "0"
            btn.style.height = "0"
            btn.style.fontSize = "0"
        })
    }
}

let mode = ""

delete_btn.onclick = () => {
    mode = "delete"
}

rename_btn.onclick = () => {
    mode = "rename"
}

document_btn.onclick = async() => {
    await fetch(
        "/action/create_document",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/x-www-form-urlencoded"
            },

            body:
            "current="+window.location.pathname.replace(
                "/home/",
                ""
            )
        }
    )

    location.reload()
}

folder_btn.onclick = async() => {
    await fetch(
        "/action/create_folder",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/x-www-form-urlencoded"
            },

            body:
            "current="+window.location.pathname.replace(
                "/home/",
                ""
            )
        }
    )

    location.reload()
}

document.querySelectorAll(".item")
.forEach(item => {

item.addEventListener(
"click",

async(e) => {

if(mode == "")
return

e.preventDefault()

let path=item.dataset.path

if(mode == "delete"){


if(
confirm(
"Delete?"
)
){

await fetch(
"/action/delete",
{

method:"POST",

headers:{
"Content-Type":
"application/x-www-form-urlencoded"
},

body:
"path="+path

}

)

location.reload()

}


mode=""

}



if(mode=="rename"){


let name=prompt(
"Rename:"
)


if(name){

await fetch(
"/action/rename",
{

method:"POST",

headers:{
"Content-Type":
"application/x-www-form-urlencoded"
},

body:
`old=${path}&new=${name}`

}

)

location.reload()

}

mode=""

}

})

})

upload_btn.onclick=()=>{

window.location=

"/upload?current="+

window.location.pathname.replace(
"/home/",
""
)

}

let modal=
document.getElementById(
"fileModal"
)

let selectedFile=""

document
.querySelectorAll(
".file-item"
)

.forEach(file=>{

file.onclick=(e)=>{

if(mode!="")
return

selectedFile=
file.dataset.path

modal.style.display=
"flex"

}

})


closeBtn.onclick=()=>{

modal.style.display=
"none"

}

openBtn.onclick=()=>{

window.location=
"/open/"+selectedFile

}

downloadBtn.onclick=()=>{

window.location=
"/download/"+selectedFile

}

infoBtn.onclick=()=>{

window.location=
"/info/"+selectedFile

}