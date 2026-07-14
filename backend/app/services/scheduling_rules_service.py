"""Scheduling Rules Service - loads and evaluates YAML-based scheduling rules."""
import ast
import logging
import math
import operator
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Callable, Optional

import yaml

logger = logging.getLogger(__name__)

FORMULA_ROOT_NAMES = {"effort", "assignee"}
FORMULA_ASSIGNEE_FIELDS = {"professionalism_coefficient", "operational_utilization"}
CONDITION_FIELDS = {
    "adjusted_effort",
    "fits_before_vacation",
    "is_deferred",
    "is_optional",
    "max_finish_date",
    "min_start_date",
    "priority",
}
CONDITION_PATTERN = re.compile(
    r"^task\.([A-Za-z_][A-Za-z0-9_]*)\s*"
    r"(==|!=|<=|>=|<|>)\s*"
    r"(null|true|false|-?\d+(?:\.\d+)?|'[^']*'|\"[^\"]*\")$",
    re.IGNORECASE,
)


@dataclass
class SortCriterion:
    """A single sort criterion."""
    field: str
    order: str = "asc"  # "asc" or "desc"


@dataclass
class SchedulingPass:
    """A scheduling pass with filter and sort rules."""
    id: str
    description: str
    filter_conditions: list[str]
    sort_criteria: list[SortCriterion]
    enabled: bool = True


@dataclass
class EffortModifier:
    """An effort modifier rule."""
    id: str
    enabled: bool
    formula: Optional[str] = None
    operation: Optional[str] = None  # "ceil", "floor", "round"
    fallback: str = "effort"
    min_value: Optional[float] = None


@dataclass
class Constraints:
    """Scheduling constraints."""
    sequential_per_assignee: bool = True
    respect_dependencies: bool = True
    min_start_date: bool = True
    max_finish_date: bool = True
    prefer_uninterrupted: bool = True
    balance_workload: Optional[dict] = None


@dataclass
class SchedulingRules:
    """Complete scheduling rules configuration."""
    schema_version: str
    effort_modifiers: list[EffortModifier]
    scheduling_passes: list[SchedulingPass]
    constraints: Constraints


