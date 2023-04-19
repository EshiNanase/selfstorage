from datetime import timedelta

from django.core.management import BaseCommand
from django.utils.timezone import now

from personal_account.models import Client
from email_sender import send_email

EXPIRED_NOTIFICATION = {
    'subject': 'Аренда закончилась',
    'text': 'Срок вашей аренды истек. Оплатите продление аренды, либо заберите вещи.'
}

SOON_EXPIRING_NOTIFICATION = {
    'subject': 'Аренда скоро заканчивается',
    'text': 'Срок вашей аренды истекает завтра. Не забудьте забрать вещи, либо оплатите продление аренды'
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        right_now = now()
        tomorrow = right_now + timedelta(days=1)

        clients_with_expired_rent = Client.objects. \
            filter(rents__expired_at__gte=right_now)

        clients_with_soon_expiring_rent = Client. \
            objects.filter(rents__expired_at__lte=tomorrow). \
            exclude(rents__expired_at__gte=right_now)

        send_email(
            receivers=clients_with_expired_rent,
            msg_body=EXPIRED_NOTIFICATION['subject'],
            subject=EXPIRED_NOTIFICATION['text']
        )

        send_email(
            receivers=clients_with_soon_expiring_rent,
            msg_body=SOON_EXPIRING_NOTIFICATION['subject'],
            subject=SOON_EXPIRING_NOTIFICATION['text']
        )
