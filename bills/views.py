import json
from datetime import datetime

from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bills.models import Bill, Сlients, Organisation, Service, ServiceBill
from bills.serializers import BillSerializer


class BillViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()
    filterset_fields = '__all__'

    def create(self, request, *args, **kwargs):
        for file in request.FILES.values():
            for idx, row in enumerate(file):
                if idx == 0:
                    continue
                try:
                    row = row.decode("utf-8").rstrip().split(',')
                    obj_client = Сlients.objects.get_or_create(name=row[0])[0]
                    obj_org = Organisation.objects.get_or_create(name=row[1])[0]
                    num = int(row[2])

                    if Bill.objects.filter(client_name__name=obj_client, client_org__name=obj_org, num=num):
                        raise Exception('Указан не уникальный номер счёта')

                    obj_bill = Bill.objects.get_or_create(
                        client_name=obj_client,
                        client_org=obj_org,
                        num=num,
                        sum=float(row[3]),
                        date=datetime.strptime(row[4], '%d.%m.%Y').date(),
                    )[0]

                    for service in row[5].split(';'):
                        obj_service = Service.objects.get_or_create(name=service)[0]
                        ServiceBill.objects.get_or_create(service=obj_service, bill=obj_bill)

                    print(obj_bill)

                except Exception as exp:
                    print(exp)
                    continue
        return Response(status=status.HTTP_201_CREATED)

    def filter_queryset(self, queryset):
        filters = json.loads(self.request.GET.get('filters', '[]'))
        for filter_data in filters:
            if filter_data['field'] == 'client_name':
                queryset = queryset.filter(client_name__name=filter_data['value'])
            elif filter_data['field'] == 'client_org':
                queryset = queryset.filter(client_org__name=filter_data['value'])
        return queryset
