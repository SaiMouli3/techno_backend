from django.db import models
from django.apps import AppConfig
from datetime import date
from django.db.models.signals import post_save, pre_delete,pre_save,post_delete
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum, Avg
import logging

logger = logging.getLogger(__name__)


# class Incentives(models.Model):
#     category = models.CharField(primary_key=True,max_length=100)
#     incentive = models.IntegerField()

#     def __str__(self):
#         return self.category

class Externals(models.Model):
    parameter = models.CharField(primary_key=True,max_length=100)
    value = models.FloatField()

    def __str__(self):
        return self.parameter



class Employee2(models.Model):
    emp_ssn = models.CharField(primary_key=True, max_length=100)
    emp_name = models.CharField(max_length=100)
    emp_designation = models.CharField(max_length=10)
    emp_shed = models.CharField(max_length=100)
    emp_dept = models.CharField(max_length=100)
    emp_efficiency = models.FloatField(default=0.0)
    emp_category = models.IntegerField()

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
    # tool_code = models.ForeignKey(Tool, on_delete=models.CASCADE, db_column='tool_code', to_field='tool_code')
    tool_code = models.ForeignKey(Tool, on_delete=models.SET_NULL, db_column='tool_code', to_field='tool_code', null=True, blank=True)

    class Meta:
        unique_together = ('part_no','component_name','operation_no','tool_code')
    def __str__(self):
        return (f"Part No: {self.part_no}, "
                f"Component Name: {self.component_name}, "
                f"Depth of Cut: {self.depth_of_cut}, "
                f"No of Holes: {self.no_of_holes}, "
                f"Operation No: {self.operation_no}, "
                f"Tool Code: {self.tool_code}")


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
    machine_id = models.CharField(max_length = 255)
    shift_number = models.IntegerField()
    shift_duration = models.FloatField()
    partial_shift = models.FloatField()
    target = models.IntegerField()
    achieved = models.IntegerField()
    remarks = models.CharField(max_length = 255)
    efficiency = models.FloatField()
    incentive_received = models.FloatField(default=0.0)



    def __str__(self):
        return f"{self.partial_shift}"

    def save(self, *args, **kwargs):

        if not self.pk:  # If this is a new instance
            print("in saving--------------------.............------------")
            remarks = self.remarks.lower()
            self.efficiency = (self.achieved/self.target)*(self.shift_duration/self.partial_shift)*100
            print(f"Achieved : {self.achieved}\n Target : {self.target}\n shift_duration : {self.shift_duration}\n partial shift :{self.partial_shift}")
            print(f"Efficiency value: {self.efficiency}")

            external_instance = Externals.objects.filter(parameter=self.remarks).first()
            efficiency_value= external_instance.value * 100


            if self.efficiency<efficiency_value and remarks not in ['2M1P']:
                print("********************________________________Entering the function that updates efficiency____________***********")
                print(f"Efficiency Value:{efficiency_value}")
                self.efficiency=efficiency_value
            print("Saved!")

        # self.incentive_received = round(self.incentive_received, 2)

        self.incentive_received = round(self.incentive_received, 2)

        super().save(*args, **kwargs)


class Breakdown(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    tool_code = models.ForeignKey(Tool,on_delete=models.CASCADE,related_name='breakdown_tool_code',to_field='tool_code')
    machine_id = models.ForeignKey(NewMachine, on_delete=models.CASCADE, db_column='machine_id', to_field='machine_id')
    length_used = models.FloatField()
    expected_length_remaining = models.FloatField()
    replaced_by = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='breakdown_replaced_by',db_column='replaced_by', to_field='tool_code')
    reason = models.CharField(max_length=100) #remarks
    change_time = models.IntegerField()
    no_of_min_into_shift = models.IntegerField()
    emp_ssn=models.ForeignKey(Employee2,on_delete=models.CASCADE,to_field='emp_ssn')
    achieved = models.IntegerField()
    shift_number = models.IntegerField()


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



class Auth(models.Model):
    role = models.CharField(max_length=40)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class SignAuth(models.Model):

    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username



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


j = 0  # Global variable to track function execution


