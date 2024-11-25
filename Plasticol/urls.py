"""
URL configuration for Plasticol project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from PlasticolApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.index),
    path("", views.index),
    path("contact/", views.contact),
    path("login/", views.signin),
    path("civilianRegister/", views.civilianRegister),
    path("civilianHome/", views.civilianHome),
    path("staffHome/", views.staffHome),
    path("adminHome/", views.adminHome),
    path("addStaff/", views.addStaff),
    path("adminViewStaff/", views.adminViewStaff),
    path("approveStaff/", views.approveStaff),
    path("rejectStaff/", views.rejectStaff),
    path("addTips/", views.addTips),
    path("viewTips/", views.viewTips),
    path("deleteTips/", views.deleteTips),
    path("updateTip/", views.updateTip),
    path("addWaste/", views.addWaste),
    path("viewFacility/", views.viewFacility),
    path("individualActivity/", views.individualActivity),
    path("myProfile/", views.myProfile),
    path("editProfile/", views.editProfile),
    path("reportDumping/", views.reportDumping),
    path("myActivity/", views.myActivity),
    path("viewSuggestions/", views.viewSuggestions),
    path("wardActivity/", views.wardActivity),
    path("adminViewFacility/", views.adminViewFacility),
    path("pickuprequest/", views.pickuprequest),
    path("viewrequests/", views.viewRequests),
    path("adminviewrequest/", views.adminviewrequest),
    path("staffviewrequests/", views.staffViewRequests),
    path("pickuporder/", views.pickuporder),
    path("forwardorder/", views.forwardorder),
    path("assignstaff/", views.assignstaff),
]
