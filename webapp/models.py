from django.db import models
from django.apps import AppConfig
from datetime import date
from django.db.models.signals import post_save, pre_delete,pre_save
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum, Avg





class Employee2(models.Model):
    emp_ssn = models.CharField(primary_key=True, max_length=100)
    emp_name = models.CharField(max_length=100)
    emp_designation = models.CharField(max_length=10)
    emp_shed = models.CharField(max_length=100)
    emp_dept = models.CharField(max_length=100)
    emp_efficiency = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.emp_ssn}"


class Tool(models.Model):
    tool_code = models.CharField(primary_key=True, max_length=100)
    tool_name = models.CharField(max_length=100)
    max_life_expectancy_in_mm = models.FloatField()
    cost = models.FloatField()
    length_cut_so_far = models.FloatField()
    no_of_brk_points = models.IntegerField(default=None, null=True)
    tool_efficiency = models.FloatField(default=None, null=True)

    def __str__(self):
        return f"{self.tool_code}"


class NewJob(models.Model):
    part_no=models.CharField(primary_key=True,max_length=100)
    def __str__(self):
        return f"{self.part_no}"


class Job(models.Model):
    part_no = models.ForeignKey(NewJob,on_delete=models.CASCADE,db_column='part_no',to_field='part_no')
    component_name = models.CharField(max_length=100)
    depth_of_cut = models.FloatField()
    no_of_holes = models.IntegerField()
    operation_no = models.IntegerField()
    tool_code = models.ForeignKey(Tool, on_delete=models.CASCADE, db_column='tool_code', to_field='tool_code')

    class Meta:
        unique_together = ('part_no','tool_code')
    def __str__(self):
        return f"Part No: {self.part_no}, Tool Code: {self.tool_code}"


class NewMachine(models.Model):
    machine_id=models.CharField(primary_key=True,max_length=100)
    def __str__(self):
        return f"{self.machine_id}"


class Machine(models.Model):
    machine_id = models.ForeignKey(NewMachine,on_delete=models.CASCADE,db_column='machine_id')
    machine_name = models.CharField(max_length=100)
    part_no = models.ForeignKey(NewJob, on_delete=models.CASCADE, db_column='part_no')
    tool_code = models.ForeignKey(Tool, on_delete=models.CASCADE, db_column='tool_code')
    target=models.IntegerField()

    class Meta:
        unique_together = ('machine_id', 'tool_code')

    def __str__(self):
        return f"{self.machine_id}"


