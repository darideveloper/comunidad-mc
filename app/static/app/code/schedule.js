// css selectors
const selector_time_wrapper = ".time .select"
const selector_time_item = ".time .select label"
const selector_day_item = ".date .select label"

function activate_item (item, selector) {
  // When click on item, disable current active item and enable new active item

  // Add lister to item
  item.addEventListener ("click", event => {
      // Disable current active element
      const active_item = document.querySelector (`${selector}.active`)
      if (active_item) {
        active_item.classList.remove ("active")
      }
    
      // Enable new active element
      item.classList.add ("active")
  })
}

function show_available_hours () {
  // Show available hours for selected day

  const current_day = document.querySelector (`${selector_day_item}.active`).innerText.toLowerCase()
  const day_hours = available_hours[current_day]
  
  // Delete current content of select element
  const select = document.querySelector (selector_time_wrapper)
  select.innerHTML = ""

  // Add new options to select element
  for (hour of hours) {

    // Disable hours already booked
    disabled_class = day_hours.includes (hour) ? "" :  "disabled"

    const item = `
      <label class=${disabled_class}>
        ${hour}:00 hrs
        <input type="radio" name="hour" value="${hour}">
      </label>
    `
    select.innerHTML += item
  }
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

// Set available hours when page loads
show_available_hours ()