const submit_button = document.querySelector(".btn.form.primary")

// Activate update button when country or time zone is changed
country.addEventListener('change', () => {
  submit_button.disabled = false
})

time_zone.addEventListener('change', () => {
  submit_button.disabled = false
})

// Show animation when click submit buttons
document.querySelectorAll(".btn").forEach ((button) => {
  button.addEventListener('click', () => {
    document.querySelector(".loading-wrapper").classList.remove("hide")
  })
})
