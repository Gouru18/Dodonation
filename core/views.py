from django.shortcuts import render

def homepage(request):
    # This page is for your Task 6.
    # [cite_start]Your System Spec shows the Donation model has a 'date_created' field[cite: 204].

    # --- FOR TESTING ---
    # We can't get real donations yet (Poshita/Vedna's task).
    # So, we will use a "dummy" list to build your template.
    recent_donations = [
        {'title': 'Sample Donation 1', 'description': 'Test desc', 'category': 'Food', 'quantity': 10, 'location': 'Here'},
        {'title': 'Sample Donation 2', 'description': 'Test desc', 'category': 'Clothing', 'quantity': 5, 'location': 'There'},
        {'title': 'Sample Donation 3', 'description': 'Test desc', 'category': 'Other', 'quantity': 2, 'location': 'Anywhere'},
    ]

    context = {
        'recent_donations': recent_donations
    }
    return render(request, 'core/homepage.html', context)