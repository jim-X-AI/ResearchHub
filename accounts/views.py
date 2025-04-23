from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def register(request):
    """Register a new user"""
    if request.method != 'POST':
        # Display a blank registration form
        form = UserCreationForm()
    else:
        # Process is completed
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # log the user in and redirect to the le_log page
            login(request, new_user)
            return redirect('ecommerce_app:index')
    # Display a blank or invalid form
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)
