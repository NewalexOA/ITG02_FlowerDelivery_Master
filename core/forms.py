from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Order, Product, Review

RATING_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone', 'address',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'address',)


class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['products', 'address', 'phone']


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = Review
        fields = ['rating', 'review']
