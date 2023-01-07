from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    '''
    AUTHERISATION_CHOICES = [
        ('NORMAL', 'Normal'), 
        ('TRAINER', 'Trainer'),
    ]
    AUTHERISATION = models.CharField(
        max_length=30,
        choices=AUTHERISATION_CHOICES,
        default='NONE',
    )
    '''
    pass

'''
class Seats(models.Model): 
    #seat_class_room = models.ForeignKey(Class_rooms, on_delete = models.CASCADE, related_name="Class_rooms")
    seat_created_date = models.DateField(auto_now = True)

    CONFIG_CHOICES = [
        ('TCHIBO', 'Tchibo'), 
        ('SKY', 'Sky'),
        # mi shtu krejt edhe munsin me shtu admini vet congifigurim nese se gjen qata qe i vyn
    ]
    Config = models.CharField(
        max_length=30,
        choices=CONFIG_CHOICES,
    )

    working_seat = models.BooleanField()
    teacher_seat = models.BooleanField()
    reserved_seat = models.BooleanField(default=None, blank=True)
'''

class Date(models.Model):
    date = models.DateField()

class Class_rooms(models.Model): 

    SITE_CHOICES = [
        ('SITE1', 'site1'), 
        ('SITE2', 'site2'),
    ]
    Site = models.CharField(
        max_length=30,
        choices=SITE_CHOICES,
    )
    seats = models.IntegerField()
    created_date = models.DateField(auto_now = True)
    class_available = models.BooleanField(default=True)
    dates_unavailable = models.ManyToManyField('Date', related_name='unavailable', blank=True, null=True) # liste e datave
    room_number = models.IntegerField(unique=True, error_messages={'unique':'This room has already been registered.'})


#class Date(models.Model):
#    date = models.DateField()
#    classroom = models.ForeignKey(Class_rooms, on_delete=models.CASCADE)


class Trainings(models.Model): 
    
    CONFIG_CHOICES = [
        ('PPROJECT1', 'Project1'), 
        ('PPROJECT2', 'Project2'),
        ('PPROJECT3', 'Project3'),
        ('PPROJECT4', 'Project4'),
        ('PPROJECT5', 'Project5'),
        # mi shtu krejt edhe munsin me shtu admini vet congifigurim nese se gjen qata qe i vyn
    ]
    Config = models.CharField(
        max_length=30,
        choices=CONFIG_CHOICES,
        default=None, 
        blank=True
    )
    PROJECT_CHOISES = [
        ('PPROJECT1', 'Project1'), 
        ('PPROJECT2', 'Project2'),
        ('PPROJECT3', 'Project3'),
        ('PPROJECT4', 'Project4'),
        ('PPROJECT5', 'Project5'),
        # mi shtu krejt edhe munsin me shtu admini vet congifigurim nese se gjen qata qe i vyn
    ]
    project = models.CharField(
        max_length=30,
        choices=PROJECT_CHOISES,
        default=None, 
        blank=True
    )
    TYPE_CHOICES = [
        ('TYPE1', 'Type1'), 
        ('TYPE2', 'Type2'),
        # mi shtu krejt edhe munsin me shtu admini vet congifigurim nese se gjen qata qe i vyn
    ]
    type_training = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default=None, 
        blank=True
    )
    class_room = models.ForeignKey(Class_rooms, on_delete = models.CASCADE, related_name="Class_rooms")
    created_date = models.DateField(auto_now = True)
    reserved_by =  models.ForeignKey(User, on_delete = models.CASCADE, related_name="User")
    pre_training_comment = models.CharField(max_length=2000, null = True, default=None, blank=True)
    post_training_comment = models.CharField(max_length=20000, null = True, default=None, blank=True)
    training_start_date = models.DateField()
    training_end_date = models.DateField()
 
class Training_days(models.Model): 
    training = models.ForeignKey(Trainings, on_delete = models.CASCADE, related_name="Trainings")
    overall_comment = models.CharField(max_length=2000)
    IT_comment = models.CharField(max_length=20000)
    training_day_date = models.DateField()

class Students(models.Model): 
    #CCMS_ID = models.IntegerField()
    training_day = models.ForeignKey(Training_days, on_delete = models.CASCADE, related_name="Training_days")
    pre_training_comment = models.CharField(max_length=2000, default=None, blank=True)
    training_day_comment = models.CharField(max_length=2000, null = True, default=None, blank=True)
    overall_comment = models.CharField(max_length=2000, null = True, default=None, blank=True)
    training_day_arrival = models.TimeField(null = True, default=None, blank=True)
    training_day_left = models.TimeField(null = True, default=None, blank=True)
    training_day_attendance = models.BooleanField(null = True, default=None, blank=True)
    student_name = models.CharField(max_length=100, null = True, default=None, blank=True)
    student_surename = models.CharField(max_length=100, null = True, default=None, blank=True)

# me bo review per trainer prej nxansave


    


