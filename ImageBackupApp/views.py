from django.shortcuts import render, redirect
from django.http import HttpResponse
from ImageBackupApp.forms import ImageForm
import owncloud
import os


# Create your views here.

imageDict = dict()


oc = owncloud.Client('http://localhost/owncloud')

oc.login('kanifanath', 'dhobale26')

#oc.mkdir('Image')

mes = ''

def handle_uploaded_file(f):  
    with open('upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  

def delete_uploaded_file(f):  
    os.remove('upload/' + f.name)

def home(request):
    imageForm = ImageForm()
    return render( request ,'home.html', {'form': imageForm})

def upload(request):
	
    global mes
    if request.method == 'POST':
        imageForm = ImageForm(request.POST, request.FILES)
        if imageForm.is_valid():
            handle_uploaded_file(request.FILES['file'])
            name = request.POST['name']
            #name = request.FILES['file'].name.split('.')[0]
            desc = request.POST['desc']
            imageDict[request.FILES['file'].name] = [name, desc]
            print(imageDict)
            oc.put_file('Image/'+request.FILES['file'].name, 'upload/' + request.FILES['file'].name)
            delete_uploaded_file(request.FILES['file'])
            mes = "Image uploaded Successfully"
    
    return redirect(allImages)       
    #return render(request, 'allImages.html', {'imageDict': imageDict, 'message' : mes})

def allImages(request):

     global mes
     
     
     #ls = oc.list('Image/')
     #length = len(ls)
     #for i in ls:      
     # imageDict[str(i).split(',')[0].split('/')[2]] = [str(i).split(',')[0].split('/')[2].split('.')[0], 'Empty']

     
     
     temp = mes
     mes = ''
     return render(request, 'allImages.html', {'imageDict': imageDict, 'message': temp})

def download(request):

    fileName = request.POST['downloadBtn']
    print(fileName)
    print(oc.get_file('Image/' + fileName, '../../Downloads/' + fileName))

    return redirect(allImages)

def delete(request):

    fileName = request.POST['deleteBtn']
    print(fileName)
    print(oc.delete('Image/' + fileName))
    del imageDict[fileName]
    return redirect(allImages)

