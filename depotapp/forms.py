#coding: utf-8
from django import forms
from models import *


ends = lambda s, suffixs: any(map(lambda x: s.endswith(x), suffixs))

class ProductForm(forms.ModelForm):
	
    class Meta:
        exclude = ['orders',]
        model = Product	
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    #title = forms.CharField(label='chage') 
    #price = forms.ChoiceField(widget=forms.widgets.RadioSelect, choices=((39, 39),
    #    (49, 49),
    #    (29.5, 29.5)))
    title = forms.CharField(initial=('一生的性计划',))
    titledict = dict([('一生的性计划','一生的性计划'),
                      ('黑客与画家','黑客与画家'),
                      ('第七天','第七天')])
    title.widget = forms.widgets.CheckboxSelectMultiple(choices=titledict.items())
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        #t=u"[u'\\u4e00\\u751f\\u7684\\u6027\\u8ba1\\u5212', u'\\u9ed1\\u5ba2\\u4e0e\\u753b\\u5bb6']"
        t = self.cleaned_data['title']
        if isinstance(t, tuple): return t
        title = [i[2:-1] for i in t[1:-1].split(', ')]
        return u', '.join(title).decode('unicode_escape')

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

