#!/usr/bin/env python3
"""
doc_validator.py: Automated linter & structural validator for human-readable technical documentation.

Validates technical documentation against:
1. Invisible Scaffolding: Zero meta-quoting of internal standards (arc42, C4 Model, IEC/IEEE, ISO, MADR, Y-statement).
2. Anti-AI Writing Guardrails: Eliminating Wikipedia Signs of AI Writing (trailing -ing commentary, legacy puffery, rule-of-threes).
3. Plain language (ISO 24495-1) and scannability.
4. Hazard alerts (ISO 20607: CAUTION, WARNING, NOTE).
5. Diagrams-as-Code (Mermaid syntax and structural completeness).
6. Architecture Decision Records (ADR structural elements & decision reasoning).
7. User Outcome Translation (Mapping technical requirements to business/user value).
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Enable utf-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Forbidden internal framework/standard citations (Scaffolding must remain invisible!)
FORBIDDEN_META_REFERENCES = [
    (r"\barc42\b", "arc42 framework"),
    (r"\bC4\s*(?:Model|Level|\s*diagram)\b", "C4 Model / Levels"),
    (r"\bIEC(?:/IEEE)?\s*82079(?:-1)?\b", "IEC/IEEE 82079-1 standard"),
    (r"\bISO\s*20607\b", "ISO 20607 standard"),
    (r"\bISO(?:/IEC(?:/IEEE)?)?\s*15289\b", "ISO/IEC/IEEE 15289 standard"),
    (r"\bISO\s*24495(?:-1)?\b", "ISO 24495-1 standard"),
    (r"\bMADR(?:\s*3\.0)?\b", "MADR template"),
    (r"\bExecutive\s*Y-Statement\b", "Executive Y-Statement label"),
    (r"\bY-[Ss]tatement\b", "Y-Statement formula citation"),
    (r"\bLean arc42\b", "Lean arc42 citation"),
]

# Forbidden methodology meta-text, research narratives, and prompt echoes
FORBIDDEN_METHODOLOGY_PATTERNS = [
    (r"\b(?:reflects\s+(?:the\s+)?system\s+implementation|directly\s+from\s+(?:the\s+)?source\s+code)\b", "Source code reflection disclaimer"),
    (r"\b(?:correspond(?:s)?\s+to\s+active\s+production\s+code)\b", "Active production code affirmation"),
    (r"\b(?:all\s+configuration\s+values,?\s*api\s+contracts,?\s*database\s+schemas)\b", "Formulaic configuration/contract claim"),
    (r"\b(?:derived\s+from\s+(?:the\s+)?(?:codebase|repository|source\s+files|active\s+code))\b", "Codebase derivation disclaimer"),
    (r"\b(?:synthesized\s+from\s+(?:the\s+)?(?:codebase|repository|source\s+code|documentation))\b", "Synthesis disclaimer"),
    (r"\b(?:based\s+on\s+(?:the\s+)?(?:codebase\s+analysis|repository\s+inspection|provided\s+instructions))\b", "Analysis/instructions disclaimer"),
    (r"\b(?:this\s+document(?:ation)?\s+(?:was|is|has\s+been)\s+(?:generated|compiled|created|derived|authored)\s+(?:by|from|using|based))\b", "Document generation meta-statement"),
    (r"\b(?:as\s+(?:per\s+(?:your\s+)?(?:request|instructions)|requested|instructed))\b", "Prompt instruction echo"),
    (r"\b(?:in\s+accordance\s+with\s+(?:the\s+)?(?:prompt|instructions|user\s+request))\b", "Prompt compliance meta-text"),
    (r"\b(?:documentation\s+suite\s+reflects)\b", "Documentation suite reflection disclaimer"),
    (r"\b(?:active\s+production\s+code)\b", "Active production code affirmation"),
]

# AI buzzword residue & puffery (Wikipedia Signs of AI Writing & Clarity audits)
AI_PUFFERY_AND_CLICHES = [
    r"\bdelve into\b",
    r"\bpivotal role\b",
    r"\bpivotal moment\b",
    r"\btestament to\b",
    r"\brich tapestry\b",
    r"\bbeacon of\b",
    r"\blandscape\b",
    r"\bseamlessly integrate\b",
    r"\bgame-changer\b",
    r"\bharnessing the power\b",
    r"\bcutting-edge\b",
    r"\bwatershed moment\b",
    r"\btransformative shift\b",
    r"\bevolving landscape\b",
    r"\bstands as a testament\b",
    r"\bserves as a reminder\b",
]

# Trailing participial commentary (Superficial analyses)
TRAILING_ING_COMMENTARY = r",\s*(?:ensuring|highlighting|underscoring|fostering|enhancing|cultivating|symbolizing|reflecting|elevating)\b"

# Rule-of-three adjective stacking
RULE_OF_THREES = r"\b(?:robust,\s*scalable,\s*and\s*resilient|fast,\s*secure,\s*and\s*seamless|flexible,\s*modular,\s*and\s*extensible|robustness\s*and\s*scalability)\b"

# Conversational chatbot leavings
CHATBOT_LEAVINGS = r"^(?:Certainly!?|Here is|Below is the|I hope this helps)\b"

VALID_MERMAID_TYPES = [
    "flowchart", "graph", "sequenceDiagram", "classDiagram",
    "stateDiagram", "stateDiagram-v2", "erDiagram", "xychart-beta"
]

VALID_ALERT_TYPES = [
    "NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"
]


class ValidationResult:
    def __init__(self, filename: str):
        self.filename = filename
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.metrics: Dict[str, Any] = {}

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


def validate_invisible_scaffolding(content: str, result: ValidationResult):
    """Enforces the rule that internal standards & frameworks must never be quoted."""
    found_citations = []
    for pattern, label in FORBIDDEN_META_REFERENCES:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        for m in matches:
            found_citations.append((m.group(0), label))

    if found_citations:
        for citation, label in found_citations:
            result.errors.append(
                f"Forbidden meta-citation '{citation}' ({label}) found. "
                f"Standards and frameworks are internal AI agent scaffolding and must NEVER be quoted in human-facing docs. "
                f"Use natural engineering headings instead."
            )


def validate_methodology_meta_text(content: str, result: ValidationResult):
    """Enforces zero methodology meta-text, research narratives, or prompt echoing."""
    found_meta = []
    for pattern, label in FORBIDDEN_METHODOLOGY_PATTERNS:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        for m in matches:
            found_meta.append((m.group(0), label))

    if found_meta:
        for match_text, label in found_meta:
            result.errors.append(
                f"Forbidden methodology meta-text '{match_text}' ({label}) found. "
                f"Technical documentation must describe ONLY actual content related to the project. "
                f"Never explain how the document was generated or affirm that it reflects source code. Remove this sentence."
            )


def validate_ai_writing_guardrails(content: str, result: ValidationResult):
    """Audits against Wikipedia: Signs of AI writing."""
    # 1. Chatbot leavings
    if re.search(CHATBOT_LEAVINGS, content.strip(), re.IGNORECASE):
        result.errors.append(
            "Found conversational chatbot preamble ('Certainly...', 'Here is...'). Output must begin directly with document content."
        )

    # 2. Grand legacy puffery & AI buzzwords
    found_puffery = []
    for pattern in AI_PUFFERY_AND_CLICHES:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            found_puffery.extend(matches)
    if found_puffery:
        result.warnings.append(
            f"Found AI puffery/buzzwords (Wikipedia Signs of AI Writing): {set(found_puffery)}. "
            f"Replace with concrete engineering facts and metrics."
        )

    # 3. Superficial commentary (-ing participle clauses)
    trailing_matches = re.findall(TRAILING_ING_COMMENTARY, content, re.IGNORECASE)
    if trailing_matches:
        result.warnings.append(
            f"Found {len(trailing_matches)} trailing participial commentary phrases ({set(trailing_matches)}). "
            f"Remove superficial '-ing' wrappers and state facts directly."
        )

    # 4. Rule-of-three adjective stacking
    triples = re.findall(RULE_OF_THREES, content, re.IGNORECASE)
    if triples:
        result.warnings.append(
            f"Found rule-of-three adjective stacking ({set(triples)}). "
            f"Replace generic triples with quantifiable metrics."
        )

    # 5. Sentence-initial transition spam (Additionally, Furthermore, etc.)
    transitions = re.findall(r"(?:^|\n)(?:Additionally|Furthermore|Notably|Consequently|Ultimately),\s*", content)
    if len(transitions) > 2:
        result.warnings.append(
            f"Overuse of sentence-initial transitional adverbs ({len(transitions)} instances). "
            f"Vary sentence structure to avoid robotic LLM cadence."
        )

    # 6. Thesaurus inflation
    thesaurus = re.findall(r"\b(?:utilize[ds]?|commence[ds]?)\b", content, re.IGNORECASE)
    if thesaurus:
        result.warnings.append(
            f"Found thesaurus inflation ({set(thesaurus)}). Use plain verbs ('use'/'start')."
        )


def validate_mermaid_blocks(content: str, result: ValidationResult):
    """Verifies syntax integrity of embedded Mermaid diagrams."""
    pattern = r"```mermaid\s*\n(.*?)```"
    matches = list(re.finditer(pattern, content, re.DOTALL))
    result.metrics["mermaid_diagram_count"] = len(matches)

    for i, match in enumerate(matches, 1):
        block = match.group(1).strip()
        lines = [line.strip() for line in block.split("\n") if line.strip() and not line.strip().startswith("%%")]
        if not lines:
            result.errors.append(f"Mermaid diagram #{i} is empty.")
            continue

        first_line = lines[0]
        diagram_type = first_line.split()[0] if first_line.split() else ""
        if diagram_type not in VALID_MERMAID_TYPES:
            result.errors.append(
                f"Mermaid diagram #{i} has invalid or unsupported diagram type '{diagram_type}'. "
                f"Must be one of {VALID_MERMAID_TYPES}."
            )

        # Check bracket and parenthesis matching
        counts = {char: block.count(char) for char in "[](){}"}
        if counts["["] != counts["]"]:
            result.warnings.append(f"Mermaid diagram #{i} has mismatched square brackets '[' and ']'.")
        if counts["("] != counts[")"]:
            result.warnings.append(f"Mermaid diagram #{i} has mismatched parentheses '(' and ')'.")


def validate_safety_notices(content: str, result: ValidationResult):
    """Verifies hazard alert notice formatting."""
    alert_pattern = r">\s*\[!([A-Z]+)\]\s*\n((?:>.*(?:\n|$))*)"
    matches = list(re.finditer(alert_pattern, content))
    result.metrics["safety_alert_count"] = len(matches)

    for i, match in enumerate(matches, 1):
        alert_type = match.group(1)
        body = match.group(2)
        if alert_type not in VALID_ALERT_TYPES:
            result.errors.append(f"Safety notice #{i} uses unrecognized alert type '[!{alert_type}]'.")
            continue

        if alert_type in ["WARNING", "CAUTION"]:
            has_action = any(kw in body.lower() for kw in ["action", "required", "ensure", "execute", "must", "do not", "confirm", "check"])
            if not has_action:
                result.warnings.append(
                    f"Safety notice #{i} ([!{alert_type}]) does not clearly state a required action or preventative step."
                )


def validate_scannability(content: str, result: ValidationResult):
    """Audits paragraph length for scannability."""
    paragraphs = re.split(r"\n\s*\n", content)
    long_paras = 0
    for p in paragraphs:
        if p.strip().startswith("```") or p.strip().startswith("|") or p.strip().startswith(">"):
            continue
        sentences = re.findall(r"[.!?]+(?:\s+|$)", p)
        if len(sentences) > 8:
            long_paras += 1
    
    if long_paras > 0:
        result.warnings.append(f"Found {long_paras} paragraphs with > 8 sentences. Break into scannable chunks.")


def validate_adr_compliance(content: str, result: ValidationResult):
    """Validates ADR structure if the document is an Architecture Decision Record."""
    is_adr = re.search(r"#\s*(?:ADR|Architecture Decision Record)", content, re.IGNORECASE)
    if not is_adr:
        return

    result.metrics["is_adr"] = True
    required_sections = ["Context", "Decision", "Consequences"]
    for sec in required_sections:
        if not re.search(rf"##?\s*{sec}", content, re.IGNORECASE):
            result.errors.append(f"ADR is missing required section: '{sec}'.")

    # Status declaration
    has_status = re.search(r"(?:##?\s*Status|[-*]\s*(?:\*\*)?Status(?:\*\*)?:)", content, re.IGNORECASE)
    if not has_status:
        result.errors.append("ADR is missing required 'Status' declaration (e.g. '## Status' or '- **Status**: Accepted').")

    # Check for decision reasoning formula
    has_reasoning = re.search(
        r"In the context of\s+.*?\s+facing\s+.*?\s+we decided for\s+.*?\s+to achieve\s+.*?\s+accepting\s+.*?",
        content,
        re.DOTALL | re.IGNORECASE
    )
    if not has_reasoning:
        result.warnings.append("ADR is missing standard 5-clause decision reasoning ('In the context of..., facing..., we decided for..., to achieve..., accepting...').")


def validate_outcome_translation(content: str, result: ValidationResult):
    """Checks for presence of user outcome translation tables in architectural docs."""
    has_outcome_table = re.search(r"\|\s*(?:Requirement|Category|Goal)\s*\|\s*(?:.*?(?:Tech|Implementation).*?)\s*\|\s*(?:.*?(?:Outcome|User Value|Impact).*?)\s*\|", content, re.IGNORECASE)
    result.metrics["has_outcome_translation"] = bool(has_outcome_table)


def validate_storage_location(filepath: Path, result: ValidationResult, allow_any_path: bool = False):
    """Checks that documentation is stored inside a documentation/ directory or user-specified path."""
    if allow_any_path:
        return
    norm_parts = [p.lower() for p in filepath.resolve().parts]
    if "documentation" not in norm_parts and "evals" not in norm_parts:
        result.warnings.append(
            f"File '{filepath.name}' is saved in '{filepath.parent}'. "
            f"Guideline: Store documentation inside a 'documentation/' folder in the active path,"
            f"or as suggested by the user."
        )


def validate_document(filepath: Path, allow_any_path: bool = False) -> ValidationResult:
    result = ValidationResult(str(filepath))
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        result.errors.append(f"Failed to read file: {e}")
        return result

    result.metrics["line_count"] = len(content.splitlines())
    result.metrics["char_count"] = len(content)

    validate_storage_location(filepath, result, allow_any_path=allow_any_path)
    validate_invisible_scaffolding(content, result)
    validate_methodology_meta_text(content, result)
    validate_ai_writing_guardrails(content, result)
    validate_mermaid_blocks(content, result)
    validate_safety_notices(content, result)
    validate_scannability(content, result)
    validate_adr_compliance(content, result)
    validate_outcome_translation(content, result)

    return result


def main():
    parser = argparse.ArgumentParser(description="Validate technical documentation against industry standards.")
    parser.add_argument("files", nargs="+", help="Markdown files to validate")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--allow-any-path", action="store_true", help="Bypass the documentation/ folder placement check")
    args = parser.parse_args()

    import glob
    expanded_files = []
    for file_pattern in args.files:
        if any(char in file_pattern for char in "*?[]"):
            matched = glob.glob(file_pattern, recursive=True)
            if matched:
                expanded_files.extend([Path(m) for m in matched])
            else:
                expanded_files.append(Path(file_pattern))
        else:
            expanded_files.append(Path(file_pattern))

    all_passed = True
    for path in expanded_files:
        if not path.is_file():
            print(f"Error: {path} is not a file.")
            all_passed = False
            continue

        print(f"\n==================================================")
        print(f"Auditing: {path.name}")
        print(f"==================================================")

        res = validate_document(path, allow_any_path=args.allow_any_path)
        print(f"Lines: {res.metrics.get('line_count', 0)} | "
              f"Mermaid Diagrams: {res.metrics.get('mermaid_diagram_count', 0)} | "
              f"Safety Alerts: {res.metrics.get('safety_alert_count', 0)} | "
              f"ADR: {res.metrics.get('is_adr', False)}")

        if res.errors:
            print("\n[ERROR] Errors:")
            for err in res.errors:
                print(f"  - {err}")
            all_passed = False

        if res.warnings:
            print("\n[WARN] Warnings:")
            for warn in res.warnings:
                print(f"  - {warn}")
            if args.strict:
                all_passed = False

        if res.passed and (not res.warnings or not args.strict):
            print("\n[PASS] Document PASSED standards audit.")

    print("\n--------------------------------------------------")
    if all_passed:
        print("[SUCCESS] All documents verified successfully.")
        sys.exit(0)
    else:
        print("[FAILURE] Document audit failed. Correct issues listed above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