class SchedulingRulesService:
    """Service for loading and evaluating scheduling rules from YAML."""

    _instance: "Optional[SchedulingRulesService]" = None
    _rules: Optional[SchedulingRules] = None

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the service.

        Args:
            config_path: Path to scheduling_rules.yaml. If None, uses default location.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "scheduling_rules.yaml"

        self.config_path = config_path
        self._load_rules()

    @classmethod
    def get_instance(cls, config_path: Optional[Path] = None) -> "SchedulingRulesService":
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls(config_path)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset singleton (for testing)."""
        cls._instance = None
        cls._rules = None

    def _load_rules(self) -> None:
        """Load rules from YAML file."""
        if not self.config_path.exists():
            logger.warning(f"Scheduling rules file not found: {self.config_path}. Using fallback.")
            self._rules = None
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            self._rules = self._parse_rules(data)
            logger.info(f"Loaded scheduling rules v{self._rules.schema_version} from {self.config_path}")
        except Exception:
            # Rules files are optional at startup; deterministic defaults remain safe.
            logger.error(
                "Failed to load scheduling rules; using fallback",
                exc_info=True,
                extra={"path": str(self.config_path)},
            )
            self._rules = None

    def _parse_rules(self, data: dict) -> SchedulingRules:
        """Parse YAML data into SchedulingRules."""
        # Parse effort modifiers
        modifiers = []
        for mod_data in data.get("effort_modifiers", []):
            modifiers.append(EffortModifier(
                id=mod_data["id"],
                enabled=mod_data.get("enabled", True),
                formula=mod_data.get("formula"),
                operation=mod_data.get("operation"),
                fallback=mod_data.get("fallback", "effort"),
                min_value=mod_data.get("min_value"),
            ))

        # Parse scheduling passes
        passes = []
        for pass_data in data.get("scheduling_passes", []):
            filter_data = pass_data.get("filter", {})
            filter_conditions = filter_data.get("all", [])

            sort_criteria = []
            for sort_data in pass_data.get("sort", []):
                sort_criteria.append(SortCriterion(
                    field=sort_data["field"],
                    order=sort_data.get("order", "asc"),
                ))

            passes.append(SchedulingPass(
                id=pass_data["id"],
                description=pass_data.get("description", ""),
                filter_conditions=filter_conditions,
                sort_criteria=sort_criteria,
                enabled=pass_data.get("enabled", True),
            ))

        # Parse constraints
        constraints_data = data.get("constraints", {})
        balance_workload = constraints_data.get("balance_workload")

        constraints = Constraints(
            sequential_per_assignee=constraints_data.get("sequential_per_assignee", True),
            respect_dependencies=constraints_data.get("respect_dependencies", True),
            min_start_date=constraints_data.get("min_start_date", True),
            max_finish_date=constraints_data.get("max_finish_date", True),
            prefer_uninterrupted=constraints_data.get("prefer_uninterrupted", True),
            balance_workload=balance_workload if isinstance(balance_workload, dict) else None,
        )

        rules = SchedulingRules(
            schema_version=data.get("schema_version", "1.0"),
            effort_modifiers=modifiers,
            scheduling_passes=passes,
            constraints=constraints,
        )
        self._validate_rules(rules)
        return rules

    @property
    def rules(self) -> Optional[SchedulingRules]:
        """Get loaded rules."""
        return self._rules

    @property
    def has_rules(self) -> bool:
        """Check if rules are loaded."""
        return self._rules is not None

    def get_constraints(self) -> Constraints:
        """Get constraints, with defaults if no rules loaded."""
        if self._rules:
            return self._rules.constraints
        return Constraints()

    def get_rules_as_dict(self) -> dict:
        """Convert current rules to API-friendly dictionary format."""
        if not self._rules:
            # Return defaults
            return self._get_default_rules_dict()

        return {
            "schema_version": self._rules.schema_version,
            "effort_modifiers": [
                {
                    "id": m.id,
                    "enabled": m.enabled,
                    "formula": m.formula,
                    "operation": m.operation,
                    "fallback": m.fallback,
                    "min_value": m.min_value,
                }
                for m in self._rules.effort_modifiers
            ],
            "scheduling_passes": [
                {
                    "id": p.id,
                    "description": p.description,
                    "enabled": p.enabled,
                    "filter": {"all": p.filter_conditions},
                    "sort": [
                        {"field": s.field, "order": s.order}
                        for s in p.sort_criteria
                    ],
                }
                for p in self._rules.scheduling_passes
            ],
            "constraints": {
                "sequential_per_assignee": self._rules.constraints.sequential_per_assignee,
                "respect_dependencies": self._rules.constraints.respect_dependencies,
                "min_start_date": self._rules.constraints.min_start_date,
                "max_finish_date": self._rules.constraints.max_finish_date,
                "prefer_uninterrupted": self._rules.constraints.prefer_uninterrupted,
                "balance_workload": self._rules.constraints.balance_workload,
            },
        }

    def _get_default_rules_dict(self) -> dict:
        """Get default rules configuration."""
        return {
            "schema_version": "1.0",
            "effort_modifiers": [
                {
                    "id": "professionalism",
                    "enabled": True,
                    "formula": "effort / assignee.professionalism_coefficient",
                    "operation": None,
                    "fallback": "effort",
                    "min_value": None,
                },
                {
                    "id": "operational_overhead",
                    "enabled": True,
                    "formula": "effort / (1 - assignee.operational_utilization / 100)",
                    "operation": None,
                    "fallback": "effort",
                    "min_value": None,
                },
                {
                    "id": "round_up",
                    "enabled": True,
                    "formula": None,
                    "operation": "ceil",
                    "fallback": "effort",
                    "min_value": 1,
                },
            ],
            "scheduling_passes": [
                {
                    "id": "critical_deadline",
                    "description": "Задачи с дедлайном — ближайший срок раньше",
                    "enabled": True,
                    "filter": {"all": [
                        "task.max_finish_date != null",
                        "task.is_deferred == false",
                    ]},
                    "sort": [
                        {"field": "max_finish_date", "order": "asc"},
                        {"field": "priority", "order": "asc"},
                    ],
                },
                {
                    "id": "before_vacation",
                    "description": "Задачи до отпуска",
                    "enabled": True,
                    "filter": {"all": [
                        "task.fits_before_vacation == true",
                        "task.is_deferred == false",
                    ]},
                    "sort": [
                        {"field": "is_optional", "order": "asc"},
                        {"field": "priority", "order": "asc"},
                        {"field": "adjusted_effort", "order": "asc"},
                    ],
                },
                {
                    "id": "after_vacation",
                    "description": "Задачи после отпуска",
                    "enabled": True,
                    "filter": {"all": [
                        "task.fits_before_vacation == false",
                        "task.is_deferred == false",
                    ]},
                    "sort": [
                        {"field": "is_optional", "order": "asc"},
                        {"field": "priority", "order": "asc"},
                        {"field": "adjusted_effort", "order": "desc"},
                    ],
                },
            ],
            "constraints": {
                "sequential_per_assignee": True,
                "respect_dependencies": True,
                "min_start_date": True,
                "max_finish_date": True,
                "prefer_uninterrupted": True,
                "balance_workload": None,
            },
        }

    def update_rules(self, data: dict) -> None:
        """Update rules from API data and save to YAML file.

        Args:
            data: Dictionary matching SchedulingRulesSchema structure

        Raises:
            ValueError: If data is invalid
        """
        # Convert API format to YAML format
        yaml_data = {
            "schema_version": data.get("schema_version", "1.0"),
            "effort_modifiers": [],
            "scheduling_passes": [],
            "constraints": {},
        }

        # Convert effort modifiers
        for mod in data.get("effort_modifiers", []):
            mod_entry = {"id": mod["id"], "enabled": mod.get("enabled", True)}
            if mod.get("formula"):
                mod_entry["formula"] = mod["formula"]
            if mod.get("operation"):
                mod_entry["operation"] = mod["operation"]
            if mod.get("fallback"):
                mod_entry["fallback"] = mod["fallback"]
            if mod.get("min_value") is not None:
                mod_entry["min_value"] = mod["min_value"]
            yaml_data["effort_modifiers"].append(mod_entry)

        # Convert scheduling passes
        for sp in data.get("scheduling_passes", []):
            pass_entry = {
                "id": sp["id"],
                "description": sp.get("description", ""),
            }
            if sp.get("filter"):
                pass_entry["filter"] = {"all": sp["filter"].get("all", [])}
            if sp.get("sort"):
                pass_entry["sort"] = [
                    {"field": s["field"], "order": s.get("order", "asc")}
                    for s in sp["sort"]
                ]
            yaml_data["scheduling_passes"].append(pass_entry)

        # Convert constraints
        constraints = data.get("constraints", {})
        yaml_data["constraints"] = {
            "sequential_per_assignee": constraints.get("sequential_per_assignee", True),
            "respect_dependencies": constraints.get("respect_dependencies", True),
            "min_start_date": constraints.get("min_start_date", True),
            "max_finish_date": constraints.get("max_finish_date", True),
            "prefer_uninterrupted": constraints.get("prefer_uninterrupted", True),
        }
        if constraints.get("balance_workload"):
            yaml_data["constraints"]["balance_workload"] = constraints["balance_workload"]

        # Validate the normalized YAML shape before it can reach disk.
        self._parse_rules(yaml_data)

        # Write to YAML file
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

            # Reload rules
            self._load_rules()

            # Clear formula cache
            if hasattr(self, '_formula_cache'):
                self._formula_cache.clear()

            logger.info(f"Updated scheduling rules in {self.config_path}")
        except Exception as exc:
            logger.error(
                "Failed to save scheduling rules",
                exc_info=True,
                extra={"path": str(self.config_path)},
            )
            raise ValueError(f"Failed to save rules: {exc}") from exc

    def _validate_rules(self, rules: SchedulingRules) -> None:
        """Validate user-editable rules before persistence or activation."""
        for modifier in rules.effort_modifiers:
            if modifier.formula:
                self._get_compiled_formula(modifier.formula)
            if modifier.fallback:
                self._get_compiled_formula(modifier.fallback)
        for scheduling_pass in rules.scheduling_passes:
            for condition in scheduling_pass.filter_conditions:
                self._parse_condition(condition)

    def reset_to_defaults(self) -> None:
        """Reset scheduling rules to default values."""
        default_data = self._get_default_rules_dict()
        self.update_rules(default_data)

    def calculate_adjusted_effort(
        self,
        base_effort: float,
        professionalism_coefficient: float = 1.0,
        operational_utilization: float = 0.0,
    ) -> int:
        """Calculate adjusted effort using configured modifiers.

        Falls back to hardcoded logic if no rules loaded.
        """
        if not self._rules:
            # Fallback to original hardcoded logic
            adjusted = base_effort / professionalism_coefficient if professionalism_coefficient > 0 else base_effort
            adjusted = adjusted / (1 - operational_utilization / 100) if operational_utilization < 100 else adjusted
            return max(1, math.ceil(adjusted))

        effort = base_effort
        context = {
            "effort": effort,
            "assignee": {
                "professionalism_coefficient": professionalism_coefficient,
                "operational_utilization": operational_utilization,
            }
        }

        for modifier in self._rules.effort_modifiers:
            if not modifier.enabled:
                continue

            if modifier.formula:
                try:
                    effort = self._evaluate_formula(modifier.formula, {**context, "effort": effort})
                except Exception:
                    # A configured modifier may fall back to its explicit safe formula.
                    logger.warning(
                        "Scheduling effort formula failed; evaluating configured fallback",
                        exc_info=True,
                        extra={"modifier_id": modifier.id},
                    )
                    effort = self._evaluate_formula(modifier.fallback, {**context, "effort": effort})

            elif modifier.operation == "ceil":
                effort = math.ceil(effort)
            elif modifier.operation == "floor":
                effort = math.floor(effort)
            elif modifier.operation == "round":
                effort = round(effort)

            if modifier.min_value is not None and effort < modifier.min_value:
                effort = modifier.min_value

        return max(1, int(effort))

    def _evaluate_formula(self, formula: str, context: dict) -> float:
        """Evaluate a formula using a compiled AST evaluator.

        Formulas are compiled once and cached, then executed efficiently.

        Supports simple expressions like:
        - "effort / assignee.professionalism_coefficient"
        - "effort * (1 + assignee.operational_utilization / 100)"
        """
        compiled_fn = self._get_compiled_formula(formula)
        return compiled_fn(context)

    def _get_compiled_formula(self, formula: str) -> Callable[[dict], float]:
        """Get or compile a formula to a callable function.

        Uses AST parsing for safe, fast execution without eval().
        """
        if not hasattr(self, '_formula_cache'):
            self._formula_cache: dict[str, Callable[[dict], float]] = {}

        if formula in self._formula_cache:
            return self._formula_cache[formula]

        try:
            tree = ast.parse(formula, mode='eval')

            bin_ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.FloorDiv: operator.floordiv,
                ast.Mod: operator.mod,
            }

            unary_ops = {
                ast.UAdd: operator.pos,
                ast.USub: operator.neg,
            }

            cmp_ops = {
                ast.Eq: operator.eq,
                ast.NotEq: operator.ne,
                ast.Lt: operator.lt,
                ast.LtE: operator.le,
                ast.Gt: operator.gt,
                ast.GtE: operator.ge,
            }

            allowed_node_types = (
                ast.Expression,
                ast.Constant,
                ast.Name,
                ast.Attribute,
                ast.BinOp,
                ast.UnaryOp,
                ast.Compare,
                ast.IfExp,
            )

            def validate_node(node: ast.AST) -> None:
                if not isinstance(node, allowed_node_types):
                    raise ValueError(f"Unsupported AST node type: {type(node).__name__}")
                if isinstance(node, ast.Name):
                    if node.id not in FORMULA_ROOT_NAMES:
                        raise ValueError(f"Unsupported formula variable: {node.id}")
                elif isinstance(node, ast.Attribute):
                    if node.attr.startswith("_"):
                        raise ValueError("Private attributes are not allowed in formulas.")
                    if not isinstance(node.value, ast.Name) or node.value.id != "assignee":
                        raise ValueError("Only assignee.<field> attribute access is allowed.")
                    if node.attr not in FORMULA_ASSIGNEE_FIELDS:
                        raise ValueError(f"Unsupported assignee formula field: {node.attr}")
                elif isinstance(node, ast.BinOp):
                    if type(node.op) not in bin_ops:
                        raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
                elif isinstance(node, ast.UnaryOp):
                    if type(node.op) not in unary_ops:
                        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
                elif isinstance(node, ast.Compare):
                    for op in node.ops:
                        if type(op) not in cmp_ops:
                            raise ValueError(f"Unsupported comparison operator: {type(op).__name__}")
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.operator, ast.unaryop, ast.cmpop, ast.expr_context)):
                        continue
                    validate_node(child)

            validate_node(tree)

            def evaluate_node(node: ast.AST, ctx: dict) -> Any:
                """Recursively evaluate an AST node."""
                if isinstance(node, ast.Expression):
                    return evaluate_node(node.body, ctx)

                elif isinstance(node, ast.Constant):
                    # Python 3.8+ uses ast.Constant for all literals
                    return node.value

                elif isinstance(node, ast.Name):
                    if node.id in ctx:
                        return ctx[node.id]
                    raise KeyError(f"Variable '{node.id}' not found")

                elif isinstance(node, ast.Attribute):
                    obj = evaluate_node(node.value, ctx)
                    if not isinstance(obj, dict):
                        raise ValueError("Formula attributes can only read dict context.")
                    return obj[node.attr]

                elif isinstance(node, ast.BinOp):
                    left = evaluate_node(node.left, ctx)
                    right = evaluate_node(node.right, ctx)
                    op_func = bin_ops.get(type(node.op))
                    if op_func is None:
                        raise ValueError(f"Unsupported binary operator: {type(node.op)}")
                    return op_func(left, right)

                elif isinstance(node, ast.UnaryOp):
                    operand = evaluate_node(node.operand, ctx)
                    op_func = unary_ops.get(type(node.op))
                    if op_func is None:
                        raise ValueError(f"Unsupported unary operator: {type(node.op)}")
                    return op_func(operand)

                elif isinstance(node, ast.Compare):
                    # Handle: a > b, a < b < c, etc.
                    left = evaluate_node(node.left, ctx)
                    for op, comparator in zip(node.ops, node.comparators):
                        right = evaluate_node(comparator, ctx)
                        cmp_func = cmp_ops.get(type(op))
                        if cmp_func is None:
                            raise ValueError(f"Unsupported comparison: {type(op)}")
                        if not cmp_func(left, right):
                            return False
                        left = right
                    return True

                elif isinstance(node, ast.IfExp):
                    # Ternary: a if condition else b
                    test = evaluate_node(node.test, ctx)
                    if test:
                        return evaluate_node(node.body, ctx)
                    return evaluate_node(node.orelse, ctx)

                else:
                    raise ValueError(f"Unsupported AST node type: {type(node)}")

            def compiled_formula(ctx: dict) -> float:
                result = evaluate_node(tree, ctx)
                return float(result)

            self._formula_cache[formula] = compiled_formula
            logger.debug(f"Compiled formula: {formula}")
            return compiled_formula

        except SyntaxError as e:
            logger.warning(f"Failed to parse formula '{formula}': {e}")
            raise ValueError(f"Invalid formula syntax: {formula}") from e
        except Exception as exc:
            logger.warning(
                "Failed to compile scheduling formula",
                exc_info=True,
            )
            raise ValueError(f"Unsupported formula: {formula}") from exc

    def get_sort_key_function(
        self,
        pass_id: str,
        task_context_getter: Callable[[Any], dict],
    ) -> Callable[[Any], tuple]:
        """Get a sort key function for a specific scheduling pass.

        Args:
            pass_id: ID of the scheduling pass
            task_context_getter: Function that takes a task and returns its context dict

        Returns:
            A function suitable for use with sorted(..., key=...)
        """
        if not self._rules:
            # Return identity function for fallback
            return lambda t: (0,)

        # Find the pass
        target_pass = None
        for sp in self._rules.scheduling_passes:
            if sp.id == pass_id:
                target_pass = sp
                break

        if not target_pass:
            return lambda t: (0,)

        def sort_key(task: Any) -> tuple:
            ctx = task_context_getter(task)
            key_parts = []

            for criterion in target_pass.sort_criteria:
                value = ctx.get(criterion.field, 0)

                # Handle None values
                if value is None:
                    value = float('inf') if criterion.order == "asc" else float('-inf')

                # Invert for descending order
                if criterion.order == "desc":
                    if isinstance(value, (int, float)):
                        value = -value
                    elif isinstance(value, bool):
                        value = not value

                key_parts.append(value)

            return tuple(key_parts)

        return sort_key

    def matches_pass_filter(self, pass_id: str, task_context: dict) -> bool:
        """Check if a task matches the filter for a scheduling pass.

        Args:
            pass_id: ID of the scheduling pass
            task_context: Dict with task properties

        Returns:
            True if task matches all filter conditions
        """
        if not self._rules:
            return True

        # Find the pass
        target_pass = None
        for sp in self._rules.scheduling_passes:
            if sp.id == pass_id:
                target_pass = sp
                break

        if not target_pass:
            return False

        for condition in target_pass.filter_conditions:
            if not self._evaluate_condition(condition, task_context):
                return False

        return True

    def _evaluate_condition(self, condition: str, context: dict) -> bool:
        """Evaluate a filter condition without dynamic code execution.

        Supports:
        - "task.field == value"
        - "task.field != null"
        - "task.field <= 2"
        """
        field_name, operator_token, expected_value = self._parse_condition(condition)
        current_value = context.get(field_name)
        if isinstance(current_value, date):
            current_value = current_value.isoformat()

        cmp_ops = {
            "==": operator.eq,
            "!=": operator.ne,
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge,
        }
        cmp_func = cmp_ops[operator_token]
        try:
            return bool(cmp_func(current_value, expected_value))
        except TypeError:
            return False

    def _parse_condition(self, condition: str) -> tuple[str, str, Any]:
        """Parse the limited filter condition grammar."""
        match = CONDITION_PATTERN.match(condition.strip())
        if not match:
            raise ValueError(f"Unsupported scheduling filter condition: {condition}")
        field_name, operator_token, raw_value = match.groups()
        if field_name not in CONDITION_FIELDS:
            raise ValueError(f"Unsupported scheduling filter field: {field_name}")
        return field_name, operator_token, self._parse_condition_value(raw_value)

    def _parse_condition_value(self, raw_value: str) -> Any:
        """Parse a literal used in a scheduling filter condition."""
        lowered = raw_value.lower()
        if lowered == "null":
            return None
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if raw_value.startswith(("'", '"')):
            return raw_value[1:-1]
        if "." in raw_value:
            return float(raw_value)
        return int(raw_value)

    def get_scheduling_passes(self) -> list[SchedulingPass]:
        """Get all enabled scheduling passes."""
        if not self._rules:
            return []
        return [p for p in self._rules.scheduling_passes if p.enabled]
