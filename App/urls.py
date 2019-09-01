from django.urls import path, re_path

from App import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('market/', views.market, name='market'),
    path('cart/', views.cart, name='cart'),
    path('mine/', views.mine, name='mine'),
    re_path('marketwithparams/(\d+)/(\d+)/(\d+)/', views.market_with_params, name='market_with_params'),
    path('userregister/', views.user_register, name='user_register'),
    path('userlogout/', views.user_logout, name='user_logout'),
    path('checkuser/', views.check_user, name='check_user'),
    path('checkemail/', views.check_email, name='check_email'),
    path('userlogin/', views.user_login, name='user_login'),
    path('activeaccount/', views.active_account, name='active_account'),
    path('addtocart/', views.add_to_cart, name='add_to_cart'),
    path('subtocart/', views.sub_to_cart, name='sub_to_cart'),
    path('changecartstatus/', views.change_cart_status, name='change_cart_status'),
    path('changecartsstatus/', views.change_carts_status, name='change_carts_status'),
    path('makeorder/', views.make_order, name='make_order'),
    path('orderdetail/', views.order_detail, name='order_detail'),
    path('alipaycallback/', views.alipay_callback, name='alipay_callback')
]