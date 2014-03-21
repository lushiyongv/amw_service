# coding=utf-8
from amway_customer_service.customer.models import CustomerInfo
from restless.models import serialize
from restless.views import Endpoint


class HelloWorld(Endpoint):
    def get(self, request, cid):
        name = request.params.get('name', 'World')
        customer_info = CustomerInfo.objects.get(pk=1)
        return {'message': 'Hello, %s! %s' % (name, cid), 'user': serialize(customer_info)}

    def post(self, request):
        name = request.params.get('name', 'World')
        return {'message': 'Hello, %s!' % name}


class SRUserView(Endpoint):

    def post(self, request):
        """
        提交注册新的SR，如果已经注册，返回该SR的 Follow Up type
        :param request:
        :return: 返回 Follow up types json
        """
        return

    def get(self, request, sr_id):

        """

        :param request:
        :param sr_id:
        :return: 返回 SR 的 follow up 的类型
        """
        return