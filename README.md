\# Smart Expense Tracker



A web-based expense management application developed using Python, Django, and MySQL. The application helps users record daily expenses, manage categories, set monthly budgets, analyze spending, and export expense reports.



\## Features



\* User Registration, Login, and Logout

\* Protected pages using Django authentication

\* Category Management



&#x20; \* Add Category

&#x20; \* View Categories

&#x20; \* Update Category

&#x20; \* Delete Category

\* Expense Management



&#x20; \* Add Expense

&#x20; \* View Expenses

&#x20; \* Update Expense

&#x20; \* Delete Expense

\* Search expenses by description

\* Filter expenses by category

\* Filter expenses by date

\* Sort expenses by amount

\* Monthly Budget Management

\* Budget Report

\* Dashboard Summary

\* Recent Expenses

\* Bar Chart and Pie Chart

\* Export Expense Report as PDF

\* Export Expense Report as Excel

\* Success and Error Messages



\## Technologies Used



\* Python

\* Django

\* MySQL

\* HTML

\* CSS

\* Bootstrap

\* JavaScript

\* Chart.js

\* ReportLab

\* OpenPyXL



\## Project Modules



1\. User Authentication

2\. Category Management

3\. Expense Management

4\. Budget Management

5\. Budget Report

6\. Dashboard and Analytics

7\. PDF and Excel Export



\## Database Models



\### Category



Stores expense category information.



Fields:



\* `id`

\* `name`



\### Expense



Stores daily expense information.



Fields:



\* `id`

\* `category`

\* `amount`

\* `description`

\* `expense\_date`

\* `created\_at`



\### Budget



Stores the monthly budget for each category.



Fields:



\* `id`

\* `category`

\* `monthly\_limit`



\## Installation and Setup



1\. Clone the repository:



bash

git clone <repository-url>





2\. Open the project folder:



bash

cd ExpenseTracker





3\. Create and activate a virtual environment.



4\. Install the required packages:



bash

pip install -r requirements.txt





5\. Configure the MySQL database in `ExpenseTracker/settings.py`.



6\. Run migrations:



bash

python manage.py makemigrations

python manage.py migrate





7\. Start the development server:



bash

python manage.py runserver





8\. Open the application in a browser:



text

http://127.0.0.1:8000/





\## Future Enhancements



\* User-specific expenses, categories, and budgets

\* Password reset functionality

\* Budget limit notifications

\* Monthly and yearly reports

\* Expense receipt image upload

\* Advanced analytics

\* Django REST Framework API

\* Mobile application

\* Machine learning-based expense prediction



\## Developer



\*\*Gubbala Saimani\*\*



B.Tech – Computer Science and Engineering



\## Project Status



Completed and tested.



