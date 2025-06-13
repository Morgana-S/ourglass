# Testing and Code Validation

## Automated Testing
The project contains two apps, the events app and the contact app. These apps are tested seperately. My primary focus for the project was implementing functionality, so unit testing was not carried out until afterward.  I have still included automated tests based on that process to demonstrate an understanding of the concept, as well as a desire to gain further familiarity with the process.

Automated testing was carried out using the in-built django testing library, which is based on unittest. While testing, I used an sqlite database to create mock data for the tests. This allowed me to focus on the behaviour of the forms and views rather than worrying about creating or using junk data in the PostgreSQL database.

Fortunately, the testing process revealed a few bugs and many instances of poorly-planned
views, which have since been altered and refactored. The history of these refactors is available in the git commits, but I have also included these in the bugs section below.

### Events App Automated Testing
There is a warning in the below tests that an unordered list may result in inconsistent order
when paginating - this is for the reviews, which do not necessarily need to be ordered to be presented; I am therefore ignoring this warning.
![Testing - Events App](/documentation/testing-images/testing-events.png)

### Contact App Automated Testing
![Testing - Contact App](/documentation/testing-images/testing-contact.png)

## Manual Testing
All Testing was carried out on the latest deployed version of the project on Heroku. 
The following tests were carried out:

### Browser Compatability

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
Browser - Basic Functionality | Website was opened with Microsoft Edge, Google Chrome and Mozilla Firefox. Website functionality was tested with the tests below. | Website loads correctly on all browsers. | Website loaded correctly on all tested browsers. Further information about individual tests carried out in the below sections. |
| Device - Basic Functionality | Website was opened using a desktop PC, Google Pixel 7 Mobile device, iPhone, and iPad. Website functionality was tested with the tests below. | Website loads correctly on all devices. | Website loaded correctly on all tested devices. Further information on individual tests carried out in the below sections.

