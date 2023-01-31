// css selectors
const selector_time_wrapper = ".time .select"
const selector_time_item = ".time .select label"
const selector_day_item = ".date .select label"
const selector_confirmation = ".confirmation .info"
const selector_confirmation_day = ".confirmation .day"
const selector_confirmation_date = ".confirmation .date"
const selector_confirmation_time = ".confirmation .time"

// Global nodes
confirmation_day = document.querySelector (selector_confirmation_day)
confirmation_date = document.querySelector (selector_confirmation_date)
confirmation_time = document.querySelector (selector_confirmation_time)

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
  
  // Delete current content of select element
  const time_items = document.querySelectorAll (selector_time_item)

  // Get current hour
  const now = new Date ()
  const current_hour = now.getHours ()

  // Add new options to select element
  time_items.forEach (time_item => {

    // Get item hour
    hour = time_item.querySelector ("input").value

    // Remove disabled class
    time_item.classList.remove ("disabled")
    time_item.classList.remove ("active")

    // Disable hours before current time
    let disabled = false
    if (today_week_name == current_day) {
      disabled = parseInt(hour) < current_hour ? true : false
    }
    
    // Disable hours already booked
    if (disabled == false) {
      disabled = day_hours.includes (hour) ? false : true
    }

    // Disable item
    if (disabled) {
      time_item.classList.add ("disabled")
    }
  })
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

// Activate day when ckick on it
const day_items = document.querySelectorAll (selector_day_item)
day_items.forEach(day_item => {
  // Add lister to item
  day_item.addEventListener ("click", event => {
    // Activate item
    activate_item (day_item, selector_day_item)

    // Set available hours
    show_available_hours ()

    // Disable submit button
    toggle_submit (false)

    // Reset confirmation info 
    confirmation_day.innerText = ""
    confirmation_date.innerText = ""
    confirmation_time.innerText = ""
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

    // Update date confirmation
    const day = document.querySelector (`${selector_day_item}.active`).innerText
    const date = document.querySelector (`${selector_day_item}.active > input`).getAttribute ("data-date")
    const time = document.querySelector (`${selector_time_item}.active`).innerText.toLowerCase()
    confirmation_day.innerText = day
    confirmation_date.innerText = date
    confirmation_time.innerText = time
  })
});


// Set available hours when page loads
show_available_hours ()