from rest_framework import viewsets
from .models import CustomUser,Module
from .serializers import UserSerializer,AdminUserSerializer,ModuleSerializer,UserLoginSerializer
from .permissions import NormalUser, AdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from rest_framework.response import Response
from rest_framework import status

class UserLoginApiView(APIView):
    def post(self, request):
        # Deserialize and validate input data
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
           
            return Response({
                'user_id': user.user_id,
                'is_admin': user.is_admin,
                'username': user.username,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            request.delete()  # Delete token to log out
            return Response(status=204)
        except:
            return Response({'error': 'Logout failed'}, status=400)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
      
        user_id = self.request.query_params.get('user_id')  # Retrieve `user_id` from query parameters
        print(user_id,"user_id")
        if user_id:
            return CustomUser.objects.filter(user_id=user_id)  # Filter by user_id
        return CustomUser.objects.all()  # Return all users if no user_id is provided


class AdminViewset(viewsets.ModelViewSet):
    serializer_class=AdminUserSerializer

    def get_queryset(self):
        if  self.request.user.is_admin:
            return CustomUser.objects.filter(is_admin=True)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        if  self.request.user.is_admin:
            return Module.objects.all()
        return Module.objects.filter(user=self.request.user)