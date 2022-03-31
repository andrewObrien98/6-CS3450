from django.urls import path

from . import views

app_name = 'moneyLawndering'
urlpatterns = [
    path('', views.index, name='signin'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('createuser/', views.createUser, name='createUser'),
    path('updateuser/', views.updateUser, name='updateUser'),
    path('account/', views.account, name='account'),
    path('publiclistings/', views.publicListing, name='publicListing'),
    path('<int:listing_id>/acceptlisting/', views.acceptListing, name='acceptListing'),
    path('mylistings/', views.myListing, name='myListing'),
    path('<int:listing_id>/updateListing/', views.updateListing, name='updateListing'),
    path('<int:listing_id>/deleteListing/', views.deleteListing, name='deleteListing'),
    path('createListing/', views.createListing, name='createListing'),
    path('newListing/', views.newListing, name='newListing'),
    path('acceptedjobs/', views.acceptedJobs, name='acceptedJobs'),
    path('directtransfer/', views.directTransfer, name='directTransfer'),
    path('history/', views.history , name='history'),
    path('<int:listing_id>/applicantlist/', views.applicantList, name='applicantlist'),
    path('acceptapplicant/<int:listing_id>/<int:worker_id>', views.acceptApplicant, name='acceptApplicant'),
    path('completedJob/<int:listing_id>', views.completedJob, name='completedJob'),
    path('admin/', views.admin, name='admin'),
    path('customerreview/<int:listing_id>', views.customerReview, name='customerReview'),
    path('sendMoney/', views.sendMoney, name='sendMoney'),
    path('categories/', views.categories, name='category'),
    path('createCategory/', views.createCategory, name='createCategory'),
    path('deleteCategory/<int:category_id>/', views.deleteCategory, name='deleteCategory'),
    path('workerreviews/<int:listing_id>/<int:worker_id>/', views.workerReviews, name='workerreviews')
]