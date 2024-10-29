from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class CoordinatorDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'coordinator_detail.html'
    context_object_name = 'coordinator'

    def get_object(self):
        # Get the event name from the URL
        event_name = self.kwargs.get('event_name')
        # Construct the expected group name
        group_name = f'Coordinator_{event_name}'

        # Ensure the logged-in user is displayed and belongs to the right group
        return get_object_or_404(User, id=self.request.user.id, groups__name=group_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['role'] = 'Coordinator'
        # Additional context data related to coordinator events can be added here
        context['event_name'] = self.kwargs.get('event_name')  # Add event name to context
        return context