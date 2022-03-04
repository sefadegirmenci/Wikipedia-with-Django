from django.http import HttpResponseRedirect
from django.shortcuts import render
from matplotlib.style import context
from django import forms
from . import util
import markdown2
import random

image_links=[]
def index(request):
    entries = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "image_links": image_links
    })


def entry(request, name):
    name=name.strip()
    markdown_entry = util.get_entry(name)
    if not markdown_entry:
        return render(request, "encyclopedia/error.html", {
            "error": "Could not find entry "+name
        })
    
    entry= markdown2.markdown(markdown_entry)
    context = {
        "name": name,
        "entry": entry
    }
    return render(request, "encyclopedia/entry.html", context)


def search(request):
    if request.method == "GET":
        searched = request.GET.get("q")
        entry = util.get_entry(searched)
        if not entry:
            entries = [entry for entry in util.list_entries() if searched.lower() in entry.lower()]
            return render(request, "encyclopedia/search_result.html", {
                "entries": entries,
                "searched":searched
            })
        return HttpResponseRedirect(searched)
    return render(request, "encyclopedia/error.html")

def newpage(request):
    if request.method == "POST":
        title = request.POST.get("new-page-title").strip()
        content = request.POST.get("new-page-content")
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "error": "Page with title " + title + " already exists"
            })
        util.save_entry(title,content)
        return HttpResponseRedirect(title)
    else:
        return render(request, "encyclopedia/new_page.html")

def editpage(request):
    if request.method == "POST":
        title = request.POST.get("new-page-title")
        content = request.POST.get("new-page-content")
        util.save_entry(title,content)
        return HttpResponseRedirect(title)
    elif request.method == "GET":
        title = request.GET.get("title")
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "content":content
            })
def randompage(request):
    entries = util.list_entries()
    size = len(entries)
    rand = random.randint(0,size-1)
    entry = entries[rand]
    return HttpResponseRedirect(entry)
