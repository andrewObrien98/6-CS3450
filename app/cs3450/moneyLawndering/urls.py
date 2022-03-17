from django.urls import path

from . import views

app_name = 'moneyLawndering'
urlpatterns = [
    path('', views.index, name='signin'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('createuser/', views.createUser, name='createUser'),
    path('<int:user_id>/updateuser/', views.updateUser, name='updateUser'),
    path('<int:user_id>/account/', views.account, name='account'),
    path('<int:user_id>/', views.account, name='account'),
    path('<int:user_id>/publiclistings/', views.publicListing, name='publicListing'),
    path('<int:user_id>/<int:listing_id>/acceptlisting/', views.acceptListing, name='acceptListing'),
    path('<int:user_id>/mylistings/', views.myListing, name='myListing'),
    path('<int:user_id>/createListing/', views.createListing, name='createListing'),
    path('<int:user_id>/newListing/', views.newListing, name='newListing'),
    path('<int:user_id>/acceptedjobs/', views.acceptedJobs, name='acceptedJobs'),
    path('<int:user_id>/directtransfer/', views.directTransfer, name='directTransfer'),
    path('<int:user_id>/history/', views.history, name='history'),
    path('<int:user_id>/admin/', views.admin, name='admin'),
    path('<int:user_id>/sendMoney/', views.sendMoney, name='sendMoney'),
]