from email.mime import image
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q, Sum
from django.contrib import messages
from .models import *
from datetime import datetime, date
from django.http import JsonResponse


# Create your views here.


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def signin(request):
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]
        if Login.objects.filter(username=email, viewPass=password).exists():
            data = authenticate(username=email, password=password)
            if data is not None:
                print("Data")
                login(request, data)
                if data.userType == "Civilian":
                    print("Civilian")
                    request.session["uid"] = data.id
                    messages.success(request, "Login Success")
                    return HttpResponse(
                        "<script>alert('Login Success');window.location.href='/civilianHome';</script>"
                    )
                elif data.userType == "Admin":
                    print("Admin")
                    messages.success(request, "Login Success")
                    return HttpResponse(
                        "<script>alert('Login Success');window.location.href='/adminHome';</script>"
                    )
                else:
                    print("Staff")
                    request.session["uid"] = data.id
                    messages.success(request, "Login Success")
                    return HttpResponse(
                        "<script>alert('Login Success');window.location.href='/staffHome';</script>"
                    )
            else:
                print("Not Approved")
                messages.error(request, "Sorry You are Not Approved")
                return redirect("/login")
        else:
            messages.error(request, "Incorrect Email/Password..😥")
    return render(request, "COMMON/login.html")


def civilianRegister(request):
    msg = ""
    wardNumber = Staff.objects.values("ward").distinct()
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        houseno = request.POST["houseno"]
        password = request.POST["password"]
        address = request.POST["message"]
        ward = request.POST["ward"]
        image = request.FILES["imgfile"]
        time = request.POST["time"]
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
        else:
            if not Civilians.objects.filter(houseno=houseno).exists():
                logQry = Login.objects.create_user(
                    username=email,
                    password=password,
                    userType="Civilian",
                    viewPass=password,
                    is_active=1,
                )
                logQry.save()
                regQry = Civilians.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    loginid=logQry,
                    houseno=houseno,
                    ward=ward,
                    image=image,
                    time=time,
                )
                regQry.save()
                return HttpResponse(
                    "<script>alert('Registration Successfull');window.location.href='/login';</script>"
                )
            else:
                msg = "Member from same house already registered"
    return render(
        request,
        "COMMON/civilianRegister.html",
        {"msg": msg, "wardNumber": wardNumber},
    )


# -------------------------------------------   CIVILIAN   -------------------------------------------


def civilianHome(request):
    return render(request, "CIVILIANS/civilianHome.html")


# -------------------------------------------   ADMIN   -------------------------------------------


def adminHome(request):
    return render(request, "ADMIN/adminHome.html")


def addStaff(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        age = request.POST["age"]
        ward = request.POST["ward"]
        password = request.POST["password"]
        address = request.POST["address"]
        image = request.FILES["imgfile"]

        if Login.objects.filter(username=email).exists():
            return HttpResponse("<script>alert('Email already Exists');</script>")
        else:
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="Staff",
                viewPass=password,
                is_active=1,
            )
            logQry.save()
            addData = Staff.objects.create(
                name=name,
                email=email,
                phone=phone,
                age=age,
                ward=ward,
                address=address,
                image=image,
                loginid=logQry,
            )
            addData.save()
            return HttpResponse(
                "<script>alert('Added Successfully');window.location.href='/adminViewStaff';</script>"
            )

    return render(request, "ADMIN/addStaff.html")


def adminViewStaff(request):
    data = Staff.objects.all()
    return render(request, "ADMIN/viewStaff.html", {"data": data})


def approveStaff(request):
    id = request.GET["id"]
    staff = Login.objects.get(username=id)
    staff.is_active = 1
    staff.save()
    return HttpResponse(
        "<script>alert('Approved');window.location.href='/adminViewStaff';</script>"
    )


def rejectStaff(request):
    id = request.GET["id"]
    staff = Login.objects.get(username=id)
    staff.is_active = 0
    staff.save()
    return HttpResponse(
        "<script>alert('Rejected');window.location.href='/adminViewStaff';</script>"
    )


def addTips(request):
    if request.POST:
        subject = request.POST["tip"]
        description = request.POST["description"]

        addTip = Suggestions.objects.create(subject=subject, details=description)
        addTip.save()
        return HttpResponse(
            "<script>alert('Suggestion Added');window.location.href='/viewTips'</script>"
        )
    return render(request, "ADMIN/addTips.html")


def viewTips(request):
    data = Suggestions.objects.all().order_by("-date")
    return render(request, "ADMIN/viewTips.html", {"data": data})


def deleteTips(request):
    id = request.GET["id"]
    result = Suggestions.objects.filter(id=id).delete()
    return HttpResponse(
        "<script>alert('Deleted');window.location.href='/viewTips'</script>"
    )


