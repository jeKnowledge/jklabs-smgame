# Create your views here.
from models import Article, Comment
from gamecore.models import MenuItem
from django.shortcuts import render_to_response
from django.template import RequestContext

def bloglist(request):
	#content
	menu_items=MenuItem.objects.all()
	articles=Article.objects.all()
	return render_to_response("article_list.html", {'menu_items':menu_items, 'articles':articles}, context_instance=RequestContext(request))
	
def article_view(request, art_id):
	#content
	menu_items=MenuItem.objects.all()
	article=Article.objects.get(id=int(art_id))
	comments=Comment.objects.filter(carticle=article)
	return render_to_response("article_view.html", {'menu_items':menu_items, 'article':article, 'comments':comments} , context_instance=RequestContext(request))
