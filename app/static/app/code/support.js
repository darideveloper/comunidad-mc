import {show_message} from "./alerts.js"

const copy_buttons = document.querySelectorAll (".btn.cta.copy")
copy_buttons.forEach (function (button) {

  // Add event listener to each button
  button.addEventListener ("click", function (event) {
    
    // Copy user to clipboard
    const copy_text = button.parentNode.querySelector ("p.name").innerText
    navigator.clipboard.writeText(copy_text)

    // Change button
    button.classList.add ("active")
    const inner_span = button.querySelector ("span")
    inner_span.innerText = "Copiado!"

    // Reset button 
    setTimeout(() => {
      button.classList.remove ("active")
      inner_span.innerText = "Copiar"
    }, 2000)

  })
})