export function update_form_redirect () {
    const url_current = window.location.href
    const url_base = url_current.split ("?")[0]
    const url_redirect = `${url_base}?thanks=true`
    const form_redirect_input = document.querySelector ("form #redirect")
    form_redirect_input.value = url_redirect
}
