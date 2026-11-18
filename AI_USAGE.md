# AI Usage Documentation

## Tools Used
- GitHub Copilot - used it mostly for debugging setup errors, speeding up the repetitive HTML/Flask code, and generating test data.

## Key Prompts
1. "what is a clean folder structure for a flask app with mysql and jinja templates"
2. "how do i run schema.sql in powershell when mysql isnt recognized"
3. "getting mysql.connector.errors.ProgrammingError 1045 access denied using password NO in python"
4. "how to parse a mysql json column in python and match it against a comma separated string"
5. "make a sample_data.sql script with a few test rows for each table"

## What Worked Well
- Setup and debugging was the biggest time saver. I kept hitting PowerShell errors trying to run `schema.sql` because `mysql` wasn't in my PATH, and Copilot pointed out I could just call `mysql.exe` directly by its full path. It also caught why Python was throwing the `using password: NO` error (my `.env` file wasn't in the root folder yet).
- After I got the `companies` page working end to end, I used Copilot to help crank out the HTML forms and Flask routes for `jobs`, `applications`, and `contacts` since they follow the same pattern.
- It helped me figure out the JSON side of things, like turning the comma-separated skills string from the form into a JSON array for MySQL and then pulling it back out to calculate the match percentage on the Job Match page.

## What I Modified
- Simplified a lot of the CSS and Python variable names it suggested so the code stayed easy to read and debug.
- Set up `database.py` to pull my MySQL login from a `.env` file using `python-dotenv` and added `.env` to `.gitignore` so my password wouldn't end up on GitHub.
- Double-checked `ON DELETE CASCADE` in `schema.sql` so deleting a company or job wouldn't throw foreign key errors in the app.
- Tested every form in the browser and checked the rows in MySQL Workbench. Had to tweak how blank optional fields (like salary, website, and interview notes) were handled so they save as `NULL` instead of causing errors.

## Lessons Learned
- Building one full CRUD table first and making sure it actually works before touching the rest saves a lot of headaches.
- Pasting the exact terminal error message gets you a real fix way faster than trying to describe the problem.
- Even when generated code looks right, you still have to test it locally. Little things like an unsaved file or a missing `.env` will still break everything.