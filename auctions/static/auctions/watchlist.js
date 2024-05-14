import { getCookie } from "./utils.js";


document.addEventListener('DOMContentLoaded', function(){

    // Add a button to each listing in the watchlist that allows user to remove it
    document.querySelectorAll('.watchlist-btn').forEach((button) => {button.addEventListener('click', watchlistAction)});
});


function watchlistAction(event) {
    
    const csrftoken = getCookie('csrftoken');
    let currentBtn = event.currentTarget
    const listingID = currentBtn.dataset.listing_id;
    const action = currentBtn.dataset.watchlist_action

    fetch(`/watchlist_action/${listingID}`,{
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({watchlist_action: action})
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            let cardContainer = currentBtn.closest('.card-anim');
            cardContainer.style.animationPlayState = 'running';
            cardContainer.addEventListener('animationend', () => {
                cardContainer.remove();
            });
            document.querySelector('#watchlist-count').innerHTML = `(${result.items_number})`;
        }
        else {
            console.log('Invalid');
        }
    });
    return false;
}