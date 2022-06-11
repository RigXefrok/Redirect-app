
# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import View, ListView

from redirect.models import Redirect
from django.core.cache import cache


class RedirectsView(ListView):
    queryset = Redirect.objects.all()
    context_object_name = "redirects"


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        redirect_key = kwargs['key']

        if cache.get(redirect_key):
            redirect = cache.get(redirect_key)
            response_data = {'key': redirect_key, 'url': redirect['url']}
            return JsonResponse(response_data)
        return JsonResponse({'error': 'no data'})
