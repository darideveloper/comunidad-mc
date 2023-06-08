import {loading_wrapper} from './loading.js'
import {update_profile_card_small} from './profile-card-responsive.js'

// css selectors
const selector_time_item = ".time .select label"
const selector_day_item = ".date .select label"
const selector_confirmation_day = ".confirmation .day"
const selector_confirmation_date = ".confirmation .date"
const selector_confirmation_time = ".confirmation .time"

// Global nodes
const confirmation_day = document.querySelector (selector_confirmation_day)
const confirmation_date = document.querySelector (selector_confirmation_date)
const confirmation_time = document.querySelector (selector_confirmation_time)

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

  const current_day_elem = document.querySelector (`${selector_day_item}.active`)
  const current_day = current_day_elem ? current_day_elem.innerText.toLowerCase() : "domingo"
  const day_hours = available_hours[current_day]
  
  // Delete current content of select element
  const time_items = document.querySelectorAll (selector_time_item)

  // Add new options to select element
  time_items.forEach (time_item => {

    // Get item hour
    const hour = time_item.querySelector ("input").value

    // Disable hours before current time
    let disabled = day_hours.includes (hour) ? false : true

    // Disable or enable item
    const input = time_item.querySelector ("input")
    if (disabled) {
      // Add disabled class
      time_item.classList.add ("disabled")

      // Add disabled attribute from input child
      input.setAttribute ("disabled", true)
    } else {
      // Remove disabled class
      time_item.classList.remove ("disabled")
      time_item.classList.remove ("active")

      // Remove disabled attribute from input child
      input.removeAttribute ("disabled")
    }
  })
}

function toggle_submit (activate) {
  // Enable or disable submit button

  const submit = document.querySelector ("#submit-btn")
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

    // Validate if item its not disabled
    if (day_item.classList.contains ("disabled")) {
      return ""
    }

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

// Activate time when click on it
const time_items = document.querySelectorAll (selector_time_item)
time_items.forEach(time_item => {
  // Add lister to item
  time_item.addEventListener ("click", event => {

    // Validate if item its not disabled
    if (time_item.classList.contains ("disabled")) {
      return ""
    }

    // Activate item
    activate_item (time_item, selector_time_item)

    // Enable submit button
    toggle_submit (true)

    // Update date confirmation
    const day = document.querySelector (`${selector_day_item}.active`).innerText
    const date = document.querySelector (`${selector_day_item}.active > input`).getAttribute ("date-text")
    const time = document.querySelector (`${selector_time_item}.active`).innerText.toLowerCase()
    confirmation_day.innerText = day
    confirmation_date.innerText = date
    confirmation_time.innerText = time
  })
});

// Add events to cancal buttons
const cancel_buttons = document.querySelectorAll ("button.cancel")
cancel_buttons.forEach (cancel_button => {
  cancel_button.addEventListener ("click", event => {

    // Show loading
    loading_wrapper.classList.remove ('hide')

    // Get id from attributes
    const stream_id = cancel_button.getAttribute ("data-stream")
    const cancel_url = `/cancel-stream/${stream_id}`

    // check if is a warning button
    if (cancel_button.classList.contains ("warning")) {

      // Hide loading
      loading_wrapper.classList.add ('hide')

      Swal.fire({
        title: '¿Estás seguro?',
        text: "Queda poco para iniciar este stream, si lo cancelas ahora perderás puntos",
        showDenyButton: true,
        denyButtonText: 'Sí, cancelar y perder puntos',
        confirmButtonText: 'No, mantener mis puntos',
      }).then((result) => {
        if (! result.isConfirmed) {
          // Show loading
          loading_wrapper.classList.remove ('hide')

          // Redirect to cancel page
          window.location.href = cancel_url
        }
      })      
    } else {
      // Redirect to cancel page
      window.location.href = cancel_url
    }
  })
})

// Detect when try to submit form
const form = document.querySelector ("form")
form.addEventListener ("submit", event => {
  event.preventDefault ()

  // Validate if the selected date and time, its already shcedule for the same user
  const selected_date = document.querySelector (`${selector_day_item}.active > input`).value
  const selected_time = document.querySelector (`${selector_time_item}.active > input`).value
  const match_streams = streams_date_times.filter (stream => {
    return stream.date == selected_date && stream.hour == selected_time
  })

  if (match_streams.length > 0) {
    // Show alert
    Swal.fire({
      title: 'Advertencia',
      text: "Ya tienes un stream agendado para esta fecha y hora. Si agendas otro stream, serás la única persona a quien apoye la comunidad, pero perderás el doble de puntos",
      showDenyButton: true,
      showCancelButton: true,
      confirmButtonText: 'No, no agendar doble stream',
      denyButtonText: `Sí, agendar y perder el doble de puntos`,
      showCancelButton: false,
    }).then((result) => {
      if (result.isDenied) {
        // Show loading
        loading_wrapper.classList.remove ('hide')
        
        // Submit form after conformation
        form.submit ()
      }
    })
  } else {
    // Show loading
    loading_wrapper.classList.remove ('hide')

    // Submit form directly
    form.submit ()
  }
})

// Set available hours when page loads
show_available_hours ()

// Update profile card when resize
update_profile_card_small ()
window.addEventListener ("resize", () => update_profile_card_small())