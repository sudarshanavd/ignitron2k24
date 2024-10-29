import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create or update users from an Excel file'

    def handle(self, *args, **kwargs):
        # Load the Excel file
        df = pd.read_excel('users_data.xlsx')  # Update with your file path

        for index, row in df.iterrows():
            username = row['username']
            password = row['password']
            role = row['role']
            event_name = row['event_name']
            is_staff = row['is_staff']

            # Determine the new group name based on role and event (excluding event for admin)
            new_group_name = f"{role}" if role == 'Admin' else f"{role}_{event_name}"

            # Check if the user already exists
            user, created = User.objects.get_or_create(username=username)

            # Only update user details if something has changed
            if created or not self.user_details_match(user, password, is_staff, new_group_name):
                # Update user's details and assign them to the correct group
                self.update_user(user, password, is_staff)
                self.assign_user_to_group(user, new_group_name)
            else:
                self.stdout.write(self.style.SUCCESS(f'No changes for user: {username}'))

    def user_details_match(self, user, password, is_staff, group_name):
        """
        Check if the user's existing details match the new data.
        """
        # Check if the user's current group matches the new group
        current_group = user.groups.first().name if user.groups.exists() else None
        # Check password, staff status, and group name
        return user.check_password(password) and user.is_staff == is_staff and current_group == group_name

    def update_user(self, user, password, is_staff):
        """
        Update the user's details if necessary.
        """
        # Update password and staff status if necessary
        if not user.check_password(password):
            user.set_password(password)
            self.stdout.write(self.style.WARNING(f'Updated password for user: {user.username}'))
        user.is_staff = is_staff
        user.save()

    def assign_user_to_group(self, user, group_name):
        """
        Ensure the user is only in the specified group, removing them from any others.
        """
        # Remove user from all other groups if they are in the wrong group
        for old_group in user.groups.all():
            if old_group.name != group_name:
                user.groups.remove(old_group)
                if old_group.user_set.count() == 0:  # Check if group has no users left
                    old_group.delete()  # Delete empty group
                    self.stdout.write(self.style.WARNING(f'Removed empty group: {old_group.name}'))

        # Add the user to the new group if needed
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS(f'Added {user.username} to {group_name} group'))
