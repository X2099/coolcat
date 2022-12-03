def jwt_response_payload_handler(token, user=None, request=None):
    """
    重写获取jwt载荷数据方法
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }
