from datetime import datetime
import json
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.db.models import F, Sum, Avg
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from .models import Employee2, Job, Tool, Breakdown, Machine, Performs,NewMachine, ToolChart, ToolChart, Shift, NewJob,Reviving1, Auth
from .serializers import EmployeeSerializer, JobSerializer, ToolSerializer, JobSerializer1, BreakdownSerializer, \
    MachineSerializer, PerformsSerializers, NMSerializer, ChartS, Rev
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from collections import defaultdict
from rest_framework.renderers import JSONRenderer  # Import JSONRenderer
from django.core.exceptions import MultipleObjectsReturned
from rest_framework.views import APIView
import logging

from rest_framework.decorators import api_view
from .models import SignAuth
from django.http import JsonResponse



previous_values_list = []


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeList(generics.ListAPIView):
    queryset = Employee2.objects.all()
    serializer_class = EmployeeSerializer

@method_decorator(csrf_exempt, name='dispatch')
class PerformsList(generics.ListAPIView):
    queryset = Performs.objects.all()
    serializer_class = PerformsSerializers


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeCreateView(CreateAPIView):
    queryset = Employee2.objects.all()
    serializer_class = EmployeeSerializer

# @method_decorator(csrf_exempt, name='dispatch')
# class JobsList(generics.ListAPIView):
#     serializer_class = JobSerializer

#     def get_queryset(self):
#         # Retrieve all jobs from the database
#         all_jobs = Job.objects.all()

#         # Create a dictionary to store unique jobs based on component_name, part_no, and operation_no
#         unique_jobs = {}
#         for job in all_jobs:
#             key = (job.component_name, job.part_no, job.operation_no)
#             # Add the job to the dictionary if it's not already present
#             if key not in unique_jobs:
#                 unique_jobs[key] = job

#         # Return the unique jobs
#         return unique_jobs.values()

# @method_decorator(csrf_exempt, name='dispatch')
# class JobsList(generics.ListAPIView):

#     def get_queryset(self):
#         return Job.objects.all()  # Return queryset for fetching Job objects

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()  # Call get_queryset method to get queryset
#         job_details_list = []

#         # Iterate through queryset and construct job details
#         for job in queryset:
#             job_details_list.append({
#                 'part_no': job.part_no.part_no,
#                 'component_name': job.component_name,
#                 'operation_no': job.operation_no,
#             })

#         # Return JSON response with job details
#         return JsonResponse(job_details_list, safe=False)



@method_decorator(csrf_exempt, name='dispatch')
class JobsList(generics.ListAPIView):

    def get_queryset(self):
        return Job.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        unique_job_details = set()
        job_details_list = []

        for job in queryset:
            job_detail = (job.part_no.part_no, job.component_name, job.operation_no)
            # Check if the job detail is not already in the set
            if job_detail not in unique_job_details:
                job_details = {
                    "part_no": job.part_no.part_no,
                    "component_name": job.component_name,
                    "operation_no": job.operation_no
                }
                unique_job_details.add(job_detail)
                job_details_list.append(job_details)

        return Response(job_details_list)



# @method_decorator(csrf_exempt, name='dispatch')
# class JobsList(generics.ListAPIView):

#     def get_queryset(self):
#         return Job.objects.all()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         unique_jobs = set()

#         # Collecting unique job details
#         for job in queryset:
#             key = (job.part_no.part_no, job.component_name, job.operation_no)
#             unique_jobs.add(key)

#         # Converting set of unique job details to a list of dictionaries
#         for job in unique_jobs:
#             job_details_list = [
#                 {
#                     "part_no": job[0],
#                     "component_name": job[1],
#                     "operation_no": job[2]
#                 }

#             ]

#         # Returning JSON response
#         return Response(job_details_list)


@method_decorator(csrf_exempt, name='dispatch')
class NMachineList(generics.ListAPIView):
    queryset = NewMachine.objects.all()
    serializer_class = NMSerializer

@method_decorator(csrf_exempt, name='dispatch')
class NMachineView(CreateAPIView):
    queryset = NewMachine.objects.all()
    serializer_class = NMSerializer

# @method_decorator(csrf_exempt, name='dispatch')
# class JobCreateView(CreateAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer

#     def post(self, request, *args, **kwargs):
#         part_no = request.data.get('part_no')
#         NewJob.objects.create(part_no = part_no)
#         NewJob.save()
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(csrf_exempt, name='dispatch')
# class JobCreateView(CreateAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer

#     def post(self, request, *args, **kwargs):
#         part_no = request.data.get('part_no')
#         new_job = NewJob.objects.filter(part_no=part_no).first()
#         if not new_job:
#             new_job = NewJob.objects.create(part_no=part_no)
#         if new_job:
#             serializer = self.get_serializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 new_job.delete()
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Failed to create NewJob"}, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_exempt, name='dispatch')
# class JobCreateView(CreateAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer

#     def post(self, request, *args, **kwargs):
#         part_no = request.data.get('part_no')
#         new_job = NewJob.objects.filter(part_no=part_no).first()  # Check if NewJob with given part_no exists

#         if not new_job:  # If NewJob doesn't exist, create it
#             new_job = NewJob.objects.create(part_no=part_no)

