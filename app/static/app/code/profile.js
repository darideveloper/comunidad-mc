const submit_button = document.querySelector(".content .btn.form.primary")


// Activate update button when country or time zone or phone changed
const phone = document.querySelector("#phone")
const inputs = [country, time_zone, phone] // use inputs from "select" scripts
inputs.forEach(input => {
  input.addEventListener('change', () => {
    submit_button.disabled = false
  })
})

// Show animation when click submit buttons
document.querySelectorAll(".content .btn").forEach ((button) => {
  button.addEventListener('click', () => {
    document.querySelector(".loading-wrapper").classList.remove("hide")
  })
})
