from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import PersonalInformation
from .models import Information

def get_form(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        linkedIn = request.POST.get('linkedIn')
        skypeId = request.POST.get('skypeId')
        drive_link = request.POST.get('drive_link')
        data = Information(full_name=full_name, dob=dob, email=email, phone=phone, linkedIn=linkedIn, skypeId=skypeId, drive_link=drive_link)
        data.save()
        print(drive_link)
        return render(request, 'app/handleForm.html')

    else:
        form = PersonalInformation()

    return render(request, 'app/userdata.html', {'form': form})

# def getDriveLink(request):
#     if request.method == "POST":
#         #Get the posted form
#         MyForm = PersonalInformation(request.POST)
        
#         if MyForm.is_valid():
#             drive_link = MyForm.cleaned_data['drive_link']
#     else:
#         MyForm = PersonalInformation()
            
#     return render(request, 'driveLink.html', {"drive_link" : drive_link})


def upload(request):
    if request.method == 'POST':
       uploaded_file = request.FILES['document']
       print(uploaded_file.name)
    return render(request,  'app/upload.html') 
