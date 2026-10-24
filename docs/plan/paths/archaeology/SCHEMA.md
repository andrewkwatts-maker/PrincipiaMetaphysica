# Catalogue entry schema (one JSON object per line in <your>.jsonl)

{
 "id": "kebab-case unique id, prefixed by your lane (a1-/a2-/a3-)",
 "kind": "theory_version | fork_option | mechanism | numeric_route",
 "title": "short human name",
 "fork_question": "the question this is one answer to (e.g. 'bulk dimension and signature', 'origin of b3', 'how n_gen is derived')",
 "answer": "this branch's answer to that question, one line",
 "era": "YYYY-MM-DD..YYYY-MM-DD (first seen..last live)",
 "version_label": "e.g. v16, v22.3 or null",
 "status_then": "adopted | considered | abandoned",
 "status_now": "active | considered | retired | rejected | unknown",
 "why": "why adopted / rejected / superseded; quote the source (<=40 words) when one exists",
 "what_worked": ["..."],
 "what_failed": ["..."],
 "key_results": [{"quantity": "...", "value": "...", "source": "sha:path or doc#section"}],
 "evidence": ["sha (short) + path, or document + section/page"],
 "maps_to_fork": "existing fork_id/option_id from current_forks.md, or null if no switch exists",
 "runnable_source": "sha:path of the last code that implemented it, or null"
}

Rules: never invent a number, citation or reason; if a value or reason is not in a source, leave it out.
Prefer one entry per distinct answer to a fork question; merge duplicates.
Do not read or print credential/service-account files.