### Responsiveness Testing Images
#### Index Page - Anonymous
![Anonymous Index Page - iMac](/documentation/testing-images/anon-index-imac.png)
![Anonymous Index Page - iPhone](/documentation/testing-images/anon-index-iphone-14.png)
![Anonymous Index Page - Pixel](/documentation/testing-images/anon-index-pixel.png)
![Anonymous Index Page - Tablet](/documentation/testing-images/anon-index-ipad.png)
#### Index Page - Logged In
![Authorised User Index Page - iMac](/documentation/testing-images/auth-index-mac.png)
![Authorised User Index Page - iPhone](/documentation/testing-images/auth-index-iphone.png)
![Authorised User Index Page - Pixel](/documentation/testing-images/auth-index-pixel.png)
![Authorised User Index Page - Tablet](/documentation/testing-images/auth-index-ipad.png)
#### Sign Up Page
![Sign Up Page - iMac](/documentation/testing-images/sign-up-mac.png)
![Sign Up Page - iPhone](/documentation/testing-images/sign-up-iphone.png)
![Sign Up Page - Pixel](/documentation/testing-images/sign-up-pixel.png)
![Sign Up Page - Tablet](/documentation/testing-images/sign-up-ipad.png)
#### Log In Page
![Log In Page - iMac](/documentation/testing-images/log-in-mac.png)
![Log In Page - iPhone](/documentation/testing-images/log-in-iphone.png)
![Log In Page - Pixel](/documentation/testing-images/log-in-pixel.png)
![Log In Page - Tablet](/documentation/testing-images/log-in-ipad.png)
#### Contact Us Page
![Contact Us Page - iMac](/documentation/testing-images/contact-us-mac.png)
![Contact Us Page - iPhone](/documentation/testing-images/contact-us-iphone.png)
![Contact Us Page - Pixel](/documentation/testing-images/contact-us-pixel.png)
![Contact Us Page - Tablet](/documentation/testing-images/contact-us-ipad.png)
#### My Events Page
![My Events Page - iMac](/documentation/testing-images/my-events-mac.png)
![My Events Page - iPhone](/documentation/testing-images/my-events-iphone.png)
![My Events Page - Pixel](/documentation/testing-images/my-events-pixel.png)
![My Events Page - Tablet](/documentation/testing-images/my-events-ipad.png)
#### Book Events (All Events Page)
![All Events Page - iMac](/documentation/testing-images/all-events-imac.png)
![All Events Page - iPhone](/documentation/testing-images/all-events-iphone.png)
![All Events Page - Pixel](/documentation/testing-images/all-events-pixel.png)
![All Events Page - Tablet](/documentation/testing-images/all-events-ipad.png)
#### Search Events Page
![Search Events Page - iMac](/documentation/testing-images/search-events-mac.png)
![Search Events Page - iPhone](/documentation/testing-images/search-events-iphone.png)
![Search Events Page - Pixel](/documentation/testing-images/search-events-pixel.png)
![Search Events Page - Tablet](/documentation/testing-images/search-events-ipad.png)
#### Create Event
![Create Event Page - iMac](/documentation/testing-images/create-event-mac.png)
![Create Event Page - iPhone](/documentation/testing-images/create-event-iphone.png)
![Create Event Page - Pixel](/documentation/testing-images/create-event-pixel.png)
![Create Event Page - Tablet](/documentation/testing-images/create-event-ipad.png)
#### Event Detail Page - Event Attendee
![Event Detail Page - Attendee View - iMac](/documentation/testing-images/event-attendee-mac.png)
![Event Detail Page - Attendee View - iPhone](/documentation/testing-images/event-attendee-iphone.png)
![Event Detail Page - Attendee View - Pixel](/documentation/testing-images/event-attendee-pixel.png)
![Event Detail Page - Attendee View - Tablet](/documentation/testing-images/event-attendee-ipad.png)
#### Event Detail Page - Event Organiser
![Event Detail Page - Organiser View - iMac](/documentation/testing-images/event-organiser-mac.png)
![Event Detail Page - Organiser View - iPhone](/documentation/testing-images/event-organiser-iphone.png)
![Event Detail Page - Organiser View - Pixel](/documentation/testing-images/event-organiser-pixel.png)
![Event Detail Page - Organiser View - Tablet](/documentation/testing-images/event-organiser-ipad.png)
#### Book Tickets Page
![Book Tickets Page - iMac](/documentation/testing-images/book-ticket-mac.png)
![Book Tickets Page - iPhone](/documentation/testing-images/book-ticket-iphone.png)
![Book Tickets Page - Pixel](/documentation/testing-images/book-ticket-pixel.png)
![Book Tickets Page - Tablet](/documentation/testing-images/book-ticket-ipad.png)
#### Edit Booking Page
![Edit Booking Page - iMac](/documentation/testing-images/edit-booking-mac.png)
![Edit Booking Page - iPhone](/documentation/testing-images/edit-booking-iphone.png)
![Edit Booking Page - Pixel](/documentation/testing-images/edit-booking-pixel.png)
![Edit Booking Page - Tablet](/documentation/testing-images/edit-booking-ipad.png)
#### Edit Event Page
![Edit Event Page - iMac](/documentation/testing-images/edit-event-mac.png)
![Edit Event Page - iPhone](/documentation/testing-images/edit-event-iphone.png)
![Edit Event Page - Pixel](/documentation/testing-images/edit-event-pixel.png)
![Edit Event Page - Tablet](/documentation/testing-images/edit-event-ipad.png)
#### Leave Review Page
![Review Event Page - iMac](/documentation/testing-images/review-event-mac.png)
![Review Event Page - iPhone](/documentation/testing-images/review-event-iphone.png)
![Review Event Page - Pixel](/documentation/testing-images/review-event-pixel.png)
![Review Event Page - Tablet](/documentation/testing-images/review-event-ipad.png)
#### Edit Review Page
![Edit Review Page - iMac](/documentation/testing-images/edit-review-mac.png)
![Edit Review Page - iPhone](/documentation/testing-images/edit-review-iphone.png)
![Edit Review Page - Pixel](/documentation/testing-images/edit-review-pixel.png)
![Edit Review Page - Tablet](/documentation/testing-images/edit-review-ipad.png)

### Navigation

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Unauthorised User Navigation Bar Use | Clicking all links on the navigation bar as an anonymous user. | All navigation links work and navigate to the correct page. | Working as intended. |
| Authorised User Navigation Bar Use | Log the user in, and click all links on the navigation bar. | All navigation links work and navigate to the correct pages. | Working as intended. |
| Unauthorised User Link Navigation | Go through the pages available to anonymous users and click every button or link to ensure they navigate correctly. | All navigation links work and navigate to the correct locations. | Working as intended. |
| Authorised User Link Navigation | Log the user in, go through all pages accessible to the user and ensure they lead to the correct locations. | Working as intended. | 
| Footer Link | Clicking the link to my GitHub page, as both a logged in and anonymous user. | Link opens a new tab to my GitHub page for the project. | Working as intended. |

