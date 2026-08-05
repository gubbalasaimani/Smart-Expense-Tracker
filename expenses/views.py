from django.shortcuts import render,redirect
from .models import Category, Expense, Budget
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from django.contrib import messages
from datetime import date
@login_required
def dashboard(request):
    expense_summary = Expense.objects.values('category__name').annotate(total=Sum('amount'))

    chart_labels = []
    chart_data = []

    for item in expense_summary:
        chart_labels.append(item['category__name'])
        chart_data.append(float(item['total']))
        
    recent_expenses = Expense.objects.all().order_by('-expense_date')
    total_amount = Expense.objects.aggregate(
    Sum('amount'))['amount__sum']

    if total_amount is None:
        total_amount = 0

    # This month's expense
    current_month = date.today().month
    current_year = date.today().year

    monthly_expense = Expense.objects.filter(
        expense_date__month=current_month,
        expense_date__year=current_year
    ).aggregate(
        Sum('amount')
    )['amount__sum']

    if monthly_expense is None:
        monthly_expense = 0


    top_category = Expense.objects.values('category__name').annotate(total_spent=Sum('amount')).order_by(
    '-total_spent'
    ).first()
    total_budget_amount = Budget.objects.aggregate(
    Sum('monthly_limit')
    )['monthly_limit__sum']

    if total_budget_amount is None:
        total_budget_amount = 0


    if total_budget_amount == 0:
        budget_status = "No Budget Set"

    elif total_amount > total_budget_amount:
        budget_status = "Over Budget"
    else:
        budget_status = "Within Budget"


    context = {
        'total_categories': Category.objects.count(),
        'total_expenses': Expense.objects.count(),
        'total_budgets': Budget.objects.count(),
        'recent_expenses': recent_expenses,
        'total_amount': total_amount,
        'monthly_expense': monthly_expense,

        'total_budget_amount': total_budget_amount,
        'budget_status': budget_status,
        
        'top_category': top_category,

        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }

    return render(request, 'expenses/dashboard.html', context)


@login_required
def add_expense(request):

    categories = Category.objects.all()

    if request.method == 'POST':

        category_id = request.POST['category']

        amount = float(request.POST['amount'])

        if amount <= 0:

            messages.error(
                request,
                "Expense amount must be greater than zero!"
            )

            return redirect("add_expense")

        description = request.POST['description']
        expense_date = request.POST['expense_date']

        category = Category.objects.get(id=category_id)

        Expense.objects.create(
            category=category,
            amount=amount,
            description=description,
            expense_date=expense_date
        )

        messages.success(request, "Expense added successfully!")

        return redirect('dashboard')

    context = {
        'categories': categories
    }

    return render(request, 'expenses/add_expense.html', context)

@login_required
def view_expenses(request):

    expenses = Expense.objects.all().order_by('-expense_date')
    categories = Category.objects.all()

    # Get search values
    search = request.GET.get('search')
    category = request.GET.get('category')
    date = request.GET.get('date')
    sort = request.GET.get('sort')

    # Search by description
    if search:
        expenses = expenses.filter(description__icontains=search)

    # Filter by category
    if category:
        expenses = expenses.filter(category_id=category)

    # Filter by date
    if date:
        expenses = expenses.filter(expense_date=date)

    # Sort by amount
    if sort == "low":
        expenses = expenses.order_by('amount')

    elif sort == "high":
        expenses = expenses.order_by('-amount')

    context = {
        'expenses': expenses,
        'categories': categories,
    }

    return render(request, 'expenses/view_expenses.html', context)
@login_required
def update_expense(request, id):

    expense = Expense.objects.get(id=id)

    categories = Category.objects.all()

    if request.method == 'POST':

        expense.category = Category.objects.get(
            id=request.POST['category']
        )

        expense.amount = request.POST['amount']

        expense.description = request.POST['description']

        expense.expense_date = request.POST['expense_date']

        expense.save()

        messages.success(
        request,
        "Expense updated successfully!"
        )

        return redirect('view_expenses')


    context = {
        'expense': expense,
        'categories': categories
    }

    return render(
        request,
        'expenses/update_expense.html',
        context
    )
@login_required
def delete_expense(request, id):


    expense = Expense.objects.get(id=id)

    expense.delete()

    messages.success(
        request,
        "Expense deleted successfully!"
    )

    return redirect('view_expenses')




def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check duplicate username
        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists!"
            )

            return redirect("register")

        # Check duplicate email
        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already exists!"
            )

            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Registration successful! Please login."
        )

        return redirect('login')

    return render(request, 'expenses/register.html')

def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            return render(
                request,
                'expenses/login.html',
                {'error': 'Invalid Username or Password'}
            )

    return render(request, 'expenses/login.html')


def logout_user(request):

    logout(request)

    return redirect('login')

