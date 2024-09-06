from rest_framework import generics, permissions, filters

from core.paginate import ExtraSmallResultsSetPagination
from .models import Remedy, RemedyFavorite
from .serializers import RemedyDeficiencySerializers, RemedyFavoriteSerializer, RemedySerializers, RemedyFavoriteListSerializer

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


class RemedyFavoriteListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = RemedyFavoriteListSerializer
    queryset = RemedyFavorite.objects.all()
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['remedy__name',]

    def get_queryset(self):
        return self.queryset.filter(user_profile=self.request.user.profile)

class RemedyFavoriteCreateView(generics.CreateAPIView):
    serializer_class = RemedyFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class RemedyFavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = RemedyFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        remedy = generics.get_object_or_404(Remedy, id=self.kwargs['remedy_id'])
        return generics.get_object_or_404(
            RemedyFavorite,
            remedy=remedy,
            user_profile=self.request.user.profile
        )