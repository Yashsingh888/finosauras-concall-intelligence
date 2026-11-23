
import os
import json
import time
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.summarization.prompts import SUMMARY_PROMPT, CHUNK_PROMPT


class AISummarizer:

    def __init__(self):
        # Load API key from the project's .env file
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(dotenv_path=env_path, override=True)

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("Gemini API key not found. Check your .env file.")

        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        self.client = genai.Client(api_key=api_key)

        print("Using Gemini model:", self.model)

    def generate_response(self, prompt):

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                if not response.text:
                    raise ValueError("Gemini returned an empty response.")

                return response.text

            except Exception as error:
                message = str(error).upper()

                temporary_errors = [
                    "503", "UNAVAILABLE", "429",
                    "RESOURCE_EXHAUSTED", "500", "502", "504"
                ]

                is_temporary = any(
                    code in message for code in temporary_errors
                )

                if is_temporary and attempt < 2:
                    wait_time = 10 * (attempt + 1)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise

        raise Exception("Gemini failed after 3 attempts.")

    def chunk_text(self, text, chunk_size=12000):

        if not text or not text.strip():
            raise ValueError("Transcript text is empty.")

        return [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]

    def clean_json_response(self, response):

        cleaned = response.strip()

        # Remove Markdown code fences
        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE
        )

        cleaned = re.sub(r"\s*```$", "", cleaned)

        # Extract the JSON object if extra text is present
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end < start:
            raise ValueError("No valid JSON object found in Gemini response.")

        return cleaned[start:end + 1]

    def summarize(self, transcript_text):

        print("\nStarting transcript summarization...")

        chunks = self.chunk_text(transcript_text)
        chunk_results = []

        for index, chunk in enumerate(chunks):

            print(
                f"Processing chunk {index + 1} of {len(chunks)}..."
            )

            prompt = CHUNK_PROMPT.replace(
                "{transcript}",
                chunk
            )

            result = self.generate_response(prompt)
            chunk_results.append(result)

        combined_text = "\n\n".join(chunk_results)

        print("\nGenerating final structured summary...")

        final_prompt = SUMMARY_PROMPT.replace(
            "{transcript}",
            combined_text
        )

        final_response = self.generate_response(final_prompt)

        cleaned_response = self.clean_json_response(final_response)

        try:
            summary = json.loads(cleaned_response)

        except json.JSONDecodeError as error:
            print("Gemini returned invalid JSON.")
            print("Error:", error)
            raise ValueError(
                "Could not convert Gemini response into JSON."
            ) from error

        if not isinstance(summary, dict):
            raise ValueError("Gemini response must be a JSON object.")

        print("\nSummary generated successfully!")

        return summary


if __name__ == "__main__":

    try:
        summarizer = AISummarizer()

        sample_text = """
        ABC Limited reported revenue growth of 15 percent.
        Management expects revenue growth of 12 percent
        in the coming financial year.
        """

        result = summarizer.summarize(sample_text)

        print(json.dumps(result, indent=4, ensure_ascii=False))

    except Exception as error:
        print("\nERROR:", error)