class Shift(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    date = models.DateField()
    shift_number = models.IntegerField()
    shift_efficiency = models.FloatField()

    def __str__(self):
        return f"{self.shift_number}"

class ShiftEfficiency(models.Model):
    shift_number=models.IntegerField(primary_key=True)
    shift_efficiency=models.FloatField()

    def __str__(self):
        return f"{self.shift_number}"

class Performs(models.Model):
    date = models.DateField()
    emp_ssn = models.ForeignKey(Employee2, on_delete=models.CASCADE, db_column='emp_ssn', to_field='emp_ssn')
    # machine_id = models.ForeignKey(NewMachine, on_delete=models.CASCADE, db_column='machine_id', to_field='machine_id')
    machine_id = models.CharField(max_length=100)
    shift_number = models.IntegerField()
    shift_duration = models.FloatField()
    partial_shift = models.FloatField()
    target = models.IntegerField()
    achieved = models.IntegerField()


    def __str__(self):
        return f"{self.date}"


class Breakdown(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    tool_code = models.ForeignKey(Tool,on_delete=models.CASCADE,related_name='breakdown_tool_code',to_field='tool_code')
    machine_id = models.ForeignKey(NewMachine, on_delete=models.CASCADE, db_column='machine_id', to_field='machine_id')
    length_used = models.FloatField()
    expected_length_remaining = models.FloatField()
    replaced_by = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='breakdown_replaced_by',db_column='replaced_by', to_field='tool_code')
    reason = models.CharField(max_length=100)
    change_time = models.IntegerField()
    no_of_min_into_shift = models.IntegerField()
    emp_ssn=models.ForeignKey(Employee2,on_delete=models.CASCADE,to_field='emp_ssn')

    def __str__(self):
        return f"{self.tool_code}"




class Reviving1(models.Model):
    tool_code=models.OneToOneField(Tool,on_delete=models.CASCADE,primary_key=True)
    date=models.DateField()
    def __str__(self):
        return f"{self.tool_code}"


class ToolChart(models.Model):
    tool_code = models.CharField(max_length=50)
    no_of_brk_points = models.IntegerField()
    tool_efficiency = models.FloatField()
    part_no_count = models.IntegerField()

    def __str__(self):
        return self.tool_code


# class ShiftEfficiency(models.Model):
#     id = models.BigAutoField(primary_key=True, auto_created=True,default=None)
#     date = models.DateField()
#     shift_number = models.IntegerField()
#     shift_efficiency = models.FloatField()
#
#     def __str__(self):
#         return f"{self.shift_number}"



#----------------------Post updation of performs table--------------

    #Tool table updation
# def tool_table_updation(sender,instance,created,**kwargs):

#     machine_id = instance.machine_id

#     machine_instance=get_object_or_404(Machine,machine_id=machine_id)
#     tool_code = machine_instance.tool_code
#     print("In tool table updation!")
#     part_no = machine_instance.part_no


#     job_tuple=get_object_or_404(Job,tool_code=tool_code,part_no=part_no)

#     depth_of_cut = job_tuple.depth_of_cut

#     no_of_holes=job_tuple.no_of_holes

#     additional_length=depth_of_cut*no_of_holes


#     tool_tuple=get_object_or_404(Tool,tool_code=tool_code)
#     tool_tuple.length_cut_so_far+=additional_length

#     tool_tuple.save()


#     new_efficiency=calculate_tool_efficiency(tool_code,tool_tuple.length_cut_so_far)
#     tool_tuple.tool_efficiency=new_efficiency
#     tool_tuple.save()

# post_save.connect(tool_table_updation,sender=Performs)

def tool_table_updation(sender, instance, created, **kwargs):
    try:
        machine_id = instance.machine_id
        achieved = instance.achieved

        machine_instances = Machine.objects.filter(machine_id=machine_id)
        for machine_instance in machine_instances:
            tool_code = machine_instance.tool_code
            print(tool_code)
            part_no = machine_instance.part_no

            job_tuple = Job.objects.get(tool_code=tool_code, part_no=part_no)

            depth_of_cut = job_tuple.depth_of_cut
            no_of_holes = job_tuple.no_of_holes
            additional_length = achieved * depth_of_cut * no_of_holes

            tool_tuple = Tool.objects.get(tool_code=tool_code)
            tool_tuple.length_cut_so_far += additional_length
            tool_tuple.save()

            new_efficiency = calculate_tool_efficiency(tool_code, tool_tuple.length_cut_so_far)
            tool_tuple.tool_efficiency = new_efficiency
            tool_tuple.save()

    except Exception as e:
        print(f"An error occurred: {e}")

post_save.connect(tool_table_updation, sender=Performs)



def calculate_tool_efficiency(tool_code,length_cut_so_far):

    tool_tuple=get_object_or_404(Tool,tool_code=tool_code)


    new_efficiency = (length_cut_so_far / tool_tuple.max_life_expectancy_in_mm)*100

    return new_efficiency


def calculate_tool_efficiency_after_updating_breakdown(sender,instance,created,**kwargs):
    print("In calculate tool efficiency after breakdown")
    tool_code=instance.tool_code
    tool_tuple=get_object_or_404(Tool,tool_code=tool_code)
    length_cut_so_far=tool_tuple.length_cut_so_far
    max_life_expectancy=tool_tuple.max_life_expectancy_in_mm
    new_efficiency = (length_cut_so_far / max_life_expectancy)*100
    tool_tuple.tool_efficiency=new_efficiency
    tool_tuple.save()


post_save.connect(calculate_tool_efficiency_after_updating_breakdown,sender=Breakdown)

    #Shift Table updation-----------------------

# def calculate_shift_efficiency(sender,instance,created,**kwargs):
#     shift_number=instance.shift_number
#     print(shift_number)
#     performs_aggregated = Performs.objects.filter(shift_number=shift_number).aggregate(
#         shift_duration_sum=Sum('shift_duration'),
#         partial_shift_sum=Sum('partial_shift'),
#         target_sum=Sum('target'),
#         achieved_sum=Sum('achieved')
#     )

#     shift_duration_sum = performs_aggregated['shift_duration_sum']
#     partial_shift_sum = performs_aggregated['partial_shift_sum']
#     target_sum = performs_aggregated['target_sum']
#     achieved_sum = performs_aggregated['achieved_sum']


#     x = target_sum * (partial_shift_sum / shift_duration_sum)

#     efficiency = (achieved_sum / x)*100

#     efficiency=round(efficiency,2)



#     shift_tuple=get_object_or_404(ShiftEfficiency,shift_number=shift_number)
#     print(shift_tuple)

#     shift_tuple.shift_efficiency=efficiency

#     shift_tuple.save()

#     new_shift = Shift.objects.create(
#     date=date.today(),
#     shift_number=shift_number,
#     shift_efficiency=efficiency
#     )

#     new_shift.save()



# post_save.connect(calculate_shift_efficiency,sender=Performs)



def calculate_shift_efficiency(sender, instance, created, **kwargs):
    try:
        print("in calculate efficiency of shift")
        shift_number = instance.shift_number
        print(shift_number)

        performs_aggregated = Performs.objects.filter(shift_number=shift_number).aggregate(
            shift_duration_sum=Sum('shift_duration'),
            partial_shift_sum=Sum('partial_shift'),
            target_sum=Sum('target'),
            achieved_sum=Sum('achieved')
        )

        shift_duration_sum = performs_aggregated['shift_duration_sum']
        partial_shift_sum = performs_aggregated['partial_shift_sum']
        target_sum = performs_aggregated['target_sum']
        achieved_sum = performs_aggregated['achieved_sum']

        x = target_sum * (partial_shift_sum / shift_duration_sum)

        efficiency = (achieved_sum / x) * 100
        efficiency = round(efficiency, 2)


        shift_tuple = get_object_or_404(ShiftEfficiency, shift_number=shift_number)
        print(efficiency)

        shift_tuple.shift_efficiency = efficiency
        shift_tuple.save()

        new_shift = Shift.objects.create(
            date=date.today(),
            shift_number=shift_number,
            shift_efficiency=efficiency
        )

        new_shift.save()

    except Exception as e:
        print(f"An error occurred: {e}")


post_save.connect(calculate_shift_efficiency,sender=Performs)





#------------------------------------------------------------------------------------



def employee_table_updation(sender, instance, created, **kwargs):

    emp_ssn = instance.emp_ssn

    performs = Performs.objects.filter(emp_ssn=emp_ssn)

    total_efficiency_sum = 0

    # Calculate efficiency for each entry and sum them up
    for entry in performs:
        x = entry.target * (entry.partial_shift / entry.shift_duration)
        efficiency = (entry.achieved / x) * 100
        total_efficiency_sum += efficiency

    # Calculate average efficiency

    total_entries = performs.count()
    avg_efficiency = total_efficiency_sum / total_entries if total_entries > 0 else 0

    # Update the employee's average efficiency
    employee = Employee2.objects.get(emp_ssn=emp_ssn)
    employee.emp_efficiency = avg_efficiency
    employee.save()


post_save.connect(employee_table_updation,sender=Performs)


updating_from_make_daily_entry = False


def partial_shift_update(sender, instance, **kwargs):
    global updating_from_make_daily_entry

    if not updating_from_make_daily_entry:
        breakdown_entry = Breakdown.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date).first()
        if breakdown_entry:
            change_time = breakdown_entry.change_time / 60.0
            no_of_min_into_shift = breakdown_entry.no_of_min_into_shift / 60.0

            instance.partial_shift -= change_time + no_of_min_into_shift


