from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
import stripe
from .models import PaymentDetails
from instructor.models import Course, UserCourses
from users.models import CustomUser
from .serializers import PaymentDetailSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            course_id = self.kwargs["pk"]
            course = Course.objects.get(id=course_id)
            user_id = request.user.id
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "unit_amount": int(course.price * 100),
                            "product_data": {
                                "name": course.title,
                                "images": [
                                    "https://blog.coursify.me/wp-content/uploads/2014/12/e-learning-platform-coursifyme.jpg"
                                ],
                            },
                        },
                        "quantity": 1,
                    },
                ],
                metadata={
                    "course_id": course.id,
                    "user_id": user_id,
                },
                mode="payment",
                success_url=settings.SITE_URL + "/chapters?success=true&courseId=" + str(course_id) + "&session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.SITE_URL + "/chapters?canceled=true&courseId=" + str(course_id),
            )
            return Response(
                {
                    "redirect_url": checkout_session.url,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Unable to process the payment now. Error: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers["STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if (
        event["type"] == "checkout.session.completed"
        or event["type"] == "checkout.session.async_payment_succeeded"
    ):
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]
        course_id = session["metadata"]["course_id"]
        payment_id = session["payment_intent"]
        status = session["payment_status"]
        total_amount = session["amount_total"]

        try:
            with transaction.atomic():
                user = CustomUser.objects.get(id=user_id)
                course = Course.objects.get(id=course_id)

                user_courses, created = UserCourses.objects.get_or_create(
                    student=user, course=course
                )

                price_in_rupees = total_amount / 100
                payment_detail = PaymentDetails.objects.create(
                    user=user,
                    payment_id=payment_id,
                    course=course,
                    price=price_in_rupees,
                    payment_status=status,
                )
                print(payment_detail, "payment_detail")

        except CustomUser.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Course.DoesNotExist:
            return JsonResponse({"message": "Course not found"}, status=404)
    else:
        print("Unhandled event type {}".format(event["type"]))
    return HttpResponse(status=200)


class PaymentDetailsListCreateEdit(generics.ListCreateAPIView):
    serializer_class = PaymentDetailSerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return PaymentDetails.objects.filter(user=user_id)


class OrderHistoryList(ListAPIView):
    queryset = PaymentDetails.objects.all()
    serializer_class = PaymentDetailSerializer
