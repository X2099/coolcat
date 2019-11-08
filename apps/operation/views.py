from rest_framework.viewsets import ModelViewSet

from operation.models import LeavingMessage
from operation.serializers import LeavingMsgSerializer


class LeavingMsgViewSet(ModelViewSet):
    """留言"""

    serializer_class = LeavingMsgSerializer
    queryset = LeavingMessage.objects.all().order_by('-create_time')

    def get_authenticators(self):
        """
        根据不同的请求方式获取不同的认证权限
        """
        if self.request.method == 'GET':
            return []
        else:
            return [auth() for auth in self.authentication_classes]

    def get_permissions(self):
        """
        根据不同的请求方式获取不同的认证权限
        """
        if self.action == 'list' or self.action == 'retrieve':
            return []
        else:
            return [permission() for permission in self.permission_classes]