def updateTip(request):
    id = request.GET["id"]
    data = Suggestions.objects.get(id=id)
    if request.POST:
        subject = request.POST["tip"]
        description = request.POST["description"]

        data.subject = subject
        data.details = description
        data.save()
        return HttpResponse(
            "<script>alert('Updated Successfully');window.location.href='/viewTips'</script>"
        )
    return render(request, "ADMIN/updateTips.html", {"data": data})


def wardActivity(request):
    wardData = []
    ward_numbers = Staff.objects.values("ward").distinct()
    if request.POST:
        ward_number = request.POST["ward"]
        wardData = Waste.objects.filter(staff_id__ward=ward_number)
        print(wardData, "WARD DATA")
        waste_data_list = [
            {
                "sname": w.staff_id.name,
                "cname": w.civil_id.name,
                "note": w.note,
                "date": w.date,
                "houseno": w.civil_id.houseno,
                "weight": w.weight,
            }
            for w in wardData
        ]
        response_data = {"wasteData": waste_data_list}
        return JsonResponse(response_data)
    return render(
        request,
        "ADMIN/wardActivity.html",
        {"ward_numbers": ward_numbers},
    )


def adminViewFacility(request):
    data = Storage.objects.get(id=1)
    capacity = data.capacity
    return render(request, "ADMIN/viewFacility.html", {"capacity": capacity})

def adminviewrequest(request):
    data = Waste_request.objects.all()
    staffData = Staff.objects.all()
    return render(
        request, "ADMIN/adminviewrequest.html", {"data": data, "staffData": staffData}
    )

def assignstaff(request):
    if request.POST:
        id = request.POST["id"]
        staff = request.POST["staff"]
        staffId = Staff.objects.get(id=staff)
        assign = Waste_request.objects.filter(id=id).update(staff_id=staffId, status="Assigned")
        return HttpResponse(
            "<script>alert('Assigned Successfully');window.location.href='/adminviewrequest';</script>"
        )



# -------------------------------------------   STAFF   -------------------------------------------


def staffHome(request):
    return render(request, "STAFF/staffHome.html")


def addWaste(request):
    uid = request.session["uid"]
    staffId = Staff.objects.get(loginid=uid)
    print(uid)
    data = Civilians.objects.filter(ward=staffId.ward)
    print(data)
    current_date = date.today()
    if request.POST:
        civil_id = request.POST["civil_id"]
        weight = request.POST["weight"]
        note = request.POST["notes"]
        civilId = Civilians.objects.get(id=civil_id)
        if Waste.objects.filter(civil_id=civil_id).exists():
            prevData = Waste.objects.get(civil_id=civil_id)
            previous_date = prevData.date
            # previous_date_str = "2024-01-15"
            # previous_date = datetime.strptime(previous_date_str, "%Y-%m-%d").date()
            if current_date.month == previous_date.month:
                return HttpResponse(
                    "<script>alert('Waste Collected for this Month From this User');window.location.href='/addWaste'</script>"
                )
        else:
            updateStorage = Storage.objects.get(id=1)
            if updateStorage.capacity > 0:
                if not int(weight) > updateStorage.capacity:
                    addData = Waste.objects.create(
                        staff_id=staffId, civil_id=civilId, weight=weight, note=note
                    )
                    addData.save()
                    updateStorage.capacity -= int(weight)
                    updateStorage.save()
                    return HttpResponse(
                        "<script>alert('Waste Collected Successfully');window.location.href='/addWaste'</script>"
                    )
                else:
                    return HttpResponse(
                        "<script>alert('Facility is Full');window.location.href='/addWaste'</script>"
                    )
            else:
                return HttpResponse(
                    "<script>alert('Facility is at Maximum Capacity');window.location.href='/addWaste'</script>"
                )
    return render(request, "STAFF/addWaste.html", {"data": data})


def viewFacility(request):
    data = Storage.objects.get(id=1)
    capacity = data.capacity
    return render(request, "STAFF/viewFacility.html", {"capacity": capacity})


def individualActivity(request):
    wasteData = []
    uid = request.session["uid"]
    staffId = Staff.objects.get(loginid=uid)
    print("UID", uid)
    civData = Civilians.objects.filter(ward=staffId.ward)
    print(civData)
    if request.POST:
        person = request.POST["person"]
        print(person)
        wasteData = Waste.objects.filter(Q(civil_id=person) & Q(staff_id__loginid=uid))
        print(wasteData)
        waste_data_list = [
            {
                "name": w.civil_id.name,
                "phone": w.civil_id.phone,
                "email": w.civil_id.email,
                "address": w.civil_id.address,
                "houseno": w.civil_id.houseno,
                "weight": w.weight,
            }
            for w in wasteData
        ]
        response_data = {"wasteData": waste_data_list}
        return JsonResponse(response_data)
    return render(
        request,
        "STAFF/individualActivity.html",
        {"civData": civData, "wasteData": wasteData},
    )

