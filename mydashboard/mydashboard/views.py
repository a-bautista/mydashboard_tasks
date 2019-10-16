from django.shortcuts import render
# Create your views here.

def home(request):
    # Basic function based view
    my_title = "Hello there"
    # I had to configure the template dir in the settings of the app
    template_name = 'home.html'
    context = {"title": my_title, "my_list": [1, 2, 3, 4, 5]}
    return render(request, template_name, context)

def about(request):
    return render(request, "about.html", {"title": "About"})