### User Authentication and Authorisation

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Signing Up | Anonymous user navigates to the sign up page, provides account credentials, and clicks the sign up button. | User account is created, they receive an email that contains a link for them to click to verify their account. Once clicked, the user has full access to the site. | Working as intended. |
| Unverified User unable to access site | Anonymous user signs up, and then, before verifying their account, attempts to log in. | User is informed that they need to verify their account, and another confirmation email is sent to their registered email address. | Working as intended.
| Logging In | Anonymous user navigates to the log in page, and signs into account using details. | User logs in successfully, is informed that they have logged in, and is redirected back to the index page. | Working as intended.
| Anonymous User - Attempt to Create an Event | While not logged in, user navigates to /events/create-event/. | User is redirected to index page, and a message displays saying they can't create an event. | Working as intended. | 
| Anonymous User - Attempt to Edit an Event | While not logged in, user navigates to /events/edit-event/32. | User is redirected to index page, and a message displays saying they can't edit an event. | Working as intended. | 
| Anonymous User - Attempt to Delete an Event | While not logged in, user navigates to /events/delete-event/32. | User is redirected to index page, and a message displays saying they can't delete an event. | Working as intended. | 
| Anonymous User - Attempt to Book Tickets for an Event | While not logged in, user navigates to /events/book-tickets/72. | User is redirected to index page, and a message displays saying they can't book tickets for an event. | Working as intended. | 
| Anonymous User - Attempt to Edit Booking for an Event | While not logged in, user navigates to /events/edit-booking/17. | User is redirected to index page, and a message displays saying they can't edit tickets for an event. | Working as intended - message indicates they are attempting to book tickets rather than edit a booking. Fixed message. | 
| Anonymous User - Attempt to Delete Tickets for an Event | While not logged in, user navigates to /events/delete-booking/17. | User is redirected to index page, and a message displays saying they aren't logged in. | Working as intended. | 
| Anonymous User - Attempt to Review an Event | While not logged in, user navigates to /events/review-event/32. | User is redirected to index page, and a message displays saying they aren't logged in. | Working as intended. | 
| Anonymous User - Attempt to Edit a Review | While not logged in, user navigates to /events/edit-review/10. | User is redirected to index page, and a message displays saying they aren't logged in. | Working as intended. | 
| Anonymous User - Attempt to Delete a Review | While not logged in, user navigates to /events/delete-review/10. | User is redirected to index page, and a message displays saying they aren't logged in. | Working as intended. | 
| Authorised User - Attempt to Edit an Event (not organiser) | While logged in, user navigates to /events/edit-event/15/ They are not the organiser of this event. | User is unable to edit the event, and is prompted to return to the event detail page. | Working as intended. | 
| Authorised User - Attempt to Delete an Event (not organiser) | While logged in, user navigates to /events/delete-event/15/ They are not the organiser of this event. | User is unable to delete event, and is redirected to the event detail page. A message displays saying the user can't delete the event. | Working as intended. | 
| Authorised User - Attempt to Review Event (not attendee) | While logged in, user navigates to /events/review-event/4/. They are not an attendee for the event. | User is able to enter content in the review, but upon submission, they are directed back to the event detail page with a message about not being able to leave a review. | Working as intended. | 
| Authorised User - Attempt to Edit a Review (not reviewer) | While logged in, user navigates to /events/edit-review/10/. They are not the original reviewer. | User is able to edit the review content, but upon submission, they are returned to the event page with a message about the review not being updated. | Working as intended. | 
| Authorised User - Attempt to Delete a Review (not reviewer) | While logged in, user navigates to /events/delete-review/10/. They are not the original reviewer. | As the only way for this request to be accessed by ordinary use is a GET request (if they are not the original reviewer), the user is directed back to the index page with an error message. | Working as intended. Considered changing the GET request error, but given that users should not access the delete-review view this way under ordinary circumstances, I will leave as-is as it's something the site admins should be contacted about.|


