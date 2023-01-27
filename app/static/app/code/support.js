import {show_message} from "./alerts.js"

const copy_buttons = document.querySelectorAll (".btn.cta.copy")
copy_buttons.forEach (function (button) {

  // Add event listener to each button
  button.addEventListener ("click", function (event) {
    
    // Copy user to clipboard
    const copy_text = button.parentNode.querySelector ("p.name").innerText
    navigator.clipboard.writeText(copy_text)

    // Show alert
    show_message ("Nombre de usuario copiado al portapapeles.")

  })
})