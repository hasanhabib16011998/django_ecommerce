from django import forms
from .models import *

class ProductSearchForms(forms.Form):
    query=forms.CharField(label='Search Product',max_length=100,required=False)
    catagory=forms.ModelChoiceField(queryset=Catagory.objects.all(),empty_label='All Catagories',required=False)
    SubCatagory=forms.ModelChoiceField(queryset=SubCatagory.objects.all(),empty_label='All Sub Catagories',required=False)
    size=forms.ModelChoiceField(queryset=Size.objects.all(),empty_label='All Sizes',required=False)
    color=forms.ModelChoiceField(queryset=Color.objects.all(),empty_label='All Color',required=False)
    condition=forms.ModelChoiceField(queryset=Condition.objects.all(),empty_label='All Conditions',required=False)