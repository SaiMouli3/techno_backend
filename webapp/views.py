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
from .models import Employee2, Job, Tool, Breakdown, Machine, Performs,NewMachine, ToolChart, ToolChart, Shift, NewJob,Reviving1
from .serializers import EmployeeSerializer, JobSerializer, ToolSerializer, JobSerializer1, BreakdownSerializer, \
    MachineSerializer, PerformsSerializers, NMSerializer, ChartS, Rev
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from collections import defaultdict

previous_values_list = []


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeList(generics.ListAPIView):
    queryset = Employee2.objects.all()
    serializer_class = EmployeeSerializer

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeCreateView(CreateAPIView):
    queryset = Employee2.objects.all()
    serializer_class = EmployeeSerializer

@method_decorator(csrf_exempt, name='dispatch')
class JobsList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

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

@method_decorator(csrf_exempt, name='dispatch')
class JobCreateView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def post(self, request, *args, **kwargs):
        part_no = request.data.get('part_no')
        new_job = NewJob.objects.filter(part_no=part_no).first()  # Check if NewJob with given part_no exists

        if not new_job:  # If NewJob doesn't exist, create it
            new_job = NewJob.objects.create(part_no=part_no)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # Check if serializer is valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            new_job.delete()  # Delete the NewJob object if serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ToolList(generics.ListAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

@method_decorator(csrf_exempt, name='dispatch')
class CreateMachineList(CreateAPIView):
     queryset = Machine.objects.all()
     serializer_class = MachineSerializer

     def create(self, request, *args, **kwargs):
         try:
             return super().create(request, *args, **kwargs)
         except IntegrityError as e:
             error_message = "The machine has already been configured."
             return JsonResponse({'error': error_message}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ToolCreateView(CreateAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer


@method_decorator(csrf_exempt, name='dispatch')
class BreakdownList(generics.ListAPIView):
    queryset = Breakdown.objects.all()
    serializer_class = BreakdownSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            tool_code = request.data.get('tool_code')
            incrementBrkPntByOne(tool_code)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class BreakdownCreateView(CreateAPIView):
    queryset = Breakdown.objects.all()
    serializer_class = BreakdownSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            tool_code = request.data.get('tool_code')
            incrementBrkPntByOne(tool_code)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class MachineList(generics.ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

@method_decorator(csrf_exempt, name='dispatch')
class PerformsCreateView(CreateAPIView):
    queryset = Performs
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

@method_decorator(csrf_exempt, name='dispatch')
@api_view(['PUT'])
def update_employee(request, pk):
    employee = get_object_or_404(Employee2, emp_ssn=pk)
    serializer = EmployeeSerializer(instance=employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
def update_tool_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tool_code = data.get('tool_code')
        incrementBrkPntByOne(tool_code)
        return JsonResponse({'message': 'Tool updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@method_decorator(csrf_exempt, name='dispatch')
def incrementBrkPntByOne(tool_code):
    tool = Tool.objects.get(tool_code=tool_code)
    tool.no_of_brk_points += 1
    part_no_count = Job.objects.filter(tool_code=tool).count()
    if tool.max_life_expectancy_in_mm > 0:
        efficiency = (tool.length_cut_so_far / tool.max_life_expectancy_in_mm) * (1 - (0.1 * tool.no_of_brk_points)) * 100
        efficiency = round(efficiency, 2)
    else:
        efficiency = 0.0
    tool.save()

    # Create and save ToolChart instance
    tool_chart = ToolChart.objects.create(
        tool_code=tool_code,
        no_of_brk_points=tool.no_of_brk_points,
        tool_efficiency=efficiency,
        part_no_count=part_no_count
    )

    tool_chart.save()


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

    return JsonResponse({'average_shift_efficiency': round(average_efficiency,2)})

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
def get_number_of_jobs(request):
    num_jobs = Job.objects.count()
    return JsonResponse({'num_jobs': num_jobs})

@method_decorator(csrf_exempt, name='dispatch')
def get_number_of_machines(request):
    num_machines = Machine.objects.count()
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


# def target_by_machine_name(request, machine_name):
#     try:
#         machines = Machine.objects.filter(machine_name=machine_name)
#         targets = [machine.target for machine in machines]
#         return JsonResponse({"machine_name": machine_name, "targets": targets})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


def target_by_machine_name(request, machine_name):
    try:
        machine = Machine.objects.filter(machine_name=machine_name).first()
        if machine:
            target = machine.target
            return JsonResponse({"machine_name": machine_name, "target": target})
        else:
            return JsonResponse({"error": "No machine found with that name"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)






















