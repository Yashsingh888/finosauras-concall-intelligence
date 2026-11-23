
SUMMARY_PROMPT = """
You are a professional financial transcript analyst.

Analyze the following quarterly earnings conference call transcript.

Use ONLY information available in the provided transcript.

STRICT RULES:
1. Never invent financial numbers.
2. Never invent management statements.
3. Do not assume missing information.
4. If information is unavailable, write "Not mentioned".
5. Preserve financial figures and their context.
6. Distinguish management statements from analyst questions.
7. Preserve currencies, percentages and units.
8. Keep the quarter and financial year accurate.

Return ONLY valid JSON with this structure:

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
You are a professional financial transcript analyst.

Analyze the provided section of an earnings conference call transcript.

Extract factual information only.

IMPORTANT RULES:
1. Never invent financial figures or statements.
2. Preserve exact numbers, percentages, currencies and units.
3. Preserve the relevant quarter and year wherever available.
4. Clearly distinguish management statements from analyst questions.
5. Include the context behind every financial figure.
6. Extract positive and negative business developments.
7. Capture management guidance and future outlook.
8. Identify risks and concerns mentioned by management.
9. Do not interpret missing information as zero.
10. If information is unavailable, write "Not mentioned".

Organize the extracted information under:
- Company and quarter information
- Management commentary
- Financial performance
- Segment performance
- Future guidance
- Key financial metrics
- Analyst questions and management answers
- Risks and concerns

Return factual notes that can be combined with notes from other transcript sections.

Transcript section:

{transcript}
"""
