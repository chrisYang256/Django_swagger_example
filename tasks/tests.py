from django.test  import TestCase, Client

from tasks.models import *

client = Client()

class TasksTest(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_search_test(self):
        response = client.get("/tasks/search?title=한국인&department=cardiology")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
        {
            "count": 2,
            "data": [
                {
                "number": "C130012",
                "title": "한국인 유전성(가족성) 부정맥 질환 임상연구 네트워크 구축",
                "department": "Cardiology",
                "institute": "고려대안암병원",
                "number_of_target": "250",
                "duration": "8년",
                "type": "관찰연구",
                "trial_stage": "코호트",
                "scope": "국내다기관"
                },
                {
                "number": "C130002",
                "title": "한국인 유전성(가족성) 심근병증 유전자 발굴을 위한 임상자료 및 유전체자원 수집",
                "department": "Cardiology",
                "institute": "세브란스병원",
                "number_of_target": "250",
                "duration": "7개월",
                "type": "관찰연구",
                "trial_stage": "코호트",
                "scope": "국내다기관"
                }
            ]
            })
        
        # 알맞지 않은 값을 보낸 경우 400을 리턴합니다.
        response = client.get("/tasks/search?limit=xxx")
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(), {'messsage' : 'TYPE_ERROR'})
        
    def test_a_detail_get_success(self):
        
        response = client.get('/tasks/5')
        created_at = Task.objects.get(id=5).created_at
        updated_at = Task.objects.get(id=5).updated_at
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'message' : 'SUCCESS',
            'task_info' : {
                "number"           : "C140012",
                "title"            : "우울증 임상연구네트워크구축",
                "duration"         : "11개월",
                "scope"            : "국내다기관",
                "type"             : "관찰연구",
                "institute"        : "가톨릭대 여의도성모병원",
                "trial_stages"     : "코호트",
                "number_of_target" : "300",
                "department"       : "Psychiatry",
                "created_at"       : created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                "updated_at"       : updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
            }
        })
        
    def test_a_detail_get_task_does_not_exist(self):
        
        client = Client()
        response = client.get('/tasks/277')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            'message' : 'TASK_DOES_NOT_EXIST',
            
        })   

    def test_list_get_success(self):

        data = [
        {
            "title": "조직구증식증 임상연구 네트워크 구축 및 운영(HLH)",
            "number": "C130010",
            "duration": "3년",
            "number_of_target": "120",
            "trial_stage": "코호트",
            "department": "Pediatrics",
            "institute": "서울아산병원",
            "scope": "국내다기관",
            "type": "관찰연구"
        },
        {
            "title": "대한민국 쇼그렌 증후군 코호트 구축",
            "number": "C130011",
            "duration": "6년",
            "number_of_target": "500",
            "trial_stage": "코호트",
            "department": "Rheumatology",
            "institute": "가톨릭대 서울성모병원",
            "scope": "국내다기관",
            "type": "관찰연구"
        },
        {
            "title": "Lymphoma Study for Auto-PBSCT",
            "number": "C100002",
            "duration": "1년",
            "number_of_target": "",
            "trial_stage": "코호트",
            "department": "Hematology",
            "institute": "가톨릭대 서울성모병원",
            "scope": "단일기관",
            "type": "관찰연구"
        },
        {
            "title": "악성림프종의 임상양상과 항암 화학요법의 치료 성적 조사 및 예후 예측 지표 분석, retrospective study",
            "number": "C110007",
            "duration": "",
            "number_of_target": "200",
            "trial_stage": "Case-only",
            "department": "Hematology",
            "institute": "가톨릭대 서울성모병원",
            "scope": "단일기관",
            "type": "관찰연구"
        },
        {
            "title": "우울증 임상연구네트워크구축",
            "number": "C140012",
            "duration": "11개월",
            "number_of_target": "300",
            "trial_stage": "코호트",
            "department": "Psychiatry",
            "institute": "가톨릭대 여의도성모병원",
            "scope": "국내다기관",
            "type": "관찰연구"
        }
    ]

        response = client.get('/tasks/list?offset=0&limit=5', content_type="application/json")

        self.assertEqual(response.json(), {'data' : data})
        self.assertEqual(response.status_code, 201)