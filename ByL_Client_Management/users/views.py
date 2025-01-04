from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import bylLoginForm

class bylLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = bylLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('customer_list')

class bylLogoutView(LogoutView):
    next_page = reverse_lazy('login')