def tool_table_updation(sender, instance, created, **kwargs):
    global j  # Declare j as global to modify it inside the function
    if j == 1:
        print("Function has already been called once, skipping execution.")
        j=0
        return

    print("=================Function is called!========================")
    try:
        machine_id = instance.machine_id
        achieved = instance.achieved

        machine_instances = Machine.objects.filter(machine_id=machine_id)
        print(machine_instances)
        for machine_instance in machine_instances:
            tool_code = machine_instance.tool_code
            print("tool_code is ....")
            print(tool_code)
            part_no = machine_instance.part_no
            print("part_no is ....")
            print(part_no)
            # job_tuple = Job.objects.get(tool_code=tool_code, part_no=part_no)

            # depth_of_cut = job_tuple.depth_of_cut
            # no_of_holes = job_tuple.no_of_holes
            # additional_length = achieved * depth_of_cut * no_of_holes
            # print("Additional Length")
            # print(additional_length)
            tool_tuple = Tool.objects.get(tool_code=tool_code)
            print(".......................jaggg................................................................................")
            print(tool_tuple)
            tool_tuple.length_cut_so_far = tool_tuple.length_cut_so_far + achieved
            print(f"Length Cut So far :{tool_tuple.length_cut_so_far}")
            print(f"Achieved Value :{achieved}")

            new_efficiency = calculate_tool_efficiency(tool_code, tool_tuple.length_cut_so_far)
            tool_tuple.tool_efficiency = new_efficiency
            tool_tuple.save()

        j = 1  # Set the global variable to 1 after the function executes

    except Exception as e:
        print(f"An error occurred: {e}")

# Connect the signal to the Performs model
post_save.connect(tool_table_updation, sender=Performs)

# Function to reset the global variable j, if needed
# def reset_tool_table_updation():
#     global j
#     j = 0
#     print("Reset the function call tracker variable j to 0.")

# def tool_table_updation(sender, instance, created, **kwargs):
#     print("=================Function is called!========================")
#     try:
#         machine_id = instance.machine_id
#         achieved = instance.achieved

#         machine_instances = Machine.objects.filter(machine_id=machine_id)
#         print(machine_instances)
#         for machine_instance in machine_instances:
#             tool_code = machine_instance.tool_code
#             print("tool_code is ....")
#             print(tool_code)
#             part_no = machine_instance.part_no
#             print("part_no is ....")
#             print(part_no)
#             # job_tuple = Job.objects.get(tool_code=tool_code, part_no=part_no)

#             # depth_of_cut = job_tuple.depth_of_cut
#             # no_of_holes = job_tuple.no_of_holes
#             # additional_length = achieved * depth_of_cut * no_of_holes
#             # print("Additional Length")
#             # print(additional_length)
#             tool_tuple = Tool.objects.get(tool_code=tool_code)
#             print(".......................jaggg................................................................................")
#             print(tool_tuple)
#             tool_tuple.length_cut_so_far =  tool_tuple.length_cut_so_far + (achieved)
#             print(f"Length Cut So far :{tool_tuple.length_cut_so_far}")
#             print(f"Achieved Value :{achieved}")


#             new_efficiency = calculate_tool_efficiency(tool_code, tool_tuple.length_cut_so_far)
#             tool_tuple.tool_efficiency = new_efficiency
#             tool_tuple.save()


#     except Exception as e:
#         print(f"An error occurred: {e}")

# post_save.connect(tool_table_updation, sender=Performs)


def update_tool_length_cut(sender, instance, **kwargs):

    machine = instance.machine_id
    part_no_tool_code = Machine.objects.filter(machine_id=machine).values_list('part_no', 'tool_code')

    print(part_no_tool_code)
    for part_no, tool_code in part_no_tool_code:
        job = Job.objects.get(part_no=part_no, tool_code=tool_code)
        tool = Tool.objects.get(tool_code=tool_code)
        tool.length_cut_so_far -= (job.depth_of_cut * job.no_of_holes * instance.achieved)
        print(f"Tool length cut so far : {tool.length_cut_so_far}")
        new_efficiency=calculate_tool_efficiency(tool_code,tool.length_cut_so_far)
        tool.tool_efficiency=new_efficiency

        tool.save()

post_delete.connect(update_tool_length_cut,sender=Performs)


def calculate_tool_efficiency(tool_code,length_cut_so_far):

    tool_tuple=get_object_or_404(Tool,tool_code=tool_code)


    new_efficiency = (length_cut_so_far / tool_tuple.max_life_expectancy_in_mm)*100

    return new_efficiency


