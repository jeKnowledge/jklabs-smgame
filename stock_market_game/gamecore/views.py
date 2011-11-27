# Create your views here.
from django.shortcuts import render_to_response
from gamecore.models import Proposal, MenuItem, Company, Investment, GEvent, TradeForm, EventComment, CommentForm
from playerinfo.models import UserCredit

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext


from datetime import date, timedelta, datetime


def trading(request):
	"""List of all sale events """
	proposals=Proposal.objects.all()
	menu_items=MenuItem.objects.all()
	#for item in sales:
	#	print item.e_from.username
	day=timedelta(days=1)
	today=date.today()
	yesterdays=GEvent.objects.filter(event_date=(today-day))
	todays=GEvent.objects.filter(event_date=today)
	
	values_list=generate_diference(todays, yesterdays)
	
	form = TradeForm()
	return render_to_response('trade.html', {'proposals':proposals, 'menu_items':menu_items,'form':form, 'values_list':values_list},context_instance=RequestContext(request))

def proposal_view(request, prop_id):

	actual_pro=Proposal.objects.get(id=int(prop_id))
	menu_items=MenuItem.objects.all()
	return render_to_response('proposal.html', {'actual_pro':actual_pro, 'menu_items':menu_items})
	
@login_required
def buy(request, prop_id):
	#attention it is still need to remove the investment from the other
	#player, and is still needed to study the case where one user buys shares
	#of the same company in diferent times/values
	if request.method == "POST":
		form = TradeForm(request.POST)
		if form.is_valid():
			nshares=form.cleaned_data['shares']
			svalue=form.cleaned_data['value']
			proposal=Proposal.objects.get(id=int(prop_id))
			menu_items=MenuItem.objects.all()
			
			if request.user.username == proposal.player_from.username:
				return render_to_response('cannot.html', {'menu_items':menu_items})
			
			if proposal.shares < nshares:
				return render_to_response('cannot.html', {'menu_items':menu_items})
			
			if proposal.p_type == 'sell':
				if proposal.per_share > svalue:
					return render_to_response('cannot.html', {'menu_items':menu_items})
				ucredits=UserCredit.objects.get(user=request.user)
				if ucredits.current_credits < nshares*svalue:
					return render_to_response('cannot.html', {'menu_items':menu_items})
				
				invest=Investment(owner=request.user,of_company=proposal.company,n_shares=nshares, initial_value=svalue)
				invest.save()
				ucredits.debit(nshares*svalue)
				ucredits.save()
				tocredits=UserCredit.objects.get(user=proposal.player_from)
				tocredits.credit(nshares*svalue)
				tocredits.save()
				new_event=GEvent(e_type='trade',player_from=proposal.player_from,player_to=request.user,company=proposal.company,amount_of_shares=nshares, total_credits=nshares*svalue, event_date=date.today())
				new_event.save()	
				
				if proposal.player_from.username != 'Market':
					todecrement=Investment.objects.get(owner=proposal.player_from, of_company=proposal.company)
					todecrement.n_shares-=nshares
					if todecrement.n_shares == 0:
						todecrement.delete()
					else:
						todecrement.save()
				
			elif proposal.p_type== 'buy':
				if proposal.per_share < svalue:
					return render_to_response('cannot.html', {'menu_items':menu_items})
				ucredits=UserCredit.objects.get(user=proposal.player_from)
				if ucredits.current_credits < nshares*svalue:
					return render_to_response('cannot.html', {'menu_items':menu_items})
				
				invest=Investment(owner=proposal.player_from,of_company=proposal.company,n_shares=nshares, initial_value=svalue)
				invest.save()
				ucredits.debit(nshares*svalue)
				ucredits.save()
				tocredits=UserCredit.objects.get(user=request.user)
				tocredits.credit(nshares*svalue)
				tocredits.save()
				new_event=GEvent(e_type='trade',player_from=request.user,player_to=proposal.player_from,company=proposal.company,amount_of_shares=nshares, total_credits=nshares*svalue, event_date=date.today())
				new_event.save()
				
				todecrement=Investment.objects.get(owner=request.user, company=proposal.company)
				todecrement.n_shares-=nshares
				if todecrement.n_shares == 0:
					todecrement.delete()
				else:
					todecrement.save()
			
			if proposal.shares==nshares:
				proposal.delete()
			else:
				proposal.shares = proposal.shares - nshares;
				proposal.save()
			
			return render_to_response('success.html', {'menu_items':menu_items})

