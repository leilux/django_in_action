from django.contrib.auth import authenticate, login, logout
from depotapp.views import list_product, store_view
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext

def login_view(request):
    user = authenticate(username=request.POST.get('username'),
                        password=request.POST.get('password'))
    if user:
        login(request, user)
        url = request.POST.get('next')
        return HttpResponseRedirect(url or '/depotapp/store/')
    else:
        # get ?next=url
        next_url = request.GET.get('next', '')
        t = get_template('login.html')
        c = RequestContext(request, locals())
        return HttpResponse(t.render(c))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/depotapp/store/')

