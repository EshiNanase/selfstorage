from django.shortcuts import render


def show_my_orders(request):
    orders = [
        {
            'storage': {
                'title': 'Мой склад №1',
                'address': 'Одинцово, ул. Северная, д. 36',
                'box': {
                    'name': 'Мой бокс',
                    'number': '№2389-12'
                }
            },
            'expired_soon': True,
            'started_at': '15.03.2022',
            'expired_at': '28.06.2022'
        },
        {
            'storage': {
                'title': 'Мой склад №2',
                'address': 'Люберцы, ул. Советская, д. 88',
                'box': {
                    'name': 'Мой бокс',
                    'number': '№2335-10'
                }
            },
            'expired_soon': False,
            'started_at': '18.03.2022',
            'expired_at': '21.09.2022'
        }
    ]
    context = {
        'orders': orders,
        'client': {
            'name': 'Екатерина'
        }
    }
    return render(request, template_name='active-storages.html', context=context)
