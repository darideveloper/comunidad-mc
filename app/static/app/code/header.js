
// const header_btn = document.querySelector ("#header .btn.display")
// const header = document.querySelector('#header')

// header_btn.addEventListener ("click", function (e) {
//     header.classList.toggle ("clossed")
//     console.log ("click")
// })

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
menu_item_active.classList.add ("active")
menu_item_active.querySelector("a").setAttribute ("href", "#")
