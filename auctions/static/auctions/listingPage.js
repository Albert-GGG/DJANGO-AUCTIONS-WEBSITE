import { getCookie } from "./utils.js";

document.addEventListener('DOMContentLoaded', function(){

    // Depending on the user and the user's session add the functionalities of closing or opening an auction,
    // adding or removing an item from the watchlist, adding a comment and placing a bid.
    const bidForm = document.querySelector('#new-bid-form');
    const commentForm = document.querySelector('#new-comment-form');
    const changeAuctionBtn = document.querySelector('#change-auction-btn');
    const WatchlistBtn = document.querySelector('#watchlist-btn');
    
    if (bidForm) {
        bidForm.onsubmit = submitBid;
    }

    if (commentForm) {
        commentForm.onsubmit = submitComment;
    } 

    if (changeAuctionBtn) {
        changeAuctionBtn.onclick = changeAuctionState;
    } 

    if (WatchlistBtn) {
        WatchlistBtn.onclick = watchlistAction;
    }

});


// For each one of the following functionalities, a fetch request is sent to the server, and according to the
// response, the content of the page changes.

function submitComment() {
    const commentField = document.querySelector('#id_addedComment');
    const listingd = document.querySelector('#listing-id').dataset['listing_id'];
    const csrftoken = getCookie('csrftoken');
    const bidMessage = document.querySelector('#comment-message');

    fetch(`/add_comment/${listingd}`,{
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: new FormData(document.querySelector('#new-comment-form'))
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            commentField.value = '';
            bidMessage.style.color = 'green';
            bidMessage.style.display = 'block';
            bidMessage.innerHTML = "Comment added succesfully!";
        }
        else {
            bidMessage.style.color = 'red';
            bidMessage.style.display = 'block';
            bidMessage.innerHTML = "Invalid comment";
        }
    });
    return false;
}


function submitBid() {
    const listingID = document.querySelector('#listing-id').dataset['listing_id']
    const csrftoken = getCookie('csrftoken');
    const newInput = document.querySelector('#id_new_bid');
    const bidMessage = document.querySelector('#bid-message');
    
    fetch(`/submit_bid/${listingID}`,{
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            new_bid: newInput.value
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            let newValue = result.new_min_bid;
            newInput.placeholder = Number(newValue);
            newInput.value = '';
            newInput.min = Number(newValue);
            document.querySelector('#strong-price').innerHTML = '$' + newValue;
            bidMessage.style.color = 'green';
            bidMessage.style.display = 'block';
            bidMessage.innerHTML = "Bid placed successfully!";
        }
        else {
            if (result.new_min_bid) {
                let newValue = result.new_min_bid;
                newInput.placeholder = Number(newValue);
                newInput.value = '';
                newInput.min = Number(newValue);
                document.querySelector('#strong-price').innerHTML = '$' + newValue;
                bidMessage.style.color = 'red';
                bidMessage.style.display = 'block';
                bidMessage.innerHTML = `Bid not placed. Current bid is $${newValue}`;
            }
            else {
                newInput.value = '';
                bidMessage.style.color = 'red';
                bidMessage.style.display = 'block';
                bidMessage.innerHTML = result.errors;
            }
        }
        
    });
    return false;
}


function changeAuctionState(event) {
    const listingID = document.querySelector('#listing-id').dataset['listing_id'];
    const csrftoken = getCookie('csrftoken');
    let currentBtn = event.currentTarget
    const action = currentBtn.dataset.action
    console.log(currentBtn)

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
                currentBtn.className = 'mb-3 btn btn-info w-100';
                currentBtn.innerHTML = 'Open Auction';
                currentBtn.dataset.action = 'open';
                listingStatus.style.color = 'darkred'
                listingStatus.innerHTML = 'No Longer Active'
            }
            else {
                currentBtn.className = 'mb-3 btn btn-warning w-100';
                currentBtn.innerHTML = 'Close Auction';
                currentBtn.dataset.action = 'close';
                listingStatus.style.color = 'darkblue'
                listingStatus.innerHTML = 'Active'
            }
        }
        else {
            console.log('Invalid')
        }
    });
    return false;
}


function watchlistAction(event) {
    const listingID = document.querySelector('#listing-id').dataset['listing_id'];
    const csrftoken = getCookie('csrftoken');
    let currentBtn = event.currentTarget
    const action = currentBtn.dataset.watchlist_action

    fetch(`/watchlist_action/${listingID}`,{
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({watchlist_action: action})
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            if (action == 'remove') {
                currentBtn.className = 'btn btn-success mb-3 w-100';
                currentBtn.innerHTML = 'Add to Watchlist';
                currentBtn.dataset.watchlist_action = 'add';
            }
            else {
                currentBtn.className = 'btn btn-outline-danger mb-3 w-100';
                currentBtn.innerHTML = 'Remove From Watchlist';
                currentBtn.dataset.watchlist_action = 'remove';
            }
            document.querySelector('#watchlist-count').innerHTML = `(${result.items_number})`;
        }
        else {
            console.log('Invalid')
        }
    });
    return false;
}