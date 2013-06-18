
from django import forms
from models import *


ends = lambda s, suffixs: any(map(lambda x: s.endswith(x), suffixs))

class ProductForm(forms.ModelForm):
	
    class Meta:
        model = Product	
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('price must > 0')
        return price

    def clean_image_url(self):
        url = self.cleaned_data['image_url']
        suffixs = ['.jpg', '.png', '.gif']
        if not ends(url, suffixs):
            raise forms.ValidationError('img must %s' % str(suffixs))
        return url


class OrderForm(forms.ModelForm):
	
    class Meta:
        model = Order	
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

