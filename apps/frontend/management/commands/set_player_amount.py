from django.core.management.base import BaseCommand
from apps.trainings.models import Exercise, PlayerAmount


class Command(BaseCommand):
    def handle(self, *args, **options):
        exercises = Exercise.objects.all()
        for exercise in exercises:
            amounts = []
            for f in exercise.filters.all():
                if f.name.startswith('Spielerzahl'):
                    amount = int(f.name.split(': ')[1])
                    amounts.append(amount)
            player_amounts = PlayerAmount.objects.filter(amount__in=amounts)
            exercise.player_amount.set(player_amounts)
            exercise.save()
