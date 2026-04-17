# Weekly Reports - Event Hub

Group No: 7
Event Hub
Weekly Report 1
Date: 19/12/2025

**Accomplishments this Week:**
Numerous Project Ideas were taken into consideration, such as:
• **College Canteen Ordering System:**
A system to avoid long queues during lunch breaks by allowing students to pre-order food. However, it requires complex real-time payment integration and inventory tracking, which might be too large for the mini-project scope.
• **Library Resource Manager:**
A platform to check the availability of textbooks and reserve them online. Found to be too similar to existing systems already deployed by the college.
• **Event Hub (College Event Management):**
Currently, information about technical symposiums, cultural fests, and workshops is scattered across WhatsApp groups and notice boards. An organized central repository is needed so students don't miss opportunities. Event Hub would serve as a unified platform to discover, register for, and manage campus events, offering an admin dashboard for organizers and a clean public interface for students.

**Challenges Faced:**
- Inability to find a suitable and unique topic initially.
- Evaluating the technical feasibility of different ideas within the time constraints.

**Plan for Next Week:**
- Finalize the project idea and get it approved by the guide.
- Read existing literature and analyze similar event management platforms.
- Prepare the initial project proposal and presentation outline.

**Discussion and Decisions:**
"Event Hub" has been selected as the primary choice for the mini-project. It solves a real problem on campus by streamlining event discovery and management. 

**Upcoming Deadline:**
02/01/2026: Topic Approval Presentation

**Next Weekly Report Due:**
02/01/2026

**Submitted By:**
NITHIN SAMUEL (ADR23CS087)
NADHA MOHAMMED (LADR23CS119)
MOHAMMED SHAFEEK S (ADR23CS072)
MUHAMMED ABEES S (ADR23CS075)

----------------------------------------------

Group No: 7
Event Hub
Weekly Report 2
Date: 02/01/2026

**Accomplishments this Week:**
- "Event Hub" was presented to the review committee and officially approved as our mini-project topic.
- Discussed the core features: Public Homepage for students, Admin Dashboard for organizers, and an automated attendance/registration tracking system.
- Created the initial UI wireframes for the public-facing homepage and the admin login flow.

**Challenges Faced:**
- Defining the exact scope of the project so that it is achievable (decided to stick to a single-admin model for colleges rather than a multi-vendor system).

**Plan for Next Week:**
- Begin frontend development (HTML, CSS, JavaScript).
- Design the overarching layout, integrating a modern, premium UI using CSS variables and flexbox/grid.

**Discussion and Decisions:**
Decided to build the frontend without heavy frontend frameworks (like React) to keep the project lightweight, relying on vanilla HTML/CSS/JS with a Python/Flask backend.

**Upcoming Deadline:**
09/01/2026: Frontend Prototype Submission

**Next Weekly Report Due:**
09/01/2026

**Submitted By:**
NITHIN SAMUEL (ADR23CS087)
NADHA MOHAMMED (LADR23CS119)
MOHAMMED SHAFEEK S (ADR23CS072)
MUHAMMED ABEES S (ADR23CS075)

----------------------------------------------

Group No: 7
Event Hub
Weekly Report 3
Date: 09/01/2026

**Accomplishments this Week:**
- Developed the public frontend homepage. Built the interactive navigation bar, Hero section, About section, and Contact section.
- Designed the "Events Grid" layout where upcoming and ongoing events will be dynamically displayed.
- Standardized the visual aesthetics using a consistent color palette (primary blues, dark text, clean white cards).

**Challenges Faced:**
- Making the layout fully responsive for mobile devices, particularly the Hero section and navigation menu.
- Implementing modern styling (like glassmorphism and smooth transition effects) using pure CSS.

**Plan for Next Week:**
- Start backend development.
- Setup the Flask environment and configure a local MySQL database.
- Create the initial database schemas for storing event details.

**Discussion and Decisions:**
Agreed to use a modular CSS approach (e.g., separating `public_styles.css` from `admin_styles.css`) to prevent styling conflicts between the public site and admin tools.

**Upcoming Deadline:**
23/01/2026: Backend Integration Review

**Next Weekly Report Due:**
23/01/2026

**Submitted By:**
NITHIN SAMUEL (ADR23CS087)
NADHA MOHAMMED (LADR23CS119)
MOHAMMED SHAFEEK S (ADR23CS072)
MUHAMMED ABEES S (ADR23CS075)

----------------------------------------------

Group No: 7
Event Hub
Weekly Report 4
Date: 23/01/2026

**Accomplishments this Week:**
- Set up the Python Flask backend server and configured routing.
- Designed and initialized the MySQL database (created the `events` and `admin_username_pass` tables).
- Developed the Admin Login system with session management to protect dashboard routes.
- Began drafting the layout for the internal Admin Dashboard.

**Challenges Faced:**
- Setting up secure database connections and handling Python virtual environments.
- Managing Flask sessions reliably across browser restarts.

**Plan for Next Week:**
- Complete the Admin Dashboard UI.
- Implement the "Create Event" functionality (handling form inputs, dates, and image uploads) so admins can add events to the database.

**Discussion and Decisions:**
Decided to store uploaded event banner images locally in a `static/uploads` directory rather than using a cloud bucket to simplify deployment for the mini-project evaluation.

**Upcoming Deadline:**
06/02/2026: Dashboard & CRUD Operations

**Next Weekly Report Due:**
06/02/2026

**Submitted By:**
NITHIN SAMUEL (ADR23CS087)
NADHA MOHAMMED (LADR23CS119)
MOHAMMED SHAFEEK S (ADR23CS072)
MUHAMMED ABEES S (ADR23CS075)

