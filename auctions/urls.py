from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_page, name="listing_page"),
    path("submit_bid/<int:listing_id>", views.submit_bid, name="submit_bid"),
    path("change_auction/<int:listing_id>", views.change_auction_state, name="change_auction"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_action/<int:listing_id>", views.watchlist_action, name="watchlist_action"),
    path("categories", views.load_categories, name="load_categories"),
    path("category/<int:category_id>", views.search_categories, name="search_categories"),
    path("user_listings", views.user_listings, name="user_listings"),
    path("bid_history/<int:listing_id>", views.bid_history, name="history"),
    path("user_bids", views.user_bids, name="user_bids"),
    path("search", views.search, name="search")

]
