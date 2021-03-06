import serpy
from .models import FormEntry
from rest_framework import serializers

class AcademySmallSerializer(serpy.Serializer):
    id = serpy.Field()
    slug = serpy.Field()
    name = serpy.Field()

class FormEntrySerializer(serpy.Serializer):
    id = serpy.Field()
    course = serpy.Field()
    location = serpy.Field()
    language = serpy.Field()
    utm_url = serpy.Field()
    utm_medium = serpy.Field()
    utm_campaign = serpy.Field()
    utm_source = serpy.Field()
    tags = serpy.Field()
    country = serpy.Field()
    lead_type = serpy.Field()
    academy = AcademySmallSerializer(required=False)
    created_at = serpy.Field()


class FormEntrySmallSerializer(serpy.Serializer):
    id = serpy.Field()
    course = serpy.Field()
    location = serpy.Field()
    language = serpy.Field()
    utm_url = serpy.Field()
    utm_medium = serpy.Field()
    utm_campaign = serpy.Field()
    utm_source = serpy.Field()
    tags = serpy.Field()
    storage_status = serpy.Field()
    country = serpy.Field()
    lead_type = serpy.Field()
    created_at = serpy.Field()

class PostFormEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FormEntry
        exclude = ()
