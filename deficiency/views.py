from rest_framework import generics, permissions, filters

from core.paginate import ExtraSmallResultsSetPagination
from .models import Deficiency, DeficiencyFavorite, DeficiencySymptom
from .serializers import DeficiencyFavoriteSerializer, DeficiencySerializers, DeficiencyDetailSerializers, DeficiencyFavoriteListSerializer

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


class DeficiencyFavoriteListView(generics.ListAPIView):
    serializer_class = DeficiencyFavoriteListSerializer
    queryset = DeficiencyFavorite.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['deficiency__name',]
    
    def get_queryset(self):
        return self.queryset.filter(user_profile=self.request.user.profile)


class DeficiencyFavoriteCreateView(generics.CreateAPIView):
    serializer_class = DeficiencyFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class DeficiencyFavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = DeficiencyFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        deficiency = generics.get_object_or_404(Deficiency, id=self.kwargs['deficiency_id'])
        return generics.get_object_or_404(
            DeficiencyFavorite,
            deficiency=deficiency,
            user_profile=self.request.user.profile
        )