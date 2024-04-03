from django.urls import path
from BackEnd import views
urlpatterns=[
    path('index_page/',views.index_page,name="index_page"),
    path('paintings_form/',views.paintings_form,name="paintings_form"),
    path('paintings_type_form/',views.paintings_type_form,name="paintings_type_form"),
    path('paintings_type_table/',views.paintings_type_table,name="paintings_type_table"),
    path('paintings_type_delete/<int:p_id>',views.paintings_type_delete,name="paintings_type_delete"),
    path('paintings_save/',views.paintings_save,name="paintings_save"),
    path('paintings_table/',views.paintings_table,name="paintings_table"),
    path('paintings_edit/<int:p_id>',views.paintings_edit,name="paintings_edit"),
    path('paintings_update/<int:p_id>',views.paintings_update,name="paintings_update"),
    path('paintings_delete/<int:p_id>',views.paintings_delete,name="paintings_delete"),
    path('paintings_type_save/',views.paintings_type_save,name="paintings_type_save"),



    path('artist_form/', views.artist_form, name="artist_form"),
    path('artist_save/', views.artist_save, name="artist_save"),
    path('artist_table/', views.artist_table, name="artist_table"),
    path('artist_edit/<int:a_id>', views.artist_edit, name="artist_edit"),
    path('artist_update/<int:a_id>', views.artist_update, name="artist_update"),
    path('artist_delete/<int:a_id>', views.artist_delete, name="artist_delete"),



    path('contact_save/',views.contact_save,name="contact_save"),
    path('contact_table/',views.contact_table,name="contact_table"),
    path('contact_delete/<int:c_id>/',views.contact_delete,name="contact_delete"),


    path('Coupon/',views.Coupon,name="Coupon"),
    path('save_coupon/',views.save_coupon,name="save_coupon"),
    path('display_coupon/',views.display_coupon,name="display_coupon"),
    path('edit_coupon/<int:c_id>/',views.edit_coupon,name="edit_coupon"),
    path('update_coupon/<int:c_id>/',views.update_coupon,name="update_coupon"),
    path('delete_coupon/<int:c_id>/',views.delete_coupon,name="delete_coupon"),
    path('activate_coupon/', views.activate_coupon, name='activate_coupon'),
    path('deactivate_coupon/', views.deactivate_coupon, name='deactivate_coupon'),
    path('check_coupon_status/', views.check_coupon_status, name='check_coupon_status'),


    path('user_orders/', views.user_orders, name='user_orders'),
    path('order_details/<str:username>/', views.order_details, name='order_details'),


    path('learning_art_form/', views.learning_art_form, name='learning_art_form'),
    path('learning_art_save/', views.learning_art_save, name='learning_art_save'),


]