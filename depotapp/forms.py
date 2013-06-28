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
    # type: radio
    price = forms.DecimalField()
    price.widget = forms.widgets.RadioSelect(
            choices=((39, 39), (49, 49), (29.5, 29.5)))
    # type: checkbox
    title = forms.CharField(initial=('一生的性计划',))
    title.widget = forms.widgets.CheckboxSelectMultiple(
            choices=[('一生的性计划','一生的性计划'),
                      ('黑客与画家','黑客与画家'),
                      ('第七天','第七天')])
    # type: select
    date_available = forms.DateTimeField(initial='2013-6-1')
    date_available.widget = forms.widgets.Select(
            choices=(('2012-1-1', '2012-1-1'),
                     ('2013-6-1', '2013-6-1'),
                     ('2013-12-1', '2013-12-1')))

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


class UploadForm(forms.Form):
    # type: file
    f = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)

    def clean_f(self):
        f = self.cleaned_data['f']
        suffixs = ['.scm', '.png', '.jpg', '.gif', '.txt']
        if not ends(f.name, suffixs):
            raise forms.ValidationError(
                    'you can upload file endswith:%s'%str(suffixs))
        return f

