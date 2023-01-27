"use strict";

var _alerts = require("./alerts.js");

var copy_buttons = document.querySelectorAll(".btn.cta.copy");
copy_buttons.forEach(function (button) {
  // Add event listener to each button
  button.addEventListener("click", function (event) {
    // Copy user to clipboard
    var copy_text = button.parentNode.querySelector("p.name").innerText;
    navigator.clipboard.writeText(copy_text); // Show alert

    (0, _alerts.show_message)("Nombre de usuario copiado al portapapeles.");
  });
});