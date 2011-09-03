# Create your views here.
from django.shortcuts import render_to_response
from gamecore.models import GEvent

def sales(request):
	"""List of all sale events """
	sales=GEvent.objects.filter(e_type="sale")
	return render_to_response('sales_list.html', {'sales':sales})
