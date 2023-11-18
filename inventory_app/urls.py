from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.ItemListView.as_view(), name='items'), 
    path('items/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('items/create_item/', views.createItem, name='create_item'),
    path('items/update_item/<int:item_id>', views.updateItem, name='update_item'), 
    path('items/delete_item/<int:item_id>', views.deleteItem, name='delete_item'),

    # accounts/ login/ [name='login']
    # accounts/ logout/ [name='logout']
    # accounts/ password_change/ [name='password_change']
    # accounts/ password_change/done/ [name='password_change_done']
    # accounts/ password_reset/ [name='password_reset']
    # accounts/ password_reset/done/ [name='password_reset_done']
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/ reset/done/ [name='password_reset_complete']
    path('accounts/register/', views.registerPage, name = 'register_page'),
    path('accounts/login/', views.loginPage, name = 'login'),
    path('accounts/logout/', views.logoutUser, name = 'logout'),
]
