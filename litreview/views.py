from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator
from . import forms
from authentication.models import User, UserFollows
from litreview.models import Ticket, Review


@login_required
def feed(request):
    tickets = Ticket.objects.filter(Q(user__in=request.user.abonnements.all()) | Q(user=request.user))
    reviews = Review.objects.filter(Q(user__in=request.user.abonnements.all()) | Q(user=request.user))
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)
    paginator = Paginator(tickets_and_reviews, settings.MAX_ITEMS_PER_PAGE)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "litreview/feed.html", context={"page_obj": page_obj})


@login_required
def posts(request):
    tickets = Ticket.objects.filter(Q(user=request.user))
    reviews = Review.objects.filter(Q(user=request.user))
    posts = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)
    paginator = Paginator(posts, settings.MAX_ITEMS_PER_PAGE)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "litreview/posts.html", context={"page_obj": page_obj})


@login_required
def add_ticket(request):
    ticket_creation_form = forms.TicketCreationForm()
    if request.method == "POST":
        ticket_creation_form = forms.TicketCreationForm(request.POST, request.FILES)
        if ticket_creation_form.is_valid():
            ticket_form = ticket_creation_form.save(commit=False)
            ticket_form.user = request.user
            ticket_form.save()
            messages.success(request, message="Ticket publié")
            return redirect("feed")
    return render(request, "litreview/add_ticket.html", context={"ticket_creation_form": ticket_creation_form})


@login_required
def change_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket_creation_form = forms.TicketCreationForm(instance=ticket)
    if request.method == "POST":
        ticket_creation_form = forms.TicketCreationForm(request.POST, request.FILES, instance=ticket)
        if ticket.user == request.user:
            if ticket_creation_form.is_valid():
                ticket.save()
                messages.success(request, message="Ticket mis à jour")
                return redirect("feed")
    return render(request, "litreview/change_ticket.html", context={"ticket": ticket})


@login_required
def delete_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == "POST":
        if ticket.user == request.user:
            ticket.delete()
            messages.success(request, message="Ticket supprimé")
            return redirect("feed")
    return render(request, "litreview/delete_ticket.html", context={"ticket": ticket})


@login_required
def change_review(request, id):
    review = Review.objects.get(id=id)
    review_creation_form = forms.ReviewCreationForm(instance=review)
    if request.method == "POST":
        review_creation_form = forms.ReviewCreationForm(request.POST, request.FILES, instance=review)
        if review.user == request.user:
            if review_creation_form.is_valid():
                review.save()
                messages.success(request, message="Critique mise à jour")
                return redirect("feed")
    return render(request, "litreview/change_review.html", context={"review": review})


@login_required
def delete_review(request, id):
    review = Review.objects.get(id=id)
    ticket = Ticket.objects.get(review.ticket)
    if request.method == "POST":
        if review.user == request.user:
            review.delete()
            ticket.has_been_reviewed = False
            messages.success(request, message="Critique supprimée")
            return redirect("feed")
    return render(request, "litreview/delete_review.html", context={"review": review})


@login_required
def add_review(request):
    ticket_creation_form = forms.TicketCreationForm()
    review_creation_form = forms.ReviewCreationForm()
    context = {"ticket_creation_form": ticket_creation_form, "review_creation_form": review_creation_form}
    if request.method == "POST":
        ticket_creation_form = forms.TicketCreationForm(request.POST, request.FILES)
        review_creation_form = forms.ReviewCreationForm(request.POST)
        if all([ticket_creation_form.is_valid(), review_creation_form.is_valid()]):
            if review_creation_form.cleaned_data:
                rating_digit_value = review_creation_form['rating'].data
                ticket_form = ticket_creation_form.save(commit=False)
                ticket_form.user = request.user
                ticket_form.has_been_reviewed = True
                ticket_form.save()
                review_form = review_creation_form.save(commit=False)
                review_form.ticket = ticket_form
                review_form.rating = rating_digit_value
                review_form.user = request.user
                review_form.save()
                messages.success(request, message="Requête et critique ajoutées")
                return redirect("feed")
    return render(request, "litreview/add_review.html", context=context)


@login_required
def add_response_review(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    ticket_creation_form = forms.TicketCreationForm(instance=ticket)
    review_creation_form = forms.ReviewCreationForm()
    if ticket is not None:
        if request.method == "POST":
            review_creation_form = forms.ReviewCreationForm(request.POST)
            ticket_creation_form = forms.TicketCreationForm(instance=ticket)
            if review_creation_form.is_valid():
                if review_creation_form.cleaned_data:
                    rating_digit_value = review_creation_form['rating'].data
                    ticket_form = ticket_creation_form.save(commit=False)
                    ticket_form.has_been_reviewed = True
                    ticket_form.save()
                    review_form = review_creation_form.save(commit=False)
                    review_form.ticket = ticket
                    review_form.rating = rating_digit_value
                    review_form.user = request.user
                    review_form.save()
                    messages.success(request, message="Critique publiée en réponse au ticket")
                    return redirect("feed")
    context = {"review_creation_form": review_creation_form, "ticket": ticket}
    return render(request, "litreview/add_response_review.html", context=context)


@login_required
def subscriptions(request):
    follow_form = forms.UserFollowForm()
    unsubscribe_form = forms.UnsubscribeForm()
    if request.method == "POST":
        if "follow_user" in request.POST:
            form = forms.UserFollowForm(request.POST)
            if form.is_valid():
                if request.POST["username"] != "":
                    username_searched = request.POST["username"]
                    followed_user = User.objects.get(username=username_searched.lower())
                    user_follow = UserFollows(user=request.user, followed_user=followed_user)
                    if followed_user.username == request.user:
                        return redirect("feed")
                    if followed_user is not None:
                        user_follow.save()
                        request.user.save()
                        User.objects.get(username=username_searched.lower()).save()
                        messages.success(request, message="Abonnement pris en compte")
                        return redirect("feed")
        elif "unsubscribe_user" in request.POST:
            form = forms.UnsubscribeForm(request.POST)
            if form.is_valid():
                if request.POST["username"] != "":
                    username_searched = request.POST["username"].lower()
                    followed_user = User.objects.get(username=username_searched)
                    user_follow = UserFollows.objects.get(user=request.user, followed_user=followed_user)
                    user_follow.delete()
                    messages.success(request, message="Désabonnement pris en compte")
                    return redirect("feed")
    user_subscriptions = request.user.following.all().exclude(followed_user=request.user)
    user_followers = request.user.followed_by.all().exclude(user=request.user)
    context = {
        "follow_form": follow_form,
        "unsubscribe_form": unsubscribe_form,
        "subscriptions": user_subscriptions,
        "followers": user_followers}
    return render(request, "litreview/subscriptions.html", context=context)
