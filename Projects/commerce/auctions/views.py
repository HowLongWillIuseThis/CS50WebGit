from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .models import User, Listing, Comment, Bid

winner = {}

class CreateForm(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        labels = {
            'image_url': _('Url'),
            'description': _('Description')
        }
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 10}),
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

def index(request):
    if request.method == "POST":
        new_listing = CreateForm(request.POST)
        if new_listing.is_valid():
            listing = Listing(
                user=request.user,
                image_url=new_listing.cleaned_data['image_url'],
                name=new_listing.cleaned_data['name'],
                price=new_listing.cleaned_data['price'],
                category=new_listing.cleaned_data['category'],
                description=new_listing.cleaned_data['description']
            )
            bid_price = new_listing.cleaned_data['price']
            bid = Bid(item=listing, bid=bid_price)
            listing.save()
            bid.save()
            return HttpResponseRedirect(reverse('index'))
        print(new_listing.errors)
    
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    return render(request, "auctions/create.html", {
        "CreateForm": CreateForm, 
    })

def bid(request, item_id):
    print(winner)
    try:
        bid_price = Bid.objects.filter(item=Listing.objects.get(pk=item_id)).latest('id').bid
    except Bid.DoesNotExist:
        bid_price = Listing.objects.get(pk=item_id).price

    except Listing.DoesNotExist:
        print(winner)
        auction_winner = winner[item_id]
        return HttpResponse(f"The winner of this auction was {auction_winner}")
    if request.method == "POST":
        new_bid = BidForm(request.POST)
        if new_bid.is_valid():
            bid = Bid(user=request.user, item=Listing.objects.get(pk=item_id) ,bid=new_bid.cleaned_data["bid"])
            if bid.bid > bid_price:
                bid.save()
                return HttpResponseRedirect(reverse('bid', args=[item_id]))

    bidForm = BidForm({'bid': bid_price})
    return render(request, "auctions/bid.html", {
        "item_detail": Listing.objects.get(pk=item_id), "BidForm": bidForm, "bidding_price" : bid_price
    })


def watchlist(request, item_id):
    item = Listing.objects.get(pk=item_id)
    item.watchlist.add(request.user)
    try:
        bid_price = Bid.objects.filter(item=Listing.objects.get(pk=item_id)).latest('id').bid
    except Bid.DoesNotExist:
        bid_price = Listing.objects.get(pk=item_id).price
    bidForm = BidForm({'bid': bid_price})
    success = True
    return render(request, "auctions/bid.html", {
        "item_detail": Listing.objects.get(pk=item_id), "BidForm": bidForm, "bidding_price" : bid_price, "watchlist_add": success
    })

def user(request, user):
    account = User.objects.get(username=user)
    listing = account.accounts.all()
    watchlist = Listing.objects.filter(watchlist=request.user.id).all()
    print(watchlist)
    return render(request, "auctions/user.html",{
        "my_listing": listing, "watchlist": watchlist
    })

def end(request, item_id):
    try:
        bid_winner = Bid.objects.filter(item=Listing.objects.get(pk=item_id)).latest('id').user
    except Bid.DoesNotExist:
        bid_winner = Listing.objects.get(pk=item_id).user
    winner[item_id] = bid_winner
    print(winner)
    Listing.objects.get(pk=item_id).delete()
    return HttpResponseRedirect(reverse('user', args=[request.user.username]))