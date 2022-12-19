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

if (error) {
    show_error(error)
}