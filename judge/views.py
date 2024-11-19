from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404,render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from coordinator.models import StudentDetail  # Adjusted import to the correct app
from django.db.models import Q

class JudgeDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'judge_detail.html'  # Template with paginated team list
    context_object_name = 'judge'

    def get_object(self):
        # Get the event name from the URL
        event_name = self.kwargs.get('event_name')
        # Construct the expected group name
        group_name = f'Judge_{event_name}'

        # Ensure the logged-in user is displayed and belongs to the right group
        return get_object_or_404(User, id=self.request.user.id, groups__name=group_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_name = self.kwargs.get('event_name')
        query = self.request.GET.get('q')

        # Filter StudentDetails based on event_name and search query
        teams = StudentDetail.objects.filter(event_name=event_name)
        if query:
            teams = teams.filter(team_name__icontains=query)

        # Paginate the teams, showing 10 per page
        paginator = Paginator(teams, 10)
        page_number = self.request.GET.get('page')
        page_obj = (paginator.get_page(page_number))

        context.update({
            'username': self.request.user.username,
            'role': 'Judge',
            'event_name': event_name,
            'page_obj': page_obj,
            'query': query,  # Pass the query to context for display in the search bar
        })
        return context

class JudgeEvaluationView(LoginRequiredMixin, DetailView):
    model = StudentDetail
    template_name = 'judge_evaluation.html'
    context_object_name = 'team'

    def get_object(self):
        # Retrieve team based on team_name only
        team_name = self.kwargs.get('team_name')
        
        # Get the student detail for the specific team
        return get_object_or_404(StudentDetail, team_name=team_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_name'] = self.kwargs.get('team_name')
        context['username'] = self.request.user.username
        return context

    def get(self, request, *args, **kwargs):
        # Retrieve the object and render the template with necessary context
        self.object = self.get_object()  # Retrieve the team object
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
