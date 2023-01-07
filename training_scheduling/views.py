from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django import forms
from django.contrib import admin
from datetime import datetime, date
import pandas
from django.shortcuts import redirect
from django.urls import reverse
from django.db import IntegrityError
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import re
from pandas import Timestamp
from dateutil.rrule import rrule, DAILY
from datetime import datetime
from django.contrib.auth import authenticate, logout, login

from .models import User, Class_rooms, Trainings, Training_days, Students, Date

class NewClassroomForm(forms.Form):
    room = forms.IntegerField()
    seats = forms.IntegerField()
    SITE_CHOICES = [
        ('SITE1', 'site1'), 
        ('SITE2', 'site2'),
    ]
    Site = forms.ChoiceField(
        #max_length=30,
        choices=SITE_CHOICES,
        #required=False
    )

class NewTrainingForm(forms.Form):
    #reserved_seat = forms.BooleanField()
    student_name = forms.CharField(max_length=30,required=False)
    student_surename = forms.CharField(max_length=30, required=False)
    #teacher_seat = forms.BooleanField()
    pre_training_student_comment = forms.CharField(required=False)

class NewConfigForm(forms.Form):
    
    PROJECT_CHOICES = [
        ('PPROJECT1', 'Project1'), 
        ('PPROJECT2', 'Project2'),
        ('PPROJECT3', 'Project3'),
        ('PPROJECT4', 'Project4'),
        ('PPROJECT5', 'Project5'),
        # mi shtu krejt edhe munsin me shtu admini vet congifigurim nese se gjen qata qe i vyn
    ]
    projects = forms.ChoiceField(
        #max_length=30,
        choices=PROJECT_CHOICES,
    )

    CONFIG_CHOICES = [
        ('PPROJECT1', 'Project1'), 
        ('PPROJECT2', 'Project2'),
        ('PPROJECT3', 'Project3'),
        ('PPROJECT4', 'Project4'),
        ('PPROJECT5', 'Project5'),
        # mi shtu krejt edhe munsin me shtu admini vet congifigurim nese se gjen qata qe i vyn
    ]
    config = forms.ChoiceField(
        #max_length=30,
        choices=CONFIG_CHOICES,
    )

    TRAINING_CHOICES = [
        ('TYPE1', 'Type1'), 
        ('TYPE2', 'Type2'),
        # mi shtu krejt edhe munsin me shtu admini vet congifigurim nese se gjen qata qe i vyn
    ]
    type = forms.ChoiceField(
        #max_length=30,
        choices=TRAINING_CHOICES,
    )

class NewObservationForm(forms.Form):
    student_attended = forms.BooleanField(required=False)
    student_arrival_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    student_left_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    training_day_student_comment = forms.CharField(required=False)
    

