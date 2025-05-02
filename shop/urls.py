from django.urls import path
from .views import (
    CompanyInfoView, 
    admin_page, 
    FoodListAPIView, 
    delete_food,
    order_tracking,
    update_order_status,
    OrderAPIView,
    OrderTrackingAPIView,
    UpdateOrderStatusAPIView,
    delete_order,
    CreateRazorpayOrder,
    GetPaymentDetails,
    VerifyRazorpayPayment,
    GetOrderDetails,
    TransactionListView,
)

# API endpoints
api_patterns = [
    path('company-info/', CompanyInfoView.as_view(), name='company-info'),
    path('foods/', FoodListAPIView.as_view(), name='food-list'),
    path('orders/', OrderAPIView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderAPIView.as_view(), name='order-detail'),
    path('order-tracking/', OrderTrackingAPIView.as_view(), name='order-tracking-api'),
    path('update-order-status/<int:order_id>/', UpdateOrderStatusAPIView.as_view(), name='update-order-status-api'),
    path('create-razorpay-order/', CreateRazorpayOrder.as_view(), name='create-razorpay-order'),
    path('verify-razorpay-payment/', VerifyRazorpayPayment.as_view(), name='verify-razorpay-payment'),
    path('payment-details/<str:payment_id>/', GetPaymentDetails.as_view(), name='get-payment-details'),
    path('order-details/<str:order_id>/', GetOrderDetails.as_view(), name='get-order-details'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    
]

# Admin views
admin_patterns = [
    path('admin-panel/', admin_page, name='admin-page'),
    path('delete-food/<int:food_id>/', delete_food, name='delete-food'),
    path('admin/order-tracking/', order_tracking, name='order-tracking'),
    path('admin/update-order-status/<int:order_id>/', update_order_status, name='update-order-status'),
    path('admin/delete-order/<int:order_id>/', delete_order, name='delete-order'),
]

urlpatterns = api_patterns + admin_patterns
