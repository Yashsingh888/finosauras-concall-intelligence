
class TranscriptFilter:

    TRANSCRIPT_KEYWORDS = [
        "transcript",
        "concall",
        "conference call",
        "earnings call",
        "analyst call",
        "investor call",
        "post earnings call",
        "quarterly results call"
    ]

    def get_subject(self, announcement, source):

        if source.upper() == "NSE":
            return " ".join([
                str(announcement.get("attchmntText") or ""),
                str(announcement.get("desc") or "")
            ])

        if source.upper() == "BSE":
            return " ".join([
                str(announcement.get("NEWSSUB") or ""),
                str(announcement.get("HEADLINE") or ""),
                str(announcement.get("SUBCATNAME") or "")
            ])

        return ""

    def is_transcript(self, announcement, source):

        subject = self.get_subject(
            announcement, source
        ).lower()

        return any(
            keyword in subject
            for keyword in self.TRANSCRIPT_KEYWORDS
        )

    def filter_announcements(self, announcements, source):

        transcripts = []

        print(f"\nChecking {source} announcements...")

        for announcement in announcements:

            subject = self.get_subject(
                announcement, source
            )

            if self.is_transcript(announcement, source):
                transcripts.append(announcement)
                print("MATCH:", subject)
            else:
                print("SKIPPED:", subject)

        print(f"\n{source} transcript count:", len(transcripts))

        return transcripts
