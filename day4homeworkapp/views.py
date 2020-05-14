from rest_framework.response import Response
from rest_framework.views import APIView

from day4homeworkapp import serializers
from apps.models import Students,Classes


class StudentsAPIVIew(APIView):



    def get(self, request, *args, **kwargs):

        stu_id = kwargs.get("pk")


        if stu_id:
            try:
                stu_obj = Students.objects.get(pk=stu_id)
                stu_ser = serializers.StudentsModelSerializer(stu_obj).data
                return Response({
                    "status": 200,
                    "message": "查询学生成功",
                    "results": stu_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询学生不存在",
                })
        else:
            stu_list = Students.objects.filter()
            stu_data = serializers.StudentsModelSerializer(stu_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询学生列表成功",
                "results": stu_data
            })

    def post(self, request, *args, **kwargs):

        request_data = request.data

        if isinstance(request_data, dict):
            book_ser = serializers.StudentsModelSerializer(data=request_data)
            many = False
        elif isinstance(request_data, list):
            book_ser = serializers.StudentsModelSerializer(data=request_data, many=True)
            many = True
        else:
            return Response({
                "status": 200,
                "message": "数据格式有误",
            })

        book_ser = serializers.StudentsModelSerializer(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": 200,
            "message": "success",
            "results": serializers.StudentsModelSerializer(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        st_id = kwargs.get("pk")
        if st_id:
            ids = [st_id]
        else:
            ids = request.data.get("ids")
        res = Students.objects.filter(pk__in=ids).delete()
        if res:
            return Response({
                "status": 200,
                "message": "删除成功",
            })

        return Response({
            "status": 500,
            "message": "删除失败或者已删除",
        })

    def put(self, request, *args, **kwargs):
        """
        单整体改：修改一个对象的全部字段
        :param request:   获取修改对象的值
        :param kwargs:  需要知道我要修改哪个对象   获取修改对象的id
        :return:    更新后的对象
        """
        request_data = request.data
        st_id = kwargs.get("pk")

        try:
            st_obj = Students.objects.get(pk=st_id)
        except:
            return Response({
                "status": 500,
                "message": "学生不存在",
            })


        st_ser = serializers.StudentsModelSerializer(data=request_data, instance=st_obj, partial=False)
        st_ser.is_valid(raise_exception=True)
        st_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.StudentsModelSerializer(st_obj).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        st_id = kwargs.get("pk")
        try:
            st_obj = Students.objects.get(pk=st_id)
        except:
            return Response({
                "status": 500,
                "message": "学生不存在",
            })
        st_ser = serializers.StudentsModelSerializer(data=request_data, instance=st_obj, partial=True) # partial=True  指定序列化器为更新部分字段  有哪个字段的值就修改哪个字段  没有不修改
        st_ser.is_valid(raise_exception=True)
        st_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.StudentsModelSerializer(st_obj).data
        })

