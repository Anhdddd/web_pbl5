from django.http import HttpResponse
from django.template import loader
from .models import User, License_Plate

# Create your views here.
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def homeManager(request):
    template = loader.get_template('homeManager.html')
    context = {
        'user_data': User.objects.all(),
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