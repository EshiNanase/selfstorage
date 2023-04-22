import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from personal_account.models import Client
from rents.models import Rent
from storage.models import Box


def create_checkout_session(client, box_id):

    box = Box.objects.get(id=box_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    response = stripe.Price.create(
        unit_amount=int(box.price)*100,
        product=settings.BOX_STRIPE_ID,
        currency='rub',

    )
    price_id = response['id']

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            metadata={'client_id': client.id, 'box_id': box.id},
            success_url='https://www.youtube.com/watch?v=cuX5QQXbLDQ',
        )
    except Exception as e:
        print(str(e))
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook_view(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
              payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )
        client_id = session.metadata.client_id
        box_id = session.metadata.box_id
        client = Client.objects.get(id=client_id)
        box = Box.objects.create(id=box_id)
        box_price = box.price
        Rent.objects.create(box=box, client=client, box_price=box_price)

    return HttpResponse(status=200)
