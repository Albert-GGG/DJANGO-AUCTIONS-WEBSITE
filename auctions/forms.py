from django import forms
from django.core.exceptions import ValidationError
from .models import User, AuctionListing, Category, Comment


# Form for creating a new auction listing
class NewListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["listingTitle", "listingDescription", "listingImage", "listingState", "initialPrice"]
        labels = {
            "listingTitle": "Title",
            "listingDescription": "Description",
            "listingImage": "Image",
            "listingState": "State",
            "initialPrice": "Initial Price"
        }
        widgets = {'listingTitle': forms.TextInput(attrs={'class': 'form-control'}),
                   'listingDescription': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'spellcheck': 'false'}),
                   'listingImage': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                   'listingState': forms.Select(attrs={'class': 'form-select'}),
                   'initialPrice': forms.NumberInput(attrs={'class': 'form-control'})
                   }
    
    categories = forms.MultipleChoiceField(label="Categories", choices=Category.objects.values_list('id', 'name'), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    
    def clean_listingImage(self):
        image = self.cleaned_data.get('listingImage', False)
        if image:
            if image.size > 5*1024*1024:
                raise ValidationError("Image size must not be greater than 5mb")
            return image
        else:
            raise ValidationError("Image couldn't be read")


# Bid form which minimum value can be changed according to the current bid of the listing
class BidForm(forms.Form):
    new_bid = forms.FloatField(label="New Bid", min_value=0)

    def __init__(self, *args, **kwargs):
        min_value = kwargs.pop('min_value', None)  # Remove min_amount from kwargs and save it
        super().__init__(*args, **kwargs)

        if min_value:    
            self.fields['new_bid'] = forms.FloatField(
                label="New Bid", 
                min_value=min_value, 
                widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': min_value}))


# Form for new comments on the listings
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["addedComment"]
        labels = {"addedComment": "Add Comment"}
        widgets = {'addedComment': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}   
        
        
# Form used to register a new user
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {"username": "Username", 'password': "Password", 'email': "Email Address"}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'rows': '3'}),
                    'password': forms.PasswordInput(attrs={'class': 'form-control', 'rows': '3'}),
                    'email': forms.EmailInput(attrs={'class': 'form-control', 'rows': '3'})
                } 
        
    confirmation = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        
    def clean_confirmation(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirmation']:
            raise ValidationError("Passwords don't match")