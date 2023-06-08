export function show_alert_url () {
    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString)
    var thanks = urlParams.get('thanks')
    if (thanks) {
        
        // Create alert
        Swal.fire('Thank you.', 'I will answer you as soon as possible')

        // Redirect
        window.location.href = "#header"

        return true
    }

    return false
}

export function show_error (error) {
    // Create alert
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: error,
    })
}

export function show_message (message) {
    // Create alert
    Swal.fire({
      icon: 'success',
      title: 'Listo',
      text: message,
    })
}

export function show_info (message) {
  // Create alert
  Swal.fire({
    icon: 'info',
    title: 'Importante',
    text: message,
  })
}

if (error) {
    show_error(error)
}

if (message) {
  show_message(message)
}

if (info) {
  show_info(info)
}