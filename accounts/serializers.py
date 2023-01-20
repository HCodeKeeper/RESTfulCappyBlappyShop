from rest_framework.serializers import ModelSerializer, SlugRelatedField
from user_profiles.models import Profile, Telephone


class TelephoneSerializer(ModelSerializer):
    class Meta:
        model = Telephone
        fields = ['number']


class ProfileSerializer(ModelSerializer):
    telephone = TelephoneSerializer()

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.second_name = validated_data.get('second_name', instance.second_name)
        instance.email = validated_data.get('email', instance.email)
        instance.has_premium = validated_data.get('has_premium', instance.has_premium)

        self._handle_telephone_update(instance, validated_data)

        instance.save()
        return instance

    def _handle_telephone_update(self, instance, validated_data):
        number = validated_data['telephone']['number']
        if number:
            obj, is_created = Telephone.objects.update_or_create(id=instance.telephone_id,
                                                                 defaults={'number': number,
                                                                           'user_id': instance.user_id})
            if is_created:
                instance.telephone_id = obj.id

    class Meta:
        model = Profile
        fields = ['first_name', 'second_name', 'telephone', 'email', 'has_premium']
