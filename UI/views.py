from django.shortcuts import render

# Create your views here.
def checker(request):
    return render(request,'register.html')