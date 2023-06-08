// get referral elemnt
const referral_elem = document.querySelector('.referral span')
console.log (referral_elem)

if (referral_elem) {
  referral_elem.addEventListener('click', function() {
    console.log ("Referral link copied!")

    // Get referral link
    const referral_link = referral_elem.innerHTML

    // Copy referral link to clipboard
    navigator.clipboard.writeText(referral_link)

    // Show alert
    Swal.fire('Enlace copiado!')

  })
}