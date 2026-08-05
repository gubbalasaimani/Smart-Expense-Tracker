\# Smart Expense Tracker



A web-based expense management application developed using Python, Django, and MySQL. The application helps users record daily expenses, manage categories, set monthly budgets, analyze spending, and export expense reports.



\## Features



\* User Registration, Login, and Logout

\* Protected pages using Django authentication

\* Category Management

\* Add, View, Update, and Delete Categories

\* Add, View, Update, and Delete Expenses

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



\* id

\* name



\### Expense



Stores daily expense information.



Fields:



\* id

\* category

\* amount

\* description

\* expense\_date

\* created\_at



\### Budget



Stores the monthly budget for each category.



Fields:



\* id

\* category

\* monthly\_limit



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/gubbalasaimani/Smart-Expense-Tracker.git

```



\### 2. Open the project folder



```bash

cd Smart-Expense-Tracker

```



\### 3. Create a virtual environment



```bash

python -m venv venv

```



\### 4. Activate the virtual environment



For Windows CMD:



```bash

venv\\Scripts\\activate

```



\### 5. Install the required packages



```bash

pip install -r requirements.txt

```



\### 6. Configure the MySQL database



Open:



```text

ExpenseTracker/settings.py

```



Configure your MySQL database details.



\### 7. Run migrations



```bash

python manage.py makemigrations

python manage.py migrate

```



\### 8. Start the development server



```bash

python manage.py runserver

```



\### 9. Open the application



Open this address in your browser:



```text

http://127.0.0.1:8000/

```



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



Gubbala Saimani



B.Tech – Computer Science and Engineering



\## Project Status



Completed and tested.



