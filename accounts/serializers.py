from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import CustomUserModel
import re
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    token = serializers.CharField(read_only=True)
    username_display = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nick_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if user is None:
                raise serializers.ValidationError(_("ログインに失敗しました。"))
        else:
            raise serializers.ValidationError(_("両方のフィールドを入力してください。"))

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'user': user
        }
    

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = [
            'username',
            'email',
            'nick_name',
        ]


def validate_password(value):
    if len(value) < 8:
        raise  serializers.ValidationError('最低8文字でなければなりません')
    
    if len(value) > 129:
        raise  serializers.ValidationError('128文字以下でなければなりません')
    
    if not re.search(r'[a-zA-Z]', value):
        raise serializers.ValidationError('少なくとも1つの英字が必要です')
    
    if not re.search(r'\d', value):
        raise  serializers.ValidationError('少なくとも1つの数字が必要です')
    
    if not re.search(r'^[a-zA-Z0-9]*$', value):
        raise  serializers.ValidationError('半角英数字のみを入力してください')

class SignUpUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUserModel
        fields = [
            'username',
            'email',
            'nick_name',
            'password',
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUserModel(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
