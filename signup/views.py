from django.shortcuts import redirect, render
from .forms import SignupForm
# Create your views here.

def signup_view(response):
    if response.method == 'POST':
        form = SignupForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SignupForm()
    return render(response, "registration/signup.html", {"form": form})


