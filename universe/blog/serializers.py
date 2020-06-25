from rest_framework import serializers
from blog.models import Items, Viewers, SubViewers
from django.conf import settings

ACTIONS = settings.ACTIONS

class ItemSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Items
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        return Items.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.details = validated_data.get('details', instance.details)
        instance.likes = validated_data.get('likes ', instance.likes)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance

class ViewerSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Viewers
        fields = ["reference", "id", "comment", "likes", "created_at"]

    def get_likes(self, obj):
        return obj.likes.count()

    def  create(self, validated_data):
        return Viewers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('title', instance.title)
        instance.likes = validated_data.get('likes ', instance.likes)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance

class BlogSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only = True)
    content = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Items
        fields = ["id", "details", "likes", "repost_count", "view_count"]


class ActionBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    details = serializers.CharField(allow_blank=True, required = False)

    def validate_action(self, value):
        value = value.lower().strip()
        if value in ACTIONS:
            return value
        return serializers.ValidationError(status =400)




class SubViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubViewers
        fields = ["reference", "id", "comment", "likes", "created_at"]

    def  create(self, validated_data):
        return SubViewers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('title', instance.title)
        instance.likes = validated_data.get('likes ', instance.likes)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance
