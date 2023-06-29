import { show_details_point } from './alerts.js'

// get buttons
const buttons = document.querySelectorAll('button.more-info')

buttons.forEach(button => {
  button.addEventListener('click', () => {
    // Get details from button attributes
    const details = button.getAttribute('data-details')
    show_details_point (details)
  })
})