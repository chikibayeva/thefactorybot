from rest_framework import serializers, validators, exceptions

from tg_bot import models as bot_models


class BaseChatTokenSerializer(serializers.ModelSerializer):
    token: str = serializers.CharField(
        min_length=10,
        max_length=50,
        required=True,
        validators=[
            validators.UniqueValidator(
               queryset=bot_models.UserChat.objects.all(),
               message="Token is used, please try different token.",
           )
       ]
    )


class CreateChatTokenSerializer(BaseChatTokenSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = bot_models.UserChat
        fields = ["token", "user_id"]

    def validate(self, data: dict) -> dict:
        request = self.context.get("request")
        if not request.user:
            raise exceptions.NotAuthenticated

        self.user_id = request.user.id
        user_chat = bot_models.UserChat.objects.filter(user_id=self.user_id)
        if user_chat:
            raise exceptions.ValidationError(
                {"token": "Token already exists, update token."}
            )

        return data

    def save(self, **kwargs):
        token = bot_models.UserChat.objects.create(
            user_id=self.user_id, token=self.validated_data['token']
        )
        return token


class GetChatTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = bot_models.UserChat
        fields = ["id", "token"]


class UpdateTokenSerializer(BaseChatTokenSerializer):
    class Meta:
        model = bot_models.UserChat
        fields = ["token"]

    def update(self, instance, validated_data):
        instance.token = validated_data['token']
        instance.save()
        return instance
