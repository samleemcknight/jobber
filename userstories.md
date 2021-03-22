# Jobber - Find and Register for Recruiting Events

**Elevator Pitch:** A site where users can search and register for recruiting events. Admin users can post events, change details about an event, and see a list of users registered for a specific event.
---

## Sprint 1: Basic Auth & Profiles

**All users should be able to:**

1. Navigate to "/" and see a basic splash page with:

- The name of the website.
- Links to "Log In" and "Sign Up".

2. Sign up for an account.
3. Log in to their account if they already have one.
4. Be redirected to their public profile page after logging in.
5. On their public profile page, see their name, and their join date.
6. See the site-wide header on every page with:

- A link to "Log Out" if they're logged in.
- Links to "Log In" and "Sign Up" if they're logged out.

7. Update their profile by making changes to their name.
8. An admin user should be able to add events through the admin panel.

### Bonuses

**A user should be able to:**

1. See a "default" profile photo on their profile page before adding their own photo.
2. Update their profile photo (consider using Paperclip or Uploadcare).
3. See their profile photo next to their events.
4. Receive a welcome email after creating an account.

---

## Sprint 2: CRUD

**All users should be able to:**

1. View a single event page (at "/events/1") including:

- The event title, date, and time.
- The name of the speaker or speakers.
- The industry focus of the event (tech workers/content creators/marketing etc.)
- A button to register for the event which reveals the link to join the event (links don't need to actually open a call).

2. View a list of events on the Home page:

- Sorted by date with the nearest event appearing first.
- With the event titles linked to the individual event "show" pages.

3. Use a search field to refine event results with specific keywords.
4. Use buttons to filter results by industry or type.
5. For events that the user has already registered for, show an icon or note indicating that to the user. Users can not register for events more than once.
6. Click "unregister" on ANY registered event to remove them from the guestlist, then:

- See a pop-up that says: "Are you sure you want to cancel your registration?"
- If the user confirms, take them off the event guestlist.

### Bonuses

**A user should be able to:**

1. Visit event pages via pretty urls, like "/events/node-jobs".
2. Visit user profile pages via pretty urls, like "/users/james", and see the events that user has registered for.
3. On the homepage:

- See event descriptions truncated to 1000 characters max, with a link to view more - do not display event details on the homepage. A user should have to click into the event to find out more information.
- See a relative event date, e.g. "2 days from now".

---

## Sprint 3: Validations & Authorization

**A user should be able to:**

1. Verify that an event they register for is successfully added to the profile page.

A user CANNOT save invalid data to the database, according to the following rules:

2. A user CANNOT sign up with an email (or username) that is already in use.
3. A user can update their password. Passwords should have atleast 8 characters, one capital letter, one number, and one special character.
4. An event must have a title, date, time, speaker, and description to be listed on the site.

A user is authorized to perform certain actions on the site, according to the following rules:

5. A user MUST be logged in to register/unregister for events and change their profile.
6. A user may only edit their own profile and register/unregister themselves from events.

#### Bonuses

**A user should be able to:**

1. View an error message when form validations fail, for the following validations:

- Email must be between 1 and 200 characters and should validate that the email saved to the DB is valid (contains one @ and at least one . characters)
- Passwords should have atleast 8 characters, one capital letter, one number, and one special character.

2. View only the 10 most recent events on the homepage (use pagination), with

- A link/button to the "Next" 10.
- A link/button to the "Previous" 10.

3. See a list of past events they've registered for on their public profile
4. See the number of total events they've attended.
5. Be able to view events they've attended by industry type on their public profile.

---

## Sprint 4: Admin Users

### Bonuses

**An admin user should be able to:**

1. Register and unregister any user for an event.
2. See the number of registrants an event has on the event's "show" page.
3. Be able to create, edit, and delete events through the website rather than through the admin panel - this functionality should only be available to admin users.
4. Admins should be able to an image for the event and a default image should appear for events that don't have an image specified.
