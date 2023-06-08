const select = document.querySelector("form select")
const button = document.querySelector("form .btn")

if (select) {
  // Disable button if no option is selected
  select.addEventListener ("change", (e) => {
    if (e.target.value == "") {
      button.disabled = true
    } else {
      button.disabled = false
    }
  })

  // Show loading when submit form
  document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault ()
    document.querySelector(".loading-wrapper").classList.remove("hide")
    e.target.submit()
  })
}
