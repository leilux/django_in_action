
from django.conf.urls.defaults import *
from models import *
from views import *

urlpatterns = patterns('',

    (r'^product/create/$', create_product),
    (r'^product/list/$', list_product ),
    (r'^product/edit/(?P<id>[^/]+)/$', edit_product),
    (r'^product/view/(?P<id>[^/]+)/$', view_product),
    url(r'^store/$', store_view, name='store-view'),
    (r'cart/view/', view_cart),
    (r'cart/add/(?P<id>[^/]+)/$', add_to_cart),
    (r'cart/clean/', clean_cart),
# 
    (r'order/create/$', create_order),
    (r'order/list/$', list_order ),
    (r'order/edit/(?P<id>[^/]+)/$', edit_order),
    (r'order/view/(?P<id>[^/]+)/$', view_order),
#
    (r'^API/cart/$', REST4Cart.as_view()),
)

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)
