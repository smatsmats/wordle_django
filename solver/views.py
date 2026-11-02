import re

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from . import engine


def _run(params):
    getlist = params.getlist
    known = [params.get(f"p{i}", "") for i in range(1, 6)]
    notpos = [params.get(f"not{i}", "") for i in range(1, 6)]
    regex = params.get("regex") or None
    if regex and len(regex) > 200:
        raise ValueError("regex too long")
    return engine.solve(
        use_ww=params.get("dict", "ww") != "all",
        exclude=params.get("exclude", ""),
        include=params.get("include", ""),
        known=known,
        notpos=notpos,
        no_repeats=bool(params.get("no_repeats")),
        regex=regex,
    )


def index(request):
    ctx = {
        "form": request.GET,
        "positions": [
            {"i": i, "p": request.GET.get(f"p{i}", ""), "n": request.GET.get(f"not{i}", "")}
            for i in range(1, 6)
        ],
    }
    if request.GET:
        try:
            ctx["result"] = _run(request.GET)
        except (re.error, ValueError) as e:
            ctx["error"] = str(e)
    return render(request, "solver/index.html", ctx)


@require_GET
def api_solve(request):
    try:
        return JsonResponse(_run(request.GET))
    except (re.error, ValueError) as e:
        return JsonResponse({"error": str(e)}, status=400)


def healthz(request):
    return JsonResponse({"status": "ok"})
