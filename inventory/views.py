from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache

class ItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get_object(self):
        item_id = self.kwargs["pk"]
        cached_item = cache.get(f'item_{item_id}')
        if cached_item:
            return cached_item
        item = get_object_or_404(Item, pk=item_id)
        cache.set(f'item_{item_id}', item, timeout=3600)  # Cache item for 1 hour
        return item

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        cache.delete(f'item_{self.kwargs["pk"]}')
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
