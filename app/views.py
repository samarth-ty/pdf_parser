import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import convertapi
import cv2
import pytesseract
from pdfminer.high_level import extract_text
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.shortcuts import render
from .forms import PersonalInformation
from .models import Information

EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
LINKEDIN_REG = re.compile(r'((http(s?)://)*([www])*\.|[linkedin])[linkedin/~\-]+\.[a-zA-Z0-9/~\-_,&=\?\.;]+[^\.,\s<]')

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)


def extract_linkedIn(resume_text):
    return re.findall(LINKEDIN_REG, resume_text)


def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
 
    if phone:
        number = ''.join(phone[0])
 
        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None

def write_to_gsheet(folder_id, filename, phone, email):
    Scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

    creds = ServiceAccountCredentials.from_json_keyfile_name("/home/samarth/pdfparser/pdfparser/secret_key.json", scopes=Scopes)
    file = gspread.authorize(creds)
    workbook = file.open("Candidates information")
    sheet = workbook.sheet1
    candidate_info = [folder_id, filename, phone, email, 'https://www.linkedin.com/in/sam-tyagi-6b6487245/']
    sheet.append_row(candidate_info)


def convert_to_pdf(file_path, typ):
    convertapi.api_secret = 'DBuhCGfisLXtWsTg'
    convertapi.convert('pdf', {
        'File': file_path
    }, from_format = typ).save_files('/home/samarth/pdfparser/pdfparser')


def get_form(request):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    if request.method == 'POST':
        drive_link = request.POST.get('drive_link')
        data = Information(drive_link=drive_link)
        data.save()
        print('------------'+drive_link+'--------------------------')
        x = len(drive_link)
        for i in range(x-1,-1,-1):
            if drive_link[i] == '/':
                break
            
        folder = drive_link[i+1:]
        file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
        for index, file in enumerate(file_list):
            # print(index+1, 'file downloaded : ', file['title'])
            folder_id = file['id']
            print('folder id: ', file['id'])
            fl = drive.ListFile({'q' : f"'{folder_id}' in parents and trashed=false"}).GetList()
            for f in fl:
                length = len(f['title'])
                typ = ''
                for i in range(length-1,-1,-1):
                    if f['title'][i] == '.':
                        break
                typ = f['title'][i+1:]
                if typ == 'pdf':
                    f.GetContentFile(f['title'])
                    text = extract_text(f['title'])
                    # print(text)
                    emails = extract_emails(text)
                    phone_number = extract_phone_number(text)
                    linkedIn = extract_linkedIn(text)
                    if emails:
                        print(emails[0])
                    print(phone_number)
                    write_to_gsheet(folder_id,f['title'], phone_number, emails[0])
                    os.remove(f['title'])

                elif typ == 'docx' or typ == 'doc':
                    f.GetContentFile(f['title'])
                    convert_to_pdf(f['title'], typ)
                    converted_file_path = f['title'][:i+1] + 'pdf'
                    text = extract_text(converted_file_path)
                    emails = extract_emails(text)
                    phone_number = extract_phone_number(text)
                    linkedIn = extract_linkedIn(text)
                    if emails:
                        print(emails[0])
                    print(phone_number)
                    if emails and phone_number:
                        write_to_gsheet(folder_id, f['title'], phone_number, emails[0])
                    os.remove(f['title'])
                    os.remove(converted_file_path)

                elif typ in ['png', 'jpeg', 'jpg']:
                    f.GetContentFile(f['title'])
                    tessdata_dir_config= r'/--tessdata-dir "/home/samarth/pdfparser/my_env/lib/python3.8/site-packages"'
                    img = cv2.imread(f['title'],1)
                    img_scale_up = cv2.resize(img, (0, 0), fx=1.5, fy=1.5)
                    # cv2.imshow('Upscaled Image', img_scale_up)
                    if not cv2.imwrite(r'/home/samarth/pdfparser/pdfparser/upscaled.{0}'.format(typ), img_scale_up):
                        raise Exception('Could not write image')
                    cv2.waitKey(0)
                    upscaled_image = 'upscaled.{0}'.format(typ)
                    text = pytesseract.image_to_string(upscaled_image, config=tessdata_dir_config)
                    emails = extract_emails(text)
                    phone_number = extract_phone_number(text)
                    linkedIn = extract_linkedIn(text)
                    if emails:
                        print(emails[0])
                    print(phone_number)

                    if emails and phone_number:
                        write_to_gsheet(folder_id, f['title'], phone_number, emails[0])
                    os.remove(f['title'])
                    os.remove(upscaled_image)

        return render(request, 'app/handleForm.html')

    else:
        form = PersonalInformation()

    return render(request, 'app/userdata.html', {'form': form})


def upload(request):
    if request.method == 'POST':
       uploaded_file = request.FILES['document']
       print(uploaded_file.name)
    return render(request,  'app/upload.html') 
