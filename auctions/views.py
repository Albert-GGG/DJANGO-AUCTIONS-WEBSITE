from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json


# Import models and forms
from .models import User, AuctionListing, Bid, Category, Comment
from .forms import NewListingForm, UserForm, BidForm, CommentForm

# Listings to be shown per page
ELEMENTS_PER_PAGE = 5


# View that renders the index page which displays the active listings
def index(request):
    active_listings = AuctionListing.objects.filter(isActive=True).all().order_by('-listingDate')
    listings = validate_page(request.GET.get("page"), active_listings)
    return render(request, "auctions/index.html", {"listings": listings, "title": 'Latest Listings'})


# Validates page number based on the paginator bounds (Takes ELEMENTS_PER_PAGE as the number of elements per page)
def validate_page(num_page, elements_set):
    elements_paginator = Paginator(elements_set, ELEMENTS_PER_PAGE)
    if num_page:
        try:
            num_page = int(num_page)
            if num_page > elements_paginator.page_range[-1]:
                num_page = elements_paginator.page_range[-1]
            elif num_page <= 0:
                num_page = 1
        except:
            num_page = 1
    else:
        num_page = 1
        
    return elements_paginator.page(num_page)
        
        
# View that renders the login page and validates user's info
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# View that logs user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# View that renders the registration page and validates data to create a new account
def register(request):
    if request.method == "POST":
        new_user_form = UserForm(request.POST)
        if new_user_form.is_valid():
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/register.html", {
                "new_user_form": new_user_form
            })
            
    else:
        new_user_form = UserForm()
        return render(request, "auctions/register.html", {"new_user_form": new_user_form})


# View that renders the page for adding a new listing and validates the data
@login_required(login_url='login')
def create_listing(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['listingTitle']
            description = form.cleaned_data['listingDescription']
            listingImage = form.cleaned_data['listingImage']
            state = form.cleaned_data['listingState']
            initialPrice = form.cleaned_data['initialPrice']
            creator = User.objects.get(pk=int(request.user.id))
            newListing = AuctionListing(
                listingTitle=title, listingDescription=description, listingImage=listingImage, 
                listingState=state, initialPrice=initialPrice, creator=creator)
            newListing.save()
             
            for cat in form.cleaned_data['categories']:
                listing = AuctionListing.objects.get(pk=int(newListing.pk))
                category = Category.objects.get(pk=int(cat))
                category.related.add(listing)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    else:
        form = NewListingForm()
        return render(request, "auctions/create_listing.html", {
            "form": form
        })
    

# View that renders the page that displays all the information related to a listing
def listing_page(request, listing_id):
    listing = AuctionListing.objects.get(pk=int(listing_id))
    if listing.bids.count() > 0:
        min_value = listing.bids.last().bidValue
    else:
        min_value = listing.initialPrice
        
    comment_form = CommentForm()
    bid_form = BidForm(min_value=min_value)

    return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "bid_form": bid_form,
            "comment_form": comment_form
    })
        
      
# View that validates the bid wanted to be placed by the user   
def submit_bid(request, listing_id):
    
    if request.method == 'POST':
        listing = AuctionListing.objects.get(pk=int(listing_id))
        if listing.bids.count() > 0:
            min_value = listing.bids.last().bidValue
        else:
            min_value = listing.initialPrice
            
        data = json.loads(request.body)
        try:
            new_bid = float(data.get('new_bid'))
        except:
            return JsonResponse({"error": "Invalid bid"}, status=400)   
        
        # If new bid is bigger than the current bid, update the value in the db and return the value to be displayed
        # Return current bid if user doesn't have current data.
        if new_bid > min_value:
            participant = User.objects.get(pk=int(request.user.id))
            new_listing_bid = Bid(bidValue=new_bid, listing=listing, participant=participant)
            new_listing_bid.save()       
            return JsonResponse({'success': True, 'new_min_bid': new_bid}, status=200)
        else:
            return JsonResponse({'success': False, 'new_min_bid': min_value}, status=400)
        
    return JsonResponse({"error": "Invalid request"}, status=400)        
        

