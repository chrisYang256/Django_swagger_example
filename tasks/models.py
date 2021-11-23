from django.db   import models

from core.models import TimeStampModel

class Task(TimeStampModel):
    number           = models.CharField(max_length=100, unique=True)
    title            = models.CharField(max_length=300)
    duration         = models.CharField(max_length=100, blank=True)
    number_of_target = models.CharField(max_length=100, blank=True)
    department       = models.ForeignKey('Department', null=True, on_delete=models.SET_NULL)
    institute        = models.ForeignKey('Institute', null=True, on_delete=models.SET_NULL)
    type             = models.ForeignKey('Type', null=True, on_delete=models.SET_NULL)
    trial_stage      = models.ForeignKey('TrialStage', null=True, on_delete=models.SET_NULL)
    scope            = models.ForeignKey('Scope', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'tasks'

class Department(TimeStampModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'departments'

class Institute(TimeStampModel):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'institutes'

class Type(TimeStampModel):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'types'

class TrialStage(TimeStampModel):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'trial_stages'

class Scope(TimeStampModel):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'scopes'

    