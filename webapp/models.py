from django.db import models
from django.apps import AppConfig
from datetime import date
from django.db.models.signals import post_save
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
        unique_together = ('part_no', 'tool_code')

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
    date = models.DateField(default=date.today)
    emp_ssn = models.ForeignKey(Employee2, on_delete=models.CASCADE, db_column='emp_ssn', to_field='emp_ssn')
    machine_id = models.ForeignKey(NewMachine, on_delete=models.CASCADE, db_column='machine_id', to_field='machine_id')
    shift_number = models.IntegerField()
    shift_duration = models.FloatField()
    partial_shift = models.IntegerField()
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
    change_time = models.DurationField()
    no_of_min_into_shift = models.IntegerField()

    def __str__(self):
        return f"Breakdown on {self.date} for Tool: {self.tool_code.tool_code} on Machine: {self.machine_id.machine_name}"


class Reviving(models.Model):
    tool_code=models.OneToOneField(Tool,on_delete=models.CASCADE,primary_key=True)

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
def tool_table_updation(sender,instance,created,**kwargs):
    
    machine_id = instance.machine_id

    machine_instance=get_object_or_404(Machine,machine_id=machine_id)
    tool_code = machine_instance.tool_code

    part_no = machine_instance.part_no
    
    
    job_tuple=get_object_or_404(Job,tool_code=tool_code,part_no=part_no)

    depth_of_cut = job_tuple.depth_of_cut
    
    no_of_holes=job_tuple.no_of_holes
    
    additional_length=depth_of_cut*no_of_holes
    

    tool_tuple=get_object_or_404(Tool,tool_code=tool_code)
    tool_tuple.length_cut_so_far+=additional_length
    
    tool_tuple.save()
    

    new_efficiency=calculate_tool_efficiency(tool_code)
    tool_tuple.tool_efficiency=new_efficiency
    tool_tuple.save()
    
post_save.connect(tool_table_updation,sender=Performs)

def calculate_tool_efficiency(tool_code):
    
    tool_tuple=get_object_or_404(Tool,tool_code=tool_code)
    breakpoint_factor=0.1
    
    new_efficiency = tool_tuple.tool_efficiency / (1 + (tool_tuple.no_of_brk_points * breakpoint_factor))
   
    return new_efficiency




    #Shift Table updation-----------------------

def calculate_shift_efficiency(sender,instance,created,**kwargs):
    shift_number=instance.shift_number
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
    
    efficiency = (achieved_sum / x)*100
    
    efficiency=round(efficiency,2)
    
    
    
    shift_tuple=get_object_or_404(ShiftEfficiency,shift_number=shift_number) #error here
    print(shift_tuple)
    
    shift_tuple.shift_efficiency=efficiency
    
    shift_tuple.save()

    
post_save.connect(calculate_shift_efficiency,sender=Performs)




#------------------------------------------------------------------------------------

