from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import OrderCreated
from .models import Order

from django.contrib.admin.views.decorators import staff_member_required


from django.core.mail import send_mail
def test():
    print('Enetereed TASKS ')
    subject = 'Order number{}'
    message = 'Dear, {},you c.\
               kookokoko {}'

    send_mail(subject, message, 'admin@myshop.ru', ['maulenkemalov@gmail.com'])

def send(to, message):
    import boto3
    import json
    import smtplib
    TO = to
    SUBJECT = 'book subscription'
    TEXT = message

    # Gmail Sign In
    gmail_sender = 'maulenkemalov@gmail.com'
    gmail_passwd = '4815162342maulen'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()

def trs(order_id):
    import boto3

    order = Order.objects.get(id=order_id)
    subject = 'Order Number {}'.format(order.id)
    message = 'Dear, {}, you successfully made order.\
               Number of your order {}'.format(order.first_name, order.id)


    AWS_ACCESS_KEY = 'AKIAJN4YGZEGBSRBC3CQ'     # enter your access key id
    AWS_SECRET_ACCESS_KEY = 'NJJ3U2kgxfbFEPu/eV7Bqacmv5DnNBXVGUIk+yVA' # enter your secret access key
    sqs = boto3.resource('sqs', aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name='us-east-1'
                         )

    queue = sqs.get_queue_by_name(QueueName='maulen-project')


    queue.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/323571053896/maulen-project',
        MessageAttributes={
            'Subject': {
                'DataType': 'String',
                'StringValue': str(subject)
            },
            'Email': {
                'DataType': 'String',
                'StringValue': str( order.email)
            },
            'Message': {
                'DataType': 'String',
                'StringValue': str(message)
            }
        },
        MessageBody=(
            'Information about current order receiver '
        )
    )
def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.cupon:
                order.cupon = cart.cupon
                order.discount = cart.cupon.discount
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # test()
            # Асинхронная отправка сообщения
            # OrderCreated.delay(order.id)
            #
            trs(order.id)
            return render(request, 'orders/order/created.html', {'order': order})

    form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})

#
@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})
