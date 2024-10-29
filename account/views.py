from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import Group

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        # Call the parent's form_valid method to log in the user
        super().form_valid(form)

        # Get the selected role from the form
        role = self.request.POST.get('role')
        user = self.request.user

        # Find the event name based on the user's role and group
        group = user.groups.filter(name__startswith=role).first()
        
        if group:
            # Extract the event name from the group name (assuming format is "role_event_name")
            event_name = group.name.split('_', 1)[1] if '_' in group.name else None

            if event_name or role == 'admin':  # Ensure the event name is valid
                # Redirect based on role and event assignment
                if role == 'coordinator':
                    return redirect(reverse_lazy('coordinator:coordinator_home', kwargs={
                        'event_name': event_name,
                        'username': user.username
                    }))
                elif role == 'judge':
                    return redirect(reverse_lazy('judge:judge_home', kwargs={
                        'event_name': event_name,
                        'username': user.username
                    }))
                elif role == 'admin' and user.is_staff:
                    return redirect(reverse_lazy('e_admin:admin_home', kwargs={
                    'username': user.username
                }))  # Redirect to Admin home page
                else:
                    messages.error(self.request, 'You do not have access to this role and event.')
                    return redirect(reverse_lazy('login'))  # Redirect back to the login page
            else:
                messages.error(self.request, 'Event name is not valid.')
                return redirect(reverse_lazy('login'))  # Redirect back to the login page
        else:
            messages.error(self.request, 'You do not have access to this role and event.')
            return redirect(reverse_lazy('login'))  # Redirect back to the login page

    def form_invalid(self, form):
        # Display error message for invalid login
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
