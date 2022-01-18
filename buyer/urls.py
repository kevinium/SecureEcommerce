from django.urls import path
from . import views

app_name='buyer'

urlpatterns=[
    path('home/',views.home_page),
    path('product/<slug>/',views.ItemDetailView.as_view(),name='product'),
    path('add-to-cart/<slug>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',views.remove_from_cart,name='remove-from-cart'),
    path('order-summary/',views.OrderSummaryView.as_view(),name='order-summary'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('checkout/',views.CheckoutView.as_view(),name='checkout'),
    path('pay/',views.pay,name='pay'),
    path('pay/payment-status/',views.payment_status,name='payment-status'),
    path('profile/',views.profile),
    path('add_product/', views.add_prod, name='addProd'),
    path('pay/payment-status/success',views.payment_status_success,name='payment-status-success'),
    path('pay/payment-status/failure',views.payment_status_failure,name='payment-status-failure'),
    path('search/',views.search,name='search'),
    path('logout/', views.logout_view, name='logout'),
    path('home/upgrade', views.addSeller),
    path('upgrade/', views.addSeller),
    path('admin-home/', views.admin_view,name='admin-home'),
    path('reset-account/<slug>/',views.reset_account,name='reset-account'),
    path('open-pdf/pdf/<slug>/',views.open_pdf,name='open-pdf'),
    path('remove-item/<slug>/',views.remove_item,name='remove-item'),
    path('updateProfile/', views.update_address, name='updateProfile'),
]