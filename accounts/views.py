from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

@login_required
def profile_view(request):
    user_items = request.user.album_set.all()  # Пример для модели Album
    
    context = {
        'user_items': user_items
    }
    return render(request, 'accounts/profile.html', context)

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/register.html'
