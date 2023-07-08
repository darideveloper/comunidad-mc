const select = document.querySelector("form select")
const button = document.querySelector("form .btn")
import { show_error } from "./alerts.js"

if (select) {
  // Disable button if no option is selected
  select.addEventListener("change", (e) => {
    if (e.target.value == "") {
      button.disabled = true
    } else {
      button.disabled = false
    }
  })

  // Show loading when submit form
  document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault()

    if (withdrawEnabled) {
      document.querySelector(".loading-wrapper").classList.remove("hide")
      e.target.submit()
    } else {
      show_error ("Reclamar bits no está disponible por el momento. Ya estamos trabajando en eso. No es necesario que abras un ticket.")      
    }
  })
}