@login_required
def add_budget(request):

    categories = Category.objects.all()

    if request.method == 'POST':

        category_id = request.POST['category']
        monthly_limit = request.POST['monthly_limit']

        category = Category.objects.get(id=category_id)

        # Check duplicate budget
        if Budget.objects.filter(category=category).exists():

            messages.error(
                request,
                "Budget already exists for this category!"
            )

            return redirect("add_budget")

        Budget.objects.create(
            category=category,
            monthly_limit=monthly_limit
        )

        messages.success(
            request,
            "Budget added successfully!"
        )

        return redirect('dashboard')

    context = {
        'categories': categories
    }

    return render(request, 'expenses/add_budget.html', context)

@login_required
def view_budgets(request):

    budgets = Budget.objects.all()

    context = {
        'budgets': budgets
    }

    return render(request, 'expenses/view_budgets.html', context)

@login_required
def edit_budget(request, id):

    budget = Budget.objects.get(id=id)
    categories = Category.objects.all()

    if request.method == 'POST':

        category_id = request.POST['category']
        monthly_limit = request.POST['monthly_limit']

        category = Category.objects.get(id=category_id)

        budget.category = category
        budget.monthly_limit = monthly_limit

        budget.save()

        messages.success(
        request,
        "Budget updated successfully!"
        )

        return redirect('view_budgets')


    context = {
        'budget': budget,
        'categories': categories
    }

    return render(request, 'expenses/edit_budget.html', context)
@login_required
def delete_budget(request, id):
    budget = Budget.objects.get(id=id)
    budget.delete()
    messages.success(
        request,
        "Budget deleted successfully!"
    )

    return redirect('view_budgets')




@login_required
def budget_report(request):

    budgets = Budget.objects.all()

    report = []

    for budget in budgets:

        total_spent = Expense.objects.filter(
            category=budget.category
        ).aggregate(
            Sum('amount')
        )['amount__sum']

        if total_spent is None:
            total_spent = 0

        remaining = budget.monthly_limit - total_spent

        report.append({
            'category': budget.category.name,
            'budget': budget.monthly_limit,
            'spent': total_spent,
            'remaining': remaining,
        })

    context = {
        'report': report
    }

    return render(request, 'expenses/budget_report.html', context)

@login_required
def view_categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(
        request,'expenses/view_categories.html',context)

@login_required
def add_category(request):

    if request.method == "POST":

        name = request.POST["name"]

        if Category.objects.filter(name=name).exists():

            messages.error(request, "Category already exists!")

            return redirect("add_category")

        Category.objects.create(name=name)

        messages.success(request, "Category added successfully!")

        return redirect("view_categories")

    return render(request, "expenses/add_category.html")

@login_required
def edit_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        category.name = request.POST["name"]

        category.save()

        messages.success(
            request,
            "Category updated successfully!"
        )

        return redirect("view_categories")



    
    context = { "category": category }
    return render(request, "expenses/edit_category.html", context)

@login_required
def delete_category(request, id):

    category = Category.objects.get(id=id)

    # Check whether this category has expenses
    if Expense.objects.filter(category=category).exists():

        messages.error(
            request,
            "Cannot delete category because it has expenses."
        )

        return redirect("view_categories")

    category.delete()

    messages.success(
        request,
        "Category deleted successfully!"
    )

    return redirect("view_categories")


@login_required
def export_pdf(request):

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Expense_Report.pdf"'

    # Create PDF
    p = canvas.Canvas(response)

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Expense Report")

    # Table Heading
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 760, "Category")
    p.drawString(180, 760, "Amount")
    p.drawString(280, 760, "Description")
    p.drawString(450, 760, "Date")

    # Line under heading
    p.line(50, 755, 550, 755)

    # Fetch expenses
    expenses = Expense.objects.all()

    # Starting Y position
    y = 730

    p.setFont("Helvetica", 11)

    for expense in expenses:

        p.drawString(50, y, expense.category.name)

        p.drawString(180, y, str(expense.amount))

        p.drawString(280, y, expense.description[:20])

        p.drawString(450, y, str(expense.expense_date))

        y -= 25

        # Create a new page if the current one is full
        if y < 50:
            p.showPage()
            y = 800

    p.save()

    return response


@login_required
def export_excel(request):

    # Create Excel workbook
    workbook = Workbook()

    # Select active sheet
    sheet = workbook.active

    sheet.title = "Expenses"

    # Heading Row
    sheet.append([
        "Category",
        "Amount",
        "Description",
        "Date"
    ])

    # Get all expenses
    expenses = Expense.objects.all()

    # Add rows
    for expense in expenses:

        sheet.append([
            expense.category.name,
            expense.amount,
            expense.description,
            str(expense.expense_date)
        ])

    # Create response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="Expense_Report.xlsx"'

    workbook.save(response)

    return response