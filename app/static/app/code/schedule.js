// css selectors
const selector_time_item = ".time .select label"
const selector_day_item = ".date .select label"

function activate_item (item, selector) {
  // Add lister to item
  item.addEventListener ("click", event => {
      console.log ("item clicked")
      console.log (item)
      // Disable current active element
      const active_item = document.querySelector (`${selector}.active`)
      if (active_item) {
        active_item.classList.remove ("active")
      }
    
      // Enable new active element
      item.classList.add ("active")
  })
}

// Activate time when ckick on it
const time_items = document.querySelectorAll (selector_time_item)
time_items.forEach(time_item => {
  activate_item (time_item, selector_time_item)
});

// Activate day when ckick on it
const day_items = document.querySelectorAll (selector_day_item)
day_items.forEach(day_item => {
  activate_item (day_item, selector_day_item)
})