### CRUD Functionality, Forms and Input
| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Authorised User - Create Event | The user logs in, goes to the create-event page, and fills out the details of their event, providing all fields. | Event is created with user input details. | Working as intended. |
| Authorised User - Create Event - Invalid Date | The user logs in, goes to the create-event page, and fills out the details of their event, providing all fields, but having an event in the past. | Event is not created, user receives error message confirming this and the field is shown as not being filled properly. | Working as intended. |
| Authorised User - Create Event - No image | The user logs in, goes to the create-event page, and fills out the details of their event, providing all fields, but does not submit an image | Event is not created, user is directed to upload an image.| Working as intended. |
| Authorised User - Create Event - Invalid file | The user logs in, goes to the create-event page, and fills out the details of their event, providing all fields, but submits a file that isn't an image. | Event is not created, user is directed to upload an image.| User can submit files that are not images - this is handled by displaying the alt text for the "image", which is the event name.  Bug detailed below.|
| Authorised User - Create Event - Invalid Attendee Number | The user logs in, goes to the create-event page, and fills out the details of their event, providing all fields, but sets the event attendees to 0. | Event is not created and user is given a message to explain they need to provide a valid attendee number.| Working as intended.|
| Authorised User - Create Event - Invalid Attendee Number | The user logs in, goes to the create-event page, and fills out the details of their event, providing all fields, but sets the event attendees to -60. | Event is not created and user is asked to provide a number that isn't below 0.| Working as intended.|
| Authorised User - Create Event - Invalid Attendee Number | The user logs in, goes to the create-event page, and fills out the details of their event, providing all fields, but sets the event attendees to 1000. | Event is not created and user is given a message to explain they need to provide a valid attendee number.| Working as intended.|

### Custom JavaScript Functionality

### Admin Functionality

## Peer Reviewed Testing

## Feedback

## Bugs
- **Create-Event Form: The maximum_attendees value has a min value of 0, despite being explicitely set to min value of 1.**
    - Cause: Unknown
    - Solutions tried: Validating the field within the model using the MinValidator, explicitly setting the min=1 in the forms.py file
    - Fix: I have added placeholder text asking the user to enter a number from 1 to 200. As the form validates the input to check if it's above 0, the user is not currently able to submit a form that does not do this. Given instructions are provided in the form input, the user must willfully ignore these instructions to cause the issue, so I consider this fix suitable for now.

- **Forms: Forms do not appear to update their values in the html attributes.**
    - Cause: Unknown, suspect it may have something to do with the javascript for Bootstrap's form controls.
    - Fix: When the form is POSTed, either as a new or updated form, it appears the values in the inputs are read at that moment: For example, if the maximum_attendees field has an invalid value of 0, which is then updated to 2, although the html attr value reads 0, when the form is posted, it will post with the correct value of 2. This issue appears to mostly be a visual one at present.

- **MyEventsDashBoardView - Logged in users were not being directed to the account/login page if they tried to access the my-events page.**
    - This was discovered during automated testing using the test_redirect_if_not_logged_in test.
    - Fix: Changed the view to require the LoginRequiredMixin.

- **event_detail_view: user_tickets were not being correctly instantiated if the user wasn't logged in.**
    - This was discovered during automated testing using the test_event_detail_view_status_and_template test.
    - Cause: user_tickets were being instantiated after the authentication check. 
    - Fix: Instantiate user_tickets as None before checking if the user is authenticated.

- **logout_view: While testing, despite the fact that it's testing for an anonymous user, django still tries to check if event.event_id is valid. An anonymous user should never see this template, as it's wrapped in an {% if request.user.is_authenticated %} conditional.**
    - This was discovered during automated testing using the test_logs_user_out_and_redirects test.
    - Fix: As this seems to be an unintended behaviour with how django works, a single event was mocked in the test setUp to ensure there was data that was valid.

- **delete_event_view: Anonymous users were being directed back to the event-detail page when they attempted to delete an event.**
    - Cause: This is because the view did not check whether the user is authenticated.
    - Fix: Add is_authenticated conditional and redirect user to index page with message if they are not logged in.

- **Messages: messages informing the user of the success of an action get trapped behind other page elements, such as on the my events page, they get stuck behind the event cards.**
    - Cause: This is caused by the z-index of messages not being high enough.
    - Fix: Z-Index of messages set to z-3 using bootstrap to ensure they appear above other elements.

- **Creating / Editing an Event: Attempting to upload a file that isn't an image is possible.**
    - Cause: This is because of a lack of validation of image data when submitting an image.
    - Tried Solutions: Attempting to implement a quick fix by passing cleaned image data to the Pillow library(https://pypi.org/project/pillow/) and also attempted to implement the CloudinaryFileForm input, which threw more errors as forms were not designed for use with these fields.
    - Current Status: Known issue, has been logged on the issues page. As the user is directed to upload an image by default, they would have to attempt to deliberately circumvent the image upload.
## Code Validation

## Lighthouse Reports