def calculate_tool_efficiency_after_updating_breakdown(sender,instance,created,**kwargs):
    print("In calculate tool efficiency after breakdown")
    tool_code=instance.tool_code
    tool_tuple=get_object_or_404(Tool,tool_code=tool_code)
    length_cut_so_far=tool_tuple.length_cut_so_far


    achieved = instance.achieved

    machine_id=instance.machine_id
    machine_instance = Machine.objects.filter(machine_id=machine_id).first()

    part_no = machine_instance.part_no

    job_instance = Job.objects.filter(part_no=part_no).first()

    depth_of_cut = job_instance.depth_of_cut
    no_of_holes = job_instance.no_of_holes

    length_cut_so_far += achieved * depth_of_cut * no_of_holes
    print("Length cut so far")
    print(length_cut_so_far)

    tool_tuple.length_cut_so_far = length_cut_so_far
    tool = Tool.objects.get(tool_code=tool_code)
    efficiency = (length_cut_so_far / tool.max_life_expectancy_in_mm) * 100
    part_no_count = Job.objects.filter(tool_code=tool).count()


    tool_chart = ToolChart.objects.create(
        tool_code=tool_code,
        no_of_brk_points=tool.no_of_brk_points+1,
        tool_efficiency=efficiency,
        part_no_count=part_no_count
    )



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



# def update_tool_length_cut(sender, instance, **kwargs):
#     machine = instance.machine_id
#     part_no_tool_code = Machine.objects.filter(machine_id=machine).values_list('part_no', 'tool_code')

#     for part_no, tool_code in part_no_tool_code:
#         job = Job.objects.get(part_no=part_no, tool_code=tool_code)
#         tool = Tool.objects.get(tool_code=tool_code)
#         tool.length_cut_so_far -= (job.depth_of_cut * job.no_of_holes * instance.achieved)
#         new_efficiency=calculate_tool_efficiency(tool_code,tool.length_cut_so_far)
#         tool.tool_efficiency=new_efficiency

#         tool.save()

# post_delete.connect(update_tool_length_cut,sender=Performs)


def calculate_shift_efficiency(sender, instance, created, **kwargs):
    try:

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




from django.dispatch import receiver
#------------------------------------------------------------------------------------
# @receiver(post_save, sender=Tool)
def check_job_table_after_tool_save(sender, instance, created, **kwargs):
    if created:
        try:
            tool_name = instance.tool_name  # Assuming 'tool_name' is the field name for tool name
            print(f"Tool name: {tool_name}")
            tool_codes = Tool.objects.filter(tool_name=tool_name).values_list('tool_code', flat=True)
            print(f"Tool codes: {list(tool_codes)}")

            job_exists = False
            for code in tool_codes:
                if Job.objects.filter(tool_code=code).exists():
                    print(f"Job exists for tool code: {code}")
                    job_exists = True
                    break

            if job_exists:
                new_tool_code = instance.tool_code  # Assuming 'tool_code' is the field name for the new tool code
                new_tool_instance = Tool.objects.get(tool_code=new_tool_code)
                print(f"New tool code: {new_tool_code}")
                for code in tool_codes:
                    job_queryset = Job.objects.filter(tool_code=code).all()
                    print(f"Jobs for tool code {code}: {job_queryset}")
                    for job in job_queryset:
                        print(f"Creating job for: {job}")

                        Job.objects.create(
                            part_no=job.part_no,
                            component_name=job.component_name,
                            depth_of_cut=job.depth_of_cut,
                            no_of_holes=job.no_of_holes,
                            operation_no=job.operation_no,
                            tool_code=new_tool_instance  # Update with the new tool code
                        )
                        print("Created new job")

        except Exception as e:
            print(f"Error in check_job_table_after_tool_save: {e}")
            raise

# Connect the signal
post_save.connect(check_job_table_after_tool_save, sender=Tool)
# def check_job_table_after_tool_save(sender,instance,created,**kwargs):
#     tool_name = instance.tool_name  # Assuming 'tool_name' is the field name for tool name
#     print("_________________________PRINTING TOOL NAME IN TOOL CREATE VIEW------------------------------------")
#     print(tool_name)
#     tool_codes = Tool.objects.filter(tool_name=tool_name).values_list('tool_code',flat=True)
#     print(list(tool_codes))

#     job_exists = False
#     for code in tool_codes:
#         if Job.objects.filter(tool_code=code).exists():
#             print("After JOBS FILTER 12334456777888----")
#             job_exists = True
#             break

