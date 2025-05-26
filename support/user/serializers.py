from rest_framework import serializers
from supportAPI.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'created_time', 'password', 'password2']
        read_only_fields = ['created_time']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        # Supprimer password2 car il n'est pas dans le modèle User
        validated_data.pop('password2')

        # Créer l'utilisateur
        user = User.objects.create(
            username=validated_data['username'],
            age=validated_data.get('age'),
            # Ajoutez d'autres champs si nécessaire
        )

        # Définir le mot de passe correctement (avec hachage)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        # Gestion du mot de passe lors de la mise à jour
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
