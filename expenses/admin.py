from django.contrib import admin
from .models import Category, Expense, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = [
    'id',
    'category',
    'amount',
    'expense_date',
    'created_at'
]

search_fields = [
    'description',
    'category__name'
]

list_filter = [
    'category',
    'expense_date'
]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = [
    'id',
    'category',
    'monthly_limit'
]

search_fields = [
    'category__name'
]

list_filter = [
    'category'
]
