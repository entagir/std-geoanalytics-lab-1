# Geoanalytics. Laboratory work #1

## Beginning of work

Initial data for lab in QGIS.

![1](https://user-images.githubusercontent.com/64076597/133930381-dabf88ff-fa3a-41e6-b308-0ced547744c8.png)

## Preprocessing

Some operations for preparing data.

### Filtration

Copying a polygon with "name" attribute equal to "Уфа" to a new layer and adding it to the map.
```python
layer_places_a = QgsProject.instance().mapLayersByName('places_a')[0]
query_ufa = 'name = \'Уфа\''
features_ufa = layer_places_a.getFeatures(QgsFeatureRequest().setFilterExpression(query_ufa))
layer_aoi_ufa = QgsVectorLayer('Polygon', 'AOI_Ufa', 'memory')
layer_aoi_ufa.dataProvider().addFeatures(features_ufa)

# Add layer to map
QgsProject.instance().addMapLayer(layer_aoi_ufa)
```

### Clip

```python
## Transport
layer_transport = QgsProject.instance().mapLayersByName('transport')[0]

# Clip
params = { 'INPUT': layer_transport.name(), 'OUTPUT' : 'memory:', 'OVERLAY' : layer_aoi_ufa.name() }
res = processing.run('qgis:clip', params)
layer_transport_cliped = QgsVectorLayer('Point', 'layer_transport_cliped', 'memory')
layer_transport_cliped.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_transport_cliped)
```

### Buffer

```python
# Buffer
params = {'DISTANCE' : buf_dist, 'INPUT': layer_transport_cliped.name(), 'OUTPUT': 'memory:'}
res = processing.run('qgis:buffer', params)
layer_transport_buffer = QgsVectorLayer('Polygon', 'layer_transport_buffer', 'memory')
layer_transport_buffer.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_transport_buffer)
```

Preprocessing result.

![2](https://user-images.githubusercontent.com/64076597/133930600-0c3a2049-b185-47b3-a7c8-931cd13a79de.png)

## Overlay operations

### Intersection

```python
params = { 'INPUT': layer_a.name() , 'OUTPUT' : 'memory:', 'OVERLAY': layer_b.name() }
res = processing.run('qgis:intersection', params)
layer_intersect_a_b = QgsVectorLayer('Polygon', 'intersection', 'memory')
layer_intersect_a_b.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_intersect_a_b)
```

Result.

![3](https://user-images.githubusercontent.com/64076597/133932726-a4b58cb3-b471-4cd2-8844-44aac5d73e10.png)

### Union

```python
params = { 'INPUT': layer_a.name() , 'OUTPUT' : 'memory:', 'OVERLAY': layer_b.name() }
res = processing.run('qgis:union', params)
layer_union_a_b = QgsVectorLayer('Polygon', 'union', 'memory')
layer_union_a_b.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_union_a_b)
```

Result.

![4](https://user-images.githubusercontent.com/64076597/133932738-0b20338b-4897-4918-b87c-9409deaff1c6.png)

### Difference

```python
params = { 'INPUT': layer_a.name() , 'OUTPUT' : 'memory:', 'OVERLAY': layer_b.name() }
res = processing.run('qgis:difference', params)
layer_difference_a_b = QgsVectorLayer('Polygon', 'difference', 'memory')
layer_difference_a_b.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_difference_a_b)
```

Result.

![5](https://user-images.githubusercontent.com/64076597/133932745-d223d3e3-36e4-43a9-a667-140c2c2e118d.png)

### Symmetric difference

```python
params = { 'INPUT': layer_a.name() , 'OUTPUT' : 'memory:', 'OVERLAY': layer_b.name() }
res = processing.run('qgis:symmetricaldifference', params)
layer_sym_difference_a_b = QgsVectorLayer('Polygon', 'symmetrical_difference', 'memory')
layer_sym_difference_a_b.dataProvider().addFeatures(res['OUTPUT'].getFeatures())
QgsProject.instance().addMapLayer(layer_sym_difference_a_b)
```

Result.

![6](https://user-images.githubusercontent.com/64076597/133932764-2bf8baab-2062-480f-b978-78e7f5cd5357.png)

## Conclution

The complete source code and project is presented in this repository.
