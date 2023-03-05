// Nodes
const country_code = document.querySelector("#country-code")
const phone = document.querySelector("#phone")
const full_number = document.querySelector("#full-phone")


// Update country code when the country changes
document.querySelector("#country").addEventListener("change", e => {
  const code = countries_codes.find(c => c[0] === e.target.value)[1]
  document.querySelector("#country-code").innerHTML = "+" + code
})

// Update full number when the country code or number changes
function update_full_number () {
  const code = country_code.innerHTML
  const phone_number = phone.value
  full_number.value = `${code} ${phone_number}`
}
country.addEventListener("change", update_full_number)
phone.addEventListener("change", update_full_number)

// Show loading when the form is submitted
const form = document.querySelector("form")
form.addEventListener("submit", e => {
  e.preventDefault()
  document.querySelector(".loading-wrapper").classList.remove("hide")
  form.submit ()
})