#     if job_exists:
#         new_tool_code = instance.tool_code  # Assuming 'tool_code' is the field name for the new tool code
#         print(f"New tool code :{new_tool_code}")
#         for code in tool_codes:
#             job_queryset = Job.objects.filter(tool_code=code).all()
#             print(job_queryset)
#             for job in job_queryset:
#                 print(job)
#                 print(job.part_no)
#                 print(job.component_name)
#                 print(job.depth_of_cut)
#                 print(job.no_of_holes)
#                 print(job.operation_no)
#                 print(new_tool_code)


#                 Job.objects.create(
#                     part_no=job.part_no,
#                     component_name=job.component_name,
#                     depth_of_cut=job.depth_of_cut,
#                     no_of_holes=job.no_of_holes,
#                     operation_no=job.operation_no,
#                     tool_code=new_tool_code  # Update with the new tool code
#                 )
#                 print("Created new job")




# post_save.connect(check_job_table_after_tool_save,sender=Tool)

def employee_table_updation(sender, instance, created, **kwargs):

    emp_ssn = instance.emp_ssn
    print("employee updation")
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





# def partial_shift_update(sender, instance, **kwargs):
#     global updating_from_make_daily_entry

#     if not updating_from_make_daily_entry:
#         breakdown_entry = Breakdown.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date).first()
#         if breakdown_entry:
#             change_time = breakdown_entry.change_time / 60.0
#             no_of_min_into_shift = breakdown_entry.no_of_min_into_shift / 60.0

#             instance.partial_shift -= change_time + no_of_min_into_shift


# pre_save.connect(partial_shift_update,sender=Performs)

# updating_from_make_daily_entry = False


# def partial_shift_update(sender, instance, **kwargs):
#     global updating_from_make_daily_entry

#     if not updating_from_make_daily_entry:
#         breakdown_entry = Breakdown.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date).first()
#         if breakdown_entry:
#             change_time = breakdown_entry.change_time / 60.0

#             print("----------------STARTING----------------------")

#             print(f"change_time : {change_time}")
#             print(no_of_min_into_shift)
#             instance.partial_shift -= change_time + no_of_min_into_shift

#             partial_shift = instance.partial_shift
#             print(partial_shift)

#             machine_id=breakdown_entry.machine_id

#             print(machine_id)
#             machine_instance = Machine.objects.filter(machine_id=machine_id).first()
#             m_target=machine_instance.target
#             print(m_target)

#             achieved=instance.achieved
#             print(achieved)
#             daily_efficiency = (achieved/((m_target/8)*partial_shift))*100

#             print(daily_efficiency)

#             instance.efficiency=daily_efficiency

#             prev_daily_entry = Performs.objects.filter(emp_ssn=instance.emp_ssn,date=instance.date,machine_id=instance.machine_id,shift_number=instance.shift_number).first()
#             BD_Eff=prev_daily_entry.efficiency
#             print(BD_Eff)
#             BD_PartialShift = prev_daily_entry.partial_shift
#             print(BD_PartialShift)
#             BD_incentive = prev_daily_entry.incentive_received
#             print(BD_incentive)

#             Actual_ShiftEff = (((BD_Eff * BD_PartialShift) + (daily_efficiency * partial_shift))/(partial_shift + BD_PartialShift))



#             print(Actual_ShiftEff)


#             external_instance = Externals.objects.filter(parameter="base_cost").first()
#             baseRate = external_instance.value
#             print(baseRate)

#             daily_incentive = Actual_ShiftEff * baseRate/100 - BD_incentive
#             print(daily_incentive)
#             instance.incentive_received = daily_incentive

#             print("------------------------ENDING------------------")


# pre_save.connect(partial_shift_update,sender=Performs)









# updating_from_make_daily_entry = False
# i=0
# def partial_shift_update(sender, instance, **kwargs):

#     global i
#     if i == 1:
#         i=0
#         return



#     if not updating_from_make_daily_entry:

#         breakdown_entry = Breakdown.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date,machine_id=instance.machine_id)

#         if breakdown_entry:
#             BD_ChangeTime = breakdown_entry.change_time/60

#             print("----------------STARTING----------------------")


#             BD_MinsIntoShift = breakdown_entry.no_of_min_into_shift/60

#             instance.partial_shift -= (BD_ChangeTime + BD_MinsIntoShift)

#             # partial_shift = instance.partial_shift
#             # daily_partial_shift = partial_shift - (change_time/60) - (no_of_min_into_shift/60)



#             machine_id = breakdown_entry.machine_id

