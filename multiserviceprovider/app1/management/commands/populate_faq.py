# yourapp/management/commands/populate_faq.py
from django.core.management.base import BaseCommand
from app1.models import FAQ

class Command(BaseCommand):
    help = 'Populate FAQ data in the database'

    def handle(self, *args, **options):
        # Clear existing data
        FAQ.objects.all().delete()

        # Add new FAQ entries
        faq_entries = [
             {'category': 'provider', 'question': 'How reliable are service providers?', 'answer': 'Service providers are rated based on their reliability, customer feedback, and performance. You can view provider ratings and reviews to assess their reliability.'},
            {'category': 'provider', 'question': 'What criteria determine a provider\'s reliability?', 'answer': 'A provider\'s reliability is determined by factors such as on-time service delivery, customer satisfaction, and adherence to service standards.'},
            {'category': 'provider', 'question': 'How do providers ensure quality service?', 'answer': 'Providers are expected to adhere to quality standards set by the platform. Additionally, customer reviews and ratings help maintain service quality standards.'},
            {'category': 'provider', 'question': 'Can I trust providers for multiple services?', 'answer': 'Yes, providers offering multiple services are generally reliable. You can check reviews specific to each service they offer to ensure their competence.'},
            {'category': 'provider', 'question': 'What should I consider when choosing a service provider?', 'answer': 'Consider provider ratings, customer reviews, and the variety of services offered. Choose a provider that aligns with your specific service requirements and preferences.'},
            
            {'category': 'booking', 'question': 'How to book a service?', 'answer': 'To book a service, follow these steps... 1-select the desired service , 2- Choose the desired provider, 3 - Click the book service option , 4- Give the booking details and press the book option and you have completed your booking '},
            {'category': 'booking', 'question': 'What details are required for booking?', 'answer': 'When booking a service, provide details such as date of booking contact information '},
            {'category': 'booking', 'question': 'How many bookings can I make at once?', 'answer': 'You can make only a single bookings at a time. Once the service is marked as complete you can book other service.'},
            {'category': 'booking', 'question': 'Can I modify the details of a booking after confirmation?', 'answer': 'Yes, you can modify the details of a booking after confirmation like resheduling your booking date '},
            {'category': 'booking', 'question': 'Are there any fees associated with bookings?', 'answer': 'Booking fees may apply after the booking is accepted by the provider. Check the terms and conditions for more information.'},
            
            {'category': 'order', 'question': 'How to track my order?', 'answer': 'You can track your order by using track order option given at the home page'},
            {'category': 'order', 'question': 'What if my order is delayed?', 'answer': 'In case of order delays, you can contact the provider for the issue or raise a complaint'},
            {'category': 'order', 'question': 'How to cancel an order?', 'answer': 'To cancel an order, go to your track order option and give the reason for cancelation and request cancelation.'},
            {'category': 'order', 'question': 'What payment methods are accepted for orders?', 'answer': 'Accepted payment methods for orders include NetBanking,UPI,Credit Card,Debit Card'},
            {'category': 'order', 'question': 'Can I change the delivery address after placing an order?', 'answer': 'Changing the delivery address after placing an order is possible within a certain timeframe.'},
            {'category': 'order', 'question': 'How can I view the detailed status of my order?', 'answer': 'To view the detailed status of your order, navigate to the "Order History" section and select the specific order. You will find comprehensive information, including order processing, dispatch, and delivery status.'},
           
           {'category': 'payment', 'question': 'How to update payment information?', 'answer': 'Updating payment information can be done by accessing your account settings. Navigate to the "Payment Methods" section and choose the option to edit or add a new payment method.'},
            {'category': 'payment', 'question': 'What if my payment is declined?', 'answer': 'If your payment is declined, please ensure that you have sufficient funds in your account or check the accuracy of your payment details. You may also contact your bank or financial institution for assistance. If the issue persists, try using an alternative payment method.'},
            {'category': 'payment', 'question': 'Are there any additional charges for certain payment methods?', 'answer': 'No.There will not be any additional charges'},
            {'category': 'payment', 'question': 'How to request a refund?', 'answer': 'To request a refund, go to the "Order History" section, select the specific order, and look for the option to request a refund. Provide a reason for the refund request and submit the form. The customer support team will review your request and process the refund accordingly.'},
            {'category': 'payment', 'question': 'Can I change my default payment method?', 'answer': 'Yes, you can change your default payment method by accessing your account settings. Navigate to the "Payment Methods" section, choose the preferred payment method, and set it as the default. This ensures that the selected payment method is used for future transactions.'},
            
             {'category': 'cancellation', 'question': 'What is the cancellation policy?', 'answer': 'The cancellation policy specifies the terms and conditions for canceling orders or subscriptions. It outlines the timeframe within which cancellations are accepted, any applicable fees, and the process for initiating a cancellation. Always review the cancellation policy before making a purchase.'},
            {'category': 'cancellation', 'question': 'How to cancel a booking?', 'answer': 'To cancel a booking, log in to your account, navigate to the "Bookings" and locate the option to cancel the booking. Follow the on-screen instructions, provide any required information, and confirm the cancellation. Be sure to complete the process before the next billing cycle to avoid additional charges.'},
            {'category': 'cancellation', 'question': 'Is there a fee for order cancellations?', 'answer': 'Cancellation fees may apply depending on the specific terms outlined in the cancellation policy. Some orders or subscriptions may incur fees if canceled after a certain period or under specific conditions. Refer to the cancellation policy for information on any applicable fees.'},
            {'category': 'cancellation', 'question': 'Can I reactivate a canceled subscription?', 'answer': 'Reactivating a canceled booking is not currently possible.'},
            {'category': 'cancellation', 'question': 'How to dispute a cancellation fee?', 'answer': 'If you believe a cancellation fee is unjust, you can dispute it by reaching out to customer support. Provide detailed information about the situation, including any relevant documentation or evidence. The customer support team will review your dispute and communicate the resolution.'},
        ]

        for entry in faq_entries:
            FAQ.objects.create(
                category=entry['category'],
                question=entry['question'],
                answer=entry['answer']
            )

        self.stdout.write(self.style.SUCCESS('FAQ data successfully populated.'))
