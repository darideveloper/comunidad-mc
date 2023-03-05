const button = document.querySelector(".btn.form.primary")
console.log (button)

// Activate update button when country or time zone is changed
country.addEventListener('change', () => {
  button.disabled = false
})

time_zone.addEventListener('change', () => {
  button.disabled = false
})