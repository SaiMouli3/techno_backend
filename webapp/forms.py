from django import forms
from .models import Employee2, Tool, Job, Machine,Performs


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee2
        fields = ['emp_ssn', 'emp_name', 'emp_designation', 'emp_shed','emp_dept']
        exclude=['emp_efficiency']


class PerformForm(forms.ModelForm):
    class Meta:
        model=Performs
        fields='__all__'


class EmployeeSSNForm(forms.Form):
    emp_ssn = forms.CharField(label='Employee SSN', max_length=20)


class EmployeeSSNDateForm(forms.Form):
    emp_ssn = forms.CharField(label='Employee SSN', max_length=20)
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')


class ShiftSSNForm(forms.Form):
    shift_number=forms.CharField(label="Shift Number",max_length=20)


class ShiftSSNDateForm(forms.Form):
    shift_number = forms.CharField(label='Shift Number', max_length=20)
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')


class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['tool_code', 'tool_name', 'max_life_expectancy_in_mm', 'cost', 'length_cut_so_far']
        exclude=['no_of_brk_points','tool_efficiency']
       

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['part_no', 'component_name','tools']

    tools = forms.ModelMultipleChoiceField(
        queryset=Tool.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['machine_id', 'machine_name', 'part_no', 'tool_code']

    jobs = forms.ModelMultipleChoiceField(
        queryset=Job.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )


class ToolCodeForm(forms.Form):
    tool_code = forms.CharField(label='Tool Code', max_length=50)
