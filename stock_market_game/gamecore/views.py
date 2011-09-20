# Create your views here.
from django.shortcuts import render_to_response
from gamecore.models import GEvent, MenuItem

def sales(request):
	"""List of all sale events """
	sales=GEvent.objects.filter(e_type="sale")
	menu_items=MenuItem.objects.all()
	return render_to_response('sales_list.html', {'sales':sales, 'menu_items':menu_items})
