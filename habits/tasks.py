
from celery import shared_task
import pytz

from config import settings
import requests
from datetime import datetime, timedelta
from django.utils import timezone

from habits.models import Habits

INTERVAL_MAPPING = {
    'once_a_day': 1,
    'once_a_two_day': 2,
    'once_a_three_day': 3,
    'once_a_four_day': 4,
    'once_a_five_day': 5,
    'once_a_six_day': 6,
    'once_a_week': 7,
}


def process_user_habits(habit_id):
    """Отправка пользователю сообщения о выполнении привычки"""

    habit = Habits.objects.get(id=habit_id)
    print(habit.id)

    URL = "https://api.telegram.org/bot"
    TOKEN = settings.TELEGRAM_BOT_API_KEY
    response = requests.post(
        url=f"{URL}{TOKEN}/sendMessage",
        data={
            "chat_id": habit.owner.telegram_id,
            "text": f'Привет {habit.owner.name}! Время {habit.time}. '
                    f'Пора идти в {habit.place} и сделать {habit.action}.'
                    f'Это займет {habit.duration_time} минут!'
        }
    )
    print(response)
    return response


@shared_task
def send_message_about_habits_time():
    habits = Habits.objects.all()
    for habit in habits:
        start_time_habit = habit.time
        start_date_habit = datetime.now().date()

        moscow_tz = pytz.timezone('Europe/Moscow')

        time_up = timezone.now().astimezone(moscow_tz) - timezone.timedelta(minutes=5)
        start_datetime_habit = moscow_tz.localize(datetime.combine(start_date_habit, start_time_habit))

        if time_up <= start_datetime_habit <= timezone.now().astimezone(moscow_tz):
            process_user_habits(habit.id)
            start_date_habit = start_date_habit + timedelta(days=INTERVAL_MAPPING.get(habit.interval, 0))
            habit.save()

