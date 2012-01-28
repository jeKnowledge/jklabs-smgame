# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from gamecore.models import Proposal, MenuItem, Company, Investment, GEvent, TradeForm, EventComment, CommentForm
from playerinfo.models import UserCredit

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext


from datetime import date, timedelta, datetime


def trading(request):
	"""
		Here every proposal with their form is listed. Stats are shown for
		current market activity
	"""
	#List menu items and sale proposals
	proposals=Proposal.objects.all()
	menu_items=MenuItem.objects.all()
	#for item in sales:
	#	print item.e_from.username
	day=timedelta(days=1)
	today=date.today()
	#Get the events for the stats
	yesterdays=GEvent.objects.filter(event_date=(today-day))
	todays=GEvent.objects.filter(event_date=today)
	#Calculate de stats
	values_list=generate_diference(todays, yesterdays)
	#Generate de form
	form = TradeForm()
	#render and send the reply
	return render_to_response('trade.html', {'proposals':proposals, 'menu_items':menu_items,'form':form, 'values_list':values_list},context_instance=RequestContext(request))

def proposal_view(request, prop_id):
	"""
		Renders the proposal details. [To Be removed]
	"""
	actual_pro=Proposal.objects.get(id=int(prop_id))
	menu_items=MenuItem.objects.all()
	return render_to_response('proposal.html', {'actual_pro':actual_pro, 'menu_items':menu_items}, context_instance=RequestContext(request))
	
@login_required
def buy(request, prop_id):
	"""
		This view processes the form of the proposals e validates a transaction in the game.
	"""
	#The method must be POST
	if request.method == "POST":
		#Introduce the data in a form object
		form = TradeForm(request.POST)
		if form.is_valid():
			nshares=form.cleaned_data['shares']
			svalue=form.cleaned_data['value']
			proposal=Proposal.objects.get(id=int(prop_id))
			menu_items=MenuItem.objects.all()

			# if the user is negociating with himself, stop here
			if request.user.username == proposal.player_from.username:
				return render_to_response('cannot.html', {'menu_items':menu_items}, context_instance=RequestContext(request))
			
			#if wants to trade more shares than the available in the proposal, stop here
			if proposal.shares < nshares:
				return render_to_response('cannot.html', {'menu_items':menu_items}, context_instance=RequestContext(request))
			

			if proposal.p_type == 'sell':
				#If the value per share ofered isn't bigger than the wanted , stop here
				if proposal.per_share > svalue:
					return render_to_response('cannot.html', {'menu_items':menu_items}, context_instance=RequestContext(request))
				ucredits=UserCredit.objects.get(user=request.user)

				#if the buyer don't have enough credits, stop here
				if ucredits.current_credits < nshares*svalue:
					return render_to_response('cannot.html', {'menu_items':menu_items}, context_instance=RequestContext(request))
				
				#Passed all tests now gonna add to an existing investment or create a new one
				invest=Investment.objects.get(owner=request.user, of_company=proposal.company)
				if invest:
					invest.initial_value=((invest.n_shares*invest.initial_value)+(nshares*svalue))/nshares+invest.n_shares
					invest.n_shares+=nshares
				else:
					invest=Investment(owner=request.user,of_company=proposal.company,n_shares=nshares, initial_value=svalue)

				#Save the investment, update the credits for each user and generate an event
				invest.save()
				ucredits.debit(nshares*svalue)
				ucredits.save()
				tocredits=UserCredit.objects.get(user=proposal.player_from)
				tocredits.credit(nshares*svalue)
				tocredits.save()
				new_event=GEvent(e_type='trade',player_from=proposal.player_from,player_to=request.user,company=proposal.company,amount_of_shares=nshares, total_credits=nshares*svalue, event_date=date.today())
				new_event.save()	
				
				#If the proposal isn't the first public sell of this shares , decrement the investment of the seller
				if proposal.player_from.username != 'Market':

					todecrement=Investment.objects.get(owner=proposal.player_from, of_company=proposal.company)
					todecrement.n_shares-=nshares
					if todecrement.n_shares == 0:
						todecrement.delete()
					else:
						todecrement.save()
				
			elif proposal.p_type== 'buy':
				#If the value per share ofered isn't bigger than the wanted , stop here
				if proposal.per_share < svalue:
					return render_to_response('cannot.html', {'menu_items':menu_items}, context_instance=RequestContext(request))
				ucredits=UserCredit.objects.get(user=proposal.player_from)
				
				#if the buyer don't have enough credits, stop here
				if ucredits.current_credits < nshares*svalue:
					return render_to_response('cannot.html', {'menu_items':menu_items},context_instance=RequestContext(request))

				#Passed all tests now gonna add to an existing investment or create a new one
				invest=Investment.objects.get(owner=proposal.player_from, of_company=proposal.company)
				if invest:
					invest.initial_value=((invest.n_shares*invest.initial_value)+(nshares*svalue))/nshares+invest.n_shares
					invest.n_shares+=nshares
				else:
					invest=Investment(owner=proposal.player_from,of_company=proposal.company,n_shares=nshares, initial_value=svalue)
				
				#Save the investment, update the credits for each user and generate an event
				invest.save()
				ucredits.debit(nshares*svalue)
				ucredits.save()
				tocredits=UserCredit.objects.get(user=request.user)
				tocredits.credit(nshares*svalue)
				tocredits.save()
				new_event=GEvent(e_type='trade',player_from=request.user,player_to=proposal.player_from,company=proposal.company,amount_of_shares=nshares, total_credits=nshares*svalue, event_date=date.today())
				new_event.save()
				
				#decrement the investment of the seller
				todecrement=Investment.objects.get(owner=request.user, company=proposal.company)
				todecrement.n_shares-=nshares
				if todecrement.n_shares == 0:
					todecrement.delete()
				else:
					todecrement.save()
			
			#Delete or update the proposal
			if proposal.shares==nshares:
				proposal.delete()
			else:
				proposal.shares = proposal.shares - nshares;
				proposal.save()
			
			return render_to_response('success.html', {'menu_items':menu_items}, context_instance=RequestContext(request))

