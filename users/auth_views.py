from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """회원가입"""
    username = request.data.get('username')
    nickname = request.data.get('nickname')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not all([username, nickname, password]):
        return Response({
            'error': 'username, nickname, password는 필수입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 중복 체크
    if User.objects.filter(username=username).exists():
        return Response({
            'error': '이미 존재하는 사용자명입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(nickname=nickname).exists():
        return Response({
            'error': '이미 존재하는 닉네임입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.create_user(
            username=username,
            nickname=nickname,
            password=password,
            email=email
        )
        
        serializer = UserSerializer(user)
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'회원가입 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """로그인"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not all([username, password]):
        return Response({
            'error': 'username과 password는 필수입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            serializer = UserSerializer(user)
            return Response({
                'message': '로그인 성공',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': '비활성화된 계정입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'error': '사용자명 또는 비밀번호가 올바르지 않습니다.'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request):
    """로그아웃"""
    logout(request)
    return Response({
        'message': '로그아웃되었습니다.'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def me(request):
    """현재 로그인한 사용자 정보"""
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    else:
        return Response({
            'error': '로그인이 필요합니다.'
        }, status=status.HTTP_401_UNAUTHORIZED)
