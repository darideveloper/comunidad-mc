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

// Submit data to backend when user update the donations
const doned_checkboxs = document.querySelectorAll ("label.donation")
doned_checkboxs.forEach (function (doned_checkbox) {
  // Activate loading button
  
  // Add event listener to each checkbox
  doned_checkbox.addEventListener ("click", function (event) {
    
    document.querySelector (".loading-wrapper").classList.remove ("hide")

    // Get form and submit
    const form = doned_checkbox.parentNode
    form.submit ()
  })
})