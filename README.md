# Study Group Matcher (IVC)

## What it does
LaserLinks is a study group matcher for IVC students. You pick your classes and how you like to study, and it matches you with classmates who fit, so you don't have to find a study group on your own.

## MVP scope
### In
- IVC email verification
- Pick your classes
- Set study preferences (style, availability, in-person/online)
- Get matched into a group (3–5 people)
- Group gets a shared contact link (Discord/GroupMe)

### Out (for now)
- In-app chat
- Notifications
- Ratings/reviews
- Other colleges

## Stack
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Frontend: React (Vite) + Tailwind + shadcn/ui
- Dev: Docker Compose

## Data model
- users: id, email (@ivc.edu, unique), name, verified (bool), study_style, meeting_pref (in-person/online/either), availability (weekday mornings/afternoons/evenings, weekends), created_at
- courses: id, subject (e.g. MATH), number (e.g. 3A), title, term (e.g. Fall 2026) 
- user_courses: user_id, course_id (a user can be in many courses)
- groups: id, course_id, contact_link, status (forming/active/closed), created_at
- group_members: group_id, user_id, joined_at
- contact_link: accepts GroupMe and Discord links

## Matching rules
- Must be in the same course
- Must share at least one availability block
- Prefer same study style and meeting preference
- Groups of 3–5; if fewer than 3 matches, stay in "forming" until more sign up

## Launch plan
- Soft launch: finals study groups, mid-November
- Real launch: start of spring semester