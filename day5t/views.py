from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apps.models import Book
from day5t import serializers
from day5t.serializers import BookModelSerializer
from utils.response import MYResponse


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_list = Book.objects.filter(is_delete=False).all()
        book_ser = serializers.BookModelSerializer(book_list, many=True)
        book_data = book_ser.data

        return MYResponse(results=book_data)



class BookGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         GenericAPIView):
    queryset = Book.objects.filter(is_delete=False).all()
    serializer_class = BookModelSerializer
    # 可以指定单条查询的主键名称
    lookup_field = "id"

    # 多个
    # def get(self, request, *args, **kwargs):
    #     # book_list = Book.objects.filter(is_delete=False).all()
    #     book_list = self.get_queryset()
    #     # book_ser = serializers.BookModelSerializer(book_list, many=True)
    #     book_ser = self.get_serializer(book_list, many=True)
    #     book_data = book_ser.data
    #
    #     return MYResponse(results=book_data)

    #单个
    # def get(self, request, *args, **kwargs):
    #     # book_list = self.get_object()
    #     # book_ser = self.get_serializer(book_list)
    #     # book_data = book_ser.data
    #     #
    #     # return MYResponse(results=book_data)
    #     return self.retrieve(request, *args, **kwargs)

    # ListModelMixin提供了查询所有的逻辑
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # RetrieveModelMixin:查询单个
    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # ListModelMixin：self.list查询所有
    # RetrieveModelMixin：self.retrieve查询单个
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            response = self.retrieve(request, *args, **kwargs)
        else:
            response = self.list(request, *args, **kwargs)

        return MYResponse(results=response.data, data_message="查询成功")

    # 添加 CreateModelMixin完成对象的添加
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return MYResponse(results=response.data)

    # 单整体改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return MYResponse(results=response.data)

    # 更新单个局部
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return MYResponse(results=response.data)


class BookListCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer


# 视图集ViewSet
class BookGenericViewSet(RetrieveModelMixin,
                         ListModelMixin,
                         GenericViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer

    def my_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def my_obj(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def my_create(self, request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        return MYResponse(results="OK")

    # 删除某个书籍
    def my_destroy(self, request, *args, **kwargs):
        # 获取单个
        book_obj = self.get_object()
        print("book_obj", book_obj, type(book_obj))
        if not book_obj:
            return MYResponse(500, "删除失败")
        book_obj.is_delete = True
        book_obj.save()
        return MYResponse(200, "删除成功")


class BookExampleGenericViewSet(ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer




