
from django.urls import path
from FrontEnd import views

urlpatterns = [

    path('Login_page/', views.Login_page, name="Login_page"),
    path('Signup_page/', views.Signup_page, name="Signup_page"),
    path('save_user/', views.save_user, name="save_user"),
    path('login_view/', views.login_view, name="login_view"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('Forgot_page/', views.Forgot_page, name="Forgot_page"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('verification_page/', views.verification_page, name="verification_page"),
    path('change_password/<str:token>/', views.change_password, name="change_password"),


    path('index_page/', views.index_page, name="index_page"),
    path('Home_page/',views.Home_page,name="Home_page"),
    path('About_page/', views.About_page, name="About_page"),
    path('Contact_page/', views.Contact_page, name="Contact_page"),



    path('user_painting/', views.user_painting, name="user_painting"),
    path('user_paintings_save/', views.user_paintings_save, name="user_paintings_save"),
    path('user_painting_edit/<int:p_id>', views.user_painting_edit, name="user_painting_edit"),
    path('user_painting_update/<int:p_id>', views.user_painting_update, name="user_painting_update"),
    path('search_painting/', views.search_painting, name="search_painting"),
    path('predict_artist/', views.predict_artist, name="predict_artist"),




    path('learn_art/', views.learn_art, name="learn_art"),
    path('learn_art_save/', views.learn_art_save, name="learn_art_save"),
    path('watercolour_painting/', views.watercolour_painting, name="watercolour_painting"),
    path('digital_painting/', views.digital_painting, name="digital_painting"),
    path('oil_painting/', views.oil_painting, name="oil_painting"),
    path('encastic_painting/', views.encastic_painting, name="encastic_painting"),
    path('acrylic_painting/', views.acrylic_painting, name="acrylic_painting"),
    path('mixedmedia_painting/', views.mixedmedia_painting, name="mixedmedia_painting"),





    path('Shop/', views.Shop, name="Shop"),
    path('shop_filter/', views.shop_filter, name="shop_filter"),
    path('search/', views.search, name="search"),
    path('Single_page/<int:p_id>/', views.Single_page, name="Single_page"),


    path('Cart_page/', views.Cart_page, name="Cart_page"),
    path('save_cart/', views.save_cart, name="save_cart"),
    path('Update_cart/', views.Update_cart, name="Update_cart"),
    path('delete_cart/', views.delete_cart, name="delete_cart"),
    path('Checkout_page/',views.Checkout_page,name="Checkout_page"),
    path('apply_coupon/',views.apply_coupon,name="apply_coupon"),
    path('remove_active_coupon/', views.remove_active_coupon, name='remove_active_coupon'),
    path('payment_section/', views.payment_section, name="payment_section"),
    path('place_order/', views.place_order, name="place_order"),
    path('order_confirmed/<str:order_id>', views.order_confirmed, name="order_confirmed"),
    path('ordersbook/', views.ordersbook, name="ordersbook"),
    path('order_view/<int:order_id>', views.order_view, name="order_view"),
    path('cancel_order/<int:order_id>', views.cancel_order, name="cancel_order"),
    path('delete_selected_orders/', views.delete_selected_orders, name="delete_selected_orders"),

    path('profile_page/', views.profile_page, name="profile_page"),
    path('profile_create/', views.profile_create, name="profile_create"),
    path('save_profile/', views.save_profile, name="save_profile"),
    path('profile_edit/', views.profile_edit, name="profile_edit"),
    path('update_profile/<int:p_id>/', views.update_profile, name="update_profile"),
    path('delete_profile', views.delete_profile, name="delete_profile"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('delete_wishlist/', views.delete_wishlist, name="delete_wishlist"),
    path('profile_user_paintings/',views.profile_user_paintings,name="profile_user_paintings"),
    path('delete_painting/', views.delete_painting, name='delete_painting'),
    path('addressbook/',views.addressbook,name="addressbook"),
    path('addaddress/',views.addaddress,name="addaddress"),
    path('save_address/',views.save_address,name="save_address"),
    path('Edit_address/<int:a_id>/',views.Edit_address,name="Edit_address"),
    path('update_address/<int:a_id>/',views.update_address,name="update_address"),
    path('delete_selected_addresses/', views.delete_selected_addresses, name='delete_selected_addresses'),
    path('ordersbook/', views.ordersbook, name='ordersbook'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('profile_change_password/',views.profile_change_password,name="profile_change_password"),





]