#             machine_instance = Machine.objects.filter(machine_id=machine_id).first()
#             m_target = machine_instance.target


#             daily_achieved = instance.achieved
#             BD_AchievedSoFar = breakdown_entry.achieved



#             # daily_efficiency = (daily_achieved / ((m_target / 8) * instance.partial_shift)) * 100

#             # if(instance.efficiency>daily_efficiency):
#             #     daily_efficiency=instance.efficiency
#             # else:
#             #     instance.efficiency=daily_efficiency

#             daily_efficiency = (daily_achieved / ((m_target / 8) * instance.partial_shift)) * 100
#             instance.efficiency=daily_efficiency



#             prev_daily_entry = Performs.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date, machine_id=instance.machine_id, shift_number=instance.shift_number).first()




#             BD_PartialShift = prev_daily_entry.partial_shift
#             BD_Eff = (BD_AchievedSoFar / ((m_target/8)*BD_PartialShift))*100

#             BD_Incentive = prev_daily_entry.incentive_received


#             Actual_ShiftEff = (((BD_Eff * BD_PartialShift) + (daily_efficiency * instance.partial_shift)) / (instance.partial_shift + BD_PartialShift))


#             external_instance = Externals.objects.filter(parameter="base_cost").first()
#             baseRate = external_instance.value


#             daily_incentive = Actual_ShiftEff * baseRate / 100 - BD_Incentive
#             print(f"daily_incentive: {daily_incentive}")
#             instance.incentive_received = daily_incentive
#             i+=1
#             print(f"machine_target: {m_target}")
#             print(f"BD_MinsIntoShift: {BD_MinsIntoShift}")
#             print(f"BD_AchievedSoFar: {BD_AchievedSoFar}")
#             print(f"BD_ChangeTime: {BD_ChangeTime}")
#             print(f"baseRate: {baseRate}")
#             print(f"BD_PartialShift: {BD_PartialShift}")
#             print(f"BD_Eff: {BD_Eff}")
#             print(f"BD_Incentive: {BD_Incentive}")
#             print(f"daily_partialShift: {instance.partial_shift}")
#             print(f"daily_eff: {daily_efficiency}")
#             print(f"Actual_ShiftEff: {Actual_ShiftEff}")
#             print(f"daily_incentive : {daily_incentive}")


#             instance.save()


#             print("------------------------ENDING------------------")

# post_save.connect(partial_shift_update, sender=Performs)

updating_from_make_daily_entry = False
i = 0

def partial_shift_update(sender, instance, **kwargs):
    global i
    if i == 1:
        i = 0
        return

    if not updating_from_make_daily_entry:
        try:
            breakdown_entry = Breakdown.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date, machine_id=instance.machine_id).first()
            if breakdown_entry:
                BD_ChangeTime = breakdown_entry.change_time / 60.0
                BD_MinsIntoShift = breakdown_entry.no_of_min_into_shift / 60.0

                instance.partial_shift -= (BD_ChangeTime + BD_MinsIntoShift)

                machine_instance = Machine.objects.filter(machine_id=instance.machine_id).first()
                if not machine_instance:
                    raise ValueError("Machine instance not found")

                m_target = machine_instance.target

                daily_achieved = instance.achieved
                BD_AchievedSoFar = breakdown_entry.achieved

                if m_target == 0 or instance.partial_shift == 0:
                    raise ValueError("Division by zero detected")

                daily_efficiency = (daily_achieved / ((m_target / 8.0) * instance.partial_shift)) * 100.0
                instance.efficiency = daily_efficiency

                prev_daily_entry = Performs.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date, machine_id=instance.machine_id, shift_number=instance.shift_number).first()
                if prev_daily_entry:
                    BD_PartialShift = prev_daily_entry.partial_shift
                    BD_Eff = (BD_AchievedSoFar / ((m_target / 8.0) * BD_PartialShift)) * 100.0
                    BD_Incentive = prev_daily_entry.incentive_received

                    Actual_ShiftEff = (((BD_Eff * BD_PartialShift) + (daily_efficiency * instance.partial_shift)) / (instance.partial_shift + BD_PartialShift))

                    external_instance = Externals.objects.filter(parameter="base_cost").first()
                    if not external_instance:
                        raise ValueError("External instance for base_cost not found")

                    baseRate = external_instance.value
                    daily_incentive = Actual_ShiftEff * baseRate / 100.0 - BD_Incentive

                    instance.incentive_received = daily_incentive

                    i += 1
                    print(f"machine_target: {m_target}")
                    print(f"BD_MinsIntoShift: {BD_MinsIntoShift}")
                    print(f"BD_AchievedSoFar: {BD_AchievedSoFar}")
                    print(f"BD_ChangeTime: {BD_ChangeTime}")
                    print(f"baseRate: {baseRate}")
                    print(f"BD_PartialShift: {BD_PartialShift}")
                    print(f"BD_Eff: {BD_Eff}")
                    print(f"BD_Incentive: {BD_Incentive}")
                    print(f"daily_partialShift: {instance.partial_shift}")
                    print(f"daily_eff: {daily_efficiency}")
                    print(f"Actual_ShiftEff: {Actual_ShiftEff}")
                    print(f"daily_incentive : {daily_incentive}")

                    instance.save()
                else:
                    print("Previous daily entry not found")

                print("------------------------ENDING------------------")

        except Exception as e:
            print(f"An error occurred in partial_shift_update: {e}")

