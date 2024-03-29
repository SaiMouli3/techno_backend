
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Performs, Employee2
from .views import calculate_employee_efficiency

@receiver(post_save, sender=Performs,providing_args=["instance"])
def update_employee_efficiency(sender, instance, created, **kwargs):
    try:
        print("Hello from signal")
        if created:
            emp_ssn = instance.emp_ssn
            efficiency = calculate_employee_efficiency(emp_ssn)
            if efficiency is not None:
                print("inside efficiency line 15")
                employee = Employee2.objects.filter(emp_ssn=emp_ssn).first()
                if employee:
                    employee.emp_efficiency = efficiency
                    employee.save()
    except:
        print("exception has occured")

