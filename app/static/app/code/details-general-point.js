import { show_details_point } from './alerts.js'

// get buttons
const buttons = document.querySelectorAll('button.more-info')

buttons.forEach(button => {
  button.addEventListener('click', () => {
    // Get details from button attributes
    const details = button.getAttribute('data-details')
    const title = button.getAttribute('data-title')
    show_details_point (title, details)
  })
})