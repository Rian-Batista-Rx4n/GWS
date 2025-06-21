const upper = document.getElementById("upper")
const lower = document.getElementById("lower")
let text = document.getElementById("text")
var font_size = 15

upper.addEventListener("click", font_upper)
lower.addEventListener("click", font_lower)

function font_upper() {
    font_size += 5
    text.style.fontSize = `${font_size}px`
}

function font_lower() {
    font_size -= 5
    text.style.fontSize = `${font_size}px`
}