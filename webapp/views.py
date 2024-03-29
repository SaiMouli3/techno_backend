from datetime import datetime
import json

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

from .models import Employee2, Job, Tool, Breakdown, Machine, Performs,NewMachine, ToolChart, ToolChart, Shift
from .serializers import EmployeeSerializer, JobSerializer, ToolSerializer, JobSerializer1, BreakdownSerializer, \
    MachineSerializer, PerformsSerializers, NMSerializer, ChartS
from rest_framework.decorators import api_view
from rest_framework.response import Response

previous_values_list = []


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


class EmployeeList(generics.ListAPIView):
    queryset = Employee2.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeCreateView(CreateAPIView):
    queryset = Employee2.objects.all()
    serializer_class = EmployeeSerializer


class JobsList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class NMachineList(generics.ListAPIView):
    queryset = NewMachine.objects.all()
    serializer_class = NMSerializer


class JobCreateView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToolList(generics.ListAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer


class CreateMachineList(CreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


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


class MachineList(generics.ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class PerformsCreateView(CreateAPIView):
    queryset = Performs
    serializer_class = PerformsSerializers


def top_employees(request):

    top_employees = Employee2.objects.annotate(
        efficiency=F('emp_efficiency')
    ).order_by('-efficiency')[:9]
    top_employees_data = list(top_employees.values('emp_ssn', 'emp_name', 'emp_efficiency'))

    return JsonResponse(top_employees_data, safe=False)


def top_least_employees(request):
    least_employees = Employee2.objects.order_by('emp_efficiency')[:9]
    data = [{'emp_name': employee.emp_name, 'emp_ssn': employee.emp_ssn} for employee in least_employees]
    return JsonResponse(data, safe=False)


@api_view(['PUT'])
def update_employee(request, pk):
    employee = get_object_or_404(Employee2, emp_ssn=pk)
    serializer = EmployeeSerializer(instance=employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


def update_tool_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tool_code = data.get('tool_code')
        incrementBrkPntByOne(tool_code)
        return JsonResponse({'message': 'Tool updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


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


def RGH(request):
    global previous_values_list
    json_response = json.dumps(previous_values_list)
    return JsonResponse(json_response, safe=False)


class ChartList(generics.ListAPIView):
        queryset = ToolChart.objects.all()
        serializer_class = ChartS


def tool_chart_details(request, tool_code):
    tool_chart = ToolChart.objects.filter(tool_code=tool_code)
    if tool_chart.exists():
        data = list(tool_chart.values())
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'message': 'No data found for the provided tool code.'}, status=404)



def get_tool_data(request):
    tools = Tool.objects.values('tool_code', 'tool_efficiency', 'no_of_brk_points')
    tool_data = list(tools)
    return JsonResponse(tool_data, safe=False)


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


def shift_eff(request, shift_number):
    d = Shift.objects.filter(shift_number=shift_number)
    shift_data = list(d.values())
    return JsonResponse(shift_data, safe=False)


def get_shift_efficiency(request, shift_number):
    efficiency = calculate_shift_efficiency(shift_number)
    return JsonResponse({'shift_number': shift_number, 'efficiency': efficiency})


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



def get_number_of_jobs(request):
    num_jobs = Job.objects.count()
    return JsonResponse({'num_jobs': num_jobs})


def get_number_of_machines(request):
    num_machines = Machine.objects.count()
    return JsonResponse({'num_machines': num_machines})


def get_number_of_tools(request):
    num_tools = Tool.objects.count()
    return JsonResponse({'num_tools': num_tools})


def get_number_of_employees(request):
    num_employees = Employee2.objects.count()
    return JsonResponse({'num_employees': num_employees})


def get_tool_codes(request, part_no):
    tool_codes = Job.objects.filter(part_no=part_no).values('tool_code')
    tool_codes_list = list(tool_codes)
    return JsonResponse(tool_codes_list, safe=False)



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


def cal(request,date_a, date_b, shift_number):
        avg_efficiency =0
        date_a = datetime.strptime(date_a, '%Y-%m-%d').date()
        date_b = datetime.strptime(date_b, '%Y-%m-%d').date()
        shift_efficiencies = Shift.objects.filter(date__range=[date_a, date_b], shift_number=shift_number)
        if shift_efficiencies.exists():
            avg_efficiency = shift_efficiencies.aggregate(avg_efficiency=Avg('shift_efficiency'))['avg_efficiency']
        return avg_efficiency


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
    



















