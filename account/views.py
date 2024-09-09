# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import RegisterSerializer, LoginSerializer
# from rest_framework import status



# class RegisterView(APIView):

#     def post(self, request):
#         try:
#             data = request.data

#             serializer = RegisterSerializer(data = data)

#             if not serializer.is_valid():
#                 return Response({
#                     'data': serializer.errors,
#                     'message': 'Something went wrong'
#                 }, status = status.HTTP_400_BAD_REQUEST)

#             serializer.save()
#             return Response({
#                 'data': {},
#                 'message': 'Your account has been created successfully'
#             }, status = status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({
#                 'data': {},
#                 'message': f'Something went wrong: {str(e)}'
#             }, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):

#     def post(self, request):
#         try:
#             data = request.data
#             serializer = LoginSerializer(data=data, context={'request': request})

#             if not serializer.is_valid():
#                 print("Serializer validation failed.")
#                 return Response({
#                     'data': serializer.errors,
#                     'message': 'Something went wrong'
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             response = serializer.get_jwt_token(serializer.validated_data)

#             return Response(response, status=status.HTTP_200_OK)
        
#         except Exception as e:
#             print(f"An exception occurred: {str(e)}")
#             return Response({
#                 'data': {},
#                 'message': f'Something went wrong: {str(e)}'
#             }, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data': {},
                'message': 'Your account has been created successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'data': {},
                'message': f'Something went wrong: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data, context={'request': request})

            if not serializer.is_valid():
                print("Serializer validation failed.")
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.validated_data)

            return Response(response, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
            return Response({
                'data': {},
                'message': f'Something went wrong: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
