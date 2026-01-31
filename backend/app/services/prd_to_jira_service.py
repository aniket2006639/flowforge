import json
import re
from typing import Set

from app.llm.router import get_llm_client
from app.schemas.prd_generation_response_schema import PRDGenerationResponse


STOPWORDS: Set[str] = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "are",
    "will",
}


class PRDToJiraService:

    @staticmethod
    async def generate(
        prd_text: str,
        provider: str | None = None,
    ) -> PRDGenerationResponse:

        if not prd_text or len(prd_text.strip()) < 50:
            raise ValueError("PRD must be at least 50 characters long")

        prompt = (
            "Produce a single JSON object and nothing else. The JSON MUST exactly follow this format:\n"
            "{\n"
            "  \"epics\": [\n"
            "    {\n"
            "      \"title\": \"Epic title from PRD\",\n"
            "      \"justification\": \"Exact PRD line or section\",\n"
            "      \"stories\": [\n"
            "        {\n"
            "          \"title\": \"Story title\",\n"
            "          \"description\": \"Implementation goal\",\n"
            "          \"acceptance_criteria\": [\"Criterion tied to PRD behavior\"],\n"
            "          \"justification\": \"Exact PRD line or section\"\n"
            "        }\n"
            "      ]\n"
            "    }\n"
            "  ]\n"
            "}\n\n"
            "Rules:\n"
            "1) Every justification MUST come from the PRD text below.\n"
            "2) Do NOT invent features.\n"
            "3) Output JSON only.\n\n"
            "PRD:\n"
            + prd_text
        )

        llm_client = get_llm_client(provider)
        raw = await llm_client.generate_tasks(prd_text=prompt, project_key="")

        if isinstance(raw, dict):
            parsed = raw
        elif isinstance(raw, str):
            try:
                parsed = json.loads(raw)
            except Exception as e:
                raise ValueError(f"LLM returned non-JSON response: {e}")
        else:
            raise ValueError("LLM returned unexpected type")

        if isinstance(parsed, dict) and parsed.get("error"):
            raise ValueError(parsed["error"])

        parsed = PRDToJiraService._normalize_llm_output(parsed)

        try:
            validated = PRDGenerationResponse.parse_obj(parsed)
        except Exception as e:
            raise ValueError(f"Schema validation failed: {e}")

        PRDToJiraService._validate_justifications_and_references(
            validated, prd_text
        )

        return validated

    # ---------------- NORMALIZATION ----------------

    @staticmethod
    def _normalize_llm_output(parsed: dict) -> dict:
        if not isinstance(parsed, dict) or "epics" not in parsed:
            return parsed

        normalized_epics = []

        for epic in parsed.get("epics", []):
            if not isinstance(epic, dict):
                continue

            title = epic.get("title") or epic.get("epic_name")
            if not title:
                continue

            justification = epic.get(
                "justification",
                epic.get("description", title),
            )

            stories = []
            for story in epic.get("stories", []):
                if not isinstance(story, dict):
                    continue

                stories.append(
                    {
                        "title": story.get("title", ""),
                        "description": story.get("description", ""),
                        "acceptance_criteria": story.get(
                            "acceptance_criteria", []
                        ),
                        "justification": story.get(
                            "justification",
                            story.get("description", story.get("title", "")),
                        ),
                    }
                )

            normalized_epics.append(
                {
                    "title": title,
                    "justification": justification,
                    "stories": stories,
                }
            )

        return {"epics": normalized_epics}

    # ---------------- VALIDATION ----------------

    @staticmethod
    def _tokenize_text(text: str) -> Set[str]:
        parts = re.split(r"[^a-zA-Z0-9]+", text.lower())
        return {p for p in parts if len(p) >= 3 and p not in STOPWORDS}

    @staticmethod
    def _is_traceable(justification: str, prd_text: str) -> bool:
        j = justification.strip().lower()
        prd_lower = prd_text.lower()

        if j in prd_lower:
            return True

        return (
            len(
                PRDToJiraService._tokenize_text(justification)
                & PRDToJiraService._tokenize_text(prd_text)
            )
            >= 2
        )

    @staticmethod
    def _validate_justifications_and_references(
        validated: PRDGenerationResponse,
        prd_text: str,
    ):
        for epic in validated.epics:
            if not PRDToJiraService._is_traceable(
                epic.justification, prd_text
            ):
                raise ValueError(
                    f"Epic justification not traceable to PRD: {epic.justification}"
                )

            for story in epic.stories:
                if not PRDToJiraService._is_traceable(
                    story.justification, prd_text
                ):
                    raise ValueError(
                        f"Story justification not traceable to PRD: {story.justification}"
                    )

                for ac in story.acceptance_criteria:
                    if len(ac.strip()) < 5:
                        raise ValueError(
                            "Acceptance criteria must be meaningful"
                        )

                    if not PRDToJiraService._is_traceable(
                        ac, prd_text
                    ):
                        raise ValueError(
                            "Acceptance criteria must be tied to PRD behavior"
                        )
