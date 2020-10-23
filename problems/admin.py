from django.contrib import admin

from .models import Rule, Calculation, Problem, MathSession, FlashCard, Category

# Register your models here.


class RuleAdmin(admin.ModelAdmin):
    list_display = [
        "left",
        "left_exact",
        "right",
        "right_exact",
        "allowed_ops",
        "created",
    ]


admin.site.register(Rule, RuleAdmin)

admin.site.register(MathSession)


class ProblemAdmin(admin.ModelAdmin):
    list_display = ["user", "calculation", "value", "correct", "answered"]
    ordering = ["created"]


admin.site.register(Problem, ProblemAdmin)


def recalculate(modeladmin, request, queryset):
    for c in queryset:
        c.calculate()


recalculate.short_description = "Recalculate the answers"


class CalculationAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created"]
    ordering = ["created"]
    actions = [recalculate]


admin.site.register(Calculation, CalculationAdmin)

admin.site.register(Category)


class FlashCardAdmin(admin.ModelAdmin):
    list_display = ["__str__", "category"]


admin.site.register(FlashCard, FlashCardAdmin)
