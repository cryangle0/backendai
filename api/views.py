from django.http import HttpResponse


def example_view(request):
    return HttpResponse("hello world!")
