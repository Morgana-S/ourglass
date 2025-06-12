# Ourglass - Workshop, Course, and Event Booking Web Application

![Ourglass Site Mockup](/documentation/feature-images/devices-mockup.png)

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

### Context Sensitive Index Page
![Context Sensitive Index Page](/documentation/feature-images/context-sensitive-index.gif)
If the user is not logged in, they are presented with a landing page which explains the purpose of the website. When an account is created and they are logged in, this is replaced with more relevant functionality, such as a list of the latest events and the ability to search for events.

### Context Sensitive Navbar
![Context Sensitive Navbar](/documentation/feature-images/context-sensitive-navbar.gif)
The user's navbar changes depending on if they are logged in or not, providing relevant options to both users and funneling anonymous users towards creating an account for utilisation of the website.

### Account Registration
![Account Registration](/documentation/feature-images/account-registration.gif)
Users are able to register accounts on the website using django all-auth and crispy-forms. Users are then required to verify their email address before being able to access site features.

### Account Login
![Account Login](/documentation/feature-images/account-login.gif)
Users can then log into their account once it has been verified, and are provided a message confirming the success of doing so.

### Account Logout
![Account logout](/documentation/feature-images/account-logout.gif)
When the user is done with their session, they can easily log out of their account in one click on the navbar.


### Search for Events
![Searching for Events](/documentation/feature-images/search-for-events.gif)
Users can search for events when logged in by typing in words associated with the event. If the search field is left blank, all events will be listed. Clicking 'view event' on each one takes you to the event detail page.

### View Latest Events
![Viewing Latest Events](/documentation/feature-images/latest-events.gif)
A carousel on the index page appears for logged in users, which documents the last five created events. This provides event organisers with a chance to have their events on every user's index page, encouraging them to join. A bootstrap carousel component is used to make this feature both visually appealing and mobile accessible, as mobile users can swipe between the carousel items. Desktop users are able to user the included arrow icons to navigate. Clicking 'view event' on each one takes you to the event detail page.

### Event Detail Page
![Event Detail Page](/documentation/feature-images/event-detail-page.gif)
When a user has found an event they like, they can then view the event details in full. This includes the event name, event address or url, number of people booked, as well as a longer description of the event, rather than the short description often provided on event cards. The Event detail page also contains the option to book tickets for the event, and view reviews for past events.

### Booking Tickets
![Booking Tickets](/documentation/feature-images/booking-tickets.gif)
If a user decided to attend an event, they can then book tickets using a simple form which only asks them to provide the number of tickets they want to book. The event then updates to show that the number of tickets has been booked, and navigating to the users My Events page, the user can then find a list of all their future bookings.

### Editing or Cancelling a Booking
![Editing or cancelling a booking](/documentation/feature-images/cancelling-booking.gif)
If a user decided they want to book more or less tickets for an event, or cancel their booking all together, they can do so from both the My Events page and the Event Detail page. The user is asked to change their ticket amounts - these are checked against the current availability of tickets for the user. If the user decided to cancel their booking altogether, they are asked to confirm before the booking is cancelled.

### Creating an Event
![Creating an Event](/documentation/feature-images/creating-events.gif)
Creating an event is a simple process. The user can click on the Create Event option on the navbar, fill out the details of their event and provide an image (with formatting for a long description provided by django-summernote) and submit their event.

### Editing or Deleting Events
![Editing an Event](/documentation/feature-images/editing-events.gif)
![Deleting an Event](/documentation/feature-images/deleting-events.gif)
If the user makes a mistake, or would like to edit the event details, they can do so by editing the event on the Event Details page, or their My Events page. Users can also delete Events if they decide to cancel them, and are asked to confirm that they would like to do so via a modal.

### The My Events Dashboard
![My Events Dashboard](/documentation/feature-images/my-events.gif)
The My Events page acts as a dashboard for the user, where they can see at a glance all upcoming bookings, their organised events, and any past events so they can leave a review. Each area is paginated to allow for ease of reading and navigation.

### Leaving Reviews
![Leaving a Review](/documentation/feature-images/leaving-a-review.gif)
Users who have attended an event can leave a review where they rate the event and provide feedback to the organiser. All reviews need to be approved before they are visible to anyone who is not the reviewer. This can be done by the site staff in the admin panel.

### Editing or Deleting a Review
![Editing or Deleting a Review](/documentation/feature-images/editing-a-review.gif)
If the user makes a mistake during the review, it is easy for them to edit the review, or if they decide they don't want to leave a review after all, they can easily delete the review after confirming through a modal. If a user's review is approved, editing the review changes it back to unapproved, to avoid people using approved reviews to circumvent the site's policy on having friendly content.

