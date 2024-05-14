import { getCookie } from "./utils.js";

document.addEventListener('DOMContentLoaded', function(){

    // Close or open the auction from the listing bids page
    
    const changeAuctionBtn = document.querySelector('#change-auction-btn');
    
    if (changeAuctionBtn) {
        changeAuctionBtn.onclick = changeAuctionState;
    } 

});


function changeAuctionState(event) {
    const listingID = document.querySelector('#listing-id').dataset['listing_id'];
    const csrftoken = getCookie('csrftoken');
    let currentBtn = event.currentTarget;
    const action = currentBtn.dataset.action;
    console.log(currentBtn);

    fetch(`/change_auction/${listingID}`,{
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({action: action})
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            const listingStatus = document.querySelector('#listing-status')
            if (action == 'close') {
                currentBtn.className = 'mb-3 mt-3 btn btn-info';
                currentBtn.innerHTML = 'Open Auction';
                currentBtn.dataset.action = 'open';
                listingStatus.style.color = 'darkred'
                listingStatus.innerHTML = 'Closed'
            }
            else {
                currentBtn.className = 'mb-3 mt-3 btn btn-warning';
                currentBtn.innerHTML = 'Close Auction';
                currentBtn.dataset.action = 'close';
                listingStatus.style.color = 'darkgreen'
                listingStatus.innerHTML = 'Active'
            }
        }
        else {
            console.log('Invalid')
        }
    });
    return false;
}


