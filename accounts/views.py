from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

class SignupUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        with transaction.atomic():
            email = request.data.get("email").lower()
            password = request.data.get("password")
            user_type = request.data.get("type")

            if not email or not password or not user_type:
                return Response({"error": "Email, password, and type are required."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return Response({"error": "User with this email already exists."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Create user
            try:
                user = User.objects.create_user(email=email, password=password)
                
                # Set the user type and additional fields
                if user_type == User.Types.EMPLOYEE:
                    user.type = [User.Types.EMPLOYEE]
                    user.save()
                    # Create related EmployeeAdditional model instance
                    EmployeeAdditional.objects.create(user=user, address=request.data.get("address", ""))
                elif user_type == User.Types.ORGANIZATION:
                    user.type = [User.Types.ORGANIZATION]
                    user.save()
                    # Create related OrganizationAdditional model instance
                    OrganizationAdditional.objects.create(
                        user=user, 
                        gst=request.data.get("gst", ""), 
                        organization_location=request.data.get("organization_location", "")
                    )
                else:
                    return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    "email": user.email,
                    "user_type": user.type,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate if email and password are provided
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfile(APIView):

    def get(self, request):
        user = request.user
        user_data = {
            'email': user.email,
            'name': user.name,
            'type': user.type,
        }

        if 'Employee' in user.type:
            emp_obj = Employee.objects.get(email = user.email)
            user_data['address'] = emp_obj.showAdditional.address
        if 'Organization' in user.type:
            emp_obj = Organization.objects.get(email = user.email)
            user_data['gst'] = emp_obj.showAdditional.gst
            user_data['organization_location'] = emp_obj.showAdditional.organization_location

        return Response(f"{user_data}", status=status.HTTP_200_OK)
