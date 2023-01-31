// css selectors
const selector_time_wrapper = ".time .select"
const selector_time_item = ".time .select label"
const selector_day_item = ".date .select label"

function activate_item (item, selector) {
  // Disable current active item and enable new active item

  // Disable current active element
  const active_item = document.querySelector (`${selector}.active`)
  if (active_item) {
    active_item.classList.remove ("active")
  }

  // Enable new active element
  item.classList.add ("active")
}

function show_available_hours () {
  // Show available hours for selected day

  const current_day = document.querySelector (`${selector_day_item}.active`).innerText.toLowerCase()
  const day_hours = available_hours[current_day]

  console.log ({available_hours})
  
  // Delete current content of select element
  const select = document.querySelector (selector_time_wrapper)
  select.innerHTML = ""

  // Get current hour
  now = new Date ()
  current_hour = now.getHours ()

  // Add new options to select element
  for (hour of hours) {

    console.log ({today_week_name, current_day})

    // Disable hours before current time
    let disabled_class = ""
    if (today_week_name == current_day) {
      disabled_class = hour < current_hour ? "disabled" : ""
    }
    
    // Disable hours already booked
    if (disabled_class == "") {
      disabled_class = day_hours.includes (hour) ? "" :  "disabled"
    }

    const item = `
      <label class=${disabled_class}>
        ${hour}:00 hrs
        <input type="radio" name="hour" value="${hour}">
      </label>
    `
    select.innerHTML += item
  }
}

function toggle_submit (activate) {
  // Enable or disable submit button

  const submit = document.querySelector ("#submit")
  if (activate) {
    submit.removeAttribute ("disabled")
  } else {
    submit.setAttribute ("disabled", true)
  }
}

const day_items = document.querySelectorAll (selector_day_item)
// Activate day when ckick on it
day_items.forEach(day_item => {
  // Add lister to item
  day_item.addEventListener ("click", event => {
    // Activate item
    activate_item (day_item, selector_day_item)

    // Set available hours
    show_available_hours ()

    // Disable submit button
    toggle_submit (false)
  })
})

// Activate time when ckick on it
const time_items = document.querySelectorAll (selector_time_item)
time_items.forEach(time_item => {
  // Add lister to item
  time_item.addEventListener ("click", event => {
    // Activate item
    activate_item (time_item, selector_time_item)

    // Enable submit button
    toggle_submit (true)
  })
});


// Set available hours when page loads
show_available_hours ()