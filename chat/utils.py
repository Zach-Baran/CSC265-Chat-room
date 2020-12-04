from django.utils.crypto import get_random_string
from django.http import JsonResponse


def create_token():
    token = get_random_string(length=6)
    return token

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': self.object.content,
                'author' : self.object.author.username,
                'date' : self.object.date
            }
            return JsonResponse(data)
        else:
            return response