# Create your views here.
def index(request):
    classes = Class_rooms.objects.all()
    return render(request, 'training_scheduling/index.html', {
        "Classes": classes
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "training_scheduling/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "training_scheduling/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "training_scheduling/register.html")



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "training_scheduling/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, 'training_scheduling/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def class_room(request, page):
    
    dates_unavailable = []
    date_list = []
    #number_of_seats = Class_rooms.objects.extra(where=[f"id = '{page}'"]).values_list('seats',flat = True).get()
    #page = int(page)
    page = int(page)
    number_of_seats = Class_rooms.objects.filter(id = page).values_list('seats',flat = True).get()
    list_of_seats = list(range(1,number_of_seats+1))
    #list_of_seats = list(range(1,3))
    room_number = Class_rooms.objects.filter(id = page).values_list('room_number',flat = True).get()
    
    if request.method == "POST":
        form = request.POST
        form1 = NewConfigForm(request.POST)
        
        list_of_student_name = form.getlist('student_name')
        list_of_student_surename = form.getlist('student_surename')
        list_of_pre_training_student_comment= form.getlist('pre_training_student_comment')
        comment_pre_all = form.get('comment_all')
        #start_date = form.get('from_date')
        start_date = datetime.strptime(form.get('from_date'), '%Y-%m-%d')
        #end_date = form.get('to_date')
        end_date = datetime.strptime(form.get('to_date'), '%Y-%m-%d')
        if form1.is_valid():
            project = form1.cleaned_data["projects"]
            config = form1.cleaned_data["config"]
            type_training = form1.cleaned_data["type"]

        #date_list = pandas.date_range(start_date,end_date(days=1),freq='d')
        date_list = pandas.date_range(start_date,end_date)

        # qetu me test a o qikjo date list ne unavailable days
        dates_unavailable_ids = list(Class_rooms.objects.filter(id = page).values_list('dates_unavailable',flat = True))
        dates_unavailable = []

        if dates_unavailable_ids[0] == None: 
            pass
        else:
            for element in dates_unavailable_ids:
                dateobj = Date.objects.get(id=element)
                dates_unavailable.append(dateobj.date)

        for date1 in date_list:
    
            if date1 in dates_unavailable:

                return render(request, 'training_scheduling/class.html', {
                    "seats": list_of_seats,
                    "form": NewTrainingForm(),
                    "types": NewConfigForm(),
                    "room": room_number,
                    "page": page,
                    "error": "Class is not available at that date",
                    "all_dates": dates_unavailable,
                    #"all_proj": reserved_by_proj
                    #"error1": dates_unavailable_ids
                    #"date": MyDateForm()
                })
    
        Trainings(Config=config, class_room=Class_rooms.objects.get(id=page), reserved_by=request.user,
                pre_training_comment = comment_pre_all, training_start_date=start_date,
                training_end_date = end_date, project = project, type_training = type_training).save()

        # qetu i krijoj training days

        trainingID = Trainings.objects.filter(class_room = Class_rooms.objects.get(id=page), training_start_date=start_date,
                training_end_date = end_date).get()
        
        # add unavailable dates
        class_dates = Class_rooms.objects.get(id=page)
        
        for element in date_list:
            Training_days(training = trainingID, training_day_date = element).save()
            training_dayID = Training_days.objects.filter(training = trainingID, training_day_date = element).get()
            
            date_unavailble = Date.objects.create(date=element)
            class_dates.dates_unavailable.add(date_unavailble)

            for name, surename, pre_comment in zip(list_of_student_name, list_of_student_surename, list_of_pre_training_student_comment):
                Students(training_day = training_dayID, student_name = name, 
                student_surename = surename, pre_training_comment = pre_comment).save()

        
        class_dates.save()

        #reserved = Trainings.objects.all()
        #list_of_res = list(range(1,len(list(reserved))+1))

        active_user = request.user
        reserved = Trainings.objects.filter(reserved_by = active_user).all()
        list_of_res = list(range(1,len(list(reserved))+1))

        return render(request, 'training_scheduling/reserved_trainings.html', {
        "reserved": zip(reserved, list_of_res),
        #"error": dates_unavailable,
        #"error1": date_list,
    })

    dates_unavailable_ids = list(Class_rooms.objects.filter(id = page).values_list('dates_unavailable',flat = True))
    dates_unavailable = []

    if dates_unavailable_ids[0] == None: 
        pass
    else:
        for element in dates_unavailable_ids:
            dateobj = Date.objects.get(id=element)
            dates_unavailable.append(dateobj.date)
    
    #reserved_by_proj = []
    #for date in dates_unavailable:
    #    day = Training_days.objects.get(training_day_date = date)
    #    obj = Trainings.objects.get(id = 71)
    #    reserved_by_proj.append(obj.project)

    return render(request, 'training_scheduling/class.html', {
        "seats": list_of_seats,
        "form": NewTrainingForm(),
        "types": NewConfigForm(),
        "room": room_number,
        "page": page,
        "all_dates": dates_unavailable,
        #"all_proj": zip(reserved_by_proj, reserved_by_proj)
        #"error": dates_unavailable,
        #"error1": date_list,
        #"date": MyDateForm()
    })

def reserved_trainings(request):
    active_user = request.user
    reserved = Trainings.objects.filter(reserved_by = active_user).all()
    list_of_res = list(range(1,len(list(reserved))+1))

    return render(request, 'training_scheduling/reserved_trainings.html', {
        "reserved": zip(reserved, list_of_res),
    })

def training_observation(request, page = 0, trainingday = 0):

    if request.method == "POST":

        if "remove" in request.POST:
            training_to_remove = Trainings.objects.get(id = page)
            class_reserved = training_to_remove.class_room
            training_start = training_to_remove.training_start_date
            training_end = training_to_remove.training_end_date
            date_list_remove = pandas.date_range(training_start,training_end)
            training_to_remove.delete()

            # Convert the dates to Date objects
            dates_to_remove = [Date.objects.filter(date=date).first() for date in date_list_remove]

            # Use the remove method to remove the dates from the dates_unavailable field
            Class_rooms.objects.get(id = class_reserved.id).dates_unavailable.remove(*dates_to_remove)

            # Don't forget to save the changes to the model
            Class_rooms.objects.get(id = class_reserved.id).save()

        return redirect(reverse('index'))
        

    days = list(Training_days.objects.filter(training = page))
    days_list = []
    #trainingday = 0
    trainingday = trainingday
    for element in days:
        day = Students.objects.filter(training_day = element)
        days_list.append(day)
    
    if trainingday == 999:
        return render(request, 'training_scheduling/training_observation_overall.html', {
            "days": days,
            "page": page,
            "day_students": days_list[0], 
            "form_obs": NewObservationForm()
        }) 

    return render(request, 'training_scheduling/training_observation.html', {
        "days": days,
        "page": page,
        "day_students": days_list[trainingday],
        "trainingdayID": days[0],
        "form_obs": NewObservationForm()

    })    

def training_observation_change(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    list_of_ids = data.get("list_of_ids")
    list_of_inputs = data.get("list_of_inputs")

    list_of_student_id = list_of_ids
    student_attended = []
    student_arrival = []
    student_left = []
    student_comment = [] 

    for element in list_of_inputs:
        student_attended.append(element[0]) 
        student_arrival.append(element[1]) 
        student_left.append(element[2])
        student_comment.append(element[3]) 


    for id, comm, att, arrive, left in zip(list_of_student_id, student_comment, student_attended, student_arrival, student_left):
        student = Students.objects.get(id=id)
        student.training_day_comment = comm

        if att == 'True':
            student.training_day_attendance = True
        elif att == 'False':
            student.training_day_attendance = False

        if arrive == '':
            student.training_day_arrival = student.training_day_arrival
        else:
            student.training_day_arrival = arrive

        if left == '':
            student.training_day_left = student.training_day_left
        else:
            student.training_day_left = left
        
        student.save()

    return JsonResponse({"message": list_of_inputs}, status=201)


#@method_decorator(csrf_exempt, name='dispatch')
def class_available(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    startdate_list = data.get("startdate")
    enddate_list = data.get("enddate")
    class_id_list = data.get("class_id")

    output_list = []
    testing2 = 0
    testing3 = 0
    testing4 = 0
    for startdate, enddate, class_id in zip(startdate_list, enddate_list, class_id_list):
        
        start_year = startdate[0]

        if startdate[1][0] == '0':
            start_month = startdate[1][1]
        else:
            start_month = startdate[1]

        if startdate[2][0] == '0':
            start_day = startdate[2][1]
        else:
            start_day = startdate[2]
        

        end_year = enddate[0]
        
        if enddate[1][0] == '0':
            end_month = enddate[1][1]
        else:
            end_month = enddate[1]

        if enddate[2][0] == '0':
            end_day = enddate[2][1]
        else:
            end_day = enddate[2]

        start_date = datetime(int(start_year), int(start_month), int(start_day))
        end_date = datetime(int(end_year), int(end_month), int(end_day))
    
        date_list = list(rrule(DAILY, dtstart=start_date, until=end_date))

        # me marr ni training object me filtru me startdate edhe end date
        # nbaze tqasaj edhe klases me gjet a osht free qajo klas
        # nese jo me kqyr kush e ka rezervu
        # JO me marr klasen edhe mi marr dates unavailble tklases
        # edhe me kqyr a po osht naj dit nqit liste tditve

        #class_room = list(Class_rooms.objects.filter(id = class_id[1:]).values_list('dates_unavailable',flat = True))
        class_room = list(Class_rooms.objects.filter(id = class_id).values_list('dates_unavailable',flat = True))
        dates = []

        output = ''
        testing = []
        
        testing2 = testing2+1
        #if len(class_room) == 1:
        if class_room[0] == None:

            output = "True"
            
            testing.append('first')
            testing3 = testing3 + 1

        else:
            testing4 = testing4 + 1
            testing.append('second')
            for date in class_room:
                dates.append(list(Date.objects.filter(id = date).values_list('date',flat = True)))
                #dates.append(Date.objects.filter(id = date).values_list('date',flat = True))
            
            dates_unavailable = []
            for element in dates:
                dates_unavailable.append(element[0])

            #date_list1 = [datetime.strptime(date.strftime("%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S") for date in date_list]
            date_list2 = [datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d") for date in dates_unavailable]

            
            for date1 in date_list:
                for date2 in date_list2:
                    if date1 == date2:
                        output = 'False'
                        
                        testing.append('third')
                        break
                else:
                    continue
                break
            else:
                output = 'True'
                
                testing.append('forth')

        output_list.append(output)
        

    return JsonResponse({"message": output_list}, status=201)

'''
@method_decorator(csrf_exempt, name='dispatch')
def change_day(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    #csrf_token = request.headers.get('csrf_token')
    #if csrf_token and csrf.get_token(request) == csrf_token:
    data = json.loads(request.body)
    page = data.get("page")
    trainingday = data.get("training_day")

    #return redirect('training_observation')
    #return JsonResponse({"message": trainingday}, status=201)
    url = 'trainingdays/{}/{}'.format(page, trainingday)
    #return redirect('observation', page = 14, trainingday = 2)
    return redirect(reverse('trainingdays/14/2'))
    #return redirect('observation', page=page)
    #else:
    #    return HttpResponseForbidden('CSRF token missing or invalid')
'''

def add_classroom(request):
    form_list = ["What is the room number?","How many Seats?","In what site?"]
    if request.method == "POST":
        form = NewClassroomForm(request.POST)

        if "remove" in request.POST:
            remove_id = request.POST["remove_class"]
            Class_rooms.objects.filter(id = remove_id).delete()
            #request.POST["remove_class"]

        # me shkru kod per me hek classroom mandej mi bo migrimet
        if form.is_valid():
            # me shtu error message nese i qet room t njejt
            if "add" in request.POST:
                seats = form.cleaned_data["seats"]
                site = form.cleaned_data["Site"]
                room = form.cleaned_data["room"]

                #active_user = request.user
                try:
                    Class_rooms(seats=seats, Site=site, room_number=room).save()
                except IntegrityError:
                    return render(request, 'training_scheduling/add_classroom.html', {
                        'form': zip(NewClassroomForm(),form_list), 
                        'error_message': 'Requested room is already taken'})
                #return HttpResponseRedirect(reverse("new_listing", args=(page,)))
                return redirect(reverse('index'))

        else:
            return render(request, "training_scheduling/add_classroom.html", {
            "form": zip(form,form_list)
        })
    return render(request, "training_scheduling/add_classroom.html", {
            "form": zip(NewClassroomForm(),form_list)

        })
    

'''
Notes: 
- me hek seats krejt spo vyn sen
- me ndrru ne class me bo qe konfigurimin me zgedh veq me 1 button
- me shtu ni form per observations edhe me bo qat pjese me javascript

<!--{% for day_student in day_students %}
                {% for student in day_student %}
                    <tr>
                        <td id="{{ student.training_day.training_day_date }}std">{{ student.training_day.training_day_date }}</td>
                        <td id="{{ student.training_day.training_day_date }}std">{{ student.student_name }}</td>
                        <td id="{{ student.training_day.training_day_date }}std">{{ student.student_surename }}</td>
                        <td id="{{ student.training_day.training_day_date }}std"><input type="checkbox" id="attended" /></td>
                        <td id="{{ student.training_day.training_day_date }}std"><input type="time" id="arrival" /></td>
                        <td id="{{ student.training_day.training_day_date }}std"><input type="time" id="left" /></td>
                        <td id="{{ student.training_day.training_day_date }}std">{{ student.training_day.training.class_room.room_number }}</td>
                        <td id="{{ student.training_day.training_day_date }}std"><input type="text" id="comment" /></td>
                    </tr>
                {% endfor %}
            {% endfor %}-->



QIKJO PER POST OBSERVATION NESE SDU ME BO ME JACASCRIPT
        overall_training_comment = form.get('comment_all')
        list_of_student_id = form.get('studentID1')
        student_attended = form.getlist("student_attended")
        student_arrival = form.getlist("student_arrival_time")
        student_left = form.getlist("student_left_time")
        student_comment = form.getlist("training_day_student_comment")

        studentIDs = re.findall(r'\(([^)]+)\)', list_of_student_id)

        for id, comm, att, arrive, left in zip(studentIDs, student_comment, student_attended, student_arrival, student_left):
            student = Students.objects.get(id=id)
            student.training_day_comment = comm
            if att == 'on':
                student.training_day_attendance = True
            elif att == 'off':
                student.training_day_attendance = False
            student.training_day_arrival = arrive
            student.training_day_left = left
            #student.save()

        return render(request, 'training_scheduling/login.html', {
            "test": student_left
        })
'''

'''
- me bo export pdf
- me bo varsisht prej userit edhe loginit
- me bo ni view per me ta qit kur o klasa free


href="/{{ class_room.id }}"

test komment
'''
