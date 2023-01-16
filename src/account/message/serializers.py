from rest_framework import serializers

from account import models as account_models
from tg_bot.tasks import send_messages


class SendMessageSerializer(serializers.Serializer):
    message: str = serializers.CharField(required=True, max_length=20000, write_only=True)

    class Meta:
        model = account_models.Message

    def save(self, **kwargs):
        user = self.context.get("request").user
        messages = account_models.Message.objects.create_telegram_messages(
            message=self.validated_data['message'],
            user=user
        )
        send_messages.delay(user.id, [message.id for message in messages])

class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_models.Message
        fields = '__all__'
