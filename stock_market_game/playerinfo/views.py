# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from social_auth.backends import BACKENDS
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from gamecore.models import MenuItem, GEvent, Investment
from models import UserCredit, Award, PrivateMessage, MessageForm

import datetime

#This is just a temporary variable representing the incial credits by the user.
#TODO : Have to create some configuration objects so we can manage this at the admin frontend
DEFAULT_CREDITS=1000

def home(request):
	'''
		This function is used to generate the login page or
		redirect the already logged users to his dashboard
	'''
	if request.user.is_authenticated():
		return HttpResponseRedirect('dashboard')
	else:
		backends=[]
		for name, backend in BACKENDS.iteritems():
			if name == 'facebook':
				backends.append((name,backend))
				break
		return render_to_response('home.html',{'backends':backends},RequestContext(request))

@login_required
def dashboard(request):
	'''
		This function shows the lastgame events and the user private messages.
		If is the users first time, it appends to his account the inicial credits. 
	'''
	#requests user credits
	total_credits=UserCredit.objects.filter(user=request.user)
	#if is the first time adds the credits
	if len(total_credits) == 0:
		inicial_credits=UserCredit(user=request.user, current_credits=DEFAULT_CREDITS)
		inicial_credits.save()
		total_credits=inicial_credits

		badge=Award(title="Tester", winner=request.user, creation_date=datetime.date.today(), badge="firstbadge.png")
		badge.save()
	else:
		total_credits=total_credits[0]
	
	#gets the menu elements and game events from the database
	menu_items=MenuItem.objects.all()
	last_events=GEvent.objects.all()[:20]
	
	#gets users private messagens and send form
	private_messages=PrivateMessage.objects.filter(receiver=request.user)
	form=MessageForm()
	
	#render page and reply to user
	return render_to_response('dash.html',{'user':request.user.username,
											'name':request.user.first_name,'menu_items':menu_items, 'credits':total_credits.current_credits, 'last_events':last_events, 'private_messages':private_messages, 'form':form},
											RequestContext(request))
	
@login_required
def exit_game(request):
	'''
		just logs out the current user
	'''
	logout(request)
	return HttpResponseRedirect('/')
	

def profile(request, user_id):
	'''
		this funtion receives one user id and generates a response
		with the user info.
	'''

	#fetchs the need data
	userob=User.objects.get(id=int(user_id))
	ucredits=UserCredit.objects.get(user=userob)
	uawards=Award.objects.filter(winner=userob)
	sells=GEvent.objects.filter(player_from=userob)
	buys=GEvent.objects.filter(player_to=userob)
	menu_items=MenuItem.objects.all()
	
	#render page and reply to the user
	return render_to_response('profile.html', {'userob':userob, 'ucredits':ucredits, 'uawards':uawards, 'sells':sells, 'buys':buys, 'menu_items':menu_items}, RequestContext(request))


def send(request):
	'''
		Checks if it is a POST request, and if valid creates a new
		private message.
	'''
	menu_items=MenuItem.objects.all()
	if request.method == 'POST': # If the form has been submitted...
		form = MessageForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			#Get the needed content
			userto=form.cleaned_data['player_to']
			theuser=User.objects.get(username=userto)
			sendcontent=form.cleaned_data['mcontent']
			now=datetime.datetime.now()
			#Created a new message
			newmsg=PrivateMessage(sender=request.user, receiver=theuser, send_date=now, content=sendcontent)
			newmsg.save()
			#Redirect to the dashboad
			return HttpResponseRedirect('/dashboard')
	else:
		#If its not a POST request, reply generate and reply a custom error message
		return render_to_response('cannot.html', {'menu_items':menu_items})