### Contact Us Page
![Contact Us Form](/documentation/feature-images/contact-us.gif)
If users want to contact the site administrators, they can fill out the form on the Contact Us page. If the user is logged in, they are not required to provide their contact details such as their name or email address, as these are pulled from their instance of the user model.

### Form Verification
![Form Validation - Events](/documentation/feature-images/form-validation.gif)
![Form Validation - Reviews](/documentation/feature-images/form-validation-review.gif)
All user forms, for creating events, making bookings, or writing reviews, are validated to prevent invalid or nonsensical inputs. Examples include booking events too far in the future, for too many people, leaving reviews that are too short.

### Context-sensitive Event Details
![Context Sensitive Event Details](/documentation/feature-images/context-sensitive-event-details.gif)
Where it makes sense to, the user is prevented from doing things that don't really make sense - such as an event organiser booking tickets to their own event, users being able to edit events which they aren't the organiser of, and leaving reviews for events that haven't happened yet - or leaving more than one review per event, or leaving reviews for events they didn't attend.


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

For details of automated and manual tests, as well as code validation, please see the [TESTING.md](/TESTING.md) document.

## Changes and Considerations whilst the project was underway

- Originally each model's id was named something unique, such as event_id, user_id, etc. This was changed to just "id" for each model as this is generated by default in Django. Common use practices with Django indicate that using the "model_id" format is typically reserved for foreign keys.

- The Comment model was scrapped due to a lack of uniqueness. While the functionality of leaving comments on an event is useful, this is essentially the purpose of the Review model, which demonstrates more unique properties.

- The current_attendees variable for the event model is now dynamically defined using an @property decorator in the Event model. This is then subsequently validated in the BookingForm.

- Initial user stories did not include delete functionality for Events, Bookings, or Reviews. This was added in later.

## Potential Future Improvements

- Google Maps, or similar Map API implementation on the event page to show users better details on where the events are.

- Ratings data aggregation on the user profile pages, as well as fleshing out the user profile page more so that it's easier to see how many ratings an event organiser has, the average of their ratings, etc.

- Implementation of a proper user-to-user messaging system, as opposed to the defunct Comment model. This would allow users to message event organisers directly for any questions they might have.

- Account management on the user's behalf is barebones at the moment, with basic styling on the pages for password resets. Enhancing these features for users should be a priority for future work in the project, as this is an area the site is woefully lacking. Basic functionality exists if a user -needs- to reset, their password, but I wouldn't describe it as complete.

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

- [Django](https://www.djangoproject.com/) - Python-based web framework that allows fast deployment of web applications.

- [Bootstrap](https://getbootstrap.com/) - JavaScript and CSS Framework that provides versatile classes for use in styling a website and providing interactivity.

## Libraries

## Third-Party

- [dj_database_url](https://pypi.org/project/dj-database-url/) - Allows usage of the DATABASE_URL environment variable for providing a django-compatible database definition.

- [django-allauth](https://docs.allauth.org/en/latest/) Integrated authentication applications that assist with registration and management of user accounts.

- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) Provide bootstrap-capable form inputs using django template language.

-[dj3-cloudinary-storage](https://github.com/tiagocordeiro/dj3-cloudinary-storage) Django integration with cloudinary storage API.

- [django-summernote](https://github.com/lqez/django-summernote) - WYSIWYG Text editor for use in Django web applications.

- [whitenoise](https://whitenoise.readthedocs.io/en/stable/django.html) - Allows deployment of static files to django projects when hosted on heroku via WSGI.

- [gunicorn](https://gunicorn.org/) - Python WSGI HTTP server for hosting on heroku.

- [psycopg2](https://pypi.org/project/psycopg2/) - PostgreSQL database adapter for use with Python.

- [flatpickr](https://flatpickr.js.org/) - Datetime picker that enables localisation of date-time picking for create-event functionality.


### Python

- [pathlib](https://docs.python.org/3/library/pathlib.html) - Object-oriented Filesystem Paths

- [os](https://docs.python.org/3/library/os.html) - Miscellaneous operating system interfaces

- [datetime.timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects) - Used for validation of event creation to make sure users aren't creating events that are too far in the future. 

- [unittest](https://docs.python.org/3/library/unittest.html) - Library for performing unit testing of views and forms. Used through django.test by importing TestCase.

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

- [Bootstrap Icons](https://icons.getbootstrap.com/) - Provide the basis for svgs used to render as icons for the latest events carousel
