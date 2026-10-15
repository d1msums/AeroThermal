def simulate(payload):
    """
    Temporary integration placeholder.
    Jia replaces this function with her real calculation engine.
    """

    def empty_result():
        return {
            "path_shade_pct": None,
            "shaded_seats": None,
            "shadows": {
                "type": "FeatureCollection",
                "features": [],
            },
        }

    return {
        "schema_version": "ecocool.v1",
        "model_version": "placeholder-v1",
        "mode": "mock",
        "timestamp": payload["timestamp"],
        "baseline": empty_result(),
        "proposed": empty_result(),
        "delta_pp": None,
        "added_trees": sum(
            tree["status"] == "proposed"
            for tree in payload["trees"]
        ),
        "warnings": [
            "Simulation not connected. No shade calculations performed."
        ],
    }