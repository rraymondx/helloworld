from django.shortcuts import render

# Create your views here.

# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from .models import Item, ToDoList
from django.contrib.auth import logout

def homePageView(request):
    # return request object and specify page.
    return render(request, 'home.html', {
        'mynumbers':[1,2,3,4,5,6,],
        'firstName': 'Raymond',
        'lastName': 'Xie'},)


def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')

def raymondPageView(request):
    return render(request, 'raymond.html')


from django.http import HttpResponseRedirect
from django.urls import reverse
import pdb;

def homePost(request):
    # Use request object to extract choice.

    choice = -999
    gmat = -999  # Initialize gmat variable.

    try:
        # Extract value from request object by control name.
        currentChoice = request.POST['choice']
        gmatStr = request.POST['gmat']
        # print("Just before Raymond's breakpoint")
        # pdb.set_trace()
        # breakpoint()
        # print("Just after breakpoint")

        # Crude debugging effort.
        print("*** Years work experience: " + str(currentChoice))
        choice = int(currentChoice)
        gmat = float(gmatStr)
    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage': '*** The data submitted is invalid. Please try again.',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'choice': choice, 'gmat': gmat}, ))


import pickle
import pandas as pd


def results(request, choice, gmat):
    print("*** Inside reults()")
    # load saved model
    with open('/Users/BCIT/Desktop/BCIT CST/Term4/COMP4949/Lessons/Django/helloworld/config/model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['gmat', 'work_experience'])

    workExperience = float(choice)
    print("*** GMAT Score: " + str(gmat))
    print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf._append({'gmat':gmat,
                                            'work_experience':workExperience},
                                        ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))

    return render(request, 'results.html', {'choice': workExperience, 'gmat':gmat,
                'prediction':singlePrediction})

def todos(request):
    print("*** Inside todos()")
    items = Item.objects
    itemErrandDetail = items.select_related('todolist')
    print(itemErrandDetail[0].todolist.name)
    return render(request, 'ToDoItems.html',
                {'ToDoItemDetail': itemErrandDetail})

from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(response):
    # Handle POST request.
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('message',
                                                kwargs={'msg': "Your are registered.", 'title': "Success!"}, ))
    # Handle GET request.
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})

def message(request, msg, title):
    return render(request, 'message.html', {'msg': msg, 'title': title })

def logoutView(request):
    print("just before break")
    pdb.set_trace()
    print("after trace")
    logout(request)
    print("*****  You are logged out.")
    return HttpResponseRedirect(reverse('home'))




