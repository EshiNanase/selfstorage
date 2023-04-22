import stripe
from django.conf import settings
from django.shortcuts import redirect
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
            success_url='http://81.163.31.199/profile/',
        )
    except Exception as e:
        print(str(e))
    return redirect(checkout_session.url, code=303)
