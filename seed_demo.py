import json

from django.conf import settings
from planner.models import Project


def rectangle(west, south, east, north):
    return {
        "type": "Polygon",
        "coordinates": [[
            [west, south],
            [east, south],
            [east, north],
            [west, north],
            [west, south],
        ]],
    }


fixture_path = (
    settings.BASE_DIR / "contracts" / "request-v1.json"
)

with fixture_path.open(encoding="utf-8") as file:
    fixture = json.load(file)

planting_area = rectangle(
    101.4997, 3.0997,
    101.5013, 3.1007,
)

lake = rectangle(
    101.4998, 3.1003,
    101.5004, 3.1006,
)

site_data = {
    "site": fixture["site"],
    "default_timestamp": fixture["timestamp"],
    "path": fixture["path"],
    "seats": fixture["seats"],
    "existing_trees": [
        tree for tree in fixture["trees"]
        if tree["status"] == "existing"
    ],
    "planting_area": planting_area,
    "lake": lake,
    "source_note": (
        "Synthetic demonstration geometry. "
        "Not a verified Elmina survey. "
        "Tree dimensions are assumptions."
    ),
    "display_geojson": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"kind": "planting_area"},
                "geometry": planting_area,
            },
            {
                "type": "Feature",
                "properties": {"kind": "lake"},
                "geometry": lake,
            },
            {
                "type": "Feature",
                "properties": {"kind": "path"},
                "geometry": fixture["path"],
            },
        ],
    },
}

project, created = Project.objects.get_or_create(
    name="EcoCool Demonstration Park",
    defaults={
        "site_version": "synthetic-v1",
        "site_data": site_data,
    },
)

print(
    "Created project:" if created else "Project already exists:",
    project.id,
    project.name,
)