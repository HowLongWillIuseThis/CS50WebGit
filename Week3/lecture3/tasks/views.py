from django.shortcuts import render
from django import forms


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"].append(task)
        else:
            return render(request, "tasks/add.html", {
                "forms": form
            })

    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):

    return render(request, "tasks/add.html", {
        "form": NewTaskForm
    })