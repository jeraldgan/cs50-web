from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import resolve
from django import forms
from random import choice

from . import util

markdowner = Markdown()


class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="")


def index(request):
    search_keyword = request.GET.get('q', None)
    if search_keyword is not None:

        search_result = util.search_entries(search_keyword)

        if (type(search_result) is not list):
            return HttpResponseRedirect(f"/wiki/{search_result}")
        else:
            return render(request, "encyclopedia/search.html", {
                "search_results": util.search_entries(search_keyword)
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def edit(request, title):
    return render(request, "encyclopedia/contentEdit.html", {
        "form": NewEntry({
            "title": title,
            "content": util.get_entry(title),
            "function": "Edit"
        })
    })

def editPost(request):
    form = NewEntry(request.POST)

    if form.is_valid():
        title = form.cleaned_data["title"]

        if util.entry_exists(title):
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

        return HttpResponseRedirect(f"/wiki/{title}")


def entry(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdowner.convert(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": None,
        })


def create(request):
    if request.method == "POST":
        form = NewEntry(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]

            if util.entry_exists(title):
                return render(request, "encyclopedia/contentEdit.html", {
                    "form": NewEntry(),
                    "error": "Entry already exist with the given title",
                    "function": "Create"
                })

            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/contentEdit.html", {
        "form": NewEntry(),
        "function": "Create"
    })


def randomPage(request):
    title = choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{title}")
