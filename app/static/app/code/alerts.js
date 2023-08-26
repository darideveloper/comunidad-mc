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

export function show_details_point (title, details) {
  // Create alert
  Swal.fire({
    icon: 'error',
    title: title,
    text: details,
    showDenyButton: true,
    confirmButtonText: 'Ok',
    denyButtonText: `Abrir un ticket`,
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isDenied) {
      Swal.fire({
        icon: 'info',
        title: 'Importante',
        html: "<b>Para abrir un ticket</b>, en caso de que comentaras correctamente en el stream, o no reconozcas los puntos negativos, deberás contar con <b>capturas de pantalla.</b> <br><br> Si abres el ticket pero <b>no tienes capturas</b>, se te penalizará con <b>20 puntos</b>",
        showDenyButton: true,
        confirmButtonText: 'No tengo capturas',
        denyButtonText: 'Sí tengo capturas, abrir ticket',
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isDenied) {
          window.open("https://discord.gg/yCAGQ8wQ55", '_blank');
        }
      })
    }
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