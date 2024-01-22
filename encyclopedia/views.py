from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def conv_to_html(title):
    markdowner = Markdown()
    input = util.get_entry(title)

    if input == None:
        return None
    else:
        return markdowner.convert(input)
    
def entry(request, title):
    page = title
    content = conv_to_html(title)

    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": page,
            "entry": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": 'The page was not found!'
        })
    
def search(request):
    if request.method == "POST":
        query = request.POST['q']
        entries = util.list_entries()
        content = conv_to_html(query)

        if content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "entry": content
            })
        else:
            list = []
            for subs in entries:
                if query.lower() in subs.lower():
                    list.append(subs)
            if list:
                return render(request, "encyclopedia/search.html", {
                    "entries": list
                })
            else:
                return index(request)
            
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        content = request.POST['content']

        if conv_to_html(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": 'This encyclopedia already exists!'
            })
        else:
            util.save_entry(title, content)
            new_page = conv_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": new_page
            })

def edit_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return entry(request, title)
        
def random_page(request):
    random_page = random.choice(util.list_entries())
    return entry(request, random_page)
        