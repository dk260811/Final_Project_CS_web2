# Training Scheduling

In this project, I build a Django application that handles organizing training classes or conference room reservations.
I got the Idea from the company I work in, sometimes trainers and managers have problems keeping track of which class or room is free to use and which ones are reserved.

## Distinctiveness and Complexity

I believe that the complexity of my project is sufficient. I did now copy any of the other projects that we did in this course or any prior project done by other students.
Not only that, but I have used Django and have created 5 models that utilize foreign keys and many to many fields, my application uses 12 URLs and 10 views. I use 6 JavaScript functions that utilize fetch methods with get and post.

## Created Files

### Training_scheduling
This is the name of my Django project inside my main folder (final_project).

### - static
- "inbox.js": this is my JavaScript file and these are the functions that I used:
    - show_availability: this function is active in the index page and changes the last row of the table depending on the room availability in the selected reservation interval
    - load_observation: this function is active on the class observation page, it activates when clicking save observation after editing it
    - change_day: this function is active on the class observation page, it activates when you click on one of the dates in the dates' navigation bar and changes the training day in order to fill in information for that specific date
    - save_observation: his function is active on the class observation page, it activates when clicking edit observation and lets you input data about the training day and save to display it.
- "styles.css": this is where I style my HTML code

### - templates
These are all the HTML templates that I use
- "add_classroom.html"
- "class.html"
- "index.html"
- "layout.html"
- "login.html"
- "register.html"
- "reserved_trainings.html"
- "training_observation.html"

### - views
- The views and classes that I used:
    - "NewClassroomForm": class to generate Forms rendered in HTML code
    - "NewTrainingForm": class to generate Forms rendered in HTML code
    - "NewConfigForm": class to generate Forms rendered in HTML code
    - "NewObservationForm": class to generate Forms rendered in HTML code
    - "index": the view for the index page
    - "register": the view for the register page
    - "login_view": the view for the login_view page
    - "logout_view": the view for the logout_view page
    - "class_room": this view works with get (to render the class HTML) and post (to save reservation and render the reserved_trainings page) requests
    - "reserved_trainings": this view renders the reserved_trainings page when it's accessed by clicking the main navigation bar link
    - "training_observation": this view uses get requests to render the training_observation page (initially it displays the first day of the reserved training but the change_day JavaScript function also sends get requests to this view in order to change the training day in the training_observation page) and post requests to remove reserved trainings
    - "training_observation_change": this view only works with post requests, and uses JSON data to save information about students in a specific training day and display it to the page
    - "class_available": this view uses only post requests to return JSONResponses to the show_availability JavaScript function in order to change the availability information in the index page (the last row of the table of classes in that page)
    - "add_classroom": uses get requests to render the add_classroom HTML file and post request to add rooms

### - URLs
I use 12 URLs in my application

### - models
- The models that I used:
    - Date: saves the dates in which the rooms are reserved
    - Class_rooms: information about the rooms
    - Trainings: information about the reserved trainings
    - Training_days: information about every training day that is created when reserving a room
    - Students: information about students that will participate in the trainings

## Requirements

- The needed requirements:
    - asgiref==3.5.2
    - DateTime==4.7
    - Django==4.1.3
    - numpy==1.23.5
    - pandas==1.5.2
    - python-dateutil==2.8.2
    - pytz==2022.6
    - six==1.16.0
    - sqlparse==0.4.3
    - tzdata==2022.6
    - zope.interface==5.5.2


## Usage

The starting page or the index page displays all created/existing classrooms in table form over which is a navigation bar, depending on if the user is logged in or not you will see different navigation links.
If you are not logged in you will see 3 navigation links Training Rooms/Reserve Class (the page you are currently on), Log In (to login if you have a user) and Register (to register if you don't have a user).
Even if you don't have a user you can still view the classrooms and see if they are available. In the starting page over the table with classrooms there are two date input fields where you can select the interval for which you want to reserve the room, by clicking the "try dates" button the last row of the table changes depending on the availability of the classrooms, if it changes to false that means that the class is not available in that interval.
Nevertheless, even if a room is reserved you can still open the room view by clicking the numbers in the first column, clicking on one of the room IDs opens up the room page where you can reserve the room, this requires that you are logged in.
The only input that is required in order to reserve a class is the date input, but you can also select for what project the class is being reserved for, what configuration you want the PCs in the classroom to have and what type of training the reserved training will be, if the attendees are known you can also fill in their names and write comments about them. After filling in the required data, you can click on Reserve Classroom, which of course sets the reservation for the selected dates.
Clicking the reserve button opens up the "Reserved trainings" page, where you can see all classes reserved by the active user, this page is also reachable directly from the navigation bar. From this page you can view reserved rooms by clicking on the number in the first column, this opens up the "Training Observation" page.
The observation page lets you keep information (attendance, arrival time, left time and comments) on each student for every training day. You can switch between days by clicking on the dates in the navigation bar directly under the main navigation bar, and you can put in information by clicking the Edit Observation button which changes the view of the page, after filling out the desired fields you click on save observation and the page reloads with the new field values. Each user can cancel any reservation by clicking on "Remove reservation" in this page, which makes those dates of that training in that class available for new reservations.
Finally, the last button in the main navigation link "Add classrooms" opens up a page where you can add new rooms by selecting the Site (Building), the room number and the number of seats available in that room.
When finished, the user can log out by clicking the Logout button on the main navigation bar.
