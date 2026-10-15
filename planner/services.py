import math
from datetime import datetime

from shapely.geometry import Point, shape


def numeric(value, field):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
    ):
        raise ValueError(f"{field} must be a finite number.")

    return float(value)


def build_payload(project, submitted):
    if not isinstance(submitted, dict):
        raise ValueError("The request must be a JSON object.")

    timestamp = submitted.get("timestamp")

    if not isinstance(timestamp, str):
        raise ValueError("Select a date and time.")

    try:
        parsed = datetime.fromisoformat(timestamp)
    except ValueError:
        raise ValueError("Invalid date and time.")

    if parsed.utcoffset() is None:
        raise ValueError("The timestamp must include its timezone.")

    trees = submitted.get("proposed_trees", [])

    if not isinstance(trees, list) or len(trees) > 100:
        raise ValueError("Submit a list of at most 100 proposed trees.")

    site = project.site_data
    existing = site["existing_trees"]

    if len(existing) + len(trees) > 200:
        raise ValueError("This prototype supports at most 200 total trees.")

    allowed_area = shape(site["planting_area"])
    lake = shape(site["lake"])

    ids = {tree["id"] for tree in existing}
    clean_trees = []

    for index, tree in enumerate(trees):
        prefix = f"Tree {index + 1}"

        if not isinstance(tree, dict):
            raise ValueError(f"{prefix} must be an object.")

        tree_id = tree.get("id")

        if (
            not isinstance(tree_id, str)
            or not tree_id.strip()
            or len(tree_id) > 100
            or tree_id in ids
        ):
            raise ValueError(f"{prefix} has an invalid or duplicate ID.")

        if tree.get("status") != "proposed":
            raise ValueError(f"{prefix} must have proposed status.")

        coordinates = tree.get("coordinates")

        if not isinstance(coordinates, list) or len(coordinates) != 2:
            raise ValueError(f"{prefix} needs longitude and latitude.")

        longitude = numeric(coordinates[0], f"{prefix} longitude")
        latitude = numeric(coordinates[1], f"{prefix} latitude")

        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            raise ValueError(f"{prefix} has invalid coordinates.")

        location = Point(longitude, latitude)

        if not allowed_area.covers(location) or lake.covers(location):
            raise ValueError(
                f"{prefix} must be inside the planting area "
                "and outside the lake."
            )

        radius = numeric(
            tree.get("canopy_radius_m"),
            f"{prefix} canopy radius",
        )

        height = numeric(
            tree.get("canopy_height_m"),
            f"{prefix} model canopy height",
        )

        if not 0.5 <= radius <= 15:
            raise ValueError(f"{prefix} radius must be 0.5-15 metres.")

        if not 1 <= height <= 30:
            raise ValueError(f"{prefix} canopy height must be 1-30 metres.")

        ids.add(tree_id)

        clean_trees.append({
            "id": tree_id,
            "status": "proposed",
            "coordinates": [longitude, latitude],
            "canopy_radius_m": radius,
            "canopy_height_m": height,
        })

    return {
        "schema_version": "ecocool.v1",
        "site": site["site"],
        "timestamp": parsed.isoformat(),
        "path": site["path"],
        "seats": site["seats"],
        "trees": existing + clean_trees,
    }