# Testing and Code Validation

## Automated Testing
The project contains two apps, the events app and the contact app. These apps are tested seperately. My primary focus for the project was implementing functionality, so unit testing was not carried out until afterward.  I have still included automated tests based on that process to demonstrate an understanding of the concept, as well as a desire to gain further familiarity with the process.

Automated testing was carried out using the in-built django testing library, which is based on unittest. While testing, I used an sqlite database to create mock data for the tests. This allowed me to focus on the behaviour of the forms and views rather than worrying about creating or using junk data in the PostgreSQL database.

Fortunately, the testing process revealed a few bugs and many instances of poorly-planned
views, which have since been refactored. The history of these refactors is available in the git commits, but I have also included these in the bugs section below.

### Events App Automated Testing
There is a warning in the below tests that an unordered list may result in inconsistent order
when paginating - this is for the reviews, which do not necessarily need to be ordered to be presented; I am therefore ignoring this warning.
![Testing - Events App](/documentation/testing-images/testing-events.png)

### Contact App Automated Testing
![Testing - Contact App](/documentation/testing-images/testing-contact.png)

## Manual Testing

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

## Code Validation

## Lighthouse Reports
