const cta_buttons = document.querySelectorAll('.btn.cta')
const loading = document.querySelector('.loading-wrapper')

cta_buttons.forEach((btn) => {
  btn.addEventListener('click', (e) => {
    // Show loading when click button
    loading.classList.remove('hide')
  })
})