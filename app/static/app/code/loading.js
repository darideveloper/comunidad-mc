// nodes
export const loading_wrapper = document.querySelector('.loading-wrapper')
const menu_buttons = document.querySelectorAll('.menu-wrapper ul li:not(.active) a')

// Show the loading screen shwn click menu buttons
menu_buttons.forEach (function (button) {
  button.addEventListener ('click', e => {
    // Evit redirect
    e.preventDefault()

    // Remove the hide class from the loading wrapper
    loading_wrapper.classList.remove ('hide')

    // Redirect to the page
    const link = button.getAttribute ('href')
    window.location.href = link
  })
})

// Disable loading icon when the page is loaded
window.addEventListener ('load', e => {
  loading_wrapper.classList.add ('hide')
})


