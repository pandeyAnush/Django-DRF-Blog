from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from .models import Blog
from django.db.models import Q


# public view API
class PublicView(APIView):

    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')

            # Apply search if search query is present
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            # Apply pagination
            page_number = request.GET.get('page', 1)  # Default to page 1
            paginator = Paginator(blogs, 5)  # 5 blogs per page

            # Serialize paginated blogs
            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response({
                'data': serializer.data,
                'message': 'Blogs fetched successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)  # Log the error for debugging purposes
            return Response({
                'message': 'Something went wrong',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class PublicBlogView(APIView):

    def get(self, request):
        try:
            # Fetch all blogs
            blogs = Blog.objects.all().order_by('?') 

            # Apply search if search query is present
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            # Apply pagination
            page_number = request.GET.get('page', 1)  # Default to page 1
            paginator = Paginator(blogs, 5)  # 5 blogs per page

            # Serialize paginated blogs
            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response({
                'data': serializer.data,
                'message': 'Blogs fetched successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Something went wrong',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            blogs = Blog.objects.filter(user = request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))


            serializer = BlogSerializer(blogs, many = True)

            return Response({
                'data': serializer.data,
                'message': 'Blog has been fetched successfully'
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print (e)
            return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)


         
    def post(self, request):
        try:
            data = request.data
            print('######')
            print(request.data)
            print('######')
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'Blog has been created successfully'
            }, status=status.HTTP_201_CREATED)

            return Response()
        except Exception as e:
            print (e)
            return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message':'invalid blog uid'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if request.user !=blog[0].user:
                return Response({
                    'data':{},
                    'message': 'you are not authorized to this'
                }, status = status.HTTP_400_BAD_REQUEST)


            serializer = BlogSerializer(blog[0], data = data, partial = True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'Blog has been updated successfully'
            }, status=status.HTTP_201_CREATED)


        except Exception as e:
            print (e)
            return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message':'invalid blog uid'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if request.user !=blog[0].user:
                return Response({
                    'data':{},
                    'message': 'you are not authorized to Change any containt'
                }, status = status.HTTP_400_BAD_REQUEST)

            blog[0].delete()

            return Response({
                'data': {},
                'message': 'Blog has been deleted successfully'
            }, status=status.HTTP_201_CREATED)


        except Exception as e:
            print (e)
            return Response({
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)



