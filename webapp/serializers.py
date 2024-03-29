# serializers.py

from rest_framework import serializers
from .models import Employee2, Job, Tool, Breakdown, Machine, Performs, NewMachine, ToolChart


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee2
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'


class JobSerializer1(serializers.ModelSerializer):
    tools = serializers.PrimaryKeyRelatedField(many=True, queryset=Job.objects.all())

    class Meta:
        model = Job
        fields = '__all__'


class BreakdownSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breakdown
        fields = '__all__'


class PerformsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Performs
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Machine
        fields = '__all__'


class NMSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewMachine
        fields = '__all__'


class ChartS(serializers.ModelSerializer):
    class Meta:
        model = ToolChart
        fields = '__all__'
