"use strict";

function update_profile_card_small() {
  // Manage small layut for horizontal profile card
  var profile_card_small = document.querySelector('.profile-card.horizontal'); // Remove daily points in medium layout

  if (window.matchMedia("(max-width: 950px)").matches) {
    profile_card_small.classList.remove('small');
  } else {
    profile_card_small.classList.add('small');
  } // Show daily points in small layout


  if (window.matchMedia("(max-width: 500px)").matches) {
    profile_card_small.classList.add('small');
  }
} // Update when load and resize


update_profile_card_small();
window.addEventListener('resize', update_profile_card_small);