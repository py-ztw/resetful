from rest_framework import serializers

from apps.models import Students,Classes




class StudentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ("st_name", "age", "st_id", "gender","classes")
        extra_kwargs = {
            "st_name": {
                "required": True,
                "min_length":2,
                "error_messages": {
                    "required": "学生名是必填的",
                    "min_length": "学生名长度不够"
                }
            },
            "st_id": {
                "required": True,
                "min_length": 12,
                "error_messages": {
                    "required": "学号名是必填的",
                    "min_length": "学生名长度必须为12位"
                }
            },
        }

    def validate_age(self, value):
        if  value >99:
            raise serializers.ValidationError("年龄异常")
        else:
            return value

    def validate(self, attrs):
        stid = attrs.get("st_id")
        print(stid)
        st_obj = Students.objects.filter(st_id=stid)
        if st_obj:
            raise serializers.ValidationError("学号重复")

        return attrs
