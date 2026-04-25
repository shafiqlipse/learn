from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from .filters import *

# Create your views here.
@login_required(login_url='login')
def all_elections(request):
    elections = Election.objects.all()
    election_to_edit = None

    # Detect edit mode
    election_id = request.GET.get("edit") or request.POST.get("election_id")
    if election_id:
        election_to_edit = get_object_or_404(Election, id=election_id)

    if request.method == "POST":
        form = ElectionForm(
            request.POST,
            request.FILES,
            instance=election_to_edit if election_to_edit else None
        )

        if form.is_valid():
            form.save()
            return redirect("all_elections")

    else:
        form = ElectionForm(instance=election_to_edit)

    context = {
        "elections": elections,
        "cform": form,
        "election_to_edit": election_to_edit,
    }

    return render(request, "election/elections.html", context)



@login_required(login_url='login')
def electionDetail(request, id):
    election = get_object_or_404(Election, id=id)
    results = Result.objects.filter(election=election)

    result_to_edit = None

    # Detect edit mode
    result_id = request.GET.get("edit") or request.POST.get("result_id")
    if result_id:
        result_to_edit = get_object_or_404(Result, id=result_id, election=election)

    if request.method == "POST":
        form = ResultsForm(
            request.POST,
            request.FILES,
            instance=result_to_edit if result_to_edit else None
        )

        if form.is_valid():
            result = form.save(commit=False)
            result.election = election  # enforce correct election
            result.save()

            if result_to_edit:
                messages.success(request, "Result updated successfully.")
            else:
                messages.success(request, "Result added successfully.")

            return redirect("electionDetail", election.id)

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = ResultsForm(instance=result_to_edit)

    context = {
        "election": election,
        "results": results,
        "cform": form,
        "result_to_edit": result_to_edit,
    }

    return render(request, "election/election.html", context)




def deleteElection(request, id):
    election = get_object_or_404(Election, id=id)

    if request.method == "POST":
        election.delete()
        return redirect(
            "all_elections"
        )  # Replace 'athlete_list' with the name of your list view or any other view

    context = {
        "election": election,
    }

    return render(request, "election/deleteelection.html", context)


@login_required(login_url='login')
def all_results(request):
    results = Result.objects.all()
    resultsfilter = ResultsFilter(request.GET, queryset=results)
    allresults = resultsfilter.qs
    
    context = {
        "resultsfilter": resultsfilter,
        "allresults": allresults,
        
    }

    return render(request, "results/results.html", context)



def deleteResult(request, id):
    result = get_object_or_404(Result, id=id)

    if request.method == "POST":
        result.delete()
        return redirect(
            "all_results"
        )  # Replace 'athlete_list' with the name of your list view or any other view

    context = {
        "result": result,
    }

    return render(request, "results/deleteresult.html", context)




@login_required(login_url='login')
def all_candidates(request):
    candidates = Candidate.objects.all()
    candidate_to_edit = None

    # Detect edit mode
    candidate_id = request.GET.get("edit") or request.POST.get("candidate_id")
    if candidate_id:
        candidate_to_edit = get_object_or_404(Candidate, id=candidate_id)

    if request.method == "POST":
        form = CandidateForm(
            request.POST,
            request.FILES,
            instance=candidate_to_edit if candidate_to_edit else None
        )

        if form.is_valid():
            form.save()
            return redirect("all_candidates")

    else:
        form = CandidateForm(instance=candidate_to_edit)

    context = {
        "candidates": candidates,
        "cform": form,
        "candidate_to_edit": candidate_to_edit,
    }

    return render(request, "candidates/candidates.html", context)


def deleteCandidate(request, id):
    candidate = get_object_or_404(Candidate, id=id)

    if request.method == "POST":
        candidate.delete()
        return redirect(
            "all_candidates"
        )  # Replace 'athlete_list' with the name of your list view or any other view

    context = {
        "candidate": candidate,
    }

    return render(request, "candidates/deletecandidate.html", context)

