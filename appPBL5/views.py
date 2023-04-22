from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from .models import User, License_Plate, Account, Parking_History


def check_user_is_logged_in(user):
    return user.is_authenticated


# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        accounts = Account.objects.filter(username=username, password=password)
        if len(accounts) > 0:
            request.session["id_account"] = accounts[0].id  # Khởi tạo session
            if accounts[0].isAdmin:
                return redirect("manager")
            else:
                return redirect("user")  # cacsh 1
                # return homeUser(request, accounts[0].id)
        else:
            print("LOI: ko thể in username vì không có")
            return render(request, "login.html")
    else:
        return render(request, "login.html")
        # template = loader.get_template('login.html')    cách lỗi csrf
        # return HttpResponse(template.render())


def logout(request):
    id_account = request.session.pop("id_account", None)  # Xoá session
    return redirect("login")


def homeManager(request):
    if request.session["id_account"] is None:
        return redirect("login")
    template = loader.get_template("homeManager.html")
    context = {
        "user_data": User.objects.all(),
    }
    return HttpResponse(template.render(context, request))


# Danh sách biển số xe của user
def details(request, id):
    list_License_Plate_of_user = License_Plate.objects.filter(user=id)
    name_user = User.objects.get(id=id)
    template = loader.get_template("details.html")
    context = {
        "list_License_Plate_of_user": list_License_Plate_of_user,
        "name_user": name_user,
    }
    return HttpResponse(template.render(context, request))


def createuser(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        license_plate = request.POST.get("license_plate")
        address = request.POST.get("address")
        username = request.POST["username"]
        password = request.POST["password"]
        if Account.objects.filter(username=username).exists():
            print("Username Taken")
            return redirect("createuser")
        elif License_Plate.objects.filter(number_plate=license_plate).exists():
            print("License Plate Taken")
            return redirect("createuser")
        else:
            account = Account.objects.create(username=username, password=password)
            account.save()
            user = User(name=name, phone=phone_number, address=address, account=account)
            user.save()
            license = License_Plate(number_plate=license_plate, user=user)
            license.save()
            return redirect("manager")
    else:
        return render(request, "createuser.html")


def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.name = request.POST.get("name")
        user.phone = request.POST.get("phone")
        user.address = request.POST.get("address")
        user.account.username = request.POST.get("username")
        user.account.password = request.POST.get("password")
        user.save()
        license_plate = request.POST.get("license_plate")
        if license_plate:
            user_license_plate = License_Plate.objects.filter(user=user).first()
            if user_license_plate:
                user_license_plate.number_plate = license_plate
                user_license_plate.save()
            else:
                License_Plate.objects.create(number_plate=license_plate, user=user)
        return redirect("manager")
    else:
        return render(request, "user_update.html", {"user": user})


def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("manager")


def parking_history(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "parking_history.html", context)


def homeUser(request):  # cách 1
    if request.session["id_account"] is None:
        return redirect("login")
    id_account = request.session["id_account"]
    template = loader.get_template("user.html")
    context = {
        "user": User.objects.get(account=id_account),
        "user_license_plates": License_Plate.objects.filter(user__account=id_account),
    }
    return HttpResponse(template.render(context, request))


def update_user(request):
    if request.method == "POST":
        id_account = request.session["id_account"]
        user = User.objects.get(account=id_account)
        user.name = request.POST["name"]
        user.phone = request.POST["phone"]
        user.address = request.POST["address"]
        user.save()
        return redirect("user")
    return redirect("user")


def parking_history_user(request):
    id_account = request.session["id_account"]
    user = User.objects.get(account=id_account)
    list_parking_history = Parking_History.objects.filter(license_plate__user=user)
    template = loader.get_template("parking_history_user.html")
    context = {
        "list_parking_history": list_parking_history,
    }
    return HttpResponse(template.render(context, request))


# def homeUser(request, id_account):
#     user = User.objects.get(account=id_account)
#     user_license_plates = License_Plate.objects.filter(user=user)
#     context = {
#         'user': user,
#         'user_license_plates' : user_license_plates,
#     }
#     return render(request, 'user.html', context)
