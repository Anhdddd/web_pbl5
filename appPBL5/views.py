from django.http import HttpResponse
from django.template import loader
from .models import Account, User, License_Plate, Parking_History
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            admin = Account.objects.get(username=username, password=password, isAdmin=True) 
            if admin is not None:
                return HttpResponseRedirect('manager')
            else:
                print('Invalid username or password.')

        except:
            messages.error(request, 'Invalid username or password.')
            print('Invalid username or password.')
       
    return render(request, 'login.html')

def homeManager(request):
    template = loader.get_template('homeManager.html')
    query = request.GET.get('q')
    if query:
        user_data = User.objects.filter(name__icontains=query)
    else:
        user_data = User.objects.all()
    context = {
        'user_data': user_data,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
  list_License_Plate_of_user = License_Plate.objects.filter(user=id)
  name_user = User.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'list_License_Plate_of_user': list_License_Plate_of_user,
    'name_user': name_user,
  }
  return HttpResponse(template.render(context, request))

def createuser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        license_plate = request.POST.get('license_plate')
        address = request.POST.get('address')
        username = request.POST['username']
        password = request.POST['password']
        if Account.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            print('Username Taken')
            return redirect('createuser')
        elif License_Plate.objects.filter(number_plate=license_plate).exists():
            messages.info(request, 'License Plate Taken')
            print('License Plate Taken')
            return redirect('createuser')
        else:
            account = Account.objects.create(username=username, password=password)
            account.save()
            user = User(name=name, phone=phone_number, address=address, account=account)
            user.save()
            license = License_Plate(number_plate=license_plate, user=user)
            license.save()
            messages.info(request, 'Account created')
            return redirect('createuser')
    else:
        return render(request, 'createuser.html')
    
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.account.username = request.POST.get('username')
        user.account.password = request.POST.get('password')
        user.save()
        license_plate = request.POST.get('license_plate')
        if license_plate:
            user_license_plate = License_Plate.objects.filter(user=user).first()
            if user_license_plate:
                user_license_plate.number_plate = license_plate
                user_license_plate.save()
            else:
                License_Plate.objects.create(number_plate=license_plate, user=user)
        return redirect('manager')
    else:
        return render(request, 'user_update.html', {'user': user})
    
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manager')

def parking_history(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'parking_history.html', context)

