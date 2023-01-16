from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account import models as account_models

from . import serializers


class SendMessageView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SendMessageSerializer


class MessageListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MessageListSerializer
    queryset = account_models.Message.objects.all()


    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.pk)
