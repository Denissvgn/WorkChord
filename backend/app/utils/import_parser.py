"""Parser utilities for importing tasks and team members from text files."""
import re
from dataclasses import dataclass
from typing import Optional, List
from app.models.task import Task


@dataclass
class ParsedTask:
    """Parsed task data from text import."""
    title: str
    description: Optional[str] = None
    priority: Optional[int] = None
    assignee_name: Optional[str] = None
    effort_days: Optional[float] = None
    id: Optional[int] = None  # Added for edit support


@dataclass
class ParsedTeamMember:
    """Parsed team member data from text import."""
    name: str
    position: str
    availability_percent: float
    professionalism_coefficient: float
    operational_utilization: float


def parse_tasks_text(text: str) -> list[ParsedTask]:
    """
    Parse tasks from text format.

    Extended format (with local ID support for editing):
    - [ID: 123] - <Priority> <Assignee> <Effort> <Title>
      <Description>

    Also supports new creation without ID:
    - <Priority> <Assignee> <Effort> <Title>

    Args:
        text: Raw text with tasks

    Returns:
        List of ParsedTask objects

    Raises:
        ValueError: If a line has invalid format
    """
    tasks: list[ParsedTask] = []
    lines = text.split('\n')

    current_task: Optional[ParsedTask] = None
    description_lines: list[str] = []

    # ID Pattern: Optional [ID: 123] at start
    id_pattern = re.compile(r'^\[ID:\s*(\d+)\]\s*(.*)$')

    # Regex for extended format: - <priority> "<name>" <effort> <title>
    pattern_quoted = re.compile(
        r'^-\s+(\d+)\s+"([^"]+)"\s+(\d+(?:\.\d+)?)\s+(.+)$'
    )
    pattern_unquoted = re.compile(
        r'^-\s+(\d+)\s+(\S+)\s+(\d+(?:\.\d+)?)\s+(.+)$'
    )

    for line_num, line in enumerate(lines, 1):
        line_content = line

        # Check for ID prefix
        task_id = None
        match_id = id_pattern.match(line)
        if match_id:
            task_id = int(match_id.group(1))
            line_content = match_id.group(2)

        # Check if this is a task title line (starts with "- ")
        if line_content.startswith('- '):
            # Save previous task if exists
            if current_task is not None:
                if description_lines:
                    current_task.description = '\n'.join(description_lines).strip()
                tasks.append(current_task)
                description_lines = []

            # Try extended format first (with quotes)
            match = pattern_quoted.match(line_content)
            if match:
                priority_str, assignee, effort_str, title = match.groups()
                priority = int(priority_str)
                effort = float(effort_str)

                _validate_task_fields(line_num, priority, effort)

                current_task = ParsedTask(
                    title=title.strip(),
                    priority=priority,
                    assignee_name=assignee,
                    effort_days=effort,
                    id=task_id
                )
                continue

            # Try extended format (without quotes - single word name)
            match = pattern_unquoted.match(line_content)
            if match:
                priority_str, assignee, effort_str, title = match.groups()
                priority = int(priority_str)
                effort = float(effort_str)

                _validate_task_fields(line_num, priority, effort)

                current_task = ParsedTask(
                    title=title.strip(),
                    priority=priority,
                    assignee_name=assignee,
                    effort_days=effort,
                    id=task_id
                )
                continue

            # Fall back to simple format (just title)
            title = line_content[2:].strip()
            if title:
                current_task = ParsedTask(title=title, id=task_id)

        # Check if this is a description line (starts with tab or spaces)
        elif current_task is not None and (line.startswith('\t') or line.startswith('    ')):
            # Remove leading tab/spaces and add to description
            stripped = line.lstrip('\t').lstrip('    ').rstrip()
            if stripped:
                description_lines.append(stripped)

        # Empty line - preserve in multi-line description
        elif current_task is not None and line.strip() == '' and description_lines:
            description_lines.append('')

    # Don't forget the last task
    if current_task is not None:
        if description_lines:
            current_task.description = '\n'.join(description_lines).strip()
        tasks.append(current_task)

    return tasks


def _validate_task_fields(line_num: int, priority: int, effort: float):
    if not (1 <= priority <= 10):
        # Using lenient logging or raising error?
        # For bulk edit, strict validation is better to prevent data corruption.
         raise ValueError(f"Line {line_num}: Priority must be between 1 and 10, got {priority}")
    if not (0.0 <= effort <= 365):
         raise ValueError(f"Line {line_num}: Effort must be between 0.0 and 365 days, got {effort}")


def serialize_tasks_to_text(tasks: List[Task]) -> str:
    """
    Convert a list of tasks into the editable text format.
    Format: [ID: 123] - <Priority> <Assignee> <Effort> <Title>
            <Description>
    """
    output = []

    # Sort by sort_order or id
    sorted_tasks = sorted(tasks, key=lambda t: t.sort_order if t.sort_order else t.id)

    for task in sorted_tasks:
        line = f"[ID: {task.id}] - "

        # Priority (default 5 if none)
        p = task.priority if task.priority else 5

        # Assignee (Name or "Unassigned")
        # Optimization: We need assignee names. Assuming task.assignee relationship is loaded.
        a_name = "Unassigned"
        if task.assignee:
            a_name = task.assignee.name

        if " " in a_name:
            a_name = f'"{a_name}"'

        # Effort
        e = task.effort_days if task.effort_days else 1.0

        line += f"{p} {a_name} {e} {task.title}"
        output.append(line)

        # Description
        if task.description:
            for desc_line in task.description.split('\n'):
                output.append(f"\t{desc_line}")

    return "\n".join(output)


def parse_team_members_text(text: str) -> list[ParsedTeamMember]:
    """
    Parse team members from text format.

    Format:
    -- "John Doe" Developer 100 1.0 20
    -- "Jane Marie Smith" Designer 80 1.2 15

    Format: -- "<name>" <Position> <Availability> <Prof. Coeff.> <Utilization>

    Args:
        text: Raw text with team members

    Returns:
        List of ParsedTeamMember objects

    Raises:
        ValueError: If a line has invalid format
    """
    members: list[ParsedTeamMember] = []
    lines = text.split('\n')

    # Regex pattern: -- "name" position availability professionalism utilization
    # Name is in quotes, rest are space-separated
    pattern = re.compile(
        r'^--\s+"([^"]+)"\s+(\S+)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*$'
    )

    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip lines that don't start with --
        if not line.startswith('-- '):
            continue

        match = pattern.match(line)
        if not match:
            raise ValueError(
                f"Line {line_num}: Invalid format. Expected: "
                f'-- "<name>" <Position> <Availability> <Prof.Coeff.> <Utilization>\n'
                f"Got: {line}"
            )

        name, position, availability, professionalism, utilization = match.groups()

        # Validate ranges
        availability_val = float(availability)
        professionalism_val = float(professionalism)
        utilization_val = float(utilization)

        if not (0 <= availability_val <= 100):
            raise ValueError(
                f"Line {line_num}: Availability must be between 0 and 100, got {availability_val}"
            )

        if not (0.5 <= professionalism_val <= 5.0):
            raise ValueError(
                f"Line {line_num}: Professionalism coefficient must be between 0.5 and 5.0, "
                f"got {professionalism_val}"
            )

        if not (0 <= utilization_val <= 100):
            raise ValueError(
                f"Line {line_num}: Operational utilization must be between 0 and 100, "
                f"got {utilization_val}"
            )

        members.append(ParsedTeamMember(
            name=name,
            position=position,
            availability_percent=availability_val,
            professionalism_coefficient=professionalism_val,
            operational_utilization=utilization_val
        ))

    return members
