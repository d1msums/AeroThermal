import json
import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from simulation.engine import simulate

from .models import AuditEvent, Membership, Scenario
from .services import build_payload


logger = logging.getLogger(__name__)


@login_required
def home(request):
    memberships = (
        Membership.objects
        .filter(user=request.user)
        .select_related("project")
    )

    return render(
        request,
        "planner/home.html",
        {"memberships": memberships},
    )


@login_required
def dashboard(request, project_id):
    membership = get_object_or_404(
        Membership.objects.select_related("project"),
        user=request.user,
        project_id=project_id,
    )

    project = membership.project

    scenarios = list(
        Scenario.objects
        .filter(project=project)
        .select_related("created_by")
        .order_by("-created_at")[:20]
    )

    saved_layouts = [
        {
            "id": scenario.id,
            "name": scenario.name,
            "input": scenario.input_data,
            "site_version": scenario.site_version,
        }
        for scenario in scenarios
    ]

    events = (
        AuditEvent.objects
        .filter(project=project)
        .select_related("actor")
        .order_by("-created_at")[:20]
    )

    from resilience.visuals import page_data
    can_edit = membership.role == "planner"

    return render(
        request,
        "planner/dashboard.html",
        {
            "project": project,
            "site": project.site_data,
            "can_edit": can_edit,
            "membership": membership,
            "scenarios": scenarios,
            "saved_layouts": saved_layouts,
            "events": events,
            "visual_data": page_data(project, request.user, can_edit),
        },
    )


@require_POST
def run_action(request, project_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Your session expired. Please log in again."},
            status=401,
        )

    membership = (
        Membership.objects
        .select_related("project")
        .filter(user=request.user, project_id=project_id)
        .first()
    )

    if membership is None:
        return JsonResponse(
            {"error": "Project not found."},
            status=404,
        )

    if membership.role != "planner":
        return JsonResponse(
            {"error": "You have view-only access."},
            status=403,
        )

    if request.content_type != "application/json":
        return JsonResponse(
            {"error": "Expected JSON."},
            status=415,
        )

    if len(request.body) > 100_000:
        return JsonResponse(
            {"error": "Request is too large."},
            status=413,
        )

    project = membership.project

    try:
        submitted = json.loads(request.body)

        if not isinstance(submitted, dict):
            raise ValueError("The request must be a JSON object.")

        action = submitted.get("action")

        if action not in {"simulate", "save"}:
            raise ValueError("Unknown action.")

        name = submitted.get("name", "")

        if action == "save":
            if not isinstance(name, str) or not 1 <= len(name.strip()) <= 120:
                raise ValueError("Enter a scenario name of 1-120 characters.")

        payload = build_payload(project, submitted)
        result = simulate(payload)

        # Ensure the engine returned JSON-safe data.
        json.dumps(result, allow_nan=False)

    except (ValueError, UnicodeDecodeError) as error:
        return JsonResponse({"error": str(error)}, status=400)

    except Exception:
        logger.exception("Simulation failed")
        return JsonResponse(
            {"error": "The simulation failed. Check the server terminal."},
            status=500,
        )

    scenario_id = None

    if action == "save":
        with transaction.atomic():
            scenario = Scenario.objects.create(
                project=project,
                name=name.strip(),
                site_version=project.site_version,
                input_data=payload,
                result_data=result,
                created_by=request.user,
            )

            AuditEvent.objects.create(
                project=project,
                actor=request.user,
                action="scenario_created",
                details={
                    "scenario_id": scenario.id,
                    "scenario_name": scenario.name,
                    "mode": result["mode"],
                },
            )

        scenario_id = scenario.id

    return JsonResponse({
        "result": result,
        "scenario_id": scenario_id,
    })