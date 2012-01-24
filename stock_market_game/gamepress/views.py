# Create your views here.
from models import Article, Comment
from gamecore.models import MenuItem
from django.shortcuts import render_to_response
from django.template import RequestContext

def bloglist(request):
	'''
		this function returns a response page containing a list with all the blog posts
	'''
	menu_items=MenuItem.objects.all()
	articles=Article.objects.all()
	return render_to_response("article_list.html", {'menu_items':menu_items, 'articles':articles}, context_instance=RequestContext(request))
	
def article_view(request, art_id):
	'''
		returns a response with the article of the given if and his comments
	'''
	menu_items=MenuItem.objects.all()
	article=Article.objects.get(id=int(art_id))
	comments=Comment.objects.filter(carticle=article)
	return render_to_response("article_view.html", {'menu_items':menu_items, 'article':article, 'comments':comments} , context_instance=RequestContext(request))
