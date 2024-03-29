from import_export import resources, fields
from .models import Employee2,Tool,Job

class Employee2Resource(resources.ModelResource):
    emp_ssn = fields.Field(attribute='emp_ssn', column_name='emp_ssn')
    emp_name = fields.Field(attribute='emp_name', column_name='emp_name')
    emp_designation = fields.Field(attribute='emp_designation', column_name='emp_designation')
    emp_shed = fields.Field(attribute='emp_shed', column_name='emp_shed')
    emp_dept = fields.Field(attribute='emp_dept', column_name='emp_dept')
    emp_efficiency=fields.Field(attribute='emp_efficiency',column_name='emp_efficiency')
   

    class Meta:
        model = Employee2
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['emp_ssn']  


class ToolResource(resources.ModelResource):
    tool_code = fields.Field(attribute='tool_code', column_name='tool_code')
    tool_name = fields.Field(attribute='tool_name', column_name='tool_name')
    max_life_expectancy_in_mm = fields.Field(attribute='max_life_expectancy_in_mm', column_name='max_life_expectancy_in_mm')
    cost = fields.Field(attribute='cost', column_name='cost')
    length_cut_so_far = fields.Field(attribute='length_cut_so_far', column_name='length_cut_so_far')
    no_of_brk_points=fields.Field(attribute='no_of_brk_points',column_name='no_of_brk_points')
    tool_efficiency=fields.Field(attribute='tool_efficiency',column_name="tool_efficiency")
   

    class Meta:
        model = Tool
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['tool_code']  
        


class JobResource(resources.ModelResource):
   
    part_no = fields.Field(attribute='part_no', column_name='part_no')
    component_name = fields.Field(attribute='component_name', column_name='component_name')
    depth_of_cut = fields.Field(attribute='depth_of_cut', column_name='depth_of_cut')
    no_of_holes= fields.Field(attribute='no_of_holes', column_name='no_of_holes')
    operation_no=fields.Field(attribute='operation_no',column_name='operation_no')
    tool_code = fields.Field(attribute='tool_code', column_name='tool_code')
    
   

    class Meta:
        model = Job
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['part_no']  
