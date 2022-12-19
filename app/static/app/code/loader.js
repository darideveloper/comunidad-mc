import {show_alert} from './alerts.js'
import {update_form_redirect} from './contact_form.js'

function sleep(s) {
    // Wait specific seconds
    return new Promise(resolve => setTimeout(resolve, s*1000));
}

window.onload = async function () {
    // Show alerts and update contact form
    const thanks_altert = show_alert()
    update_form_redirect ()
}

window.onresize = function() {
    console.log ("Resize")
}