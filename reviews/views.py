from django.shortcuts import render, redirect
from .models import GeneralReview
from .forms import ReviewForm

def leave_review(request):
    # This handles when a user submits the form
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_review') # Redirect back to the same page

    # This handles when a user just visits the page (a GET request)
    else:
        form = ReviewForm() # Give them a blank form

    # Get all existing reviews from the database to show them
    reviews = GeneralReview.objects.order_by('-created_at') # Newest first

    context = {
        'form': form,
        'reviews': reviews
    }
    return render(request, 'reviews/leave_review.html', context)