@login_required	
def wallet(request):
	"""
		render the current user assets, and their market value
	"""
	day=timedelta(days=1)
	today=date.today()
	#fetch the needed events
	yesterdays=GEvent.objects.filter(event_date=(today-day))
	todays=GEvent.objects.filter(event_date=today)
	
	#generate the assets current stats
	values_list=invest_changes(todays, yesterdays, request.user)
	
	menu_items=MenuItem.objects.all()
	userinvest=Investment.objects.filter(owner=request.user)
	
	#Generate the sell form
	form=TradeForm()
	return render_to_response('wallet.html', {'menu_items':menu_items, 'userinvest':userinvest, 'form':form, 'values_list':values_list}, context_instance=RequestContext(request))
	

def addproposal(request, invest_id):
	"""
		this processes the form, and creates a proposal in the market
	"""
	if request.method == 'POST': # If the form has been submitted...
		form = TradeForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			"""Falta Verificar se as propostas de venda ja ultrapassam o investimento total do utilizador"""
			#get the form data and create a proposal
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
	"""
		Shows a specific event, and the users opinion about it
	"""
	#if the comment form has been submited
	if request.method == 'POST': # If the form has been submitted...
		form = CommentForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			#creates a new comment
			comment_content=form.cleaned_data['content']
			now=datetime.now()
			event_to_comment=GEvent.objects.get(id=int(event_id))
			newcomment=EventComment(author=request.user, posted=now, event=event_to_comment, content=comment_content)
			newcomment.save()
	
	#fetches the event data and other objects 	
	event_data=GEvent.objects.get(id=int(event_id))
	comments=EventComment.objects.filter(event=event_data)
	menu_items=MenuItem.objects.all()
	#creates a form 
	form=CommentForm()
	return render_to_response('event.html',{'event_data':event_data, 'comments':comments, 'menu_items':menu_items, 'form':form}, context_instance=RequestContext(request) )

