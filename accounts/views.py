from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)  # Log the user in immediately after signing up
            messages.success(request, "You have successfully signed up and logged in!")
            return redirect('home')  # Redirect to home or dashboard
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})
