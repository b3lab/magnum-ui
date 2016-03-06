/*
 * Copyright 2015 NEC Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function() {
  "use strict";

  angular
    .module('horizon.dashboard.containers.baymodels')
    .controller('BayModelDetailController', BayModelDetailController);

  BayModelDetailController.$inject = [
    '$scope',
    '$window',
    '$location',
    '$routeParams',
    'horizon.app.core.openstack-service-api.magnum',
    'horizon.app.core.openstack-service-api.glance',
    'horizon.dashboard.containers.baymodels.events',
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.dashboard.containers.baymodels.resourceType'
  ];

  function BayModelDetailController($scope, $window, $location, $routeParams, magnum, glance, events, registry, baymodelResourceType) {
    var ctrl = this;
    ctrl.baymodel = {};
    ctrl.image_uuid;
    ctrl.baymodelResource = registry.getResourceType(baymodelResourceType);

    var baymodelId = $routeParams.baymodelId;

    var deleteWatcher = $scope.$on(events.DELETE_SUCCESS, onDeleteSuccess);

    $scope.$on('$destroy', destroy);

    init();

    function init() {
      registry.initActions(baymodelResourceType, $scope);
      // Load the elements that are used in the overview.
      magnum.getBayModel(baymodelId).success(onGetBayModel);
    }

    function onGetBayModel(baymodel) {
      ctrl.baymodel = baymodel;
      ctrl.baymodel.id = baymodel.uuid;
      glance.getImages().success(onGetImages);
    }

    function onGetImages(images) {
      angular.forEach(images.items, function(image) {
        if (image.name === ctrl.baymodel.image_id) {
          ctrl.image_uuid = image.id;
        }
      });
    }

    function onDeleteSuccess(e, removedIds){
      $location.path('/project/baymodels');
    }

    function destroy() {
      deleteWatcher();
    }

  }
})();