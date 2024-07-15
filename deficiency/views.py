from rest_framework import generics, permissions, filters

from core.paginate import ExtraSmallResultsSetPagination
from .models import Deficiency, DeficiencySymptom
from .serializers import DeficiencySerializers, DeficiencyDetailSerializers

class DeficiencyListView(generics.ListAPIView):
    serializer_class = DeficiencySerializers
    queryset = Deficiency.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class DeficiencyDetailView(generics.RetrieveAPIView):
    serializer_class = DeficiencyDetailSerializers
    queryset = Deficiency.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    