@login_required	
def wallet(request):
	day=timedelta(days=1)
	today=date.today()
	yesterdays=GEvent.objects.filter(event_date=(today-day))
	todays=GEvent.objects.filter(event_date=today)
	
	values_list=invest_changes(todays, yesterdays, request.user)
	
	menu_items=MenuItem.objects.all()
	userinvest=Investment.objects.filter(owner=request.user)
	form=TradeForm()
	return render_to_response('wallet.html', {'menu_items':menu_items, 'userinvest':userinvest, 'form':form, 'values_list':values_list}, context_instance=RequestContext(request))
	

def addproposal(request, invest_id):
	if request.method == 'POST': # If the form has been submitted...
		form = TradeForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			"""Falta Verificar se as propostas de venda ja ultrapassam o investimento total do utilizador"""
			invest=Investment.objects.get(id=int(invest_id))
			n_shares=form.cleaned_data['shares']
			svalue=form.cleaned_data['value']
			prop_company=invest.of_company
			new_prop = Proposal(p_type='sell', shares=n_shares, per_share=svalue, player_from=request.user, company=prop_company)
			new_prop.save()
			return HttpResponseRedirect('trading')
	else:
		menu_items=MenuItem.objects.all()
		return render_to_response('cannot.html', {'menu_items':menu_items})


def eventdetails(request, event_id):
	if request.method == 'POST': # If the form has been submitted...
		form = CommentForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			comment_content=form.cleaned_data['content']
			now=datetime.now()
			event_to_comment=GEvent.objects.get(id=int(event_id))
			newcomment=EventComment(author=request.user, posted=now, event=event_to_comment, content=comment_content)
			newcomment.save()
			
	event_data=GEvent.objects.get(id=int(event_id))
	comments=EventComment.objects.filter(event=event_data)
	menu_items=MenuItem.objects.all()
	form=CommentForm()
	return render_to_response('event.html',{'event_data':event_data, 'comments':comments, 'menu_items':menu_items, 'form':form}, context_instance=RequestContext(request) )

#Auxiliar functions
def generate_diference(todays, yesterday):
	if not todays or not yesterday:
		return []
	
	companies=Company.objects.all()
	values_dic={}
	values_list=[]
	for item in companies:
		values_dic[item.name]=[0,0,0,0]
	
	## Atention this may need another counting aproach
	for item in yesterday:
		values_dic[item.company.name][0]+=item.total_credits/item.amount_of_shares
		values_dic[item.company.name][1]+=1
	
	for item in todays:
		values_dic[item.company.name][2]+=item.total_credits/item.amount_of_shares
		values_dic[item.company.name][3]+=1
		
	for comp, list in values_dic.iteritems():
		values_list.append([comp, list[0]/list[1], list[2]/list[3], (list[2]/list[3])-(list[0]/list[1])])
	
	return values_list
	
def invest_changes(todays, yesterdays, user):
	if not todays or not yesterdays:
		return []
	
	companies=[]
	
	invests=Investment.objects.filter(owner=user)
	
	values_dic={}
	values_list=[]
	
	for invest in invests:
		values_dic[invest.of_company.name]=[0,0,0,0,invest.initial_value]
	
	## Atention this may need another counting aproach
	for item in yesterday:
		if item.company.name in values_dic:
			values_dic[item.company.name][0]+=item.total_credits/item.amount_of_shares
			values_dic[item.company.name][1]+=1
	
	for item in todays:
		if item.company.name in values_dic:
			values_dic[item.company.name][2]+=item.total_credits/item.amount_of_shares
			values_dic[item.company.name][3]+=1
		
	for comp, list in values_dic.iteritems():
		values_list.append([comp, list[0]/list[1], list[2]/list[3], (list[2]/list[3])-(list[0]/list[1]), list[5], (list[2]/list[3])-list[5]])
	
	return values_list
	