----------------------------------------------

Group No: 7
Event Hub
Weekly Report 5
Date: 06/02/2026

**Accomplishments this Week:**
- Successfully implemented full CRUD (Create, Read, Update, Delete) operations for Events in the Admin Dashboard.
- Added file upload functionality in Flask so admins can attach promotional banners to event listings.
- Populated the database with test events and created a REST API endpoint (`/api/events`) to serve this data to the frontend in JSON format.

**Challenges Faced:**
- Handling multipart form data for file uploads via AJAX/Fetch API.
- Re-populating modal forms dynamically when editing an existing event.

**Plan for Next Week:**
- Wire up the public homepage to fetch real data from the new `/api/events` endpoint.
- Implement dynamic filtering (All, Upcoming, Ongoing, Completed) and search functionality on the homepage.

**Discussion and Decisions:**
Implemented strict backend validation to ensure uploaded files are valid image formats before saving them to the server.

**Upcoming Deadline:**
13/02/2026: Public Homepage Data Integration

**Next Weekly Report Due:**
13/02/2026

**Submitted By:**
NITHIN SAMUEL (ADR23CS087)
NADHA MOHAMMED (LADR23CS119)
MOHAMMED SHAFEEK S (ADR23CS072)
MUHAMMED ABEES S (ADR23CS075)

----------------------------------------------

Group No: 7
Event Hub
Weekly Report 6
Date: 13/02/2026

**Accomplishments this Week:**
- Connected the public frontend (`public_script.js`) to the backend API.
- Implemented real-time dynamic filtering (filtering events by their status: Upcoming, Ongoing, Completed) on the homepage.
- Implemented a live Search Bar on the homepage that filters events based on title and description without needing page reloads.
- Created standalone Event Details pages that dynamically load detailed information based on the Event ID in the URL.

**Challenges Faced:**
- Bug: Fixed an issue where frontend filters were mistakenly querying event "category" instead of "status".
- Passing event context correctly to the details page via URL parameters.

**Plan for Next Week:**
- Implement the event registration and attendance management systems.
- Connect Google Forms/Sheets for frictionless student registration.

**Discussion and Decisions:**
To simplify registration for students, we decided to use Google Forms for event sign-ups rather than building a custom registration portal from scratch. The admin will provide the Form link and collect responses seamlessly.

**Upcoming Deadline:**
20/02/2026: Registration & Sync System

**Next Weekly Report Due:**
20/02/2026

**Submitted By:**
NITHIN SAMUEL (ADR23CS087)
NADHA MOHAMMED (LADR23CS119)
MOHAMMED SHAFEEK S (ADR23CS072)
MUHAMMED ABEES S (ADR23CS075)

----------------------------------------------

Group No: 7
Event Hub
Weekly Report 7
Date: 20/02/2026

**Accomplishments this Week:**
- Built a "Dual Link System" allowing admins to input a Google Form link (for public registration) and a Google Sheet Responses link.
- Implemented backend logic using `gspread` and Google Service Account credentials to auto-parse the spreadsheet ID from URLs.
- Developed an auto-sync route that fetches registered student data directly from Google Sheets and imports it into our local MySQL database for attendance management.

**Challenges Faced:**
- Configuring Google Cloud Console IAM permissions and dealing with Google Forms API limitations (switched fully to Google Sheets API as a workaround).
- Writing regex parsing functions to accurately extract the `spreadsheet_id` from various Google Docs URL formats.

**Plan for Next Week:**
- Finish the Attendance Tracking modal UI in the Admin Dashboard.
- Build analytical reports using Chart.js to visualize registration vs. attendance rates.
- Polish the UI and perform final system integration testing.

**Discussion and Decisions:**
The system now functions as a true hybrid: Google Forms handles the heavy lifting of user input, while Event Hub handles presentation, data centralization, and attendance tracking.

**Upcoming Deadline:**
27/02/2026: Analytics and Final Polish

**Next Weekly Report Due:**
27/02/2026

**Submitted By:**
NITHIN SAMUEL (ADR23CS087)
NADHA MOHAMMED (LADR23CS119)
MOHAMMED SHAFEEK S (ADR23CS072)
MUHAMMED ABEES S (ADR23CS075)

----------------------------------------------

Group No: 7
Event Hub
Weekly Report 8
Date: 27/02/2026

**Accomplishments this Week:**
- Finalized the Admin Students dashboard view, enabling organizers to mark and save attendance in bulk.
- Integrated `Chart.js` to render visual bar charts comparing total registrations to actual attendees per event.
- Added an Admin Settings view to allow changing the dashboard username and password securely.
- Conducted extensive UI/UX Polish: Standardized the public Contact section, fixed dynamic tracking statistics, centralized navigation links, and ensured all components render beautifully.

**Challenges Faced:**
- Ensuring the database state remains consistent when admins change event statuses (e.g., migrating "Finished" to "Completed" to sync with frontend nomenclature).
- Managing Chart.js instance destruction to prevent rendering overlaps when navigating between tabs.

**Plan for Next Week:**
- Draft the final project report documentation.
- Prepare the final presentation and execute a complete dry-run demo of the website.

**Discussion and Decisions:**
The Event Hub minimum viable product is feature-complete. The team is confident that the final product meets all established requirements.

**Upcoming Deadline:**
Final Mini-Project Presentation 

**Submitted By:**
NITHIN SAMUEL (ADR23CS087)
NADHA MOHAMMED (LADR23CS119)
MOHAMMED SHAFEEK S (ADR23CS072)
MUHAMMED ABEES S (ADR23CS075)