#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():  # Check if serializer is valid
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             new_job.delete()  # Delete the NewJob object if serializer is not valid
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class JobCreateView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def post(self, request, *args, **kwargs):

        part_no = request.data.get('part_no')
        component_name = request.data.get('component_name')
        operation_no = request.data.get('operation_no')
        tool_name = request.data.get('tool_name')

        new_job = NewJob.objects.filter(part_no=part_no).first()  # Check if NewJob with given part_no exists

        if not new_job:  # If NewJob doesn't exist, create it
            new_job = NewJob.objects.create(part_no=part_no)

        tools = Tool.objects.filter(tool_name=tool_name)
        if not tools:
            return Response({"error": f"No tools found with name '{tool_name}'"}, status=status.HTTP_404_NOT_FOUND)

        created_jobs = []

        for tool in tools:
            tool_code = tool.tool_code

            data = {
                "part_no": part_no,
                "component_name": component_name,
                "operation_no": operation_no,
                "tool_code": tool_code,
                "depth_of_cut": request.data.get('depth_of_cut'),  # Assuming depth_of_cut is provided in the request
                "no_of_holes": request.data.get('no_of_holes')  # Assuming no_of_holes is provided in the request
            }

            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                created_jobs.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_jobs, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class ToolList(generics.ListAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

# @method_decorator(csrf_exempt, name='dispatch')
# class CreateMachineList(CreateAPIView):
#     queryset = Machine.objects.all()
#     serializer_class = MachineSerializer

#     def perform_create(self, serializer):
#         machine_id = self.request.data.get('machine_id')
#         existing_machines = Machine.objects.filter(machine_id=machine_id)
#         if existing_machines:
#             existing_machines.delete()
#         serializer.save()

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class CreateMachineList(APIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def perform_create(self, serializer):
        machine_id = self.request.data.get('machine_id')
        tool_code = self.request.data.get('tool_code')
        existing_machines = Machine.objects.filter(machine_id=machine_id, tool_code=tool_code)


        for existing_machine in existing_machines:
            existing_machine.delete()

        serializer.save()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, many=isinstance(data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)



# @method_decorator(csrf_exempt, name='dispatch')
# class CreateMachineList(APIView):
#     queryset = Machine.objects.all()
#     serializer_class = MachineSerializer

#     def add_machine_data(self, data):
#         numOfTools = data.get('numOfTools')
#         serializer = self.serializer_class(data=data, many=isinstance(data, list))
#         serializer.is_valid(raise_exception=True)

#         i = 0
#         machine_id = data.get('machine_id')
#         tool_code = data.get('tool_code')

#         if i == 0:
#             existing_machines = Machine.objects.filter(machine_id=machine_id)
#             if not existing_machines :
#                 pass
#             for existing_machine in existing_machines:
#                 existing_machine.delete()
#             i += 1
#         if i < numOfTools:
#             serializer.save()
#             i += 1

#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         return self.add_machine_data(data)


# @method_decorator(csrf_exempt, name='dispatch')
# class JobList(generics.ListAPIView):
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer


# @method_decorator(csrf_exempt, name='dispatch')
# class JobsList(generics.ListAPIView):

#     def get_queryset(self):
#         return Job.objects.all()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         job_details_set = set()

#         # Collecting unique job details
#         for job in queryset:
#             job_details_set.add((job.part_no.part_no, job.component_name, job.operation_no))

#         # Converting set to a list of dictionaries with specific keys
#         job_details_list = [
#             {
#                 "part_no": job[0],
#                 "component_name": job[1],
#                 "operation_no": job[2]
#             }
#             for job in job_details_set
#         ]

#         # Returning JSON response
#         return Response(job_details_list)



def get_tool_codess(request, part_number):
    if not part_number:
        return JsonResponse({'error': 'Part number is required'}, status=400)

    jobs = Job.objects.filter(part_no__part_no=part_number)
    tool_codes = list(jobs.values_list('tool_code__tool_code', flat=True))

    return JsonResponse({'tool_codes': tool_codes})

# @method_decorator(csrf_exempt, name='dispatch')
# class ToolCreateView(CreateAPIView):
#     queryset = Tool.objects.all()
#     serializer_class = ToolSerializer
#     def create(self, request, *args, **kwargs):
#         tool_name = request.data.get('tool name')  # Assuming 'tool_name' is the field name for tool name
#         tool_code = request.data.get('tool_code')  # Assuming 'tool_code' is the field name for tool code
#         tool_codes = Tool.objects.filter(tool_name=tool_name).values_list('tool_code', flat=True)
#         z = 0
#         for code in tool_codes:
#             if Job.objects.filter(tool_code=code).exists():
# 			z = 1
#         if z == 1 :
#         	for code in tool_code :
#         	    job_exists = Job.objects.filter(tool_code=code).exists()
#         	    job_exist = Job.objects.filter(tool_code=code)
#                 if job_exists:
#                     Job.objects.create(
#                     part_no=job_exist.part_no,
#                     component_name=job_exist.component_name,
#                     depth_of_cut=job_exist.depth_of_cut,
#                     no_of_holes=job_exist.no_of_holes,
#                     operation_no=job_exist.operation_no,
#                     tool_code=code  # Update with the new tool code
#                 )


@method_decorator(csrf_exempt, name='dispatch')
class ToolCreateView(CreateAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    # def create(self, request, *args, **kwargs):
    #     tool_name = request.data.get('tool_name')  # Assuming 'tool_name' is the field name for tool name
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
    #         new_tool_code = request.data.get('tool_code')  # Assuming 'tool_code' is the field name for the new tool code
    #         print(f"New tool code :{new_tool_code}")
    #         for code in tool_codes:
    #             job_queryset = Job.objects.filter(tool_code=code).all()
    #             print(job_queryset)
    #             for job in job_queryset:
    #                 print(job)

    #                 Job.objects.create(
    #                     part_no=job.part_no,
    #                     component_name=job.component_name,
    #                     depth_of_cut=job.depth_of_cut,
    #                     no_of_holes=job.no_of_holes,
    #                     operation_no=job.operation_no,
    #                     tool_code=new_tool_code  # Update with the new tool code
    #                 )
    #                 print("Created new job")

    #     return super().create(request, *args, **kwargs)






@method_decorator(csrf_exempt, name='dispatch')
class BreakdownList(generics.ListAPIView):
    queryset = Breakdown.objects.all()
    serializer_class = BreakdownSerializer

@method_decorator(csrf_exempt, name='dispatch')
class BreakdownCreateView(CreateAPIView):
    queryset = Breakdown.objects.all()
    serializer_class = BreakdownSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            tool_code = request.data.get('tool_code')
            machine_id = request.data.get('machine_id')
            replaced_by_tool_code = request.data.get('replaced_by')
            incrementBrkPntByOne(tool_code)
            update_machine_tool_code(machine_id,tool_code, replaced_by_tool_code)



            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def update_machine_tool_code(machine_id,tool_code, replaced_by_tool_code):
    try:
        # Update the tool_code in Machine table
        Machine.objects.filter(machine_id=machine_id,tool_code=tool_code).update(tool_code=replaced_by_tool_code)
    except Exception as e:
        print(f"An error occurred while updating machine tool code: {e}")

@method_decorator(csrf_exempt, name='dispatch')
class MachineList(generics.ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

@method_decorator(csrf_exempt, name='dispatch')
class PerformsCreateView(CreateAPIView):
    queryset = Performs.objects.all()
    serializer_class = PerformsSerializers

@method_decorator(csrf_exempt, name='dispatch')
def top_employees(request):

    top_employees = Employee2.objects.annotate(
        efficiency=F('emp_efficiency')
    ).order_by('-efficiency')[:9]
    top_employees_data = list(top_employees.values('emp_ssn', 'emp_name', 'emp_efficiency'))

    return JsonResponse(top_employees_data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
def top_least_employees(request):
    least_employees = Employee2.objects.order_by('emp_efficiency')[:9]
    data = [{'emp_name': employee.emp_name, 'emp_ssn': employee.emp_ssn} for employee in least_employees]
    return JsonResponse(data, safe=False)

# @method_decorator(csrf_exempt, name='dispatch')
# def update_employee(request, pk):
#     employee = get_object_or_404(Employee2, emp_ssn=pk)

#     if request.method == 'POST':
#         serializer = EmployeeSerializer(instance=employee, data=request.data)  # Assuming data is sent via POST form data
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#     else:
#         return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@method_decorator(csrf_exempt, name='dispatch')
def update_employee(request, pk):
    # Get the employee instance
    employee = get_object_or_404(Employee2, emp_ssn=pk)

    # Check if data is sent via POST request
    if request.method == 'POST':
        # Deserialize the JSON data sent by Axios
        data = json.loads(request.body)
        serializer = EmployeeSerializer(instance=employee, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@method_decorator(csrf_exempt, name='dispatch')
def update_tool_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tool_code = data.get('tool_code')
        incrementBrkPntByOne(tool_code)
        return JsonResponse({'message': 'Tool updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

# @method_decorator(csrf_exempt, name='dispatch')
# def incrementBrkPntByOne(tool_code):

#     tool = Tool.objects.get(tool_code=tool_code)
#     tool.no_of_brk_points += 1
#     part_no_count = Job.objects.filter(tool_code=tool).count()


#     efficiency=(tool.length_cut_so_far/tool.max_life_expectancy_in_mm)*100

#     print("=-=-=-=-=-=-=-=-=EFFICIENCY IN TOOL CHART-=-=--=-=-=-=-=-=")
#     print(f"{efficiency}")
#     print(f"Length cut so far {tool.length_cut_so_far}")
#     print(f"Max Life {tool.max_life_expectancy_in_mm}")

#     # Create and save ToolChart instance
#     tool_chart = ToolChart.objects.create(
#         tool_code=tool_code,
#         no_of_brk_points=tool.no_of_brk_points,
#         tool_efficiency=efficiency,
#         part_no_count=part_no_count
#     )

#     tool.tool_efficiency=0
#     tool.length_cut_so_far=0
#     tool_chart.save()
#     tool.save()

from django.db.models.signals import pre_save, post_save
from .models import check_job_table_after_tool_save

def incrementBrkPntByOne(tool_code):

    print("IN INCREMENT BRK POINT BY ONE")
    # # Disconnect signals
    post_save.disconnect(check_job_table_after_tool_save,sender=Tool)



    tool = Tool.objects.get(tool_code=tool_code)
    tool.no_of_brk_points += 1
    part_no_count = Job.objects.filter(tool_code=tool).count()

    efficiency = (tool.length_cut_so_far / tool.max_life_expectancy_in_mm) * 100

    print("=-=-=-=-=-=-=-=-=EFFICIENCY IN TOOL CHART-=-=--=-=-=-=-=-=")
    print(f"{efficiency}")
    print(f"Length cut so far {tool.length_cut_so_far}")
    print(f"Max Life {tool.max_life_expectancy_in_mm}")

    # Create and save ToolChart instance
    # tool_chart = ToolChart.objects.create(
    #     tool_code=tool_code,
    #     no_of_brk_points=tool.no_of_brk_points,
    #     tool_efficiency=efficiency,
    #     part_no_count=part_no_count
    # )
    print("tool_chart is saved .............")
    tool.tool_efficiency = 0
    print("effiency ...................")
    tool.length_cut_so_far = 0
    print("length.................")
    # tool_chart.save()
    tool.save()
    print("tool is saved ................")

    post_save.connect(check_job_table_after_tool_save,sender=Tool)
    print("connected ..........................")


def RGH(request):
    global previous_values_list
    json_response = json.dumps(previous_values_list)
    return JsonResponse(json_response, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class ChartList(generics.ListAPIView):
        queryset = ToolChart.objects.all()
        serializer_class = ChartS

@method_decorator(csrf_exempt, name='dispatch')
def tool_chart_details(request, tool_code):
    tool_chart = ToolChart.objects.filter(tool_code=tool_code)
    if tool_chart.exists():
        data = list(tool_chart.values())
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'message': 'No data found for the provided tool code.'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
def get_tool_data(request):
    tools = Tool.objects.values('tool_code', 'tool_efficiency', 'no_of_brk_points')
    tool_data = list(tools)
    return JsonResponse(tool_data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
def calculate_shift_efficiency(shift_number):
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

    if shift_duration_sum and partial_shift_sum and target_sum and achieved_sum:
        x = target_sum * (partial_shift_sum / shift_duration_sum)
        efficiency = (achieved_sum / x)*100
        efficiency=round(efficiency,2)
        return efficiency
    else:
        return None


# def shift_eff(request, shift_number):
#     d = Shift.objects.filter(shift_number=shift_number)
#     shift_data = list(d.values())
#     return JsonResponse(shift_data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
def get_shift_efficiency(request, shift_number):
    efficiency = calculate_shift_efficiency(shift_number)
    return JsonResponse({'shift_number': shift_number, 'efficiency': efficiency})

@method_decorator(csrf_exempt, name='dispatch')
def shift_eff(request, shift_number):
    shift_data = Shift.objects.filter(shift_number=shift_number)
    average_efficiency = shift_data.aggregate(avg_efficiency=Avg('shift_efficiency'))['avg_efficiency']

    if average_efficiency is None:
        average_efficiency = 0.0
    else:
        average_efficiency = round(average_efficiency, 2)

    return JsonResponse({'average_shift_efficiency': average_efficiency})

@method_decorator(csrf_exempt, name='dispatch')
def get_total_avg_efficiency(request):
    total_efficiency = 0
    for shift_number in range(1, 4):
        efficiency = calculate_shift_efficiency(shift_number)
        if efficiency is not None:
            total_efficiency += efficiency
    total_avg_efficiency = total_efficiency / 3
    return JsonResponse({'total_avg_efficiency': total_avg_efficiency})


@method_decorator(csrf_exempt, name='dispatch')
def delete_employee_by_ssn(request, emp_ssn):
    try:
        employee = Employee2.objects.get(emp_ssn=emp_ssn)
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully'})
    except Employee2.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
# def get_number_of_jobs(request):
#     num_jobs = Job.objects.count()
#     return JsonResponse({'num_jobs': num_jobs})

@method_decorator(csrf_exempt, name='dispatch')
def get_number_of_jobs(request):
    num_jobs = Job.objects.values('part_no').distinct().count()
    return JsonResponse({'num_jobs': num_jobs})

@method_decorator(csrf_exempt, name='dispatch')
def get_number_of_machines(request):
    num_machines = NewMachine.objects.count()
    return JsonResponse({'num_machines': num_machines})

@method_decorator(csrf_exempt, name='dispatch')
def get_number_of_tools(request):
    num_tools = Tool.objects.count()
    return JsonResponse({'num_tools': num_tools})

@method_decorator(csrf_exempt, name='dispatch')
def get_number_of_employees(request):
    num_employees = Employee2.objects.count()
    return JsonResponse({'num_employees': num_employees})

@method_decorator(csrf_exempt, name='dispatch')
def get_tool_codes(request, part_no):
    # Get tool codes associated with the provided part number
    tool_codes = Job.objects.filter(part_no=part_no).values_list('tool_code', flat=True)
    print(tool_codes)
    # Create a set to store unique tool names
    unique_tool_names = set()

    # Iterate over each tool code and retrieve the corresponding tool name
    for code in tool_codes:
        tool = Tool.objects.filter(tool_code=code).first()
        if tool:
            unique_tool_names.add(tool.tool_name)

    # Convert the set to a list
    unique_tool_names_list = list(unique_tool_names)

    return JsonResponse(unique_tool_names_list, safe=False)

# new one ______________________________________________________________
@method_decorator(csrf_exempt, name='dispatch')
def get_tool_codes1(request, part_no,operation_no):
    # Get tool codes associated with the provided part number
    tool_codes = Job.objects.filter(part_no=part_no,operation_no=operation_no).values_list('tool_code', flat=True)
    print(tool_codes)
    # Create a set to store unique tool names
    unique_tool_names = set()

    # Iterate over each tool code and retrieve the corresponding tool name
    for code in tool_codes:
        tool = Tool.objects.filter(tool_code=code).first()
        if tool:
            unique_tool_names.add(tool.tool_name)

    # Convert the set to a list
    unique_tool_names_list = list(unique_tool_names)

    return JsonResponse(unique_tool_names_list, safe=False)



@method_decorator(csrf_exempt, name='dispatch')
def shift_performance_by_date(request):
    # Aggregate data for each date and shift number
    shift_performance = Performs.objects.values('date', 'shift_number').annotate(
        total_target=Sum('target'),
        total_achieved=Sum('achieved')
    )

    # Convert queryset to dictionary for easier manipulation
    shift_performance_dict = {}
    for data in shift_performance:
        date = str(data['date'])  # Convert date to string
        shift_number = data['shift_number']
        total_target = data['total_target']
        total_achieved = data['total_achieved']

        if date not in shift_performance_dict:
            shift_performance_dict[date] = {}

        shift_performance_dict[date][shift_number] = {
            'total_target': total_target,
            'total_achieved': total_achieved
        }

    return JsonResponse(shift_performance_dict)

@method_decorator(csrf_exempt, name='dispatch')
def efficiency_by_employee(request):
    employees = Employee2.objects.all()
    efficiency_data = []
    for employee in employees:
        efficiency_data.append({
            'emp_ssn': employee.emp_ssn,
            'emp_efficiency': employee.emp_efficiency
        })
    return JsonResponse({'efficiency_data': efficiency_data})


@method_decorator(csrf_exempt, name='dispatch')
def delete_breakdown_by_tool_code(request, tool_code):
    if request.method == 'DELETE':
        breakdown = get_object_or_404(Breakdown, tool_code=tool_code)
        breakdown.delete()
        return JsonResponse({'message': 'Breakdown deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@method_decorator(csrf_exempt, name='dispatch')
def calculate_avg_shift_efficiency(request, date_a, date_b, shift_number):
    try:
        date_a = datetime.strptime(date_a, '%Y-%m-%d').date()
        date_b = datetime.strptime(date_b, '%Y-%m-%d').date()
        shift_efficiencies = Shift.objects.filter(date__range=[date_a, date_b], shift_number=shift_number)

        if shift_efficiencies.exists():
            avg_efficiency = shift_efficiencies.aggregate(avg_efficiency=Avg('shift_efficiency'))['avg_efficiency']
            return JsonResponse({'avg_efficiency': avg_efficiency})
        else:
            return JsonResponse({'avg_efficiency': 0}, status=200)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
def cal(request,date_a, date_b, shift_number):
        avg_efficiency =0
        date_a = datetime.strptime(date_a, '%Y-%m-%d').date()
        date_b = datetime.strptime(date_b, '%Y-%m-%d').date()
        shift_efficiencies = Shift.objects.filter(date__range=[date_a, date_b], shift_number=shift_number)
        if shift_efficiencies.exists():
            avg_efficiency = shift_efficiencies.aggregate(avg_efficiency=Avg('shift_efficiency'))['avg_efficiency']
        return avg_efficiency

@method_decorator(csrf_exempt, name='dispatch')
def cacl_avgs(request, date_a, date_b):
    try:
        avg_eff =0
        for i in range(1, 4):
            avg_efficiency_response = cal(request, date_a, date_b, i)
            avg_eff += avg_efficiency_response
        avg_efficiency = avg_eff/3

        return JsonResponse({'avg_efficiency': avg_efficiency}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
def add_to_reviving(request, tool_code, date):
    breakdown_instance = get_object_or_404(Breakdown, tool_code=tool_code,date=date)
    breakdown_instance.delete()
    current_date = datetime.now().date()
    Reviving1.objects.create(tool_code_id=tool_code, date=current_date)

    return JsonResponse({'message': 'Breakdown resolved successfully'}, status=200)


class LReviving1(generics.ListAPIView):
    queryset = Reviving1.objects.all()
    serializer_class = Rev




def shift_counts(request):
    # Query the Performs table to get the count of entries for each shift number for each date
    shift_counts_by_date = Performs.objects.values('date', 'shift_number').annotate(count=Count('id'))

    # Initialize a dictionary to store the counts for each date and shift number
    counts_by_date = {}

    # Iterate over the query results and populate the dictionary
    for entry in shift_counts_by_date:
        date = entry['date']
        shift_number = entry['shift_number']
        count = entry['count']

        # If the date is not already in the dictionary, create a new entry
        if date not in counts_by_date:
            counts_by_date[date] = {'date': date, '1': 0, '2': 0, '3': 0}

        # Store the count for the shift number under the corresponding date
        counts_by_date[date][str(shift_number)] = count

    # Return the result as a JSON response
    return JsonResponse(list(counts_by_date.values()), safe=False)


# def tool_codes_view(request):
#     all_tools = Tool.objects.all()
#     used_tool_codes = Breakdown.objects.values_list('tool_code__tool_code', flat=True)
#     tool_data = []

#     for tool in all_tools:
#         if tool.tool_code not in used_tool_codes:
#             tool_info = {
#                 "tool_name": tool.tool_name,
#                 "tool_codes": [tool.tool_code]
#             }
#             tool_data.append(tool_info)

#     return JsonResponse(tool_data, safe=False)



def tool_codes_view(request):
    all_tools = Tool.objects.all()
    used_tool_codes = Breakdown.objects.values_list('tool_code__tool_code', flat=True)
    tool_data = []

    for tool in all_tools:
        if tool.tool_code not in used_tool_codes:
            # Check if the tool already exists in tool_data
            tool_exists = False
            for existing_tool in tool_data:
                if existing_tool['tool_name'] == tool.tool_name:
                    existing_tool['tool_codes'].append(tool.tool_code)
                    tool_exists = True
                    break

            # If the tool doesn't exist, add it to tool_data
            if not tool_exists:
                tool_info = {
                    "tool_name": tool.tool_name,
                    "tool_codes": [tool.tool_code]
                }
                tool_data.append(tool_info)

    return JsonResponse(tool_data, safe=False)


def unique_part_numbers_view(request):
    # Fetch all unique part numbers
    unique_part_numbers = Job.objects.values('part_no').distinct()

    # Initialize a list to store unique job data
    unique_jobs_data = []
    i=0;

    # Fetch the necessary data for the first occurrence of each unique part number
    for unique_part in unique_part_numbers:
        job = Job.objects.filter(part_no=unique_part['part_no']).first()
        if job:
            i+=1
            job_data = {
                'id':i,
                'part_no': job.part_no.part_no,
                'component_name': job.component_name,
                'depth_of_cut': job.depth_of_cut,
                'no_of_holes': job.no_of_holes,
                'operation_no': job.operation_no,
                'tool_code': job.tool_code.tool_code
            }
            unique_jobs_data.append(job_data)

    # Return the list of unique job data as a JSON response
    return JsonResponse(unique_jobs_data, safe=False)


def target_by_machine_name(request, machine_name):
    try:
        machine = Machine.objects.filter(machine_name=machine_name).first()
        if machine:
            target = machine.target
            print("-----------------------------------------------MACHINE TARGET--------------------------------")
            print(target)
            return JsonResponse({"machine_name": machine_name, "target": target})
        else:
            return JsonResponse({"error": "No machine found with that name"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_machine_data(request, machine_id):
    try:
        machine = Machine.objects.filter(machine_id=machine_id).first()
        if machine:
            data = {
                "machine_id": machine.machine_id_id,
                "machine_name": machine.machine_name,
                "part_no": machine.part_no_id,
                "target": machine.target
            }

            # Collect all unique tool codes
            tool_codes = set()
            machines = Machine.objects.filter(machine_id=machine_id)
            for m in machines:
                tool_codes.add(m.tool_code_id)

            # If there are multiple tool codes, include them in an array
                data["tool_code"] = list(tool_codes)

            return JsonResponse(data)
        else:
            return JsonResponse({"message": "No machine found with the given ID"}, status=404)
    except MultipleObjectsReturned:
        # If multiple objects returned, handle it here
        machines = Machine.objects.filter(machine_id=machine_id)
        first_machine = machines.first()
        data = {
            "machine_id": first_machine.machine_id_id,
            "machine_name": first_machine.machine_name,
            "part_no": first_machine.part_no_id,
            "target": first_machine.target
        }

        # Collect all unique tool codes
        tool_codes = set()
        for m in machines:
            tool_codes.add(m.tool_code_id)

        # Include tool codes in an array
        data["tool_code"] = list(tool_codes)

        return JsonResponse(data)





@method_decorator(csrf_exempt, name='dispatch')
def delete_machines(request, machine_id):
    try:
        machine = NewMachine.objects.get(machine_id=machine_id)
        machine.delete()
        machines = Machine.objects.filter(machine_id=machine_id)
        machines.delete()
        return JsonResponse({'message': 'Machines deleted successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'No machines found with the given machine_id'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
def delete_tools_by_name(request, tool_name, tool_code):
    try:
        print(f"Attempting to delete tool with tool_name: {tool_name}, tool_code: {tool_code}")

        jobs_before_update = Job.objects.filter(tool_code=tool_code)
        print(f"Jobs before update: {[str(job) for job in jobs_before_update]}")

        job_count = Job.objects.filter(tool_code=tool_code).update(tool_code=None)
        print(f"Updated {job_count} Job records to set tool_code to NULL")

        jobs_after_update = Job.objects.filter(tool_code=tool_code)
        print(f"Jobs after update: {[str(job) for job in jobs_after_update]}")

        tools = Tool.objects.filter(tool_name=tool_name, tool_code=tool_code)
        tool_count = tools.delete()
        print(f"Deleted {tool_count[0]} Tool records with tool_name: {tool_name}, tool_code: {tool_code}")

        return JsonResponse({'message': f'All tools with tool_name {tool_name} and tool_code {tool_code} deleted successfully'})
    except Exception as e:
        print(f"Error occurred: {e}")
        return JsonResponse({'error': str(e)}, status=500)




@method_decorator(csrf_exempt, name='dispatch')
def delete_job_by_part_no(request, part_no):
    jobs = Job.objects.filter(part_no=part_no)
    new_job = get_object_or_404(NewJob, part_no=part_no)
    new_job.delete()
    jobs.delete()
    return JsonResponse({'message': f'Jobs with part number {part_no} deleted successfully'})



@method_decorator(csrf_exempt, name='dispatch')
def display_tool_codes(request, machine_id):
    try:
        machines = Machine.objects.filter(machine_id=machine_id)
        tool_codes = [machine.tool_code.tool_code for machine in machines]
        return JsonResponse({'machine_id': machine_id, 'tool_codes': tool_codes})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
def delete_performs_entry(request, date, emp_ssn, shift_number):
    try:
        data = json.loads(request.body)
        id = data.get('id')
        performs_entry = Performs.objects.filter(date=date, emp_ssn=emp_ssn, shift_number=shift_number,id =id)

    except Performs.DoesNotExist:
        return JsonResponse({'error': 'Performs entry does not exist'}, status=404)

    performs_entry.delete()
    return JsonResponse({'message': 'Performs entry deleted successfully'})


# i=0
# @method_decorator(csrf_exempt, name='dispatch')
# def update_machine(request, machine_id):
#     global i
#     try:
#         logging.info("Received GET parameters: %s", request.GET)
#         if i == 0:
#             machines = Machine.objects.filter(machine_id=machine_id)
#             machines.delete()
#         print("HII............................................................................................................")
#         target = request.GET.get("target")
#         num_of_tools = int(request.GET.get("numOfTools", 0))
#         part_no1 = request.GET.get("part_no")
#         tool_code = request.GET.get("tool_code")
#         print(part_no1)
#         print("HI............................................................................................................")

#         # # Retrieve or create the NewMachine instance
#         # new_machine, created = NewMachine.objects.get_or_create(machine_id=machine_id)

#         # # Create or update the Machine instance
#         # machine, machine_created = Machine.objects.get_or_create(machine_id=new_machine)
#         # machine.machine_name = machine_id
#         # machine.machine_id = machine_id
#         # machine.target = target
#         # machine.part_no = part_no1
#         # machine.tool_code = tool_code
#         # print(part_no1)
#         # machine.save()

#         M_instance = Machine(machine_id = machine_id,machine_name=machine_id,part_no=part_no1,tool_code=tool_code,target=target)
#         M_instance.save()

#         i += 1

#         if i == num_of_tools - 1:
#             i = 0

#         return JsonResponse({"message": "Machine updated successfully"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

# i=0
# @method_decorator(csrf_exempt, name='dispatch')
# def update_machine(request, machine_id):
#     global i
#     try:
#         if i == 0:
#             Machine.objects.filter(machine_id=machine_id).delete()
#         print("Hi....")
#         target = request.POST.get("target")
#         num_of_tools = int(request.POST.get("numOfTools", 0))
#         part_no = request.POST.get("part_no")
#         tool_code = request.POST.get("tool_code")

#         print(target)
#         new_machine, created = NewMachine.objects.get_or_create(machine_id=machine_id)

#         machine = Machine.objects.create(
#             machine_id=new_machine,
#             machine_name=machine_id,
#             part_no=part_no,
#             tool_code=tool_code,
#             target=target
#         )
#         machine.save()

#         i += 1

#         if i == num_of_tools - 1:
#             i = 0

#         return JsonResponse({"message": "Machine updated successfully"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)



# @method_decorator(csrf_exempt, name='dispatch')
# def update_machine(request, machine_id):
#     try:
#         Machine.objects.filter(machine_id=machine_id).delete()
#         print("Hi....")
#         data = json.loads(request.body)
#         target = data.get("target")
#         part_no = data.get("part_no")
#         tool_codes = data.get("tool_codes")

#         print(request)
#         new_job = NewJob.objects.get_or_create(part_no=part_no)
#         new_machine, created = NewMachine.objects.get_or_create(machine_id=machine_id)
#         for tool_code in tool_codes:
#             machine = Machine.objects.create(
#                 machine_id=new_machine,
#                 machine_name=machine_id,
#                 part_no=part_no,
#                 tool_code=tool_code,
#                 target=target
#             )
#             machine.save()

#         return JsonResponse({"message": "Machine updated successfully"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)



@method_decorator(csrf_exempt, name='dispatch')
def update_machine(request, machine_id):
    try:
        # Delete existing machines with the given machine_id
        Machine.objects.filter(machine_id=machine_id).delete()

        data = json.loads(request.body)
        target = data.get("target")
        part_no = data.get("part_no")
        tool_codes = data.get("tool_codes")

        if tool_codes is None or not isinstance(tool_codes, (list, tuple)):
            raise ValueError("tool_codes must be a list or tuple")

        new_job, _ = NewJob.objects.get_or_create(part_no=part_no)
        new_machine, _ = NewMachine.objects.get_or_create(machine_id=machine_id)

        # Create new machines for each tool_code
        for tool_code in tool_codes:
            new_tool = Tool.objects.get(tool_code=tool_code)
            machine = Machine.objects.create(
                machine_id=new_machine,
                machine_name=machine_id,
                part_no=new_job,  # Assign the NewJob instance
                tool_code=new_tool,
                target=target
            )
            machine.save()

        return JsonResponse({"message": "Machine updated successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@method_decorator(csrf_exempt, name='dispatch')
def sign_up(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')
        if role and username and password:
            new_user = Auth.objects.create(
                role=role,
                username=username,
                password=password
            )
            return JsonResponse({'message': 'User created successfully'}, status=201)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@method_decorator(csrf_exempt, name='dispatch')
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')
        if role and username and password:
            try:
                user = Auth.objects.get(role=role, username=username, password=password)
                return JsonResponse({'message': f'Login successful. Role: {role}'}, status=200)
            except Auth.DoesNotExist:
                return JsonResponse({'error': 'Invalid username, password, or role'}, status=401)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# @method_decorator(csrf_exempt, name='dispatch')
# def update_incentives(request, category, incentive):
#     try:
#         incentive_obj = Incentives.objects.get(category=category)
#         incentive_obj.incentive = incentive
#         incentive_obj.save()
#         return JsonResponse({'message': 'Incentive updated successfully'}, status=200)
#     except Incentives.DoesNotExist:
#         return JsonResponse({'error': 'Incentive not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)



# @api_view(['GET'])
# def get_incentives(request):
#     incentives = Incentives.objects.all().values('category', 'incentive')
#     incentives_data = list(incentives)
#     return JsonResponse(incentives_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
def check_credentials(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(username)
            print(password)
            if username is not None and password is not None:
                try:
                    user = SignAuth.objects.get(username=username, password=password)
                    return JsonResponse({'success': True, 'message': 'Credentials are valid.'})
                except SignAuth.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Invalid credentials.'})
            else:
                return JsonResponse({'success': False, 'message': 'Username and password are required.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed.'})

@method_decorator(csrf_exempt, name='dispatch')
def check_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        try:
            user = SignAuth.objects.get(username=username)
            return JsonResponse({'exists': True, 'userId': user.id})
        except SignAuth.DoesNotExist:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.http import JsonResponse
from .models import Externals

def externals_data(request):
    externals = Externals.objects.all()
    data = [{'parameter': external.parameter, 'value': external.value} for external in externals]
    return JsonResponse(data, safe=False)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Externals
import json

@csrf_exempt
def update_externals(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                parameter = item.get('parameter')
                value = item.get('value')
                externals_obj, created = Externals.objects.get_or_create(parameter=parameter)
                externals_obj.value = value
                externals_obj.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)






from django.http import JsonResponse
from django.db.models import F

def calculate_incentive(request, emp_ssn, start_date, end_date):
    if request.method == 'GET':
        try:
            # Get employee category
            employee = Employee2.objects.get(emp_ssn=emp_ssn)
            category = employee.emp_category

            # Get incentive value based on employee category
            parameter = "category " + str(category)
            incentive_value = Externals.objects.get(parameter=parameter).value
        except Employee2.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Externals.DoesNotExist:
            return JsonResponse({'error': 'Incentive value not found'}, status=404)

        # Filter Performs table based on emp_ssn and date range
        incentive_data = Performs.objects.filter(
            emp_ssn=emp_ssn,
            date__range=[start_date, end_date]
        ).values('date', 'shift_number', 'efficiency', 'incentive_received')

        # Convert queryset to list of dictionaries
        incentive_list = list(incentive_data)

        # Add incentive value to each dictionary in the list
        for data in incentive_list:
            data['incentive_value'] = incentive_value

        return JsonResponse(incentive_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)





def generate_report(request, date):
    if request.method == 'GET':
        # Convert date string to datetime object
        current_date = datetime.strptime(date, "%Y-%m-%d").date()

        # Fetching distinct machine IDs from Performs
        machine_ids = Performs.objects.filter(date=current_date).values_list('machine_id', flat=True).distinct()

        report = []
        for machine_id in machine_ids:
            # Get all machines with the current machine_id
            machines = Machine.objects.filter(machine_id=machine_id)


            if not machines.exists():
                continue  # If no machine exists with this ID, skip to the next one

            # Assuming you want to handle all machines with the same machine_id
            for machine in machines:
                target = machine.target

                # Fetching component names and operation numbers for the current machine
                components = Job.objects.filter(part_no__in=Machine.objects.filter(machine_id=machine_id).values_list('part_no', flat=True)).values('component_name', 'operation_no').distinct()

                for component in components:
                    component_name = component['component_name']
                    operation_no = component['operation_no']

                    # Fetching data for each shift for the current machine and component
                    shift_1_achieved = Performs.objects.filter(machine_id=machine_id, shift_number=1, date=current_date).aggregate(total_achieved=Sum('achieved'))['total_achieved'] or 0
                    shift_2_achieved = Performs.objects.filter(machine_id=machine_id, shift_number=2, date=current_date).aggregate(total_achieved=Sum('achieved'))['total_achieved'] or 0
                    shift_3_achieved = Performs.objects.filter(machine_id=machine_id, shift_number=3, date=current_date).aggregate(total_achieved=Sum('achieved'))['total_achieved'] or 0

                    per_day_target = target * 3
                    per_day_achieved = shift_1_achieved + shift_2_achieved + shift_3_achieved

                    # Calculating percentages
                    shift_1_percentage = (shift_1_achieved / target) * 100 if target > 0 else 0
                    shift_2_percentage = (shift_2_achieved / target) * 100 if target > 0 else 0
                    shift_3_percentage = (shift_3_achieved / target) * 100 if target > 0 else 0
                    per_day_achieved_percentage = (per_day_achieved / per_day_target) * 100 if per_day_target > 0 else 0

                    if {
                        'machine_id': machine_id,
                        'component_name': component_name,
                        'operation_no': operation_no,

                        'shift_target': target,
                        'quantity_achieved_shift_1': shift_1_achieved,
                        'shift_1_percentage': shift_1_percentage,
                        'quantity_achieved_shift_2': shift_2_achieved,
                        'shift_2_percentage': shift_2_percentage,
                        'quantity_achieved_shift_3': shift_3_achieved,
                        'shift_3_percentage': shift_3_percentage,
                        'per_day_target': per_day_target,
                        'per_day_achieved': per_day_achieved,
                        'per_day_achieved_percentage': per_day_achieved_percentage,
                    } not in report :
                        report.append({
                            'machine_id': machine_id,
                            'component_name': component_name,
                            'operation_no': operation_no,

                            'shift_target': target,
                            'quantity_achieved_shift_1': shift_1_achieved,
                            'shift_1_percentage': shift_1_percentage,
                            'quantity_achieved_shift_2': shift_2_achieved,
                            'shift_2_percentage': shift_2_percentage,
                            'quantity_achieved_shift_3': shift_3_achieved,
                            'shift_3_percentage': shift_3_percentage,
                            'per_day_target': per_day_target,
                            'per_day_achieved': per_day_achieved,
                            'per_day_achieved_percentage': per_day_achieved_percentage,
                        })

        return JsonResponse(report, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




# @method_decorator(csrf_exempt, name='dispatch')
# class JobsList(generics.ListAPIView):

#     def get_queryset(self):
#         return Job.objects.all()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         job_details_list = []

#         for job in queryset:
#             job_details_list.append({
#                 'part_no': job.part_no.part_no,
#                 'component_name': job.component_name,
#                 'operation_no': job.operation_no
#             })

#         return JsonResponse(job_details_list, safe=False)



from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_external(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            parameter = data.get("parameter")
            value = data.get("value")
            type1= data.get("type")
            if type1=="category":
                parameter="category "+str(parameter)
            externals_obj = Externals.objects.create(parameter=parameter,value=value)

            externals_obj.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)




@csrf_exempt
def breakdown_tool_codes(request, tool_code):
    try:
        tool = Tool.objects.get(tool_code=tool_code)
        tools_with_same_name = Tool.objects.filter(tool_name=tool.tool_name)
        tool_codes = [tool.tool_code for tool in tools_with_same_name]

        return JsonResponse({'tool_codes': tool_codes})
    except Tool.DoesNotExist:
        return JsonResponse({'error': 'Tool with the specified tool code does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_machine_jobs(request, machine_id):
    try:
        machine = Machine.objects.filter(machine_id=machine_id).first()
        if not machine:
            return JsonResponse({"error": "Machine not found"}, status=404)

        job = Job.objects.get(part_no=machine.part_no, tool_code=machine.tool_code)
        job_detail = {
            "part_no":machine.part_no.part_no,
            "operation_no": job.operation_no,
            "component_name": job.component_name
        }

        return JsonResponse(job_detail, safe=False)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Job details not found for the machine"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def update_tool(request, tool_code):
    try:
        data = json.loads(request.body)
        tool = Tool.objects.get(tool_code=tool_code)
        # tool.tool_code = data.get("tool_code")
        tool.tool_name = data.get("tool_name", tool.tool_name)
        tool.max_life_expectancy_in_mm = data.get("max_life_expectancy_in_mm", tool.max_life_expectancy_in_mm)
        tool.cost = data.get("cost", tool.cost)
        tool.length_cut_so_far = data.get("length_cut_so_far", tool.length_cut_so_far)
        tool.no_of_brk_points = data.get("no_of_brk_points", tool.no_of_brk_points)
        tool.tool_efficiency = data.get("tool_efficiency", tool.tool_efficiency)
        tool.save()
        return JsonResponse({"message": "Tool updated successfully"})
    except Tool.DoesNotExist:
        return JsonResponse({"error": "Tool not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.http import HttpResponseBadRequest

@csrf_exempt
def delete_external(request, parameter):
    try:
        external = Externals.objects.get(parameter=parameter)
        external.delete()
        return JsonResponse({'success': True})
    except Externals.DoesNotExist:
        return HttpResponseBadRequest('Item not found')


@csrf_exempt
def update_incentive(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            date = data.get('date')
            emp_ssn = data.get('emp_ssn')
            target = data.get('target')
            achieved = data.get('achieved')
            machine_id = data.get('machine_id')
            efficiency = data.get('efficiency')
            new_incentive = data.get('incentive_received')

            if None in [date, emp_ssn, target, achieved, machine_id, efficiency, new_incentive]:
                return HttpResponseBadRequest('Missing required fields')

            employee = Employee2.objects.get(emp_ssn=emp_ssn)

            perform_instance = Performs.objects.filter(
                date=date,
                emp_ssn=employee,
                target=target,
                achieved=achieved,
                machine_id=machine_id,
                efficiency=efficiency
            ).first()

            if not perform_instance:
                return HttpResponseBadRequest('Performs instance not found')

            try:
                perform_instance.incentive_received = round(float(new_incentive), 2)
                perform_instance.save()  # Save the updated instance

                return JsonResponse({'success': True, 'incentive_received': perform_instance.incentive_received})
            except ValueError:
                return HttpResponseBadRequest('Invalid incentive_received value')

        except Employee2.DoesNotExist:
            return HttpResponseBadRequest('Employee not found')
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON format')
    else:
        return HttpResponseBadRequest('Only POST requests are allowed')