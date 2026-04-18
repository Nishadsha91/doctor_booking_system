from django.urls import path
from .views import (
    CreateLeaveRequestView,
    MyLeaveRequestsView,
    AllLeaveRequestsView,
    LeaveApprovalView
)

urlpatterns = [

    path("create/", CreateLeaveRequestView.as_view()),

    path("my-leaves/", MyLeaveRequestsView.as_view()),

    path("all/", AllLeaveRequestsView.as_view()),

    path("approve/<int:pk>/", LeaveApprovalView.as_view()),

]