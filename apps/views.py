from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from apps.models import UserInfo, Student, Employee
from apps.serializers import EmployeeModelSerializer, EmployeeDeserializer


def user(request):
    if request.method == "GET":
        print("GET 查询")
        return HttpResponse("GET SUCCESS")
    elif request.method == "POST":
        print("POST 添加")
        return HttpResponse("POST SUCCESS")
    elif request.method == "PUT":
        print("PUT 修改")
        return HttpResponse("PUT SUCCESS")
    elif request.method == "DELETE":
        print("DELETE 删除")
        return HttpResponse("DELETE SUCCESS")
    return  HttpResponse(1)

class Userview(View):
    def get(self,request,*args,**kwargs):
        u_id=kwargs.get('pk')
        if u_id:
            user = UserInfo.objects.filter(pk=u_id).values("username", "password", "gender").first()
            if user:
                return JsonResponse({
                    "status": 200,
                    "message": "获取用户成功",
                    "results": user
                })
        else:
            users = list(UserInfo.objects.all().values("username", "password", "gender"))
            if users:
                return JsonResponse({
                    "status": 201,
                    "message": "获取用户列表成功",
                    "results": users
                })

        return JsonResponse({
            "status": 400,
            "message": "获取用户不存在",
            "results": "获取用户不存在"

        })

    def post(self, request, *args, **kwargs):
        print(request.POST)
        try:
            user_obj = UserInfo.objects.create(**request.POST.dict())
            print(user_obj)
            if user_obj:
                return JsonResponse({
                    "status": 200,
                    "message": "新增用户成功",
                    "results": {"username": user_obj.username, "gender": user_obj.gender}
                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "新增用户失败",
                })
        except:
            return JsonResponse({
                "status": 501,
                "message": "参数有误",
            })

    def put(self, request, *args, **kwargs):

        u_id = kwargs.get('pk')
        print(u_id)
        return HttpResponse('put')

    def delete(self, request, *args, **kwargs):
        u_id = kwargs.get('pk')
        if u_id:
            user = UserInfo.objects.get(pk=u_id).delete()
            if user:
                return JsonResponse({
                    "status": 200,
                    "message": "删除用户成功",
                    "results": ""
                })
        else:
            return JsonResponse({
                "status": 400,
                "message": "获取用户不存在",
                "results": "获取用户不存在"

        })

        # print('delete')
        # return HttpResponse('delete')



class StudentView(APIView):
    # renderer_classes = [JSONRenderer]
    # parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        u_id = kwargs.get('pk')
        if u_id:
            user = Student.objects.get(pk=u_id).values("studentname", "password", "gender").first()
            if user:
                return JsonResponse({
                    "status": 200,
                    "message": "获取用户成功",
                    "results": user
                })
        else:
            users = list(Student.objects.all().values("studentname", "password", "gender"))
            if users:
                return JsonResponse({
                    "status": 201,
                    "message": "获取用户列表成功",
                    "results": users
                })

        return JsonResponse({
            "status": 400,
            "message": "获取用户不存在",
            "results": "获取用户不存在"

        })

        # print(request._request.GET)  # 原生django request对象
        # print(request.GET)  # DRF request 对象
        # print(request.query_params)  # DRF 扩展的get请求参数
        # return Response("GET SUCCESS")

    def post(self, request, *args, **kwargs):
        try:
            user_obj = Student.objects.create(**request.data.dict())
            print(user_obj)
            if user_obj:
                return JsonResponse({
                    "status": 200,
                    "message": "新增用户成功",
                    "results": {"username": user_obj.studentname, "gender": user_obj.gender}
                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "新增用户失败",
                })
        except:
            return JsonResponse({
                "status": 501,
                "message": "参数有误",
            })
        # print(request._request.POST)  # 原生django的request对象
        # print(request.POST)           # DRF的request对象
        # print(request.data)           # DRF扩展的post请求参数
        #
        # return Response("POST SUCCESS")


class EmployeeAPIView(APIView):

    def get(self, request, *args, **kwargs):
        print(11111)
        emp_id = kwargs.get("id")
        if emp_id:
            try:
                emp_obj = Employee.objects.get(pk=emp_id)
                emp_ser = EmployeeModelSerializer(emp_obj).data
                return Response({
                    "status": 200,
                    "message": "用户查询成功",
                    "results": emp_ser,
                })
            except:
                return Response({
                    "status": 500,
                    "message": "用户不存在"
                })
        else:
            emp_list = Employee.objects.all()
            emp_ser = EmployeeModelSerializer(emp_list, many=True).data
            return Response({
                "status": 200,
                "message": "用户列表查询成功",
                "results": emp_ser,
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                "status": 500,
                "message": "数据有误"
            })
        deserializer = EmployeeDeserializer(data=request_data)
        if deserializer.is_valid():
            emp_obj = deserializer.save()
            print(emp_obj)
            return Response({
                "status": 200,
                "message": "用户创建成功",
                "results": EmployeeModelSerializer(emp_obj).data
            })
        else:
            return Response({
                "status": 500,
                "message": "用户创建失败",
                "results": deserializer.errors
            })