post_save.connect(partial_shift_update, sender=Performs)



# def pre_save_of_performs(sender,instance,**kwargs):

#      # If this is a new instance
#     print("in saving--------------------.............------------")
#     remarks = instance.remarks.lower()
#     instance.efficiency = (instance.achieved/instance.target)*(instance.shift_duration/instance.partial_shift)*100
#     # print(f"Achieved : {self.achieved}\n Target : {self.target}\n shift_duration : {self.shift_duration}\n partial shift :{self.partial_shift}")
#     # print(f"Efficiency value: {self.efficiency}")

#     external_instance = Externals.objects.filter(parameter=instance.remarks).first()
#     efficiency_value= external_instance.value * 100


#     if instance.efficiency<efficiency_value and remarks not in ['2M1P']:
#         print("********************________________________Entering the function that updates efficiency____________***********")
#         print(f"Efficiency Value:{efficiency_value}")
#         instance.efficiency=efficiency_value
#     print("Saved!")



#     instance.incentive_received = round(instance.incentive_received, 2)


# pre_save.connect(pre_save_of_performs,sender=Performs)











# updating_from_make_daily_entry = False
# i=0
# def partial_shift_update(sender, instance, **kwargs):

#     global i
#     if i == 1:
#         i=0
#         return



#     if not updating_from_make_daily_entry:

#         breakdown_entries = Breakdown.objects.filter(emp_ssn=instance.emp_ssn, date=instance.date,machine_id=instance.machine_id)


#         if(breakdown_entries):
#             x=0
#             partial_shift=instance.partial_shift
#             print(f"partial Shift 1 : {partial_shift}")
#             for entry in breakdown_entries:
#                 partial_shift = partial_shift - (entry.no_of_min_into_shift/60+entry.change_time/60-x)
#                 print(f"partial_shifts : {partial_shift}")
#                 x=entry.no_of_min_into_shift/60+entry.change_time/60
#             p_ps=instance.partial_shift
#             instance.partial_shift=partial_shift

#             remarks = instance.remarks.lower()
#             instance.efficiency = (instance.achieved/instance.target)*(instance.shift_duration/instance.partial_shift)*100


#             external_instance = Externals.objects.filter(parameter=instance.remarks).first()
#             efficiency_value= external_instance.value * 100


#             if instance.efficiency<efficiency_value and remarks not in ['2M1P']:

#                 instance.efficiency=efficiency_value



#             daily_entries = Performs.objects.filter(emp_ssn=instance.emp_ssn,date=instance.date,machine_id=instance.machine_id)

#             numerator = 0
#             denominator = 0
#             for d_entry in daily_entries:
#                 numerator += (d_entry.partial_shift*d_entry.efficiency)
#                 print(f"numerator : {numerator}")
#                 denominator+=d_entry.partial_shift
#                 print(f"denominator: {denominator}")

#             numerator+=partial_shift*instance.efficiency
#             denominator = denominator - p_ps + instance.partial_shift

#             external_instance = Externals.objects.filter(parameter="base_cost").first()
#             baseRate = external_instance.value

#             instance.incentive_received = (numerator/denominator)*(baseRate/100)
#             print(instance.incentive_received)
#             print(f"Numerator : {numerator}")
#             print(f"Denomintor : {denominator}")
#             print(f"Base Rate :{baseRate}")






