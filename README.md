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

Each of these themes

## Features

## Models

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

## Credits

## Tools

- [RealFaviconGenerator](https://realfavicongenerator.net/) - Resizing images for use in the Favicon for the site.

## Frameworks

## Visual Assets

- [Unsplash](https://unsplash.com/) - Royalty Free stock photographs used in Wireframes for Personas and in Event Images
- [SVG Repo](https://www.svgrepo.com/svg/527141/hourglass) - Royalty Free SVG that serves as the basis of the favicon
