from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from Blogapp.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def index(request):
    allposts = Post.objects.all().order_by('-timestamp')
    context = {'allposts': allposts}
    return render(request, "home/home.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["content"]
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        if len(name) < 2 or len(email) < 4 or len(phone) < 10 or len(content) < 5:
            messages.error(request, 'please enter required inputs')
        else:
            messages.success(request, 'Your message has been sent successfully')
    return render(request, "home/contact.html")


def about(request):
    return render(request, "home/about.html")


def search(request):
    query = request.GET['query']
    if len(query) > 100:
        allpost = allpost = Post.objects.none()
    else:
        allposttitle = Post.objects.filter(title__icontains=query)
        allpostauthor = Post.objects.filter(author__icontains=query)
        allpostcontent = Post.objects.filter(content__icontains=query)
        allpost = allposttitle.union(allpostauthor, allpostcontent)
    if allpost.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    context = {'allpost': allpost, 'query': query}
    return render(request, "home/search.html", context)


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) > 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been Successfully login")
            return redirect('/')
        else:
            messages.error(request, "Invalid Username or Password, Please try again")
            return redirect('/')
    return HttpResponse("404- Not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "You are successfully Logged Out")
    return redirect('home')
