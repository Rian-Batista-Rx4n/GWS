let form = document.getElementById("uploadForm")
let bar = document.getElementById("bar")
let status = document.getElementById("status")
let category = document.getElementById("category")
let subfolder = document.getElementById("subfolder")

function updateSubfolders() {
subfolder.innerHTML = ""


let current = folders.find(x=> x.category == category.value)

if (!current)
return

current.subfolders
.forEach(folder=>{

subfolder.innerHTML+=`

<option>

${folder}

</option>

`

})

}


category.onchange=
updateSubfolders

updateSubfolders()



form.addEventListener("submit", e=> {
    e.preventDefault()
    let files = document.getElementById("files").files
    let data = new FormData()

    for (let file of files) {
        data.append("files", file)
    }

    data.append("mode", document.getElementById("mode").value)
    data.append("category", category.value)
    data.append("subfolder", subfolder.value)
    data.append("current", document.getElementById("current").value)

    let xhr = new XMLHttpRequest()

    xhr.upload.addEventListener("progress", e => {
            let percent = Math.round((e.loaded / e.total) * 100)

            bar.style.width = percent + "%"
            status.innerText = percent + "%"
        })

            xhr.onload = () => {status.innerText="Upload complete"}
            xhr.open("POST","/upload_file")
            xhr.send(data)
})

// Category and subfolder selection
let mode = document.getElementById("mode")
let categories = document.getElementById("categories")

mode.addEventListener("change", () => {

    if (mode.value == "category") {
        categories.style.display="block"
    } else { 
        categories.style.display="none"
    }
})