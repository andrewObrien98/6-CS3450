from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('<int:user_id>/account/', views.account, name='account'),
    path('publiclistings/', views.publicListing, name='publicListing'),
    path('<int:user_id>/mylistings/', views.myListing, name='myListing'),
    path('newListing/', views.newListing, name='newListing'),
    path('<int:user_id>/acceptedjobs/', views.acceptedJobs, name='acceptedJobs'),
    path('<int:user_id>/directtransfer/', views.directTransfer, name='directTransfer'),
    path('<int:user_id>/history/', views.history, name='history'),

]