
// Open and close menu
const header_btns = document.querySelectorAll ("#header .btn.menu")
const menu_wrapper = document.querySelector('#header .menu-wrapper')

for (const header_btn of header_btns) {
  header_btn.addEventListener ("click", function (e) {
    menu_wrapper.classList.toggle ("open")
  })
}

// // Update header when scroll
// window.addEventListener ("scroll", function (e) {
//     // Only add class for desktop sizes
//     if (window.scrollY == 0 || window.matchMedia("(max-width: 800px)").matches) {
//         header.classList.remove ("scroll")
//     } else {
//         header.classList.add ("scroll")
//     }
// })

// Activate menu element of the current page
const menu_item_active = document.querySelector(`ul.menu li.${current_page}`)
if (menu_item_active) {
  menu_item_active.classList.add ("active")
  // menu_item_active.querySelector("a").setAttribute ("href", "#")
}