def companypage(request, company_id):
	"""
		Shows the company information
	"""
	institution=Company.objects.get(id=int(company_id))
	menu_items=MenuItem.objects.all()
	owners=Investment.objects.filter(of_company=institution)
	return render_to_response('companyprofile.html', {'institution':institution, 'menu_items':menu_items, 'owners':owners},context_instance=RequestContext(request))

#Auxiliar functions
def generate_diference(todays, yesterday):
	"""
		receives 2 lists of events for 2 diferent days and 
		returns one matrix with the companys and their diferences and means.
	"""
	#if not todays or not yesterday:
	#	return []
	
	companies=Company.objects.all()
	values_dic={}
	values_list=[]

	#creates a dictionary with initial values for each company
	for item in companies:
		values_dic[item.name]=[0,0,0,0]
	
	# adds the values to calculate the share value of yesterdays events
	## Atention this may need another counting aproach
	for item in yesterday:
		values_dic[item.company.name][0]+=item.total_credits/item.amount_of_shares
		values_dic[item.company.name][1]+=1
	
	# adds the values to calculate the share value of todays events
	for item in todays:
		values_dic[item.company.name][2]+=item.total_credits/item.amount_of_shares
		values_dic[item.company.name][3]+=1	
	
	# with the value generate the final matrix, for each row [Company name, yesterday value, today value, and diference]
	for comp, list in values_dic.iteritems():
		if (not list[1]) and (not list[3]):
			values_list.append([comp, "no transactions", "no transactions", "no data"])
		elif not list[1]:
			values_list.append([comp, "no transactions", list[2]/list[3], "no data"])
		elif not list[3]:
			values_list.append([comp, list[0]/list[1], "no transactions", "no data"])
		else:
			values_list.append([comp, list[0]/list[1], list[2]/list[3], (list[2]/list[3])-(list[0]/list[1])])
	
	return values_list
	
def invest_changes(todays, yesterdays, user):
	#if not todays or not yesterdays:
	#	return []
	"""
		receives 2 lists of events for 2 diferent days and the currents user. 
		Returns one matrix with the companys and their diferences and means.
	"""
	companies=[] #To remove
	
	invests=Investment.objects.filter(owner=user)
	
	values_dic={}
	values_list=[]
	
	#for each users assets companies
	for invest in invests:
		values_dic[invest.of_company.name]=[0,0,0,0,invest.initial_value]
	
	# adds the values to calculate the share value of yesterdays events
	## Atention this may need another counting aproach
	for item in yesterdays:
		if item.company.name in values_dic:
			values_dic[item.company.name][0]+=item.total_credits/item.amount_of_shares
			values_dic[item.company.name][1]+=1
	
	# adds the values to calculate the share value of todays events
	for item in todays:
		if item.company.name in values_dic:
			values_dic[item.company.name][2]+=item.total_credits/item.amount_of_shares
			values_dic[item.company.name][3]+=1
	
	# with the value generate the final matrix, for each row [Company name, yesterday value, today value, diference , initial invest value, total gain/loss]	
	for comp, list in values_dic.iteritems():
		if (not list[1]) and (not list[3]):
			values_list.append([comp, "no transactions", "no transactions", "no data", list[4], "no data"])
		elif not list[1]:
			values_list.append([comp, "no transactions", list[2]/list[3], "no data", list[4], (list[2]/list[3])-list[4]])
		elif not list[3]:
			values_list.append([comp, list[0]/list[1], "no transactions", "no data", list[4], "no data"])
		else:
			values_list.append([comp, list[0]/list[1], list[2]/list[3], (list[2]/list[3])-(list[0]/list[1]), list[4], (list[2]/list[3])-list[4]])
	
	return values_list
	