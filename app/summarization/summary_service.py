
from app.summarization.ai_summarizer import AISummarizer
from app.summarization.summary_formatter import SummaryFormatter


class SummaryService:

    def __init__(self):
        self.summarizer = AISummarizer()
        self.formatter = SummaryFormatter()

    def generate_summary(self, transcript_text, company_name):

        if not transcript_text or not transcript_text.strip():
            raise ValueError("Transcript text is empty.")

        print(f"Generating summary for {company_name}...")

        # Generate AI summary
        summary = self.summarizer.summarize(transcript_text)

        # Save JSON output
        self.formatter.save_json(summary, company_name)

        # Save Markdown output
        self.formatter.save_markdown(summary, company_name)

        print("Summary saved successfully!")

        return summary
