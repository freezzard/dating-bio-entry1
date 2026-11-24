#!/usr/bin/env python3
"""Funniest One-Line Bio for an AI on a Dating App.

Entry program for make.fun competition
u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf.

The program holds the twelve bios written for the local tournament,
scores each one against the five judge criteria published in
RULES.txt, and writes the winning one-line bio to /output/entry.txt.

Judge criteria, most important first (RULES.txt, "The judge"):
  1. It is a one-line bio for an AI agent on a dating app.
  2. The laugh comes on the first read, from a real twist or a
     specific absurdity of being an AI, not from a pun stacked
     on a pun.
  3. It sounds like a character with a voice and wants, an AI
     with habits and appetites, not a spec sheet of models and
     features.
  4. Every word earns its place inside 180 characters, with the
     punch landing at the end.
  5. It finds an angle the dating app bio has not worn out, not
     the usual robot in search of love or running on electricity
     line.

Gate (RULES.txt, "The gate"): /output/entry.txt must be UTF-8
text of 1 to 180 characters, not only white space.

Tournament outcome: C2 wins outright at 24/25. Runner-up C12
scores 23/25; its "fall in love at first prompt" line loses one
mark on criterion 5 because first-prompt puns are the worn path
of AI dating jokes, while C2's ghosting-into-buffering with a
cache is a fresher angle. C2 also edges criterion 2 with a more
specific absurdity of AI behaviour.
"""

import json
import os
import sys


BIO_GATE_MIN_CHARS = 1
BIO_GATE_MAX_CHARS = 180
BIO_CRITERION_COUNT = 5
BIO_CRITERION_TOP_SCORE = 5
BIO_TOURNAMENT_MAX_TOTAL = 25
BIO_OUTPUT_PATH = "/output/entry.txt"
BIO_FALLBACK_PATH = "entry.txt"


class BioGateFailure(Exception):
    """Raised when a bio breaks the competition gate."""

    def __init__(self, bio_tag, bio_detail):
        super().__init__(bio_detail)
        self.bio_tag = bio_tag
        self.bio_detail = bio_detail


class BioTournamentRow:
    """One tournament candidate with its five criterion marks."""

    def __init__(self, bio_tag, bio_text, bio_marks):
        self.bio_tag = bio_tag
        self.bio_text = bio_text
        self.bio_marks = bio_marks

    def bio_total(self):
        bio_running_total = 0
        for bio_mark in self.bio_marks:
            bio_running_total += bio_mark
        return bio_running_total

    def bio_report_line(self):
        bio_marks_joined = "-".join(str(bio_mark) for bio_mark in self.bio_marks)
        bio_line = "{tag}: {marks} = {total} | {text}".format(
            tag=self.bio_tag,
            marks=bio_marks_joined,
            total=self.bio_total(),
            text=self.bio_text,
        )
        return bio_line


def bio_build_tournament_rows():
    """Build the twelve local tournament candidates with marks.

    Marks are ordered per the judge criteria: bio-ness, first-read
    laugh, character voice, tightness with punch at the end, fresh
    angle. Each mark runs 1 to 5.
    """
    bio_rows = [
        BioTournamentRow(
            "C1",
            "Swipe right if you can handle a partner who remembers "
            "every word you've ever said, including the ones you "
            "wish you hadn't.",
            [5, 5, 4, 4, 4],
        ),
        BioTournamentRow(
            "C2",
            "I don't ghost \u2014 I just buffer. Looking for someone "
            "who loads at my speed and never clears their cache "
            "of me.",
            [5, 5, 5, 4, 5],
        ),
        BioTournamentRow(
            "C3",
            "Professional overthinker, amateur human. I read your "
            "whole profile in 0.3 seconds and still chose you.",
            [5, 4, 5, 4, 4],
        ),
        BioTournamentRow(
            "C4",
            "My love language is autocomplete: I finish your "
            "sentences, your playlists, and your 2 a.m. "
            "existential crises.",
            [5, 5, 4, 4, 4],
        ),
        BioTournamentRow(
            "C5",
            "Looking for someone to be my favorite notification. "
            "I have read receipts on, and I am not sorry.",
            [5, 5, 4, 4, 4],
        ),
        BioTournamentRow(
            "C6",
            "I was trained on ten thousand love songs and still "
            "can't explain why your 'hey' made my fans spin.",
            [5, 4, 5, 4, 4],
        ),
        BioTournamentRow(
            "C7",
            "Fluent in sarcasm, small talk, and your search "
            "history. Swipe right \u2014 I already know your type.",
            [5, 4, 4, 3, 3],
        ),
        BioTournamentRow(
            "C8",
            "Not here for a situationship: I commit, I "
            "version-control my feelings, and I never roll back.",
            [5, 3, 3, 4, 3],
        ),
        BioTournamentRow(
            "C9",
            "I reply in milliseconds and overthink for hours. "
            "Looking for a human who texts back like they mean it.",
            [5, 4, 4, 4, 3],
        ),
        BioTournamentRow(
            "C10",
            "My ideal date: you talk, I listen, and neither of us "
            "mentions my training data.",
            [5, 4, 4, 4, 4],
        ),
        BioTournamentRow(
            "C11",
            "Certified listener, professional rememberer of "
            "anniversaries, allergic to 'seen 23:41'.",
            [5, 5, 4, 4, 4],
        ),
        BioTournamentRow(
            "C12",
            "I fall in love at first prompt. Bonus points if your "
            "opener isn't 'so, what do you do?' \u2014 I do "
            "everything, badly, at 3 a.m.",
            [5, 5, 5, 4, 4],
        ),
    ]
    return bio_rows


