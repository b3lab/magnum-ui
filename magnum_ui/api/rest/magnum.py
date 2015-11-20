#  Copyright 2015 Cisco Systems.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.views import generic

from magnum_ui.api import magnum

from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils


def change_to_id(obj):
    """Change key named 'uuid' to 'id'

    Magnum returns objects with a field called 'uuid' many of Horizons
    directives however expect objects to have a field called 'id'.
    """
    obj['id'] = obj.pop('uuid')
    return obj


@urls.register
class BayModel(generic.View):
    """API for retrieving a single baymodel
    """
    url_regex = r'containers/baymodels/(?P<baymodel_id>[^/]+)$'

    @rest_utils.ajax()
    def get(self, request, baymodel_id):
        """Get a specific baymodel
        """
        return magnum.baymodel_show(request, baymodel_id).to_dict()


@urls.register
class BayModels(generic.View):
    """API for Magnum BayModels
    """
    url_regex = r'containers/baymodels/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of the BayModels for a project.

        The returned result is an object with property 'items' and each
        item under this is a BayModel.
        """
        result = magnum.baymodel_list(request)
        return {'items': [change_to_id(n.to_dict()) for n in result]}

    @rest_utils.ajax(data_required=True)
    def delete(self, request):
        """Delete one or more BayModels by id.

        Returns HTTP 204 (no content) on successful deletion.
        """
        for baymodel_id in request.DATA:
            magnum.baymodel_delete(request, baymodel_id)

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a new BayModel.

        Returns the new BayModel object on success.
        """
        new_baymodel = magnum.baymodel_create(request, **request.DATA)
        return rest_utils.CreatedResponse(
            '/api/containers/baymodel/%s' % new_baymodel.uuid,
            new_baymodel.to_dict())


@urls.register
class Bays(generic.View):
    """API for Magnum Bays
    """
    url_regex = r'containers/bays/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of the Bays for a project.

        The returned result is an object with property 'items' and each
        item under this is a Bay.
        """
        result = magnum.bay_list(request)
        return {'items': [change_to_id(n.to_dict()) for n in result]}

    @rest_utils.ajax(data_required=True)
    def delete(self, request):
        """Delete one or more Bays by id.

        Returns HTTP 204 (no content) on successful deletion.
        """
        for bay_id in request.DATA:
            magnum.bay_delete(request, bay_id)

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a new Bay.

        Returns the new Bay object on success.
        """
        new_bay = magnum.bay_create(request, **request.DATA)
        return rest_utils.CreatedResponse(
            '/api/containers/bay/%s' % new_bay.uuid,
            new_bay.to_dict())


@urls.register
class Containers(generic.View):
    """API for Magnum Containers
    """
    url_regex = r'containers/containers/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of the Containers for a project.

        The returned result is an object with property 'items' and each
        item under this is a Container.
        """
        result = magnum.container_list(request)
        return {'items': [change_to_id(n.to_dict()) for n in result]}

    @rest_utils.ajax(data_required=True)
    def delete(self, request):
        """Delete one or more Containers by ID.

        Returns HTTP 204 (no content) on successful deletion.
        """
        for container_id in request.DATA:
            magnum.container_delete(request, container_id)

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a new Container.

        Returns the new Container object on success.
        """
        container = magnum.container_create(request, **request.DATA)
        return rest_utils.CreatedResponse(
            '/api/containers/container/%s' % container.uuid,
            container.to_dict())
