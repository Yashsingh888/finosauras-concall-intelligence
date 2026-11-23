
import json
import re
from pathlib import Path


class SummaryFormatter:

    def __init__(self):
        self.output_folder = Path("data/summaries")
        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def get_file_path(self, company_name, transcript_id, extension):

        safe_name = re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            company_name
        )

        if transcript_id:
            filename = f"{safe_name}_{transcript_id}.{extension}"
        else:
            filename = f"{safe_name}.{extension}"

        return self.output_folder / filename

    def save_json(self, summary, company_name, transcript_id=None):

        file_path = self.get_file_path(
            company_name,
            transcript_id,
            "json"
        )

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                summary,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("JSON saved:", file_path)
        return file_path

    def save_markdown(self, summary, company_name, transcript_id=None):

        content = f"""
# {summary.get('company', company_name)}

## TL;DR
{self.format_list(summary.get('tldr', []))}

## Management Commentary
{self.format_list(summary.get('management_commentary', []))}

## Guidance and Outlook
{self.format_list(summary.get('guidance', []))}

## Segment Performance
{self.format_list(summary.get('segment_performance', []))}

## Key Financial Metrics
{self.format_list(summary.get('key_metrics', []))}

## Notable Q&A
{self.format_list(summary.get('notable_qa', []))}

## Risks and Concerns
{self.format_list(summary.get('risks', []))}
"""

        file_path = self.get_file_path(
            company_name,
            transcript_id,
            "md"
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        print("Markdown saved:", file_path)
        return file_path

    def format_list(self, items):

        if not items:
            return "- Not mentioned"

        lines = []

        for item in items:

            if isinstance(item, dict):
                lines.append(
                    "- " + " | ".join(
                        f"{key}: {value}"
                        for key, value in item.items()
                    )
                )
            else:
                lines.append("- " + str(item))

        return "\n".join(lines)


if __name__ == "__main__":

    formatter = SummaryFormatter()
    print("Summary Formatter initialized successfully!")
