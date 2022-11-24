from rest_framework import serializers

from bills.models import *


class СlientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Сlients
        fields = ('name',)


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('name',)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name',)


class ServiceBillSerializer(serializers.ModelSerializer):
    service = serializers.StringRelatedField(
        source='service.name', read_only=True
    )

    class Meta:
        model = ServiceBill
        fields = ('service',)


class BillSerializer(serializers.ModelSerializer):
    client_name = serializers.StringRelatedField(
        source='client_name.name', read_only=True
    )
    client_org = serializers.StringRelatedField(
        source='client_org.name', read_only=True
    )
    services = serializers.SerializerMethodField()

    @staticmethod
    def get_services(obj):
        return [ServiceBillSerializer(service).data['service'] for service in obj.services.all()]

    class Meta:
        model = Bill
        fields = '__all__'
