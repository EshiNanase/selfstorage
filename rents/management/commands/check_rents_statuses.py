from django.core.management import BaseCommand
from django.utils.timezone import now

from personal_account.models import Client
from email_sender import send_email
from rents.models import Rent

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
        expired_rents = Rent.objects.filter_expired()
        expired_rents.update(status=Rent.EXPIRED)
        expired_rent_mailing_list = {
            rent.client.email
            for rent in expired_rents
        }

        soon_expiring_rents = Rent.objects.filter_soon_expiring()
        soon_expiring_mailing_list = {rent.client.email for rent in soon_expiring_rents}

        success_sent_expired = send_email(
            receivers=expired_rent_mailing_list,
            msg_body=EXPIRED_NOTIFICATION['subject'],
            subject=EXPIRED_NOTIFICATION['text']
        )

        success_sent_soon_expiring = send_email(
            receivers=soon_expiring_mailing_list,
            msg_body=SOON_EXPIRING_NOTIFICATION['subject'],
            subject=SOON_EXPIRING_NOTIFICATION['text']
        )
        success_sent = success_sent_soon_expiring + success_sent_expired
        if success_sent:
            Client.objects.filter(email__in=success_sent).update(warning_sent_at=now())