from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from signup.models import UserProfile
from buyer.models import Item,sellerItems
from signup.models import seller



class addProductForm(forms.ModelForm):
    # Prod_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # Prod_id = forms.IntegerField(required=True, help_text='Optional.')
    # Prod_desp= forms.CharField(max_length=30, required=False, help_text='Optional.')
    # Price = forms.IntegerField(required=True)

    # Prod_img = forms.ImageField()
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # is_seller = forms.BooleanField(initial=True)


    class Meta:
        model = Item
        fields = ('title', 'price',  'slug','description','image')
    #def save():

class addSellerForm(forms.ModelForm):

    class Meta:
        model = seller
        fields = ('pdf',)
        # exclude = ('user',)

class item_to_sellerform(forms.ModelForm):
    class Meta:
        model = sellerItems
        fields = ('seller','item')

class update_user_address(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address',)