from django.shortcuts import render
from django.http import HttpResponse
from . import twitter_parser
from . import textmining
# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    return render(request, 'showyou/index.html') 

def generic(request):
    return render(request, 'showyou/generic.html') 

def elements(request):
    return render(request, 'showyou/elements.html') 

def twitterSelect(request):
    search_keyword = request.GET.get('search_keyword', '')
    print('search_keyword = ' + search_keyword)
    if search_keyword:
        print("있는 경우")
        twitter_parser.parsing(search_keyword)
        textmining.analysis()
        return render(request, 'showyou/twitterSelect.html') 
    else :
        print("없는 경우")
        return render(request, 'showyou/twitterSelect.html') 

# def twitterKeyword(request):
#     search_keyword = request.POST['search_keyword']
#     # search_keyword = request.GET.get('search_keyword', '')
#     print(search_keyword)
#     if search_keyword:
#         print(search_keyword)
#         return render(request, 'showyou/twitterSelect.html') 
#     else :
#         return render(request, 'showyou/twitterSelect.html') 