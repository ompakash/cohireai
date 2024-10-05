from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import *

User = get_user_model()

class SignupUser(APIView):
    def post(self, request):
        with transaction.atomic():
            email = request.data.get("email")
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
