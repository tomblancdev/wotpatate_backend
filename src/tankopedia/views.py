
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from .models import Tank
from .serializers import TankSerializer


from django_filters.rest_framework import DjangoFilterBackend

from utils.WOT_API import get_tanks


class TankViewSet(ReadOnlyModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    lookup_field = 'name'
    filterset_fields = [
        'nation__name',
        'tier',
        'type__name',
        'is_premium',
        'is_premium_igr',
        'is_gift',
        'is_wheeled'
    ]
    search_fields = ['name', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('user_tanks'):
            # filter only on user tanks
            pass
        if self.request.query_params.get('random'):
            print('random')
            queryset = queryset.order_by('?')
        return queryset


@api_view(['GET'])
@permission_classes([IsAdminUser, ])
def update_tankopedia(request):
    response = get_tanks()
    # return Response(response, status=status.HTTP_200_OK)
    returned_data = []
    if response['status'] == 'error':
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    data = response['data']
    for key, tank in data.items():
        # transform images to list of objects with url and name
        images = []
        for name, url in tank['images'].items():
            images.append({'name': name, 'url': url})
        tank['images'] = images
        tank['nation_name'] = tank.pop('nation')
        tank['type_name'] = tank.pop('type')
        # tank exists in database
        if Tank.objects.filter(tank_id=tank['tank_id']).exists():
            # update tank using serializer and data
            serializer = TankSerializer(
                Tank.objects.get(tank_id=tank['tank_id']), data=tank)
        else:
            # create tank using serializer and data
            serializer = TankSerializer(data=tank)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            returned_data.append({key: serializer.data})
        else:
            print(key, serializer.errors)
            returned_data.append({key: serializer.errors})
    return Response({'test': "ok"}, status=status.HTTP_200_OK)
