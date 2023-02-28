import {update_profile_card_small} from './profile-card-responsive.js'

// Update when load and resize
update_profile_card_small (start_small=true)
window.addEventListener('resize', () => update_profile_card_small(start_small=true))