#         # else:
#         #     remarks = instance.remarks.lower()
#         #     instance.efficiency = (instance.achieved/instance.target)*(instance.shift_duration/instance.partial_shift)*100


#         #     external_instance = Externals.objects.filter(parameter=instance.remarks).first()
#         #     efficiency_value= external_instance.value * 100


#         #     if instance.efficiency<efficiency_value and remarks not in ['2M1P']:

#         #         instance.efficiency=efficiency_value




#         #     instance.incentive_received = round(instance.incentive_received, 2)

#         i+=1

#         instance.save()



# post_save.connect(partial_shift_update, sender=Performs)















updating_from_make_daily_entry = False

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
    baseRate_instance=Externals.objects.filter(parameter="base_cost").first()
    baseRate=baseRate_instance.value
    print(f"base rate {baseRate}")

    # Calculate achieved

    achieved=instance.achieved
    print("...........................make daily entry after breakdown.............................")
    print(f"Achieved : {achieved}")
    print(f"Target {target}")
    print(f"Partial shift :{partial_shift}")

    incentive_received = (achieved/((target/8)*partial_shift))*100
    final_incentive= incentive_received * baseRate/100
    print(f"Incentive: {final_incentive}")

    print(".........................................Over...............................................")

    # Create Performs entry
    Performs.objects.create(
        date=breakdown.date,
        emp_ssn=breakdown.emp_ssn,
        machine_id=machine_id,
        shift_number=instance.shift_number,
        shift_duration=8,
        partial_shift=partial_shift,
        target=target,
        achieved=achieved,
        incentive_received= final_incentive,
        remarks="No Remarks"

    )

    # Reset the flag after updating Performs table
    updating_from_make_daily_entry = False


post_save.connect(make_daily_entry_after_breakdown,sender=Breakdown)




# updating_from_make_daily_entry = False



# def make_daily_entry_after_breakdown(sender, instance, **kwargs):
#     global updating_from_make_daily_entry

#     # Set the flag to True before making any changes to Performs table
#     updating_from_make_daily_entry = True



#     breakdown = instance
#     machine_id = breakdown.machine_id



#     # Calculate partial_shift in hours


#     breakdown_entries = Breakdown.objects.filter(date=instance.date,emp_ssn=instance.emp_ssn)

#     total_prev_change_times = 0
#     total_prev_partial_shifts = 0
#     if(breakdown_entries):
#         for entry in breakdown_entries:
#             total_prev_change_times += entry.change_time/60
#             print(f"total_prev_change_times : {total_prev_change_times}")
#             total_prev_partial_shifts += entry.no_of_min_into_shift/60
#             print(f"total_prev_partial_shifts : {total_prev_partial_shifts}")


#     # breakdown_entry = Breakdown.objects.filter(date=instance.date,emp_ssn=instance.emp_ssn).first()
#     breakdown_entry = Breakdown.objects.filter(date=instance.date, emp_ssn=instance.emp_ssn).order_by('-id').first()


#     total_prev_change_times-=breakdown_entry.change_time/60
#     total_prev_partial_shifts-=breakdown_entry.no_of_min_into_shift/60




#     partial_shift = instance.no_of_min_into_shift/60

#     print(f"partial shift : {partial_shift}")
#     print(f"total_prev_change_times : {total_prev_change_times}")
#     print(f"total_prev_partial_shifts : {total_prev_partial_shifts}")


#     partial_shift = partial_shift - (total_prev_change_times+total_prev_partial_shifts)

#     # Retrieve the first machine matching the criteria
#     machine = Machine.objects.filter(machine_id=machine_id).first()


#     # Retrieve target from the first machine
#     target = machine.target


#     # Calculate achieved

#     achieved=instance.achieved


#     print(".........................................Over...............................................")

#     # Create Performs entry
#     Performs.objects.create(
#         date=breakdown.date,
#         emp_ssn=breakdown.emp_ssn,
#         machine_id=machine_id,
#         shift_number=instance.shift_number,
#         shift_duration=8,
#         partial_shift=partial_shift,
#         target=target,
#         achieved=achieved,
#         incentive_received= 0,
#         remarks="No Remarks"

#     )

#     # Reset the flag after updating Performs table
#     updating_from_make_daily_entry = False


# post_save.connect(make_daily_entry_after_breakdown,sender=Breakdown)




# def make_daily_entry_after_breakdown(sender, instance, **kwargs):


#     breakdown_entries = Breakdown.objects.filter(date=instance.date,emp_ssn=instance.emp_ssn)

