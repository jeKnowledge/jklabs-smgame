# Create your views here.
from django.shortcuts import render_to_response
from gamecore.models import Proposal, MenuItem

def trading(request):
	"""List of all sale events """
	proposals=Proposal.objects.all()
	menu_items=MenuItem.objects.all()
	#for item in sales:
	#	print item.e_from.username
	return render_to_response('trade.html', {'proposals':proposals, 'menu_items':menu_items})

def proposal_view(request, prop_id):

	actual_pro=Proposal.objects.get(id=int(prop_id))
	menu_items=MenuItem.objects.all()
	return render_to_response('proposal.html', {'actual_pro':actual_pro, 'menu_items':menu_items})
	
	
