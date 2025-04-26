from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Poll, Choice, Vote
from .forms import PollForm, ChoiceFormSet
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, ListView
from django.urls import reverse_lazy
from django.utils import timezone


def index(request):
    all_polls = Poll.objects.annotate(
        vote_count=Count("choices__vote"),
        votes_total=Count("vote", distinct=True),
    )
    active_polls = [poll for poll in all_polls if poll.is_active()]
    return render(request, "polls/index.html", {"polls": active_polls})


@login_required
def create_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST, instance=Poll(), prefix="choices")

        if form.is_valid() and formset.is_valid():
            has_choice = any(
                f.cleaned_data.get("choice_text")
                and not f.cleaned_data.get("DELETE", False)
                for f in formset
            )

            if not has_choice:
                messages.error(request, "You must add at least one option.")
            else:
                poll = form.save(commit=False)
                poll.created_by = request.user
                poll.save()
                formset.instance = poll
                formset.save()
                messages.success(request, "Poll created successfully!")
                return redirect("index")
    else:
        form = PollForm()
        formset = ChoiceFormSet(instance=Poll(), prefix="choices")

    return render(request, "polls/create.html", {"form": form, "formset": formset})


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if not poll.is_active():
        messages.error(request, "This poll has expired!")
        return redirect("index")
    if Vote.objects.filter(user=request.user, poll=poll).exists():
        messages.error(request, "You have already voted on this poll!")
        return redirect("index")
    if request.method == "POST":
        choice_id = request.POST.get("choice")
        if choice_id:
            choice = Choice.objects.get(id=choice_id)
            Vote.objects.create(user=request.user, poll=poll, choice=choice)
            messages.success(request, "Vote recorded!")
            return redirect("results", poll.id)
        else:
            messages.error(request, "Please select an option!")

    return render(request, "polls/vote.html", {"poll": poll})


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    votes = (
        Vote.objects.filter(poll=poll)
        .values("choice__choice_text")
        .annotate(total=Count("choice"))
    )
    return render(request, "polls/results.html", {"poll": poll, "votes": votes})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


class MyPollsView(LoginRequiredMixin, ListView):
    template_name = "polls/my_polls.html"
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(created_by=self.request.user)


class PollUpdateView(LoginRequiredMixin, UpdateView):
    model = Poll
    form_class = PollForm
    template_name = "polls/edit_poll.html"

    def get_success_url(self):
        return reverse_lazy("my_polls")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = ChoiceFormSet(
                self.request.POST, instance=self.object, prefix="choices"
            )
        else:
            context["formset"] = ChoiceFormSet(instance=self.object, prefix="choices")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if form.is_valid() and formset.is_valid():
            has_choice = any(
                f.cleaned_data.get("choice_text")
                and not f.cleaned_data.get("DELETE", False)
                for f in formset
            )

            if not has_choice:
                messages.error(self.request, "You must add at least one option.")
                return self.form_invalid(form)

            form.save()
            formset.save()
            if "end_now" in self.request.POST:
                form.instance.expire_date = timezone.now()
                form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


def shared_poll(request, share_id):
    poll = get_object_or_404(Poll, share_id=share_id)
    if not poll.is_active():
        messages.error(request, "This poll has expired!")
        return redirect("index")
    return redirect("vote", poll_id=poll.id)