#     total_prev_change_times = 0
#     total_prev_partial_shifts = 0
#     if(breakdown_entries):
#         for entry in breakdown_entries:
#             total_prev_change_times += entry.change_time
#             total_prev_partial_shifts += entry.no_of_min_into_shift

#     partial_shift = instance.no_of_min_into_shift/60

#     partial_shift = partial_shift - (total_prev_change_times+total_prev_partial_shifts)

#     machine = Machine.objects.filter(machine_id=instance.machine_id).first()

#     target = machine.target

#     print("-----------------------PERFORMS ENTRY CREATED AFTER BREAKDOWN-------------------")

#     Performs.objects.create(
#         date=instance.date,
#         emp_ssn=instance.emp_ssn,
#         machine_id=instance.machine_id,
#         shift_number=instance.shift_number,
#         shift_duration=8,
#         partial_shift=partial_shift,
#         target=target,
#         achieved=instance.achieved,
#         incentive_received= 0,
#         remarks="No Remarks"

#     )



# post_save.connect(make_daily_entry_after_breakdown,sender=Breakdown)













from django.db.models.signals import post_save
from django.dispatch import receiver



# def update_incentive_received(sender, instance, created, **kwargs):

#     if created:
#         if instance.remarks not in ['2M1P']:
#             emp_instance = Employee2.objects.get(emp_ssn=instance.emp_ssn)
#             emp_category = "category " + str(emp_instance.emp_category)
#             print("printing emp_category")
#             print(emp_category)
#             print("Hello !!")
#             incentive_instance = Externals.objects.get(parameter=emp_category)
#             incentive_value = incentive_instance.value
#             print(incentive_value)

#             base_instance = Externals.objects.get(parameter='base_cost')
#             base_value = base_instance.value

#             final_incentive = (instance.efficiency / 100) * base_value

#             instance.incentive_received = final_incentive
#             instance.save(update_fields=['incentive_received'])

# post_save.connect(update_incentive_received,sender=Performs)

def update_incentive_received(sender, instance, created, **kwargs):
    if created:
        # Check if there is a corresponding breakdown entry
        breakdown_exists = Breakdown.objects.filter(emp_ssn=instance.emp_ssn, machine_id=instance.machine_id, date=instance.date).exists()

        if not breakdown_exists and instance.remarks not in ['2M1P']:
            emp_instance = Employee2.objects.get(emp_ssn=instance.emp_ssn)
            emp_category = "category " + str(emp_instance.emp_category)
            print("printing emp_category")
            print(emp_category)
            print("Hello !!")
            incentive_instance = Externals.objects.get(parameter=emp_category)
            incentive_value = incentive_instance.value
            print(incentive_value)

            base_instance = Externals.objects.get(parameter='base_cost')
            base_value = base_instance.value
            print(base_value)

            final_incentive = (instance.efficiency / 100) * base_value

            instance.incentive_received = final_incentive
            instance.save(update_fields=['incentive_received'])

post_save.connect(update_incentive_received, sender=Performs)



def twoMachineOnePerson(sender, instance, created, **kwargs):
    if created and instance.remarks == '2M1P':
        emp_ssn = instance.emp_ssn
        date = instance.date
        machine_id = instance.machine_id

        performs_instances = Performs.objects.filter(emp_ssn=emp_ssn, date=date)

        sum_eff = performs_instances.aggregate(Sum('efficiency'))['efficiency__sum'] or 0
        count = performs_instances.count()

        avg_efficiency = sum_eff / count

        individual_efficiency = avg_efficiency / 2

        performs_instances.update(efficiency=individual_efficiency)

        emp_instance = Employee2.objects.get(emp_ssn=instance.emp_ssn)
        emp_category = "category " + str(emp_instance.emp_category)
        incentive_instance = Externals.objects.get(parameter=emp_category)
        incentive_value = incentive_instance.value

        base_instance = Externals.objects.get(parameter='base_cost')
        base_value = base_instance.value

        tm1p_factor_instance = Externals.objects.get(parameter='2M1P')
        tm1p_value = tm1p_factor_instance.value

        final_incentive = (avg_efficiency / 100) * base_value * tm1p_value
        final_incentive= final_incentive/2
        # Save the instance
        instance.incentive_received = final_incentive
        instance.save(update_fields=['incentive_received'])

post_save.connect(twoMachineOnePerson,sender=Performs)




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
















