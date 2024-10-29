# e_admin/views.py
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class AdminDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'admin_detail.html'  # Update to your admin detail template
    context_object_name = 'admin'

    def get_object(self):
        # Ensure the logged-in user is displayed and is a staff member
        return get_object_or_404(User, id=self.request.user.id, is_staff=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['role'] = 'Admin'
        # Additional context data related to admin can be added here
        return context
