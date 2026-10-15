# Geometry and software notices

Derived geometry: © OpenStreetMap contributors, licensed under the Open Database License 1.0 (ODbL).

- https://www.openstreetmap.org/copyright
- https://opendatacommons.org/licenses/odbl/1-0/

The derived site.json database is distributed under ODbL 1.0. Preserve attribution and comply with its share-alike conditions for public use/distribution of an adapted database. The hypothetical tree proposals and provisional planting mask are additions to the OSM reference data, not assertions by OpenStreetMap contributors.

Sources retrieved 15 October 2026:

- https://www.openstreetmap.org/api/0.6/way/866543394/full
- https://www.openstreetmap.org/api/0.6/map?bbox=101.5096332,3.1762808,101.5188672,3.181746
- Park: way 866543394
- Water: ways 866518980 and 866543393
- Evaluated footway: way 909875974

Feature versions, timestamps, processing notes and context-footway IDs are in site.json provenance. Coordinates are WGS84 longitude/latitude. Buffer operations used UTM47N. The selected route is the longest dry line component inside the park. The planting mask is park inset 2 m, excluding mapped water with a 3 m buffer and mapped paths, buildings, playgrounds and pitches with 2 m buffers. Existing tree and seat inventories are absent.

This mapped park polygon is a pilot subset within City of Elmina, not a verified boundary of the entire 300-acre Central Park. Example proposed trees are a deterministic greedy four-tree example for one timestamp, not a globally optimal or approved planting plan.

Leaflet.GoogleMutant.js: version 0.16.0, Iván Sánchez Ortega. Source: https://gitlab.com/IvanSanchez/Leaflet.GridLayer.GoogleMutant . License retained alongside the script. Package: https://registry.npmjs.org/leaflet.gridlayer.googlemutant/-/leaflet.gridlayer.googlemutant-0.16.0.tgz

Google satellite imagery is loaded at runtime through Google Maps JavaScript API and remains subject to Google's terms. No imagery is bundled, downloaded for redistribution, or represented as EcoCool-owned data.
