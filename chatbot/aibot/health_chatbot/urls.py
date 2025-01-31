from django.urls import path
from . import views
urlpatterns=[
    path('', views.home, name='home' ),
    path('user', views.UserDetails.as_view(), name='create-user'), #all user
    path('appointment', views.CreateAppointment.as_view(), name='create-appointment'), #all appointments
    path('user/edit/<int:pk>', views.UserEdit.as_view(), name='edit-user'), #update user
    path('appointment/<int:pk>', views.UserAppointment.as_view(), name='edit-user'), #create/update user specific appointment
    path('chatbot', views.ChatBot.as_view(),name='chatbot'), #chat interface
    path('questions/', views.AllResponse.as_view(), name='all-questions-responses'),
    path('questions/<int:pk>/', views.UserResponse.as_view(), name='user-questions-responses'),
]
