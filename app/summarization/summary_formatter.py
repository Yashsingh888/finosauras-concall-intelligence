
import json
from pathlib import Path


class SummaryFormatter:

    def __init__(self):

        self.output_folder = Path("data/summaries")

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_json(self, summary, company_name):

        file_path = self.output_folder / (
            company_name.replace(" ", "_") + ".json"
        )

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(
                summary,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("JSON saved:", file_path)

    def save_markdown(self, summary, company_name):

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

        file_path = self.output_folder / (
            company_name.replace(" ", "_") + ".md"
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        print("Markdown saved:", file_path)

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
