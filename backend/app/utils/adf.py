"""
ADF (Atlassian Document Format) helpers

Jira Cloud requires structured JSON for fields like description.
This utility converts plain text into valid ADF format.
"""


def text_to_adf(text: str) -> dict:
    """
    Convert plain text into minimal Atlassian Document Format (ADF).

    Jira expects description fields in ADF instead of raw strings.
    This wrapper allows the rest of the app to use normal text safely.
    """

    if not text:
        text = ""

    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    }


