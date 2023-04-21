from django.core.management import BaseCommand
from django.utils.timezone import now

from services.email_sender import send_email_by_receivers
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
        expired_rent_mailing_list = {
            rent.client.email
            for rent in expired_rents
        }
        expired_rents_ids = [rent.id for rent in expired_rents]
        expired_rents.update(status=Rent.EXPIRED)

        soon_expiring_rents = Rent.objects.filter_soon_expiring()
        soon_expiring_mailing_list = {rent.client.email for rent in soon_expiring_rents}
        soon_expiring_rents_ids = [rent.id for rent in soon_expiring_rents]

        success_sent_expired = send_email_by_receivers(
            receivers=expired_rent_mailing_list,
            subject=EXPIRED_NOTIFICATION['subject'],
            msg_body=EXPIRED_NOTIFICATION['text']
        )

        success_sent_soon_expiring = send_email_by_receivers(
            receivers=soon_expiring_mailing_list,
            subject=SOON_EXPIRING_NOTIFICATION['subject'],
            msg_body=SOON_EXPIRING_NOTIFICATION['text']
        )

        Rent.objects.filter(pk__in=expired_rents_ids, client__email__in=success_sent_expired). \
            update(warning_sent_at=now())
        Rent.objects.filter(pk__in=soon_expiring_rents_ids, client__email__in=success_sent_soon_expiring). \
            update(warning_sent_at=now())