# Close or open an auction only by the creator of the listing
@login_required(login_url='login')
def change_auction_state(request, listing_id):
    
    if request.method == 'POST':
        listing = AuctionListing.objects.get(pk=int(listing_id))
        data = json.loads(request.body)
        
        if request.user == listing.creator:
        
            if data.get('action') == 'open':
                listing.isActive = True
            elif data.get('action') == 'close':
                listing.isActive = False
            else:
                return JsonResponse({"error": "Invalid action"}, status=400)
            
            listing.save()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({"error": "Unauthorized"}, status=401)
    
    else:
        return JsonResponse({"error": "Invalid request"}, status=405)  


# Add or remove an item from the wathlist
@login_required(login_url='login')    
def watchlist_action(request, listing_id):
    user = User.objects.get(pk=(request.user.id))
    listing = AuctionListing.objects.get(pk=int(listing_id))
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        if data.get('watchlist_action') == 'add':
            listing.watchlisted.add(user)
        elif data.get('watchlist_action') == 'remove':
            listing.watchlisted.remove(user)
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)
        
        return JsonResponse({'success': True, 'items_number': user.watchlisted.count()}, status=200)
    
    # User was not logged in and added the item through a GET request
    else:
        listing.watchlisted.add(user)
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
     
     
# View that renders the user's watchlist
@login_required(login_url='login')
def watchlist(request):
    user = User.objects.get(pk=(request.user.id))
    user_watchlist = user.watchlisted.all
    return render(request, "auctions/watchlist.html", {
        "user_watchlist": user_watchlist
    })


# View that adds a comment to a listing
@login_required(login_url='login')
def add_comment(request, listing_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data['addedComment']
            listing = AuctionListing.objects.get(pk=int(listing_id))
            user = User.objects.get(pk=(request.user.id))
            new_comment = Comment(commenter=user, commentedListing=listing, addedComment=comment)
            new_comment.save()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': False}, status=403)
            
    return JsonResponse({"error": "Invalid request"}, status=400)   
        
        
# View that renders the 'search by category' page
def load_categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, "auctions/categories.html", {
        'categories': categories
    })


# View that renders the page that displays all the listings for a category
def search_categories(request, category_id):
    category = Category.objects.get(pk=category_id)
    categ_listings = AuctionListing.objects.filter(relatedCategories=category).all().order_by('-listingDate')
    listings = validate_page(request.GET.get('page'), categ_listings)
    
    return render(request, "auctions/index.html", {
        'listings': listings,
        'title': f'All Listings of {category.name}'
    })


# View that renders all the listings added by a user
@login_required(login_url='login')
def user_listings(request):
    user = User.objects.get(pk=(request.user.id))
    user_listings = user.created.all().order_by('-listingDate')
    return render(request, "auctions/user_listings.html", {
        "user_listings": user_listings
    })
    
    
# View that allows the creator of a listing to see the bid history of an item
@login_required(login_url='login')
def bid_history(request, listing_id):
    user = User.objects.get(pk=(request.user.id))
    listing = AuctionListing.objects.get(pk=int(listing_id))
    if user != listing.creator:
        return HttpResponse("<h3>Unauthorized</h3>")
    else:
        return render(request, "auctions/listing_bids.html", {
            "listing": listing
        })
        

# View that renders all the bids placed by the user
@login_required(login_url='login')
def user_bids(request):
    user = User.objects.get(pk=(request.user.id))
    user_bids = user.currentBids.all()
    user_bid_listings = AuctionListing.objects.filter(bids__in=user_bids).distinct()
    
    return render(request, "auctions/user_bids.html", {
        "user_bid_listings": user_bid_listings
    })
        
        
# View that shows all the listings when the user uses the searchbar
def search(request):
    subs = request.GET.get('search')
    subs = subs.strip()
    if not subs:
        return HttpResponseRedirect(reverse('index'))
    
    searched_listings = AuctionListing.objects.filter(listingTitle__contains=subs)
    listings = validate_page(request.GET.get("page"), searched_listings)
    
    response = render(request, "auctions/index.html", {
        "title": f'Results for "{subs}"',
        "listings": listings
    })
    
    return response