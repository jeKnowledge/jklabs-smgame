# Create your views here.
from django.shortcuts import render_to_response
from gamecore.models import Proposal, MenuItem, Company, Investment, GEvent
from playerinfo.models import UserCredit

from django.contrib.auth.decorators import login_required


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
	
@login_required
def buy(request, prop_id):
	proposal=Proposal.objects.get(id=int(prop_id))
	menu_items=MenuItem.objects.all()
	if request.user.username == proposal.player_from.username:
		return render_to_response('cannot.html', {'menu_items':menu_items})
	
	ucredits=UserCredit.objects.get(user=request.user)
	if ucredits.current_credits < proposal.shares*proposal.company.share_value:
		return render_to_response('cannot.html', {'menu_items':menu_items})
	
	invest=Investment(owner=request.user,of_company=proposal.company,n_shares=proposal.shares, initial_value=proposal.company.share_value)
	invest.save()
	
	ucredits.debit(proposal.shares*proposal.company.share_value)
	ucredits.save()

	new_event=GEvent(e_type='trade',player_from=proposal.player_from,player_to=request.user,company=proposal.company,amount_of_shares=proposal.shares, total_credits=proposal.shares*proposal.company.share_value)
	new_event.save()
	
	proposal.delete()
	return render_to_response('success.html', {'menu_items':menu_items})
@login_required	
def wallet(request):
	menu_items=MenuItem.objects.all()
	userinvest=Investment.objects.filter(owner=request.user)
	return render_to_response('wallet.html', {'menu_items':menu_items, 'userinvest':userinvest})
	
	
	
	
