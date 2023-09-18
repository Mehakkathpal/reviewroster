from django.shortcuts import render
import stripe
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
from rest_framework.views import APIView
from .models import subscriptionStatus
from .serializers import subscriptionStatusserializer
from django.http import HttpResponse


stripe.api_key = ""

class subscriptionStatusView(APIView):
    def get(self,request):
        data = request.data
        customer_email = data.get("email",None)
        if(customer_email is None):
            customers_subscriptions  =  subscriptionStatus.objects.all()
            serializer = subscriptionStatusserializer(customers_subscriptions,many=True)
            return(Response(serializer.data))
        else:
            customer_subscriptions = subscriptionStatus.objects.filter(customer_email = customer_email)
            serializer = subscriptionStatusserializer(customers_subscriptions)
            return(Response(serializer.data))
    def post(self,request):
        data = request.data
        serializer = subscriptionStatusserializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def get_subscription_status(request):
  data = request.data
  email = data.get("email")
  subscribed=False
  customers = subscriptionStatus.objects.filter(customer_email=email)
  if(customers):
    subscribed = True
  else:
    product_id = "price_1NpQWSSHdkZh1gwbcpAYswOX"
    customers = stripe.Customer.list()
    for customer in customers.auto_paging_iter():
        if customer.email == email:
            subscriptions = stripe.Subscription.list(customer=customer.id)
            for subscription in subscriptions.auto_paging_iter():
                if(subscription.plan.id == product_id):
                    subscribed=True
                    break
  return JsonResponse({'subscribed':subscribed})


@api_view(['POST'])
def success_view(request):
    data = request.data
    session_id = data.get('session_id')
    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        customer_email = checkout_session.customer_details.email
        customers = subscriptionStatus.objects.filter(customer_email=customer_email)
        if(len(customers) == 0):
            customer_id = checkout_session.get('customer')
            subscription_data = {'customer_email': customer_email, 'customer_id': customer_id, "is_subscibed": True}
            serializer = subscriptionStatusserializer(data=subscription_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse({"customer_id": customer_id, "subscribed": True})
            else:
                return HttpResponse({"Error": serializer.errors})
        else:
            return HttpResponse({"message":"Record already exist"})
    except Exception as e:
        return HttpResponse({"Error": str(e)})


@api_view(["POST"])
def create_payment_intent(request):
        data = request.data
        customer_id = data.get("customerId")
        payment_method_id = data["payment_method_id"]
        payment_intent = stripe.PaymentIntent.create(
                amount=1000,
                currency="inr",
                payment_method_types=["card"],
                customer=customer_id,
                payment_method=payment_method_id,
                confirm=True,
                setup_future_usage="off_session", 
            )
        if payment_intent.status == "requires_action" and payment_intent.next_action.type == "use_stripe_sdk":
            return JsonResponse({"requires_action": True, "payment_intent_client_secret": payment_intent.client_secret,
            "payment_method_id":payment_method_id,"customer_id":customer_id})

@api_view(["POST"])
def save_stripe_info(request):
    data = request.data
    email = data["email"]
    payment_method_id = data["payment_method_id"]
    extra_msg = ""
    customer_data = stripe.Customer.list(email=email).data
    if len(customer_data) == 0:
        customer = stripe.Customer.create(email=email, payment_method=payment_method_id)

    else:
        customer = customer_data[0]
        extra_msg = "Card Details already Saved."

    return Response(
        status=status.HTTP_200_OK,
        data={
            "message": "Card Details Added.",
            "data": {"customer_id": customer.id},
            "extra_msg": extra_msg,
        },
    )

@api_view(["POST"])
def process_payment(request):
    if request.method == "POST":
        data = request.data
        token = data["token"]
        customer_id = data.get("customerID")
        intent_id = data.get("intentid")
        payment_method_id = data["payment_method_id"]
        try:
            # stripe.PaymentIntent.confirm(intent_id)
            stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)
            subscription = stripe.Subscription.create(
            customer=customer_id,
                    items=[
                        {
                            "price": "price_1NpQWSSHdkZh1gwbcpAYswOX",
                        },
                    ],
                      payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
                )
            return JsonResponse({"success": subscription,"subscriptionId":subscription.id, "clientSecret":subscription.latest_invoice.payment_intent.client_secret})
        except stripe.error.StripeError as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})

@api_view(['GET'])
def create_checkout_session(request):
    YOUR_DOMAIN = "http://localhost:3000"  # Replace with your actual domain

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                "price": "price_1NpQWSSHdkZh1gwbcpAYswOX",
                'quantity': 1,
            }],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/canceled',
        )
        return JsonResponse({'checkout_session_url':checkout_session.url})
    except Exception as e:
        return JsonResponse({'error': str(e)})



@api_view(['GET'])
def get_balance(request):
    return JsonResponse({"Balance":stripe.Balance.retrieve()})
