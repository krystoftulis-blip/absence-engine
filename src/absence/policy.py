"""Policy loading: rules as versioned, reviewable data.

Why YAML files rather than code or a database:

1.  A policy change is a *legal* change. It has to be reviewed and signed off
    by someone who is not an engineer. A YAML diff is readable by a lawyer;
    a code diff or a database UPDATE is not.
2.  Every version carries `effective_from`, so a balance can be recomputed
    exactly as it stood on any past date. That is what makes an audit
    defensible after the rules have changed.
3.  Sub-national rules (Indian states, German Bundeslaender, Spanish regions,
    Swiss cantons) are expressed as *overrides* on the entity policy, so the
    common part is stated once and only the genuine differences are visible.
"""

from __future__ import annotations

import copy
import datetime as _dt
import os
from typing import Any, Dict, List, Optional

import yaml

POLICY_DIR_DEFAULT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "policies",
)


class PolicyError(RuntimeError):
    pass


def _as_date(value: Any) -> Optional[_dt.date]:
    if value is None:
        return None
    if isinstance(value, _dt.date):
        return value
    if isinstance(value, str):
        return _dt.date.fromisoformat(value)
    raise PolicyError(f"cannot read {value!r} as a date")


def _resolve_path(container: Any, segment: str) -> Any:
    """Follow one segment of a dotted override path.

    Lists of dicts are addressed by their `id` field, so an override can say
    `buckets.earned_leave.accrual.amount` instead of `buckets.0.accrual.amount`
    - stable even when the order of buckets changes.
    """
    if isinstance(container, dict):
        return container.get(segment)
    if isinstance(container, list):
        for item in container:
            if isinstance(item, dict) and item.get("id") == segment:
                return item
        if segment.isdigit() and int(segment) < len(container):
            return container[int(segment)]
    return None


def apply_override(root: Dict[str, Any], dotted: str, value: Any) -> None:
    segments = dotted.split(".")
    cursor: Any = root
    for seg in segments[:-1]:
        nxt = _resolve_path(cursor, seg)
        if nxt is None:
            raise PolicyError(f"override path '{dotted}' does not exist (at '{seg}')")
        cursor = nxt
    last = segments[-1]
    if isinstance(cursor, dict):
        cursor[last] = value
    else:
        raise PolicyError(f"override path '{dotted}' does not end at a mapping")


class Policy:
    """One entity's rules, already resolved for a given date and region."""

    def __init__(self, entity: Dict[str, Any], version: Dict[str, Any], region: Optional[str]):
        self.entity_id: str = entity["entity_id"]
        self.legal_entity: str = entity.get("legal_entity", entity["entity_id"])
        self.jurisdiction: str = entity["jurisdiction"]
        self.country_name: str = entity.get("country_name", entity["jurisdiction"])
        self.region: Optional[str] = region
        self.raw: Dict[str, Any] = version
        self.effective_from: _dt.date = _as_date(version["effective_from"])
        self.legal_basis: str = version.get("legal_basis", "")
        self.review_due: Optional[_dt.date] = _as_date(version.get("review_due"))
        self.reviewed_by: str = version.get("reviewed_by", "")
        self.source_file: str = entity.get("_source_file", "")

    # -- convenience accessors -------------------------------------------------
    @property
    def unit(self) -> str:
        return self.raw.get("unit", "days")

    @property
    def leave_year(self) -> Dict[str, Any]:
        return self.raw.get("leave_year", {"type": "calendar"})

    @property
    def buckets(self) -> List[Dict[str, Any]]:
        return self.raw.get("buckets", [])

    @property
    def rounding(self) -> str:
        return self.raw.get("rounding", "none")

    @property
    def holiday_calendar(self) -> Optional[str]:
        return self.raw.get("holiday_calendar")

    @property
    def sick_pay(self) -> Optional[Dict[str, Any]]:
        return self.raw.get("sick_pay")

    def describe(self) -> str:
        where = f"{self.country_name}"
        if self.region:
            where += f" / {self.region}"
        return f"{self.entity_id} ({self.legal_entity}, {where})"


class PolicyRepository:
    """All entity policies plus the entity registry."""

    def __init__(self, policy_dir: str = POLICY_DIR_DEFAULT):
        self.policy_dir = policy_dir
        self._entities: Dict[str, Dict[str, Any]] = {}
        self._registry: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        registry_path = os.path.join(self.policy_dir, "registry.yaml")
        if os.path.exists(registry_path):
            with open(registry_path, "r", encoding="utf-8") as fh:
                self._registry = yaml.safe_load(fh) or {}

        for name in sorted(os.listdir(self.policy_dir)):
            if not name.endswith((".yaml", ".yml")) or name.startswith("_"):
                continue
            if name == "registry.yaml":
                continue
            path = os.path.join(self.policy_dir, name)
            with open(path, "r", encoding="utf-8") as fh:
                doc = yaml.safe_load(fh)
            if not doc or "entity_id" not in doc:
                continue
            doc["_source_file"] = os.path.relpath(path, os.path.dirname(self.policy_dir))
            self._entities[doc["entity_id"]] = doc

    # -- registry --------------------------------------------------------------
    @property
    def registry_entries(self) -> List[Dict[str, Any]]:
        return self._registry.get("entities", [])

    def treatment_for(self, entity_id: str) -> str:
        for row in self.registry_entries:
            if row.get("entity_id") == entity_id:
                return row.get("treatment", "unclassified")
        return "unclassified"

    # -- policies --------------------------------------------------------------
    def entity_ids(self) -> List[str]:
        return sorted(self._entities)

    def get(self, entity_id: str, as_of: _dt.date, region: Optional[str] = None) -> Policy:
        if entity_id not in self._entities:
            raise PolicyError(
                f"no policy file for entity '{entity_id}'. "
                f"Known entities: {', '.join(self.entity_ids()) or '(none)'}"
            )
        entity = self._entities[entity_id]
        versions = sorted(entity.get("versions", []), key=lambda v: _as_date(v["effective_from"]))
        applicable = [v for v in versions if _as_date(v["effective_from"]) <= as_of]
        if not applicable:
            raise PolicyError(
                f"entity '{entity_id}' has no policy version effective on {as_of.isoformat()}"
            )
        version = copy.deepcopy(applicable[-1])

        regions = version.pop("regions", {}) or {}
        if region:
            if region not in regions:
                known = ", ".join(sorted(regions)) or "(none defined)"
                raise PolicyError(
                    f"entity '{entity_id}' has no rules for region '{region}'. Known: {known}"
                )
            for dotted, value in (regions[region].get("overrides") or {}).items():
                apply_override(version, dotted, value)
            version["_region_label"] = regions[region].get("label", region)
        elif regions and version.get("region_required", False):
            raise PolicyError(
                f"entity '{entity_id}' requires a work_region "
                f"(one of: {', '.join(sorted(regions))}) - rules differ by region"
            )

        return Policy(entity, version, region)

    def region_keys(self, entity_id: str, as_of: _dt.date) -> List[str]:
        """Region codes defined for the version in force on `as_of`."""
        entity = self._entities.get(entity_id, {})
        versions = sorted(entity.get("versions", []), key=lambda v: _as_date(v["effective_from"]))
        applicable = [v for v in versions if _as_date(v["effective_from"]) <= as_of]
        if not applicable:
            return []
        return sorted((applicable[-1].get("regions") or {}))

    def all_versions(self, entity_id: str) -> List[Dict[str, Any]]:
        return self._entities[entity_id].get("versions", [])
