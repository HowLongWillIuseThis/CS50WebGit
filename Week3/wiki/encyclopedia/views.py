from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import markdown2
from django import forms

archive = [entry.lower() for entry in util.list_entries()]
real_archive = util.list_entries()

class SearchForm(forms.Form):
    search = forms.CharField(label="search")

class CreateForm(forms.Form):
    Title = forms.CharField(label="Title")
    Text = forms.CharField(label="Text",widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return HttpResponse("error")
    converted = markdown2.markdown(entry_content)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": converted, 
    })  

def search(request):
    is_content = False
    if request.method == "GET":
        search_content = SearchForm(request.GET)
        if search_content.is_valid():
            suggested_items = []
            result = search_content.cleaned_data["search"].lower()
            counter = 0
            for items in archive:
                if items == result:
                    return HttpResponseRedirect(f'/wiki/{result}')
                if result in items:
                    suggested_items.append(real_archive[counter])
                counter += 1
            suggested_items.sort()
            if len(suggested_items) > 0:
                is_content = True
            return render(request, "encyclopedia/search.html", {
                "suggested" : suggested_items, "search" : result, "match_found": is_content
            })
        else:
            return render(request, "encyclopedia/search.html" , {
                "match_found": is_content
            })

def new(request):
    if request.method == "POST":
        new_page = CreateForm(request.POST)
        if new_page.is_valid():
            title = new_page.cleaned_data["Title"]
            text = new_page.cleaned_data["Text"]
            for items in archive:
                if title.lower() == items:
                    return render(request, "encyclopedia/createpage.html", {
                        "createpage": CreateForm, "title_collision": True
                    })
            util.save_entry(title, text)
            archive.append(title)
            return HttpResponseRedirect('/')
    return render(request, "encyclopedia/createpage.html", {
        "createpage" : CreateForm, "title_collision": False
    })

def edit(request, entry):
    Edit = CreateForm({'Title': entry, 'Text': util.get_entry(entry)})
    return render(request, "encyclopedia/createpage.html", {
        "createpage": Edit, "title_collision": False
    })

