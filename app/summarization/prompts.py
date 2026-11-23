
SUMMARY_PROMPT = """
You are a professional financial transcript analyst.

Analyze the following quarterly earnings conference call transcript.

Create a faithful summary using ONLY information available
in the provided transcript.

STRICT RULES:
1. Never invent financial numbers.
2. Never invent management statements.
3. Do not assume missing information.
4. If information is unavailable, write "Not mentioned".
5. Preserve financial figures and their context.
6. Distinguish management statements from analyst questions.

Return valid JSON with this structure:

{
    "company": "",
    "quarter": "",
    "call_date": "",
    "tldr": [],
    "management_commentary": [],
    "guidance": [],
    "segment_performance": [],
    "key_metrics": [],
    "notable_qa": [],
    "risks": []
}

Transcript:

{transcript}
"""

CHUNK_PROMPT = """
You are analyzing a financial earnings call transcript.

Extract important factual information from this transcript section.

Include:
- Management commentary
- Financial numbers
- Business performance
- Future guidance
- Analyst questions and answers
- Risks and concerns

Do not invent information.

If a detail is missing, do not assume it.

Transcript section:

{transcript}
"""
