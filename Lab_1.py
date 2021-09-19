#### Lab 1 ####

buf_dist = 0.001

### Preprocessing ###

## Message
print('Preparing...')

## Ufa ##
layer_places_a = QgsProject.instance().mapLayersByName('places_a')[0]
query_ufa = 'name = \'Уфа\''
features_ufa = layer_places_a.getFeatures(QgsFeatureRequest().setFilterExpression(query_ufa))
layer_aoi_ufa = QgsVectorLayer('Polygon', 'AOI_Ufa', 'memory')
layer_aoi_ufa.dataProvider().addFeatures(features_ufa)

# Add layer to map
QgsProject.instance().addMapLayer(layer_aoi_ufa)

## Transport ##
layer_transport = QgsProject.instance().mapLayersByName('transport')[0]

# Clip
params = { 'INPUT': layer_transport.name(), 'OUTPUT' : 'memory:', 'OVERLAY' : layer_aoi_ufa.name() }
res = processing.run('qgis:clip', params)
layer_transport_cliped = QgsVectorLayer('Point', 'layer_transport_cliped', 'memory')
layer_transport_cliped.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_transport_cliped)

# Buffer
params = {'DISTANCE' : buf_dist, 'INPUT': layer_transport_cliped.name(), 'OUTPUT': 'memory:'}
res = processing.run('qgis:buffer', params)
layer_transport_buffer = QgsVectorLayer('Polygon', 'layer_transport_buffer', 'memory')
layer_transport_buffer.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_transport_buffer)

## Pois ##
layer_pois = QgsProject.instance().mapLayersByName('pois')[0]

# Filter
query_pois = 'fclass = \'supermarket\' or fclass = \'memorial\''
features_pois = layer_pois.getFeatures(QgsFeatureRequest().setFilterExpression(query_pois))
layer_pois_filtered = QgsVectorLayer('Point', 'pois_filtered', 'memory')
layer_pois_filtered.dataProvider().addFeatures(features_pois)
QgsProject.instance().addMapLayer(layer_pois_filtered)

# Clip
params = { 'INPUT': layer_pois_filtered.name(), 'OUTPUT' : 'memory:', 'OVERLAY' : layer_aoi_ufa.name() }
res = processing.run('qgis:clip', params)
layer_pois_cliped = QgsVectorLayer('Point', 'layer_pois_cliped', 'memory')
layer_pois_cliped.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_pois_cliped)

# Buffer
params = {'DISTANCE' : buf_dist, 'INPUT': layer_pois_cliped.name(), 'OUTPUT': 'memory:'}
res = processing.run('qgis:buffer', params)
layer_pois_buffer = QgsVectorLayer('Polygon', 'layer_pois_buffer', 'memory')
layer_pois_buffer.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_pois_buffer)

### Overlay functions ###

layer_a = layer_transport_buffer
layer_b = layer_pois_buffer

## Intersect

params = { 'INPUT': layer_a.name() , 'OUTPUT' : 'memory:', 'OVERLAY': layer_b.name() }
res = processing.run('qgis:intersection', params)
layer_intersect_a_b = QgsVectorLayer('Polygon', 'intersection', 'memory')
layer_intersect_a_b.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_intersect_a_b)

## Union

params = { 'INPUT': layer_a.name() , 'OUTPUT' : 'memory:', 'OVERLAY': layer_b.name() }
res = processing.run('qgis:union', params)
layer_union_a_b = QgsVectorLayer('Polygon', 'union', 'memory')
layer_union_a_b.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_union_a_b)

## Difference

params = { 'INPUT': layer_a.name() , 'OUTPUT' : 'memory:', 'OVERLAY': layer_b.name() }
res = processing.run('qgis:difference', params)
layer_difference_a_b = QgsVectorLayer('Polygon', 'difference', 'memory')
layer_difference_a_b.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_difference_a_b)

## Symmetric Difference

params = { 'INPUT': layer_a.name() , 'OUTPUT' : 'memory:', 'OVERLAY': layer_b.name() }
res = processing.run('qgis:symmetricaldifference', params)
layer_sym_difference_a_b = QgsVectorLayer('Polygon', 'symmetrical_difference', 'memory')
layer_sym_difference_a_b.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_sym_difference_a_b)

### Post-processing ###

## Delete temp layers
layers_id = [layer_transport_cliped.id(), layer_pois_filtered.id(), layer_pois_cliped.id()]
QgsProject.instance().removeMapLayers(layers_id)

## Message
print('Success!')
