from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from .models import StudentDetail  # Assuming this is your model

class CoordinatorDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'coordinator_detail.html'
    context_object_name = 'coordinator'
    paginate_by = 10  # Number of records per page

    def get_object(self):
        # Get the event name from the URL
        event_name = self.kwargs.get('event_name')
        group_name = f'Coordinator_{event_name}'
        return get_object_or_404(User, id=self.request.user.id, groups__name=group_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_name = self.kwargs.get('event_name')
        query = self.request.GET.get('q')

        # Filter StudentDetails based on event_name and search query
        students = StudentDetail.objects.filter(event_name=event_name)
        if query:
            students = students.filter(
                Q(team_name__icontains=query) |
                Q(team_lead_name__icontains=query) |
                Q(contact_number__icontains=query) |
                Q(institute_name__icontains=query) |
                Q(district__icontains=query) |
                Q(participant_2__icontains=query) |
                Q(participant_3__icontains=query) |
                Q(participant_4__icontains=query)
            )

        # Paginate the student details
        from django.core.paginator import Paginator
        paginator = Paginator(students, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'username': self.request.user.username,
            'role': 'Coordinator',
            'event_name': event_name,
            'page_obj': page_obj,
            'query': query,
        })
        return context
