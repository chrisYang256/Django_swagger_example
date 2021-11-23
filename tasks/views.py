import json

from datetime     import datetime, timedelta

from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi

from .serializers import TaskPostSerializer, TaskListQuerySerializer, TaskSearchSerializer

from django.db.models import Q
from django.http      import JsonResponse
from django.db        import transaction

from tasks.models          import *

class TaskView(APIView):

    # request_body는 해당 serializer에서 설정한 내용을 swagger에서 보이고 Try it out 버튼으로 보낼 수 있게 해줌.
    @swagger_auto_schema(tags=['데이터를 생성합니다.'], request_body=TaskPostSerializer)
    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            type        = Type.objects.create(name = data['type'])
            scope       = Scope.objects.create(name = data['scope'])
            institute   = Institute.objects.create(name = data['institute'])
            trial_stage = TrialStage.objects.create(name = data['trialStage'])
            department  = Department.objects.create(name = data['department'])

            Task.objects.create(
                number           = data['number'],
                title            = data['title'],
                duration         = data['duration'],
                number_of_target = data['number_of_target'],
                department_id    = department.id,
                institute_id     = institute.id,
                type_id          = type.id,
                trial_stage_id   = trial_stage.id,
                scope_id         = scope.id
            )

            return JsonResponse({'message' : 'CREATE_SUCCESS'}, status = 201)
        
        except Task.DoesNotExist:
            return JsonResponse({'message' : 'TASK_DOES_NOT_EXIST'}, status = 400)

class TaskSearchView(APIView):

    # query_serializer는 해당 serializer에서 설정한 내용을 swagger에서 인풋값으로 받을 수 있게 해줌
    @swagger_auto_schema(tags=['데이터를 검색합니다.'], query_serializer=TaskSearchSerializer, responses={200: 'Success'})
    def get(self, request):
        try:
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 10))

            title       = request.GET.get('title', None)
            department  = request.GET.get('department', None)
            institute   = request.GET.get('institute', None)
            type        = request.GET.get('type', None)
            trial_stage = request.GET.get('trial_stage', None)
            scope       = request.GET.get('scope', None)

            q = Q()

            if title:
                q.add(Q(title__icontains=title), q.AND)

            if department:
                q.add(Q(department__name__iexact=department), q.AND)

            if institute:
                q.add(Q(institute__name__contains=institute), q.AND)

            if type:
                q.add(Q(type__name=type), q.AND)

            if trial_stage:
                q.add(Q(trial_stage__name__iexact=trial_stage), q.AND)

            if scope:
                q.add(Q(scope__name=scope), q.AND)

            tasks = Task.objects.select_related('department', 'institute', 'type', 'trial_stage', 'scope')\
                                .filter(q)\
                                .order_by('updated_at')[offset:offset+limit]

            result = {
                'count' : len(tasks),
                'data'  : [{
                    'number'           : task.number,
                    'title'            : task.title,
                    'department'       : task.department.name if task.department else '',
                    'institute'        : task.institute.name if task.institute else '',
                    'number_of_target' : task.number_of_target,
                    'duration'         : task.duration,
                    'type'             : task.type.name if task.type else '',
                    'trial_stage'      : task.trial_stage.name if task.trial_stage else '',
                    'scope'            : task.scope.name if task.scope else ''
                } for task in tasks]
            }

            return JsonResponse(result, status=200)

        except TypeError:
            return JsonResponse({'message' : 'TYPE_ERROR'}, status=400)
        
        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status = 400)
        
class TaskDetailView(APIView):

    task_id = openapi.Parameter('task_id', openapi.IN_PATH, required=True, type=openapi.TYPE_NUMBER)

    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 불러옵니다.'], manual_parameters=[task_id], responses={200: 'Success'})
    def get(self, request, task_id):
        try:
            task = Task.objects.select_related(
                'type',
                'institute', 
                'department', 
                'trial_stage',
                'scope'
                ).get(id=task_id)
            
            task_info = {
                "number"           : task.number,
                "title"            : task.title,
                "duration"         : task.duration,
                "number_of_target" : task.number_of_target,
                "scope"            : task.scope.name if task.scope else '',
                "type"             : task.type.name if task.type else '',
                "institute"        : task.institute.name if task.institute else '',
                "trial_stages"     : task.trial_stage.name if task.trial_stage else '',
                "department"       : task.department.name if task.department else '',
                "created_at"       : task.created_at,
                "updated_at"       : task.updated_at
            }

            return JsonResponse({'message' : 'SUCCESS', 'task_info' : task_info}, status = 200)
        
        except Task.DoesNotExist:
            return JsonResponse({'message' : 'TASK_DOES_NOT_EXIST'}, status = 400)

class TaskUpdateListView(APIView):
    
    @swagger_auto_schema(
        tags=['최근 7일간 업데이트된 데이터들을 불러옵니다.'],
        query_serializer=TaskListQuerySerializer, 
        responses={200: 'Success'}
    )
    def get(self, request):
        try:
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 10))
            now    = datetime.now()

            one_week_list = Task.objects.select_related(
                'trial_stage', 
                'department', 
                'institute', 
                'scope',
                'type'
                ).filter(updated_at__range=[now - timedelta(days=7), now])[offset:offset+limit]

            data = [{
                'title'            : value.title,
                'number'           : value.number,
                'duration'         : value.duration,
                'number_of_target' : value.number_of_target,
                'trial_stage'      : value.trial_stage.name if value.trial_stage else '',
                'department'       : value.department.name if value.department else '',
                'institute'        : value.institute.name if value.institute else '',
                'scope'            : value.scope.name if value.scope else '',
                'type'             : value.type.name if value.type else ''
            } for value in one_week_list]

            return JsonResponse({'data' : data}, status=200)

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)