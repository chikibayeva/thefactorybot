from drf_spectacular.utils import extend_schema

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tg_bot import models as bot_models

from . import serializers


class CreateChatTokenView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CreateChatTokenSerializer


class GetChatTokenView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.GetChatTokenSerializer

    def get(self, request):
        serializer = self.get_serializer(instance=request.user.chat)
        return Response(serializer.data, 200)


@extend_schema(methods=['PUT'], exclude=True)
class UpdateChatTokenView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateTokenSerializer
    queryset = bot_models.UserChat.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "chat_id"
