from django.shortcuts import render
from matplotlib.style import context
from django import forms 
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    entry = util.get_entry(name)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "error": "Could not find entry "+name
        })
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
        context = {
            "name": searched,
            "entry": entry
        }
        return render(request, "encyclopedia/entry.html", context)
    return render(request, "encyclopedia/error.html")

def newpage(request):
    return render(request, "encyclopedia/new_page.html")
