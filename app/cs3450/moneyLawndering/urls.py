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
    path('<int:user_id>/publiclistings/', views.publicListing, name='publicListing'),
<<<<<<< HEAD
    path('<int:user_id>/acceptlisting/', views.acceptListing, name='acceptListing'),
    path('<int:user_id>/mylistings/', views.myListing, name='myListing'),
    path('<int:user_id>/createListing/', views.createListing, name='createListing'),
    path('<int:user_id>/newListing/', views.newListing, name='newListing'),
=======
    path('<int:user_id>/mylisting/', views.myListing, name='myListing'),
    path('<int:user_id>/newlisting/', views.newListing, name='newListing'),
>>>>>>> 773817f276debc9d13de22bbd0e1d6296e27b5f3
    path('<int:user_id>/acceptedjobs/', views.acceptedJobs, name='acceptedJobs'),
    path('<int:user_id>/directtransfer/', views.directTransfer, name='directTransfer'),
    path('<int:user_id>/history/', views.history, name='history'),

]