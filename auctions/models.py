from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, blank=False, null=False)
    
    
class State(models.Model):
    state_name = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.state_name}"
    

class AuctionListing(models.Model):
    listingTitle = models.CharField(max_length=32)
    listingDescription = models.TextField(max_length=512)
    listingImage = models.ImageField(upload_to='imgs')
    initialPrice =  models.FloatField(max_length=64, validators=[MinValueValidator(0)])
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    watchlisted = models.ManyToManyField(User, blank=True, related_name="watchlisted")
    isActive = models.BooleanField(default=True)
    listingState = models.ForeignKey(State, on_delete=models.CASCADE, related_name="listings", blank=False, default='New')
    listingDate = models.DateTimeField(auto_now_add=True)
    listingUpdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.listingTitle} from {self.creator} | Active: {self.isActive}"


class Bid(models.Model):
    bidValue = models.FloatField(max_length=64)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="currentBids")
    bidDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Value: {self.bidValue} Listing: {self.listing} User: {self.participant}"


class Comment(models.Model):
    addedComment = models.TextField(max_length=250, blank=False)
    commentedListing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented")
    commentDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment from {self.commenter} on {self.commentedListing}"
    
    
class Category(models.Model):
    name = models.CharField(max_length=32)
    related = models.ManyToManyField(AuctionListing, blank=True, related_name="relatedCategories")
    def __str__(self):
        return f"{self.name}"
    
    
   