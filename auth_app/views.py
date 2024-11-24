from rest_framework import viewsets
from .models import CustomUser,Module
from .serializers import UserSerializer,AdminUserSerializer,ModuleSerializer,UserLoginSerializer
from .permissions import IsAdminOrOwnModule
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework import status



class UserLoginApiView(APIView):
    def post(self, request):
        # Deserialize and validate input data
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            print(token,_)
            return Response({
                'user_id': user.user_id,
                'is_admin': user.is_admin,
                'username': user.username,
                'token': token.key,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            user = request.user
            print(user,"user")
            token = Token.objects.get(user=user)
            print(token,"token")
            token.delete()
            logout(request)
            return Response({"ok":True}) 
            # return Response
        except Token.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes=[IsAuthenticatedOrReadOnly]
    
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


# class ModuleViewSet(viewsets.ModelViewSet):
#     queryset = Module.objects.all()
#     serializer_class = ModuleSerializer
#     permission_classes=[IsAuthenticated,IsAdminOrOwnModule]

#     def get_queryset(self):
#         if  self.request.user.is_admin:
#             return Module.objects.all()
#         return Module.objects.filter(user=self.request.user)
    


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes=[IsAuthenticated,IsAdminOrOwnModule]

    def perform_create(self, serializer):
        name=serializer.validated_data.get('name')
        user_id=serializer.validated_data.get('user')
        price=serializer.validated_data.get('price')
        image_url=serializer.validated_data.get('image')
        description=serializer.validated_data.get('description')

        
        if not image_url:
            return Response({"error": "image_url not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user_id, name=name,image=image_url,price=price,description=description)

    def get_queryset(self):
        if  self.request.user.is_admin:
            return Module.objects.all()
        return Module.objects.filter(user=self.request.user)
    