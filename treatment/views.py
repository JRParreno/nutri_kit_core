from rest_framework import generics, permissions, filters

from core.paginate import ExtraSmallResultsSetPagination
from .models import Remedy
from .serializers import RemedyDeficiencySerializers, RemedySerializers

class RemedyListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = RemedySerializers
    queryset = Remedy.objects.all()
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    

class RemedyDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = RemedyDeficiencySerializers
    queryset = Remedy.objects.all()
