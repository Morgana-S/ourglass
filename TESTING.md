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

#### Book Events (All Events Page)
#### Create Event



### Navigation

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Unauthorised User Navigation Bar Use | Clicking all links on the navigation bar as an anonymous user. | All navigation links work and navigate to the correct page. | Working as intended. |
| Authorised User Navigation Bar Use | Log the user in, and click all links on the navigation bar. | All navigation links work and navigate to the correct pages. | Working as intended. |
| Unauthorised User Link Navigation | Go through the pages available to anonymous users and click every button or link to ensure they navigate correctly. | All navigation links work and navigate to the correct locations. | Working as intended. |
| Authorised User Link Navigation | Log the user in, go through all pages accessible to the user and ensure they lead to the correct locations. | Working as intended. | 

### User Authentication and Authorisation

### CRUD Functionality

### Forms and User Input

### Responsiveness

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
## Code Validation

## Lighthouse Reports
