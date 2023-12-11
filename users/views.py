from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import auth
from django.contrib.auth.views import LogoutView
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, f'Your account has been created. You can now login!')
            return redirect('users:login')
    context = {'form': form}
    return render(request, 'registration/register.html', context)

class LogoutView(LogoutView):
    template_name = 'registration/logout.html'
    next_page = 'tracker:expenses'

    def get(self, request):
        auth.logout(request)
        return render(request, self.template_name)

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your profile has been updated!') 
            return redirect('tracker:expenses')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,    
    }

    return render(request, 'registration/profile.html', context)