def staffViewRequests(request):
    uid = request.session["uid"]
    data = Waste_request.objects.filter(staff_id__loginid=uid)
    print(data)
    return render(request, "STAFF/viewPickupRequests.html", {"data": data})

def pickuporder(request):
    id = request.GET["id"]
    updateStatus = Waste_request.objects.filter(id=id).update(status="Pickedup")
    return HttpResponse(
        "<script>alert('Status Changed');window.location.href='/staffviewrequests'</script>"
    )


def forwardorder(request):
    id = request.GET["id"]
    updateStatus = Waste_request.objects.filter(id=id).update(status="Forwarded")
    return HttpResponse(
        "<script>alert('Status Changed');window.location.href='/staffviewrequests'</script>"
    )



def myProfile(request):
    uid = request.session["uid"]
    data = Civilians.objects.get(loginid=uid)
    return render(request, "CIVILIANS/myProfile.html", {"data": data})


def editProfile(request):
    msg = ""
    id = request.GET["id"]
    data = Civilians.objects.get(loginid=id)
    wardNumber = Staff.objects.values("ward").distinct()
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST.get("password")
        address = request.POST["message"]
        ward = request.POST["ward"]
        houseno = request.POST["houseno"]
        image = request.FILES.get("imgfile")
        if image:
            if not Login.objects.filter(email=email).exists():
                if not Civilians.objects.filter(houseno=houseno).exists():
                    data.name = name
                    data.email = email
                    data.phone = phone
                    data.address = address
                    data.ward = ward
                    data.houseno = houseno
                    data.image = image
                    data.save()
                    logData = Login.objects.get(id=id)
                    logData.username = email
                    logData.set_password(password)
                    logData.save()
                    return HttpResponse(
                        "<script>alert('Updated Successfully');window.location.href='/myProfile'</script>"
                    )
                else:
                    msg = "Member from same house already registered"
        else:
            if not Login.objects.filter(email=email).exists():
                if Civilians.objects.filter(houseno=houseno).exists():
                    data.name = name
                    data.email = email
                    data.phone = phone
                    data.address = address
                    data.ward = ward
                    data.houseno = houseno
                    data.save()
                    logData = Login.objects.get(id=id)
                    logData.username = email
                    logData.set_password(password)
                    logData.save()
                    return HttpResponse(
                        "<script>alert('Updated Successfully');window.location.href='/myProfile'</script>"
                    )
                else:
                    msg = "Member from same house already registered"
                    return redirect("/myProfile?msg=" + msg)
    return render(
        request,
        "CIVILIANS/editProfile.html",
        {"data": data, "msg": msg, "wardNumber": wardNumber},
    )


def reportDumping(request):
    uid = request.session["uid"]
    print(uid)
    civilId = Civilians.objects.get(loginid=uid)
    myReports = Complaints.objects.filter(civilId__loginid=uid)
    if request.POST:
        desc = request.POST["remarks"]
        address = request.POST["address"]
        image = request.FILES["imgfile"]
        addComplaint = Complaints.objects.create(
            civilId=civilId, desc=desc, address=address, image=image
        )
        addComplaint.save()
    return render(request, "CIVILIANS/reportDumping.html", {"myReports": myReports})


def myActivity(request):
    uid = request.session["uid"]
    myData = Waste.objects.filter(civil_id__loginid=uid)
    print(myData)
    return render(request, "CIVILIANS/myActivity.html", {"myData": myData})


def viewSuggestions(request):
    data = Suggestions.objects.all()
    return render(request, "CIVILIANS/viewSuggestions.html", {"data": data})

def pickuprequest(request):
    uid = request.session["uid"]
    if request.POST:
        weight = request.POST["weight"]
        desc = request.POST["notes"]
        userId = Civilians.objects.get(loginid=uid)
        addReq = Waste_request.objects.create(weight=weight, civil_id=userId, desc=desc)
        addReq.save()
        return HttpResponse(
            "<script>alert('Added Successfully');window.location.href='/pickuprequest'</script>"
        )
    return render(request, "CIVILIANS/pickupRequest.html")

def viewRequests(request):
    uid = request.session["uid"]
    data = Waste_request.objects.filter(civil_id__loginid=uid)
    print(data)
    return render(request, "CIVILIANS/viewRequests.html", {"data": data})