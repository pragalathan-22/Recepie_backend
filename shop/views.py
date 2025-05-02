from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CompanyInfo, FoodItem, Order, OrderItem
from .serializers import CompanyInfoSerializer, FoodSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CompanyInfoForm, FoodItemForm, OrderStatusForm
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.utils import timezone
from .razorpay_config import create_order, verify_payment

class CompanyInfoView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        company = CompanyInfo.objects.first()
        if company:
            serializer = CompanyInfoSerializer(company, context={'request': request})
            return Response(serializer.data)
        return Response({'error': 'Company info not found'}, status=status.HTTP_404_NOT_FOUND)

class FoodListAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            data = {
                'top_rated': FoodSerializer(
                    FoodItem.objects.filter(category='top'), 
                    many=True, 
                    context={'request': request}
                ).data,
                'recommended': FoodSerializer(
                    FoodItem.objects.filter(category='recommended'), 
                    many=True, 
                    context={'request': request}
                ).data,
                'all': FoodSerializer(
                    FoodItem.objects.filter(category='all'), 
                    many=True, 
                    context={'request': request}
                ).data,
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = OrderSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                order = serializer.save()
                return Response(OrderSerializer(order, context={'request': request}).data, 
                              status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, order_id=None):
        try:
            if order_id:
                order = get_object_or_404(Order, id=order_id)
                serializer = OrderSerializer(order, context={'request': request})
                return Response(serializer.data)
            
            orders = Order.objects.all().order_by('-created_at')
            serializer = OrderSerializer(orders, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Admin views
def admin_page(request):
    company = CompanyInfo.objects.first()
    company_form = CompanyInfoForm(request.POST or None, request.FILES or None, instance=company)
    food_form = FoodItemForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if 'save_company' in request.POST and company_form.is_valid():
            company_form.save()
        if 'add_food' in request.POST and food_form.is_valid():
            food_form.save()
        return redirect('admin-page')

    foods = FoodItem.objects.all()
    return render(request, 'admin/company_setup.html', {
        'company_form': company_form,
        'food_form': food_form,
        'foods': foods,
    })

def delete_food(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    food.delete()
    return redirect('admin-page')

def order_tracking(request):
    filter_type = request.GET.get('filter', 'today')
    selected_date = request.GET.get('date')
    
    orders = Order.objects.all().order_by('-created_at')
    
    if filter_type == 'today':
        today = timezone.now().date()
        orders = orders.filter(created_at__date=today)
    elif filter_type == 'monthly':
        this_month = timezone.now().month
        this_year = timezone.now().year
        orders = orders.filter(created_at__month=this_month, created_at__year=this_year)
    elif filter_type == 'yearly':
        this_year = timezone.now().year
        orders = orders.filter(created_at__year=this_year)
    elif filter_type == 'custom' and selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        orders = orders.filter(created_at__date=selected_date)
    
    total_orders = orders.count()
    total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    status_counts = orders.values('status').annotate(count=Count('id'))
    
    return render(request, 'admin/order_tracking.html', {
        'orders': orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'status_counts': status_counts,
        'filter_type': filter_type,
        'selected_date': selected_date,
    })

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order-tracking')
    else:
        form = OrderStatusForm(instance=order)
    
    return render(request, 'admin/update_order_status.html', {
        'form': form,
        'order': order,
    })

class OrderTrackingAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            filter_type = request.GET.get('filter', 'today')
            selected_date = request.GET.get('date')
            
            orders = Order.objects.all().order_by('-created_at')
            
            if filter_type == 'today':
                today = timezone.now().date()
                orders = orders.filter(created_at__date=today)
            elif filter_type == 'monthly':
                this_month = timezone.now().month
                this_year = timezone.now().year
                orders = orders.filter(created_at__month=this_month, created_at__year=this_year)
            elif filter_type == 'yearly':
                this_year = timezone.now().year
                orders = orders.filter(created_at__year=this_year)
            elif filter_type == 'custom' and selected_date:
                selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
                orders = orders.filter(created_at__date=selected_date)
            
            total_orders = orders.count()
            total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
            status_counts = orders.values('status').annotate(count=Count('id'))
            
            data = {
                'orders': OrderSerializer(orders, many=True, context={'request': request}).data,
                'statistics': {
                    'total_orders': total_orders,
                    'total_revenue': float(total_revenue),
                    'status_counts': list(status_counts)
                }
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            filter_type = request.data.get('filter', 'today')
            selected_date = request.data.get('date')
            
            orders = Order.objects.all().order_by('-created_at')
            
            if filter_type == 'today':
                today = timezone.now().date()
                orders = orders.filter(created_at__date=today)
            elif filter_type == 'monthly':
                this_month = timezone.now().month
                this_year = timezone.now().year
                orders = orders.filter(created_at__month=this_month, created_at__year=this_year)
            elif filter_type == 'yearly':
                this_year = timezone.now().year
                orders = orders.filter(created_at__year=this_year)
            elif filter_type == 'custom' and selected_date:
                selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
                orders = orders.filter(created_at__date=selected_date)
            
            total_orders = orders.count()
            total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
            status_counts = orders.values('status').annotate(count=Count('id'))
            
            data = {
                'orders': OrderSerializer(orders, many=True, context={'request': request}).data,
                'statistics': {
                    'total_orders': total_orders,
                    'total_revenue': float(total_revenue),
                    'status_counts': list(status_counts)
                }
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateOrderStatusAPIView(APIView):
    permission_classes = [AllowAny]
    
    def patch(self, request, order_id):
        try:
            order = get_object_or_404(Order, id=order_id)
            serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order-tracking')

#--------------

import razorpay
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreateRazorpayOrder(APIView):
    def post(self, request):
        try:
            amount = request.data.get('amount')  # Amount in rupees
            currency = request.data.get('currency', 'INR')
            receipt = request.data.get('receipt', None)
            notes = request.data.get('notes', {})

            if not amount:
                return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

            order_data = {
                "amount": int(amount) * 100,  # Convert to paise
                "currency": currency,
                "payment_capture": 1
            }

            if receipt:
                order_data["receipt"] = receipt
            if notes:
                order_data["notes"] = notes

            order = client.order.create(order_data)
            
            return Response({
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "receipt": order.get("receipt"),
                "key_id": settings.RAZORPAY_KEY_ID
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyRazorpayPayment(APIView):
    def post(self, request):
        try:
            data = request.data
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')
            amount = data.get('amount')

            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            client.utility.verify_payment_signature(params_dict)

            # Save successful transaction
            Transaction.objects.create(
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
                amount=amount,
                status="Success"
            )

            return Response({"status": "Payment Successful"})

        except razorpay.errors.SignatureVerificationError:
            # Save failed transaction
            Transaction.objects.create(
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
                amount=amount,
                status="Failed"
            )
            return Response({"status": "Payment Verification Failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetPaymentDetails(APIView):
    def get(self, request, payment_id):
        try:
            payment = client.payment.fetch(payment_id)
            return Response(payment)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetOrderDetails(APIView):
    def get(self, request, order_id):
        try:
            order = client.order.fetch(order_id)
            return Response(order)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


