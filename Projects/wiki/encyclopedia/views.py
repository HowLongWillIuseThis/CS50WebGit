from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
from markdown2 import Markdown
import random

markdowner = Markdown()

class Search(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class Edit(forms.Form):
    edit = forms.CharField(label="", widget=forms.Textarea(attrs={
        'placeholder': 'Add Content Here',
        'style': 'padding: 5px; height: 600px; text-align: center'
    }))

class Title(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'placeholder': 'Title',
        'style': 'padding: 2.5px; text-align: center; margin: 2.5px'
    }))

class Change(forms.Form):
    change = forms.CharField(label="", widget=forms.Textarea)

def index(request):
    wikientries = util.list_entries()
    if request.method == "GET":
        submit = Search(request.GET)
        if submit.is_valid():
            entry = submit.cleaned_data["search"]
            if entry in wikientries:
                return render(request, "encyclopedia/entry.html", {
                    "entries": entry, "page": convertpage(entry), "search": Search(), "random": randompage(wikientries)
                 })
            return render(request, "encyclopedia/searchresults.html", {
                "searchinput": entry, "results": suggestions(entry), "search": Search(), "random": randompage(wikientries)
            })
    return render(request, "encyclopedia/index.html", {
        "entries": wikientries, "search": Search(), "random": randompage(wikientries)
    })


def entry(request, title):
    wikientries = util.list_entries()
    if request.method == "GET":
        submit = Search(request.GET)
        if submit.is_valid():
            entry = submit.cleaned_data["search"]
            if entry in wikientries:
                return render(request, "encyclopedia/entry.html", {
                    "entries": entry, "page": convertpage(entry), "search": Search(), "random": randompage(wikientries)
                 })
            return render(request, "encyclopedia/searchresults.html", {
                "searchinput": entry, "results": suggestions(entry), "search": Search(), "random": randompage(wikientries)
            })
    if convertpage(title) == 1:
        return render(request, "encyclopedia/searchresults.html", {
            "search": Search(), "random": randompage(wikientries)
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entries": title, "page": convertpage(title), "search": Search(), "random": randompage(wikientries)
        })


def edit(request):
    wikientries = util.list_entries()
    if request.method == "POST":
        content = Edit(request.POST)
        title = Title(request.POST)
        if content.is_valid() and title.is_valid():
            page = content.cleaned_data["edit"]
            title_content = title.cleaned_data["title"]
            util.save_entry(title_content, page)
            return HttpResponseRedirect(reverse("index"))
    if request.method == "GET":
        submit = Search(request.GET)
        if submit.is_valid():
            entry = submit.cleaned_data["search"]
            if entry in wikientries:
                return render(request, "encyclopedia/entry.html", {
                    "entries": entry, "page": convertpage(entry), "search": Search(), "random": randompage(wikientries)
                 })
            return render(request, "encyclopedia/searchresults.html", {
                "searchinput": entry, "results": suggestions(entry), "search": Search(), "random": randompage(wikientries)
            })
    return render(request, "encyclopedia/newpage.html", {
        "edit": Edit(), "search": Search(), "title": Title(), "random": randompage(wikientries)
    })

def change(request, title):
    wikientries = util.list_entries()
    unconverted_entry = util.get_entry(title)
    if request.method == "POST":
        content = Change(request.POST)
        if content.is_valid():
            change_content = content.cleaned_data["change"]
            util.save_entry(title, change_content)
            return render(request, "encyclopedia/entry.html", {
                "entries": title, "search": Search(), "random": randompage(wikientries), "page": convertpage(title)
            })
    change_entry = Change(initial={'change': unconverted_entry})
    return render(request, "encyclopedia/edit.html",{
        "search": Search(), "random": randompage(wikientries), "change": change_entry
    })

def randompage(entries):
    return random.choice(entries)


def convertpage(unconverted_page):
    wikientries = util.list_entries()
    if unconverted_page in wikientries:
        page = util.get_entry(unconverted_page)
        return markdowner.convert(page)
    else:
        return 1


def suggestions(entry):
    wikientries = util.list_entries()
    results = []
    for entries in wikientries:
        if entry in entries:
            results.append(entries)
    return results 