pre_save.connect(partial_shift_update,sender=Performs)


def make_daily_entry_after_breakdown(sender, instance, **kwargs):
    global updating_from_make_daily_entry

    # Set the flag to True before making any changes to Performs table
    updating_from_make_daily_entry = True

    breakdown = instance
    machine_id = breakdown.machine_id

    no_of_min_into_shift = breakdown.no_of_min_into_shift

    # Calculate partial_shift in hours
    partial_shift = no_of_min_into_shift / 60.0

    # Retrieve the first machine matching the criteria
    machine = Machine.objects.filter(machine_id=machine_id).first()
    if not machine:
        # Handle the case where the machine or tool does not exist
        return

    # Retrieve target from the first machine
    target = machine.target

    # Calculate achieved
    achieved = (target / 8) * partial_shift  # Assuming shift duration is always 8 hours

    # Create Performs entry
    Performs.objects.create(
        date=breakdown.date,
        emp_ssn=breakdown.emp_ssn,
        machine_id=machine_id,
        shift_number=1,
        shift_duration=8,
        partial_shift=partial_shift,
        target=target,
        achieved=achieved
    )

    # Reset the flag after updating Performs table
    updating_from_make_daily_entry = False


post_save.connect(make_daily_entry_after_breakdown,sender=Breakdown)




# def partial_shift_update(sender,instance,**kwargs):

#     breakdown_entry = Breakdown.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date).first()
#     change_time=(breakdown_entry.change_time)/60.0
#     no_of_min_into_shift=(breakdown_entry.no_of_min_into_shift)/60.0


#     if breakdown_entry:

#         instance.partial_shift = instance.partial_shift-change_time-no_of_min_into_shift


# pre_save.connect(partial_shift_update,sender=Performs)





# def make_daily_entry_after_breakdown(sender,instance,**kwargs):

#     breakdown = instance
#     machine_id = breakdown.machine_id

#     no_of_min_into_shift = breakdown.no_of_min_into_shift

#     # Calculate partial_shift in hours
#     partial_shift = no_of_min_into_shift / 60.0

#     # Retrieve the first machine matching the criteria
#     machine = Machine.objects.filter(machine_id=machine_id).first()
#     if not machine:
#         # Handle the case where the machine or tool does not exist
#         return

#     # Retrieve target from the first machine
#     target = machine.target

#     # Calculate achieved
#     achieved = (target / 8) * partial_shift  # Assuming shift duration is always 8 hours

#     # Create Performs entry
#     Performs.objects.create(
#         date=breakdown.date,
#         emp_ssn=breakdown.emp_ssn,
#         machine_id=machine_id,
#         shift_number=1,
#         shift_duration=8,
#         partial_shift=partial_shift,
#         target=target,
#         achieved=achieved
#     )

# pre_save.connect(make_daily_entry_after_breakdown,sender=Breakdown)




# def set_tool_efficiency_to_zero(sender,instance,created,**kwargs):


# post_save.connect(set_tool_efficiency_to_zero,sender=Breakdown)
















