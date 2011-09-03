# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from social_auth.backends import BACKENDS
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

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
	return render_to_response('dash.html',{'user':request.user.username,
											'name':request.user.first_name},RequestContext(request))
	
		