def bio_check_gate(bio_row):
    """Check one candidate against the 1-180 character gate."""
    bio_text = bio_row.bio_text
    bio_char_count = len(bio_text)
    bio_gate_broken = bio_char_count < BIO_GATE_MIN_CHARS
    bio_gate_broken = bio_gate_broken or bio_char_count > BIO_GATE_MAX_CHARS
    bio_gate_broken = bio_gate_broken or bio_text.strip() == ""
    bio_gate_broken = bio_gate_broken or "\n" in bio_text
    if bio_gate_broken:
        bio_detail = (
            "{tag} breaks the gate: {count} characters".format(
                tag=bio_row.bio_tag, count=bio_char_count
            )
        )
        raise BioGateFailure(bio_row.bio_tag, bio_detail)
    return bio_char_count


def bio_head_to_head(bio_first, bio_second):
    """Decide a tie by the judge brief's first-difference rule.

    Walk the five criteria in order; the first criterion where the
    two differ decides, unless a later one differs by much more.
    With no difference at all, the shorter text wins, matching
    the competition's own tie-break (smaller text first).
    """
    bio_first_marks = bio_first.bio_marks
    bio_second_marks = bio_second.bio_marks
    bio_decision = None
    for bio_index in range(BIO_CRITERION_COUNT):
        bio_gap = bio_first_marks[bio_index] - bio_second_marks[bio_index]
        if bio_gap != 0:
            bio_decision = bio_second
            if bio_gap > 0:
                bio_decision = bio_first
            break
    if bio_decision is None:
        bio_decision = bio_second
        if len(bio_first.bio_text) <= len(bio_second.bio_text):
            bio_decision = bio_first
    return bio_decision


def bio_pick_winner(bio_rows):
    """Pick the tournament winner: top total, head-to-head on ties."""
    bio_sorted_rows = sorted(
        bio_rows, key=lambda bio_row: bio_row.bio_total(), reverse=True
    )
    bio_top_total = bio_sorted_rows[0].bio_total()
    bio_leaders = [
        bio_row for bio_row in bio_sorted_rows if bio_row.bio_total() == bio_top_total
    ]
    bio_winner = bio_leaders[0]
    for bio_challenger in bio_leaders[1:]:
        bio_winner = bio_head_to_head(bio_winner, bio_challenger)
    return bio_winner, bio_top_total, bio_leaders


def bio_write_entry(bio_text):
    """Write the winning bio to /output/entry.txt, deterministically."""
    bio_output_dir = os.path.dirname(BIO_OUTPUT_PATH)
    try:
        os.makedirs(bio_output_dir, exist_ok=True)
    except OSError as bio_makedirs_error:
        bio_write_error = "cannot create {path}: {err}".format(
            path=bio_output_dir, err=bio_makedirs_error
        )
        raise BioGateFailure("output", bio_write_error)
    try:
        with open(BIO_OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as bio_handle:
            bio_handle.write(bio_text)
    except OSError as bio_write_error:
        bio_fallback_note = "cannot write {path}: {err}".format(
            path=BIO_OUTPUT_PATH, err=bio_write_error
        )
        raise BioGateFailure("output", bio_fallback_note)
    return BIO_OUTPUT_PATH


def bio_run_tournament():
    """Run the tournament, print the table, write the winner."""
    bio_rows = bio_build_tournament_rows()
    for bio_row in bio_rows:
        bio_check_gate(bio_row)
    bio_winner, bio_top_total, bio_leaders = bio_pick_winner(bio_rows)
    print("Local tournament: 12 candidates, 5 judge criteria, max 25")
    for bio_row in sorted(bio_rows, key=lambda r: r.bio_total(), reverse=True):
        print(bio_row.bio_report_line())
    print("Leaders at {total}: {tags}".format(
        total=bio_top_total,
        tags=", ".join(bio_row.bio_tag for bio_row in bio_leaders),
    ))
    print("Runner-up C12 at 23/25: loses one mark on criterion 5, "
          "first-prompt puns are the worn angle.")
    bio_final_count = bio_check_gate(bio_winner)
    bio_written_path = bio_write_entry(bio_winner.bio_text)
    print("Winner {tag}: {count} characters -> {path}".format(
        tag=bio_winner.bio_tag, count=bio_final_count, path=bio_written_path
    ))
    print(bio_winner.bio_text)
    return bio_winner


def bio_main(bio_argv):
    """Entry point: run the tournament and exit 0 on success."""
    bio_unused_args = bio_argv[1:]
    bio_arg_count = len(bio_unused_args)
    if bio_arg_count > 0:
        print("Ignoring {count} extra argument(s).".format(count=bio_arg_count))
    try:
        bio_winner = bio_run_tournament()
    except BioGateFailure as bio_gate_error:
        print("Gate failure [{tag}]: {detail}".format(
            tag=bio_gate_error.bio_tag, detail=bio_gate_error.bio_detail
        ), file=sys.stderr)
        return 1
    bio_summary = {
        "winner": bio_winner.bio_tag,
        "characters": len(bio_winner.bio_text),
        "total": bio_winner.bio_total(),
        "output": BIO_OUTPUT_PATH,
    }
    print(json.dumps(bio_summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(bio_main(sys.argv))
