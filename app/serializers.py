from rest_framework import serializers
from .models import Mod, TexturePack, Modpack, World, Shader

class ModSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mod
        fields = '__all__'
class TexturePackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TexturePack
        fields = '__all__'

class ModpackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modpack
        fields = '__all__'
class WorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = '__all__'
class ShaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shader
        fields = '__all__'