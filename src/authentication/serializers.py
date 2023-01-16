from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    password: str = serializers.CharField(
        max_length=128, style={"input_type": "password"}, write_only=True
    )
    confirm_password: str = serializers.CharField(
        max_length=128, style={"input_type": "password"}, write_only=True
    )
    username: str = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Username is used, please try different username.",
            )
        ]
    )

    class Meta:
        model = User
        fields = ["id", "username", "password", "confirm_password"]

    def validate(self, data: dict) -> dict:
        password = data["password"]
        confirm_password = data["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        elif len(password) < 6:
            raise serializers.ValidationError(
                {"password": "Passwords value should be 6 or more characters."}
            )
        return data

    def save(self) -> User:
        user = User(username=self.validated_data["username"])
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username: str = serializers.CharField()
    password: str = serializers.CharField(
        max_length=128,
        write_only=True,
        style={"input_type": "password", "placeholder": "Password"},
    )
    token: str = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Token
        fields = ["token", "username", "password"]

    def validate(self, data: dict) -> dict:
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None:
            raise serializers.ValidationError("username is required")

        if password is None:
            raise serializers.ValidationError("password is required")

        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("user not found")

        if not self.user.check_password(password):
            raise serializers.ValidationError("wrong password")

        token = Token.objects.get_or_create(user=self.user)[0]

        return {"username": username, "token": token}
