import pandas as pd
from django.core.management.base import BaseCommand
from coordinator.models import StudentDetail

class Command(BaseCommand):
    help = 'Import student participation details from an Excel file'

    def handle(self, *args, **kwargs):
        # Load the Excel file
        file_path = 'student_participations_details.xlsx'
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            team_name = row['team_name']
            team_lead_name = row['team_lead_name']
            contact_number = row['contact_number']
            event_name = row['event_name']
            institute_name = row['institute_name']  # New field
            district = row['district']  # New field
            participant_2 = row.get('participant_2', None)  # New field
            participant_3 = row.get('participant_3', None)  # New field
            participant_4 = row.get('participant_4', None)  # New field

            # Retrieve or create the student record
            student_detail, created = StudentDetail.objects.get_or_create(
                team_name=team_name,
                defaults={
                    'team_lead_name': team_lead_name,
                    'contact_number': contact_number,
                    'event_name': event_name,
                    'institute_name': institute_name,
                    'district': district,
                    'participant_2': participant_2,
                    'participant_3': participant_3,
                    'participant_4': participant_4,
                }
            )

            if not created:
                # Dictionary of fields to check for changes
                fields_to_check = {
                    "team_lead_name": team_lead_name,
                    "contact_number": contact_number,
                    "event_name": event_name,
                    "institute_name": institute_name,
                    "district": district,
                    "participant_2": participant_2,
                    "participant_3": participant_3,
                    "participant_4": participant_4,
                }

                # Track if an update is needed
                update_needed = False

                # Check each field and update if different
                for field, new_value in fields_to_check.items():
                    current_value = getattr(student_detail, field)
                    if current_value != new_value:
                        setattr(student_detail, field, new_value)
                        update_needed = True

                # Only save if there was a change
                if update_needed:
                    student_detail.save()
                    self.stdout.write(self.style.WARNING(f"Updated details for team: {team_name}"))
                else:
                    self.stdout.write(self.style.NOTICE(f"No changes for team: {team_name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Added new team: {team_name}"))

        self.stdout.write(self.style.SUCCESS("Import completed."))
