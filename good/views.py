from django.shortcuts import render,HttpResponse

# Create your views here.
def good_index(request):
    return render(request,'index.html')