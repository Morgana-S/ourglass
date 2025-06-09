# Ourglass - Workshop, Course, and Event Booking Web Application

## About

Ourglass is a web application created to make the process of creating and attending public workshops and classes easier. Ourglass is a web application that utilises HTML, CSS, JavaScript and Python, as well as utilising the Django and Bootstrap frameworks.

**The deployed version of the application can be accessed [here](https://ourglass-b80df2533ddf.herokuapp.com/).**

## UI and UX Design

Ourglass was the first project in which I gave full consideration to user needs. The full wireframes for the project, which can be found [here](/documentation/wireframes/ourglass_wireframes.pdf) contain a breakdown of how this was considered, but a brief write-up will be made here.

In the process of developing the UI and UX for Ourglass, I consulted with a few prospective users of the site - as Ourglass's focus is as a tool for regular people with varying degrees of tech-savvyness, a soft, 'friendly' approach to UI design was required. Using the Bootstrap framework and the built-in themes for color that come with it made this approach very simple. Individual relevant items are often displayed using cards, and a particular area of high interest, the 'latest events' section, uses a carousel which is accessible to both Desktop and mobile users.

The colors most often used on the site are white and green - again, promoting a softer, friendlier approach. Bootstrap's "success" class was often used for elements that would allow the user to read details of items, "warning" was often used as a color to indicate configuration and editability (which is reminiscent of color schemes that use similar yellow colors to indicate construction) and bootstrap's "danger" color, red, was often used for delete functionality and to indicate mandatory instructions - for example, in forms where all fields are required, or in helper text for forms where they were not filled correctly.

Using the personas crafted in the design process, Ourglass had these principles in mind during construction:

- Simple, but not simplistic: It was important to me that users were not overwhelmed with the creation and configuration of events, bookings, and reviews - but also that they feel they have access to the full range of functionality required to really customise these items.
- Navigational practices built with ease in mind: Whether on mobile or desktop, nearly any part of the site that's relevant to users can be accessed in just a few clicks. Nothing is hidden away in menus that doesn't need to be.
- Responsive: Using the Bootstrap framework made building a responsive application very easy, as the framework is designed for mobile-first applications. The site should be pleasant to view on both desktop and mobile devices of all sizes.
- Informative: If the user does something, they should know whether it worked or not. Whether it's logging in, booking tickets, editing an existing event - the user should be informed when what they're trying to do has worked, and when something hasn't.

## Target Audience

It would be a cop-out to say that Ourglass is built for anyone looking to attend or create events and workshops, but the website was built with two specific kinds of people in mind. A full breakdown of these people is in the Persona section of the wireframes, but I would like to outline their similarities here:

- Not necessarily tech-focused, especially as one of the examples I had in mind when developing the application was providing tech support sessions at a local library;
- People with skill, knowledge and experience, who wanted to make sharing those skills as easy as possible, with limited barriers to doing so;
- People who believe that improvement is an iterative process - this was quite important in developing the Review Model, as this was the foundation of why the model existed. When speaking to the people who were aggregated in the Personas, both expressed a desire to both leave and receive feedback on the events they organised and attended.

In short, Ourglass is aimed at the following groups of people:

- Event, class and workshop organisers, who are looking for a simple platform to advertise free events and taster sessions for courses, and are able to be provided with a limited but useful range of tools for doing so in the Event creation system and the Booking tickets system;
- Site users who are looking to attend the above events, who do not want to fuss about complicated booking systems or having to understand online ticket sales - in this way, the website acts almost as an RSVP system, with the bookings only indicative of reserved spaces for an event.

## Epics and User Stories

Early on in the design phase of the website, I created the Ourglass User Pathway, which is a flowchart that envisions how users would interact with the site. This is also present in the wireframes, but I will include it here for the sake of ease:

![Ourglass User Pathway Diagram](/documentation/diagrams/ourglass_user_pathway.png)

This diagram helped with me mapping out the website into **Themes, Epics, and User Stories.**

### Themes

Themes within the pathway are expressed as general categories for what exactly the user is doing - Navigation, Authentication, Attendee/Organiser Focused Experience, Event Attendance, and Event Feedback.

### Epics

Each of these themes was then broken down into one or more Epics - these epics were specifically named for the actual action the user is taken, such as "User navigates to site" and "User searches for Events". The themes were named as general ideas about what the user would be doing, but the epics were designed to highlight specific things that the user encounters while on the site.

### User Stories

Each of these Epics was then broken down into individual user stories. The full details of each epic and their user stories can be found in the wireframes, and each user story is labelled with both its Theme and MoSCoW prioritization category on the [Issues Page](https://github.com/Morgana-S/ourglass/issues) but an example has been provided below:

#### Epic - User Finds an Event

User Stories:

---

**Event summaries**

As an event attendee I can see an event summary after searching for events so I can read event details quickly to see if they are suitable for me.

Acceptance Criteria:

**AC1:** After using the search bar, cards for each event are displayed with a summary of information about the event.

**AC2:** This information should include the event name, date, a brief description of the event, and the location as well as distance from the user's location in the search terms.

**AC3:** User can then click on an individual card to view more details on the event, which takes them to the event page, where they can read further details on the event and register attendence if desired.

---

**Book tickets for an event**

As an event attendee I can book tickets for an event so I can reserve places at the event.

Acceptance Criteria:

**AC1:** When navigating to the event's detail page, there's an option to book tickets for the event.
**AC2:** Going to the booking form through this option will allow me to specify how many tickets I would like to book.
**AC3:** When confirmed, the booking should then appear under the "My Bookings" section on the My Events page.

---

**See how many people are attending an event**

As an event attendee and event organiser I can see how many people are attending an event so I can decide whether to attend that event/make decisions about the management of the event.

Acceptance Criteria:

**AC1:** When on an event page, the user can see how many people have registered to attend an event.
**AC2:** A user can also see how many total places are available on the event, allowing them to make decisions regarding registering to attend.
**AC3:** If the user is an event organiser, I can also see the usernames of people who have registered to attend the event.

---

**Leave messages on event pages** (This user story was decided to be left out in the end - please see the issue page for details)

As an event attendee or event organiser I can leave messages on event pages so I can ask/answer questions about the event.

Acceptance Criteria:

**AC1:** Navigating to the event page shows a comment section beneath the event description, where a logged in user can leave messages for the event organiser.
**AC2:** Comments are left with information about the commenters username, date of comment, and text message content.
**AC3:** Other users can provide replies to a comment, including the event organiser (who has an indicator in their comments that they are the organiser), answering any questions the user might have.

## Features

## Models

The project uses a variety of models, primarily centered on the process of creating, booking tickets for, and reviewing Events. These models were laid out in an Entity Relationship Diagram for advanced planning of the project details, which has been included here (if the image is too small, the full sized image can be found [here](/documentation/diagrams/ourglass_model_erd.png)):

![Entity Relationship Diagram for Ourglass](/documentation/diagrams/ourglass_model_erd.png)

Details of the models can be found below:

### Event Model
The event model is the crux of the site - this defines the nature of the events that can be booked, and includes fields such as event_name, event_date, is_online, url_or_address, maximum_attendees, and a few more which can be found in the [Models.py](/events/models.py) file.

Importantly, the Event Model relies on a foreign key to define it's relationship to the event organiser. Although account deletion isn't directly covered in the project at present, I made the decision to make sure that all events were deleted if the user account was deleted as this seemed an appropriate way to tidy up.

Another decision I made was the incorporation of the Event's current_attendees property as a method that was defined rather than a field itself. This is due to the dynamic nature of an event's current attendees property; it changes as more people make bookings for the event. This allows both event organisers and event attendees to see at a glance how many tickets are left, which allows them to make better decisions about whether to book tickets at the time of viewing the event.

### Booking Model
The booking model acts as an associative table between users and the events they are attending. As **many** users can attend **many** events, the implementation of the booking model as a table that cross-references both Event and User models and allows them to be tied together.

The Booking model contains a few key properties of note - the event foreign key, with the related name "bookings", allows me to access all of the bookings that an event has, which is useful in particular on the event-detail template. Similarly, the ticketholder property allows me to access all the users who have made bookings for the event.

I have decided to implement a fairness-based limit on the number of tickets a user can book, and in this case, I've chosen a limit of 4 tickets. This is enforced by the tickets property only having selection from the NO_OF_TICKETS choices variable. I feel that 4 people is the largest *reasonable* amount of tickets a person on one account can book; as the classes and workshops I have in mind for the site are likely to be relatively small, this allows other users the chance to book while also incentivizing regular users who book as part of someone else's group to make their own account and attend events on an individual basis.

### Review Model
The Review model is my feedback-centric model for after events have been attended. It takes the event foreign key (so that reviews can be accessed in the event-detail page) and links it with an author from the user foreign key. The user can then provide a rating between 1 and 5 stars (this is, strictly speaking, only a numerical value - the actual implementation of the stars on the review is handled by some custom JavaScript code found in the static files), as well as requesting they give some feedback in the content text field. 

All reviews must be approved before being visible to anyone except the reviewer; this is to make sure that reviews are not harassing or rude in nature.

## Testing, Bugs & Code Validation

## Changes and Considerations whilst the project was underway

- Originally each model's id was named something unique, such as event_id, user_id, etc. This was changed to just "id" for each model as this is generated by default in Django. Common use practices with Django indicate that using the "model_id" format is typically reserved for foreign keys.

- The Comment model was scrapped due to a lack of uniqueness. While the functionality of leaving comments on an event is useful, this is essentially the purpose of the Review model, which demonstrates more unique properties.

- The current_attendees variable for the event model is now dynamically defined using an @property decorator in the Event model. This is then subsequently validated in the BookingForm.

- Initial user stories did not include delete functionality for Events, Bookings, or Reviews. This was added in later.

## Potential Future Improvements

- Google Maps, or similar Map API implementation on the event page to show users better details on where the events are.

- Ratings data aggregation on the user profile pages, as well as fleshing out the user profile page more so that it's easier to see how many ratings an event organiser has, the average of their ratings, etc.

- Implementation of a proper user-to-user messaging system, as opposed to the defunct Comment model. This would allow users to message event organisers directly for any questions they might have.

# Deployment

## Deployment to Heroku

The project was deployed to Heroku near inception. The steps to deploy this are as follows:

1. Fork or clone this repository directly on github, or using your IDE terminal with the following code:
    - `git clone https://github.com/Morgana-S/ourglass.git`
2. Create a new application on Heroku:
    - This requires signing up for a Heroku account, which you can do [here.](https://signup.heroku.com/login)
    - Once your account has been created, and you are on the user dashboard, you will need to create a new app and give it a name.
    - In the settings tab, ensure the correct config vars are in place. In this project, you will need to define the following vars:
        - DATABASE_URL: The url for the location of your database, if you are using a cloud-based database. This project uses a cloud-based PostgreSQL database hosted by the Code Institute.
        - CLOUDINARY_URL: Your Cloudinary API url for hosting images located on event pages. You can substitute this for your preferred alternative cloud image hosting platform, if you would prefer to not use Cloudinary as part of your event model.
        - SECRET_KEY: This is your Django secret key, used for cryptographic signing.
        - EMAIL_HOST_USER and EMAIL_HOST_PASSWORD: I am using a simple gmail SMTP for sending out account activation emails. If you would like this functionality to work, I suggest setting up your own SMTP provider and functionality.
    - In the Deploy Tab, ensure the Heroku Application is linked to your cloned version of the GitHub Repo.
    - Ensure that your Procfile contains only the following code:
        - `web: gunicorn ourglass.wsgi`
        - The Procfile has been included with this project, but please ensure that Heroku recognizes this Procfile if your version of the project fails to deploy.
    - Ensure that the `requirements.txt` file is included as well, to make sure the deployment pulls all of the required libraries.
    - Click Deploy Branch, or Enable Automatic Deployment.

## Local Deployment

The project can also be deployed locally. To do so, please follow these instructions:

1. Fork or clone this repository directly on github, or using your IDE terminal with the following code:
    - `git clone https://github.com/Morgana-S/ourglass.git`

2. Create a virtual environment (optional, but recommended):
    - On Windows, the command for this is `python -m venv .venv`
    - On Linux/macOS, (assuming you have Python 3 and pip isntalled via package manager) - `python3 -m venv .venv`

3. Activate the virtual environment:
    - On Windows: `.venv\scripts\activate`
    - On Linux/ macOS, `source .venv/bin/activate`

4. Install Dependencies - Navigate to the project directory and install dependencies found in requirements.txt
    - Navigating out of the venv folder: `cd ..`
    - Navigating from your root directory: `cd <insert filepath here>\ourglass`
    - Installing dependencies: `pip3 install -r requirements.txt`

5. Creating your env.py file:
    - Create a file named env.py in your root directory for the project.
    - Add this to your .gitignore file to ensure your variables are kept secret.
    - Ensure the file imports the os library using the `import os` line at the top, and define variables for your:
        - DATABASE_URL
        - CLOUDINARY_URL
        - SECRET_KEY
        - EMAIL_HOST_USER
        - EMAIL_HOST_PASSWORD
    - Each of the above variables can be defined by using the `os.environ.setdefault()` method. For example:
        - `os.environ.setdefault('DATABASE_URL', '<insert database url here>')`
    - If you are using Google Mail as your email host provider, you will need to sign in to your account with an app password. Information on how to do this can be found [here](https://support.google.com/accounts/answer/185833?hl=en).

6. Run the Application:
    - To run the project with your machine as a host, you can then type the following into your terminal:
        - Windows: `python manage.py runserver`
        - Linux/macOS: `python3 manage.py runserver`
    - You will then be able to view the website by clicking the link to the address in the terminal or typing the following into your browser's URL address bar:
        - `http://127.0.0.1:8000/`

## Credits

## Tools

- [RealFaviconGenerator](https://realfavicongenerator.net/) - Resizing images for use in the Favicon for the site.

- [Cloudinary](https://cloudinary.com/) - Cloud based image hosting for event page images.

- [Visual Studio Code](https://code.visualstudio.com/) - My preferred IDE for developing the project.

- [Python](https://www.python.org/) - The main language utilised in the application settings.

- [HTML5](https://developer.mozilla.org/en-US/docs/Glossary/HTML5) - Basic HTML page structure, enhanced with Django Template Language

- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Custom page styling, when required outside of the classes provided by Bootstrap

- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Interactive functionality for pages, when required outside of the classes provided by Bootstrap

- [Heroku](https://www.heroku.com/) - Project Deployment and online site hosting

- [Git](https://git-scm.com/) - Version control system

- [GitHub](https://github.com/) - Project Repo Hosting

- [Licecap](https://www.cockos.com/licecap/) - Screen Recording Software for GIFs for feature images.

## Frameworks

## Libraries

- [dj_database_url](https://pypi.org/project/dj-database-url/) - Allows usage of the DATABASE_URL environment variable for providing a django-compatible database definition.

## Modules

### Python

- [pathlib](https://docs.python.org/3/library/pathlib.html) - Object-oriented Filesystem Paths

- [os](https://docs.python.org/3/library/os.html) - Miscellaneous operating system interfaces

- [datetime.timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects) - Used for validation of event creation to make sure users aren't creating events that are too far in the future. 

### Django

- [django.contrib.admin](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/) - Admin Interface functionality

- [django.urls.path and django.urls.include](https://docs.djangoproject.com/en/5.2/ref/urls/) - Allows defining url paths with their relationship to views and related names. Include allows other url.py files to be included as a path, which allows urls to be seperated out into their respective apps.

- [django.forms](https://docs.djangoproject.com/en/5.2/topics/forms/) - Allows the ModelForm to be used when defining class based forms for use in django views.

- [django.utils.timezone](https://docs.djangoproject.com/en/5.2/topics/i18n/timezones/) When the USE_TZ setting in settings.py is True, Django uses time-zone-aware date time objects. As my models use datetime fields for some of their properties, This ensures date time inputs in forms are timezone aware too.

- [django.contrib.messages](https://docs.djangoproject.com/en/5.2/ref/contrib/messages/) Used to provide feedback to the user based on their actions. Commonly used to display success and error messages after the user has used some form of CRUD functionality, as well as logging in and logging out.

- [django.contrib.auth logout](https://docs.djangoproject.com/en/5.2/topics/auth/default/#django.contrib.auth.logout) - Used to provide a simple way to log the user out - I feel this is more user-friendly than having to confirm logouts through allauth's method.

- [django.core.paginator](https://docs.djangoproject.com/en/5.2/topics/pagination/#the-paginator-class) - Allows pagination of querysets in views. Provides methods to access the items on each page.

- [django.db.models - OuterRef, Exists, Q, Case, When, BooleanField, Value](https://docs.djangoproject.com/en/5.2/ref/models/querysets) - Allows dynamic definition of querysets for usage in the search bar for events. django.db.models is also used in models.py files to define the models fields.

- [django.shortcuts.redirect](https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/#redirect) Allows the redirection to a URL when called.

- [django.shortcuts.render](https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/#render) - Combines a template with a context dictionary for variables defined in the view to allow access to provide a Httpresponse with the rendered text.

- [django.shortcuts.get_object_or_404](https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/#get-object-or-404) Calls get() on a given queryset, but raises a 404 error if the results do not exist.

- [django.contrib.auth.models User](https://docs.djangoproject.com/en/5.2/ref/contrib/auth/#user-model) - Django's default model for users.


### Summernote

- [django_summernote.admin](https://github.com/lqez/django-summernote) Allows summernote enhancements in the admin panel.

- [django_summernote.widgets.SummernoteWidget](https://github.com/lqez/django-summernote) - Allows me to define a specific form field as summernote editor capable. Used in the long-description of events to provide formatting to the user.

### Cloudinary

- [cloudinary.models CloudinaryField](https://cloudinary.com/documentation/django_helper_methods_tutorial) Model Field that allows direct upload of images to Cloudinary.

## Visual Assets

- [Unsplash](https://unsplash.com/) - Royalty Free stock photographs used in Wireframes for Personas and in Event Images
- [SVG Repo](https://www.svgrepo.com/svg/527141/hourglass) - Royalty Free SVG that serves as the basis of the favicon
