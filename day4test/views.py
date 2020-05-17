from rest_framework.response import Response
from rest_framework.views import APIView

from day4test import serializers
from apps.models import Book


class BookAPIVIew(APIView):

    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id)
                book_ser = serializers.BookModelSerializer(book_obj).data
                return Response({
                    "status": 200,
                    "message": "查询图书成功",
                    "results": book_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询图书不存在",
                })
        else:
            book_list = Book.objects.all()
            book_data = serializers.BookModelSerializer(book_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询图书列表成功",
                "results": book_data
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        # 反序列化的时候需要将参数赋值关键字 data
        book_ser = serializers.BookModelDeSerializer(data=request_data)
        # 校验数据是否合法
        # raise_exception=True: 当校验失败的时候，马上终止当前视图方法，抛出异常到前台
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": 200,
            "message": "success",
            "results": serializers.BookModelSerializer(book_obj).data
        })


class BookAPIVIew2(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")        # 想要同时查询图书对应出版社的信息
        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id)
                book_ser = serializers.BookModelSerializer(book_obj).data
                return Response({
                    "status": 200,
                    "message": "查询图书成功",
                    "results": book_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询图书不存在",
                })
        else:
            book_list = Book.objects.all()
            book_data = serializers.BookModelSerializer(book_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询图书列表成功",
                "results": book_data
            })


class BookAPIVIewV2(APIView):

    # 查询单个  查询多个  增加单个  增加多个 删除单个  删除多个  局部修改单个 整体修改单个

    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id, is_delete=False)
                book_ser = serializers.BookModelSerializerV2(book_obj).data
                return Response({
                    "status": 200,
                    "message": "查询图书成功",
                    "results": book_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询图书不存在",
                })
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_data = serializers.BookModelSerializerV2(book_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询图书列表成功",
                "results": book_data
            })

    def post(self, request, *args, **kwargs):
        """
        单增：传的数据是与model类对应的一个字典
        群增：[ {} {} {} ]  群增的时候可以传递列表里面嵌套与model类对应的多个字典来完成群增
        """
        request_data = request.data

        if isinstance(request_data, dict):
            book_ser = serializers.BookModelSerializerV2(data=request_data) # 单增
            many = False
        elif isinstance(request_data, list):
            book_ser = serializers.BookModelSerializerV2(data=request_data, many=True)  # 群增
            many = True
        else:
            return Response({
                "status": 200,
                "message": "数据格式有误",
            })

        book_ser = serializers.BookModelSerializerV2(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": 200,
            "message": "success",
            "results": serializers.BookModelSerializerV2(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        """
        删除单个以及删除多个
        :param request: 请求的DRF对象
        # 单个删除：  有id  且是通过路径传参  v2/books/1/
        # 多个删除： 有多个id json传参 {"ids": [1,2,3]}
        """
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]   # 单删
        else:
            ids = request.data.get("ids")# 群删
        res = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)   # 判断id是否图书存在 且未删除
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
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id, is_delete=False)  # 通过获取的id来找到要修改的对象
        except:
            return Response({
                "status": 500,
                "message": "图书不存在",
            })
        # 前台提供了需要更新的数据request_data 数据更新需要校验
        # 更新数据时需要将参数赋值给data  方便钩子函数校验
        # 如果是修改操作，需要在序列化器中指定要修改的实例，否则将默认添加
        book_ser = serializers.BookModelSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()     # 如果校验通过 则保存

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.BookModelSerializerV2(book_obj).data
        })

    # def patch(self, request, *args, **kwargs):
    #     """
    #     单局部改：修改一个对象的任意字段
    #     修改的字段不同
    #     """
    #
    #     request_data = request.data
    #     book_id = kwargs.get("id")
    #
    #     try:
    #         book_obj = Book.objects.get(pk=book_id, is_delete=False)
    #     except:
    #         return Response({
    #             "status": 500,
    #             "message": "图书不存在",
    #         })
    #     # partial=True  指定序列化器为更新部分字段  有哪个字段的值就修改哪个字段  没有不修改
    #     book_ser = serializers.BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     book_ser.is_valid(raise_exception=True)
    #     book_ser.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": "更新成功",
    #         "results": serializers.BookModelSerializerV2(book_obj).data
    #     })

    def patch(self, request, *args, **kwargs):

        request_data = request.data
        book_id = kwargs.get("id")

        if book_id and isinstance(request_data, dict):
            book_ids = [book_id, ]
            request_data = [request_data, ]
        elif not book_id and isinstance(request_data, list):
            book_ids = []
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": 500,
                        "message": "ID不存在"
                    })
        else:
            return Response({
                "status": 500,
                "message": "数据不存或格式有误"
            })

        book_list = []
        # 不要循环中对列表的长度做操作!!!!!!!!
        new_data = []
        for index, pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
            except:
                continue

        book_ser = serializers.BookModelSerializerV2(data=new_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.BookModelSerializerV2(book_list, many=True).data
        })

