from rest_framework import generics
from .models import Issue, Comment
from .serializers import IssueSerializer, CommentSerializer

# Issues
class IssueListCreateAPI(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class IssueDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

# Comments
class CommentListCreateAPI(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
