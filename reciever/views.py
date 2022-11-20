from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Reciever
import socket
import time
import os

def index(request):
  myreciever = Reciever.objects.all().values()
  template = loader.get_template('index.html')
  context = {
    'myreciever': myreciever,
  }
  return HttpResponse(template.render(context, request))
  
def add(request):
  template = loader.get_template('add.html')
  return HttpResponse(template.render({}, request))

def addrecord(request):
  x = request.POST['first']
  y = request.POST['last']
  reciever = Reciever(firstname=x, lastname=y)
  reciever.save()
  return HttpResponseRedirect(reverse('index'))

def delete(request, id):
  reciever = Reciever.objects.get(id=id)
  reciever.delete()
  return HttpResponseRedirect(reverse('index'))

def update(request, id):
  myreciever = Reciever.objects.get(id=id)
  template = loader.get_template('update.html')
  context = {
    'myreciever': myreciever,
  }
  return HttpResponse(template.render(context, request))

def updaterecord(request, id):
  first = request.POST['first']
  last = request.POST['last']
  reciever = Reciever.objects.get(id=id)
  reciever.firstname = first
  reciever.lastname = last
  reciever.save()
  return HttpResponseRedirect(reverse('index'))

def reciever(request):
    host = str('192.168.29.173')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Trying to connect to socket.
    try:
        sock.connect((host, 22222))
        print("Connected Successfully")
    except:
        print("Unable to connect")
        exit(0)
    
    # Send file details.
    file_name = sock.recv(100).decode()
    file_size = sock.recv(100).decode()
    
    # Opening and reading file.
    with open("./rec/" + file_name, "wb") as file:
        c = 0
        # Starting the time capture.
        start_time = time.time()
    
        # Running the loop while file is recieved.
        while c <= int(file_size):
            data = sock.recv(1024)
            if not (data):
                break
            file.write(data)
            c += len(data)
    
        # Ending the time capture.
        end_time = time.time()
    
    mydata= print("File transfer Complete.Total time: ", end_time - start_time)
    context = {
    'mydata': mydata,}
    # Closing the socket.
    sock.close()
    return HttpResponseRedirect(reverse(context, request))