from django.urls import path

from .views import EmployeeList, EmployeeCreateView, update_employee, JobsList, ToolList, ToolCreateView, JobCreateView, \
        BreakdownList, BreakdownCreateView, MachineList, PerformsCreateView, get_shift_efficiency, \
        get_total_avg_efficiency, delete_employee_by_ssn, get_number_of_jobs, get_number_of_machines, \
        get_number_of_employees, get_number_of_tools, shift_eff, shift_performance_by_date, efficiency_by_employee, \
        delete_breakdown_by_tool_code, NMachineList, get_tool_codes, CreateMachineList, RGH, ChartList, \
        calculate_avg_shift_efficiency, LReviving1,NMachineView
from .views import update_tool_view, top_employees, top_least_employees, get_tool_data, tool_chart_details, cacl_avgs, add_to_reviving,shift_counts,tool_codes_view,unique_part_numbers_view,target_by_machine_name,PerformsList
from .views import get_machine_data,delete_machines,delete_tools_by_name,delete_job_by_part_no,display_tool_codes
from django.urls import path, re_path


urlpatterns = [
        path('api/employees/', EmployeeList.as_view(), name='employee-list'),
        path('api/employees/create/',EmployeeCreateView.as_view(), name='employee-list-create'),
        path('api/employees/update/<str:pk>/', update_employee),
        path('api/top_employees', top_employees),
        path('api/least_employee', top_least_employees),
        path('api/employees/<str:emp_ssn>/', delete_employee_by_ssn, name='delete_employee_by_ssn'),
        # path('api/breakdown/<path:tool_code>/',add_to_reviving,name="add_to_reviving"),
        path('api/break/<path:tool_code>/<str:date>',add_to_reviving,name="add_to_reviving"),
        path('api/per/', PerformsList.as_view(), name='performs-list'),

        path('display-tool-codes/<path:machine_id>/', display_tool_codes, name='display_tool_codes'),

        path('target/<path:machine_name>/', target_by_machine_name, name='target_by_machine_name'),
        path('machinesss/<path:machine_id>/', delete_machines, name='delete_machine'),
        path('delete-tools/<path:tool_name>/', delete_tools_by_name, name='delete_tools_by_name'),
        path('delete-job/<path:part_no>/', delete_job_by_part_no, name='delete_job_by_part_no'),

        path('machines/<path:machine_id>/', get_machine_data, name='get_machine_data'),

        path('api/shift_counts/',shift_counts,name='shift_counts'),
        path('api/rev',LReviving1.as_view()),
        path('calculate-shift-efficiency/<str:date_a>/<str:date_b>/<int:shift_number>/', calculate_avg_shift_efficiency, name='calculate_avg_shift_efficiency'),

        path('api/tool_reply/',tool_codes_view,name="toolcodesView"),
        path('api/nmview/',NMachineView.as_view()),
        #counting
         path('num_jobs/',get_number_of_jobs, name='num_jobs'),
         path('num_machines/',get_number_of_machines, name='num_machines'),
         path('num_tools/',get_number_of_tools, name='num_tools'),
         path('num_employees/',get_number_of_employees, name='num_employees'),


        path('api/tools/', ToolList.as_view(), name='tool-list'),

        path('api/tools/create', ToolCreateView.as_view(), name='tool-list-create'),

        path('api/update_tool', update_tool_view),
        path('api/tool_data', get_tool_data),
        path('api/tool_chart/<path:tool_code>', tool_chart_details),

        path('api/performs', PerformsCreateView.as_view()),
        path('api/submit-performance', PerformsCreateView.as_view(), name='performs-create'),


        path('api/jobs/', JobsList.as_view(), name='jobs-list'),
        path('api/jobs/create', JobCreateView.as_view(), name='jobs-list-create'),


        path('api/machines', MachineList.as_view()),
        path('api/nmachines', NMachineList.as_view()),
        path('api/machines/create', CreateMachineList.as_view()),

        path('api/breakdown', BreakdownList.as_view(), name='Break-down-list' ),
        path('api/breakdown/create', BreakdownCreateView.as_view(), name='Break-down-view'),
        path('api/breakdown/<path:tool_code>',delete_breakdown_by_tool_code),
        path('get-tool-codes/<path:part_no>/', get_tool_codes, name='get_tool_codes'),

        path('api/avg/<str:date_a>/<str:date_b>', cacl_avgs),
        path('api/jobss/', unique_part_numbers_view, name='unique_part_numbers'),


        path('shift/<int:shift_number>/', get_shift_efficiency, name='get_shift_efficiency'),
        path('total_avg_efficiency/', get_total_avg_efficiency, name='get_total_avg_efficiency'),
        path('shift_eff/<int:shift_number>',shift_eff),
        path('shift/date', shift_performance_by_date),
        path('emp/efficiency', efficiency_by_employee)
]

