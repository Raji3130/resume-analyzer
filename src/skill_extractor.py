"""
Skill extraction: finds which known skills (from skills_db) are
mentioned in a piece of text (resume or job description).

Uses word-boundary regex matching rather than a heavy NLP model so the
whole project runs with zero external downloads - a deliberate tradeoff
worth mentioning in interviews (precision/recall vs. simplicity & speed).
"""

import re
from collections import Counter

from src.skills_db import flatten_skills, skill_category


def _build_pattern(skill: str) -> re.Pattern:
    """
    Build a case-insensitive whole-phrase pattern for a skill.
    Escapes regex special characters (skills like 'c++' need this).
    """
    escaped = re.escape(skill)
    return re.compile(rf"(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])", re.IGNORECASE)


_ALL_SKILLS = flatten_skills()
_PATTERNS = {skill: _build_pattern(skill) for skill in _ALL_SKILLS}


def extract_skills(text: str) -> dict:
    """
    Scan text for known skills.
    Returns dict: {skill: mention_count}, only including skills found.
    """
    found = {}
    for skill, pattern in _PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            found[skill] = len(matches)
    return found


def extract_skills_grouped(text: str) -> dict:
    """Same as extract_skills but grouped by category for display."""
    found = extract_skills(text)
    grouped = {}
    for skill, count in found.items():
        category = skill_category(skill)
        grouped.setdefault(category, []).append((skill, count))
    for category in grouped:
        grouped[category].sort(key=lambda x: -x[1])
    return grouped
