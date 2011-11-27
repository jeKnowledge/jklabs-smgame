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

DEFAULT_CREDITS=1000

def home(request):
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
	total_credits=UserCredit.objects.filter(user=request.user)
	if len(total_credits) == 0:
		inicial_credits=UserCredit(user=request.user, current_credits=DEFAULT_CREDITS)
		inicial_credits.save()
		total_credits=inicial_credits
	else:
		total_credits=total_credits[0]

	menu_items=MenuItem.objects.all()
	last_events=GEvent.objects.all()[:20]
	
	private_messages=PrivateMessage.objects.filter(receiver=request.user)
	form=MessageForm()
	
	return render_to_response('dash.html',{'user':request.user.username,
											'name':request.user.first_name,'menu_items':menu_items, 'credits':total_credits.current_credits, 'last_events':last_events, 'private_messages':private_messages, 'form':form},
											RequestContext(request))
	
@login_required
def exit_game(request):
	logout(request)
	return HttpResponseRedirect('/')
	

def profile(request, user_id):
	userob=User.objects.get(id=int(user_id))
	ucredits=UserCredit.objects.get(user=userob)
	uawards=Award.objects.filter(winner=userob)
	sells=GEvent.objects.filter(player_from=userob)
	buys=GEvent.objects.filter(player_to=userob)
	menu_items=MenuItem.objects.all()
	
	return render_to_response('profile.html', {'userob':userob, 'ucredits':ucredits, 'uawards':uawards, 'sells':sells, 'buys':buys, 'menu_items':menu_items}, RequestContext(request))


def send(request):
	menu_items=MenuItem.objects.all()
	if request.method == 'POST': # If the form has been submitted...
		form = MessageForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			userto=form.cleaned_data['player_to']
			theuser=User.objects.get(username=userto)
			sendcontent=form.cleaned_data['mcontent']
			now=datetime.datetime.now()
			newmsg=PrivateMessage(sender=request.user, receiver=theuser, send_date=now, content=sendcontent)
			newmsg.save()
			return HttpResponseRedirect('/dashboard')
	else:
		return render_to_response('cannot.html', {'menu_items':menu_items})
