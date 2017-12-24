from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def OrderCreated(order_id):
    """
    Отправка Email сообщения о создании покупке
    """
    print('Enetereed TASKS ')
    order = Order.objects.get(id=order_id)
    subject = 'Order Number {}'.format(order.id)
    message = 'Dear, {}, you successfully made order.\
               Number of your order {}'.format(order.first_name, order.id)
    print('MAIL SNDINFg')
    mail_send = send_mail(subject, message, 'admin@myshop.ru', ['maulenkemalov@gmail.com'])
    return mail_send
