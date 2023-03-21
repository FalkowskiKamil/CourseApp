from django.shortcuts import render, get_object_or_404
from .models import Airport, Passager, Flight

# Create your views here.
def index(request):
    context = {
        "airport": Airport.objects.all(),
        "passager":Passager.objects.all(),
        "flight":Flight.objects.all(),
        }
    return render(request, template_name="airline/main.html", context=context)

def passager(request, passager_id):
    passager ={"passager": get_object_or_404(Passager, pk=passager_id)}
    return render(request, template_name="airline/passager.html", context=passager)