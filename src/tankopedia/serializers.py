from rest_framework import serializers
from .models import Nation, TankType, Tank, TankImage


class NationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = ('name', 'image')


class TankTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TankType
        fields = '__all__'


class TankImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TankImage
        fields = ('name', 'url')


class TankSerializer(serializers.ModelSerializer):
    nation = NationSerializer(read_only=True)
    nation_name = serializers.CharField(write_only=True)
    type = TankTypeSerializer(read_only=True)
    type_name = serializers.CharField(write_only=True)
    images = TankImageSerializer(many=True)

    class Meta:
        model = Tank
        fields = ('tank_id', 'name', 'description', 'tier', 'nation', 'type',
                  'is_premium', 'is_gift', 'is_premium_igr', 'is_wheeled',
                  'images', 'nation_name', 'type_name')

    def create(self, validated_data):
        print("CREATE")
        nation_name = validated_data.pop('nation_name')
        type_name = validated_data.pop('type_name')
        images_data = validated_data.pop('images')

        nation, _ = Nation.objects.get_or_create(name=nation_name)
        type, _ = TankType.objects.get_or_create(name=type_name)
        tank, _ = Tank.objects.get_or_create(
            nation=nation, type=type, **validated_data)

        for image_data in images_data:
            TankImage.objects.get_or_create(tank=tank, **image_data)

        return tank

    def update(self, instance, validated_data):
        print("UPDATE")
        nation_name = validated_data.pop('nation_name')
        type_name = validated_data.pop('type_name')
        images_data = validated_data.pop('images')

        nation, _ = Nation.objects.get_or_create(name=nation_name)
        type, _ = TankType.objects.get_or_create(
            name=type_name)
        tank, created = Tank.objects.get_or_create(
            nation=nation, type=type, **validated_data)

        for name, url in images_data:
            # check if image already exists
            image, image_created = TankImage.objects.get_or_create(
                tank=tank, name=name, url=url)
            # if image already exists update it with new url
            if not image_created:
                image.url = url
                image.save()

        return tank
