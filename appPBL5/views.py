from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from .models import User, License_Plate, Account, Parking_History
import datetime


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
        "user_data": User.objects.all().order_by('-id')
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

def add_Plate_Number(request):
    if request.method == "POST":
        plate_number = request.POST.get("plate_number")
        id = request.POST.get('id')
        if License_Plate.objects.filter(number_plate=plate_number).exists():
            name_user = User.objects.get(id=id)
            list_License_Plate_of_user = License_Plate.objects.filter(user=id)
            template = loader.get_template("details.html")
            context = {
                "list_License_Plate_of_user": list_License_Plate_of_user,
                "name_user": name_user,
            }
            return HttpResponse(template.render(context, request))
        else:
            user = User.objects.get(id=int(id))
            license_Plate = License_Plate.objects.create(number_plate=plate_number, user=user)
            license_Plate.save()
            name_user = User.objects.get(id=id)
            list_License_Plate_of_user = License_Plate.objects.filter(user=id)
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
        identity_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

        if Account.objects.filter(username=username).exists():
            print("Username Taken")
            context = {
                'error_account': 'Tên tài khoản bị trùng'
            }
            return render(request, "createuser.html", context)
        elif User.objects.filter(phone=phone_number).exists():
            context = {
                'error_phone': 'Số điện thoại bị trùng'
            }
            return render(request, "createuser.html", context)
        elif License_Plate.objects.filter(number_plate=license_plate).exists():
            print("License Plate Taken")
            context = {
                'error_number_plate': 'Biển số xe bị trùng'
            }
            return render(request, "createuser.html", context)
        else:
            account = Account.objects.create(username=username, password=password)
            account.save()
            user = User(name=name, phone=phone_number, address=address, account=account, identity_code=identity_code)
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

def search_user(request):
    if request.method == "POST":
        search = request.POST.get("search")
        users = User.objects.filter(name__contains=search)
        context = {
            "user_data": users,
        }
        return render(request, "homeManager.html", context)
# def parking_history(request):
#     users = User.objects.all()
#     context = {
#         "users": users,
#     }
#     return render(request, "parking_history.html", context)
def parking_history(request):
    parking_histories = Parking_History.objects.select_related('license_plate__user').order_by('-check_in_time').values('license_plate__user__name', 'license_plate__number_plate', 'check_in_time', 'check_out_time')
    context = {
        "parking_histories": parking_histories,
    }
    return render(request, "parking_history.html", context)


def homeUser(request):  # cách 1
    id_account = request.session.get('id_account', '')
    if id_account is None or id_account == '':
        return redirect("login")
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
    id_account = request.session.get('id_account', '')
    if id_account is None or id_account == '':
        return redirect("login")
    user = User.objects.get(account=id_account)
    list_parking_history = Parking_History.objects.filter(license_plate__user=user).order_by('-check_in_time')
    template = loader.get_template("parking_history_user.html")
    context = {
        "list_parking_history": list_parking_history,
        'code_qr': user.identity_code
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
