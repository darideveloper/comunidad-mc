// Change class of title elemns inside horizontal profile card
const titles_card = document.querySelectorAll (".profile-card.horizontal .point .title-card ")
titles_card.forEach (title_card => {
  title_card.classList.remove ("title-card")
})