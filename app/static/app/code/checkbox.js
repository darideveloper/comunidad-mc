// Acvite checkbox when click
const checkbox_wrappers = document.querySelectorAll('.checkbox-wrapper')
checkbox_wrappers.forEach (checkbox_wrapper => {

  // Get elemtns
  const checkbox = checkbox_wrapper.querySelector('input[type="checkbox"]')
  const label = checkbox_wrapper.querySelector('label')

  // Toggle active class
  checkbox.addEventListener ("change", event => {
    label.classList.toggle ("active")
  })
})