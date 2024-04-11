from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Employee2, Tool, NewJob, Job, NewMachine, Machine, Performs, Breakdown, Reviving1,ToolChart, Shift,ShiftEfficiency
from .resources import Employee2Resource, ToolResource, JobResource


@admin.register(Employee2)
class Employee2Admin(ImportExportModelAdmin):
    resource_class = Employee2Resource


@admin.register(Tool)
class ToolAdmin(ImportExportModelAdmin):
    resource_class = ToolResource

@admin.register(Job)
class JobAdmin(ImportExportModelAdmin):
    resource_class = JobResource



# Register the rest of your models here as before
admin.site.register(NewJob)
admin.site.register(NewMachine)
admin.site.register(Machine)
admin.site.register(Performs)
admin.site.register(Breakdown)

admin.site.register(Shift)
admin.site.register(ToolChart)
admin.site.register(ShiftEfficiency)
admin.site.register(Reviving1)
