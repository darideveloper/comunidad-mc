function activate_withdraw_button() {
  const select = document.querySelector("form select")
  const button = document.querySelector("form .btn")

  select.addEventListener ("change", (e) => {
    if (e.target.value == "") {
      button.disabled = true
    } else {
      button.disabled = false
    }
  })
}

activate_withdraw_button ()