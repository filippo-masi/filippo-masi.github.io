#!/usr/bin/env python3
"""Generate Quarto Markdown fragments from the site's BibTeX files.

The parser intentionally supports the subset of BibTeX used by this website and
has no third-party Python dependencies. Quarto runs it automatically before each
project render via `_quarto.yml`.
"""
from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BIB_DIR = ROOT / "bibliography"
OUT_DIR = ROOT / "generated"


@dataclass
class Entry:
    kind: str
    key: str
    fields: dict[str, str]


def clean_value(value: str) -> str:
    value = value.strip()
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value)
    # A small subset of common BibTeX escapes used in names and titles.
    replacements = {
        r"\&": "&",
        r"\%": "%",
        r"--": "–",
        r"{\'e}": "é",
        r"{\`e}": "è",
        r"{\'a}": "á",
        r"{\`a}": "à",
        r"{\^o}": "ô",
        r"{\c{c}}": "ç",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    # Remove braces used only to preserve capitalization.
    value = value.replace("{", "").replace("}", "")
    return value.strip()


def parse_bibtex(path: Path) -> list[Entry]:
    text = path.read_text(encoding="utf-8")
    entries: list[Entry] = []
    pos = 0
    length = len(text)

    while True:
        at = text.find("@", pos)
        if at < 0:
            break
        m = re.match(r"@([A-Za-z]+)\s*([\{(])", text[at:])
        if not m:
            pos = at + 1
            continue
        kind = m.group(1).lower()
        opener = m.group(2)
        closer = "}" if opener == "{" else ")"
        start = at + m.end()
        depth = 1
        quoted = False
        escaped = False
        i = start
        while i < length and depth:
            ch = text[i]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = not quoted
            elif not quoted:
                if ch == opener:
                    depth += 1
                elif ch == closer:
                    depth -= 1
            i += 1
        if depth != 0:
            raise ValueError(f"Unbalanced BibTeX entry near character {at} in {path}")

        content = text[start:i - 1].strip()
        comma = content.find(",")
        if comma < 0:
            pos = i
            continue
        key = content[:comma].strip()
        body = content[comma + 1:]
        fields = parse_fields(body)
        entries.append(Entry(kind=kind, key=key, fields=fields))
        pos = i

    return entries


def parse_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    i = 0
    n = len(body)
    while i < n:
        while i < n and (body[i].isspace() or body[i] == ","):
            i += 1
        if i >= n:
            break
        name_match = re.match(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*", body[i:])
        if not name_match:
            # Ignore malformed trailing text rather than looping forever.
            next_comma = body.find(",", i)
            if next_comma < 0:
                break
            i = next_comma + 1
            continue
        name = name_match.group(1).lower()
        i += name_match.end()
        if i >= n:
            fields[name] = ""
            break

        if body[i] == "{":
            value, i = read_balanced(body, i, "{", "}")
        elif body[i] == '"':
            value, i = read_quoted(body, i)
        else:
            end = body.find(",", i)
            if end < 0:
                end = n
            value = body[i:end]
            i = end
        fields[name] = clean_value(value)
    return fields


def read_balanced(text: str, start: int, opener: str, closer: str) -> tuple[str, int]:
    depth = 1
    quoted = False
    escaped = False
    i = start + 1
    chars: list[str] = []
    while i < len(text) and depth:
        ch = text[i]
        if escaped:
            chars.append(ch)
            escaped = False
        elif ch == "\\":
            chars.append(ch)
            escaped = True
        elif ch == '"':
            chars.append(ch)
            quoted = not quoted
        elif not quoted and ch == opener:
            depth += 1
            chars.append(ch)
        elif not quoted and ch == closer:
            depth -= 1
            if depth:
                chars.append(ch)
        else:
            chars.append(ch)
        i += 1
    if depth:
        raise ValueError("Unbalanced field value")
    return "".join(chars), i


def read_quoted(text: str, start: int) -> tuple[str, int]:
    i = start + 1
    chars: list[str] = []
    escaped = False
    while i < len(text):
        ch = text[i]
        if escaped:
            chars.append(ch)
            escaped = False
        elif ch == "\\":
            chars.append(ch)
            escaped = True
        elif ch == '"':
            return "".join(chars), i + 1
        else:
            chars.append(ch)
        i += 1
    raise ValueError("Unterminated quoted field")


def person_name(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    if "," in raw:
        last, first = [part.strip() for part in raw.split(",", 1)]
    else:
        tokens = raw.split()
        if len(tokens) == 1:
            return raw
        first, last = " ".join(tokens[:-1]), tokens[-1]

    initials: list[str] = []
    for token in re.split(r"[\s-]+", first):
        token = token.strip(". ")
        if token:
            initials.append(token[0].upper() + ".")
    formatted = (" ".join(initials) + " " + last).strip()
    if last.casefold() == "masi" and first.casefold().startswith("filippo"):
        return f"**{formatted}**"
    return formatted


def format_people(raw: str) -> str:
    people = [person_name(p) for p in re.split(r"\s+and\s+", raw) if p.strip()]
    if not people:
        return ""
    if len(people) == 1:
        return people[0]
    if len(people) == 2:
        return f"{people[0]} and {people[1]}"
    return ", ".join(people[:-1]) + f", and {people[-1]}"


def sort_entries(entries: list[Entry]) -> list[Entry]:
    def sort_key(entry: Entry) -> tuple[int, str]:
        year_text = entry.fields.get("year", "0")
        try:
            year = int(re.search(r"\d{4}", year_text).group()) if re.search(r"\d{4}", year_text) else 0
        except ValueError:
            year = 0
        return (-year, entry.fields.get("title", "").casefold())
    return sorted(entries, key=sort_key)


def markdown_link(label: str, url: str) -> str:
    return f"[{label}]({url})" if url else ""


def title_with_link(fields: dict[str, str]) -> str:
    title = fields.get("title", "Untitled")
    url = fields.get("url", "")
    return markdown_link(title, url) if url else title


def quoted_title(fields: dict[str, str]) -> str:
    raw_title = fields.get("title", "Untitled")
    linked = title_with_link(fields)
    punctuation = "" if raw_title.rstrip().endswith((".", "?", "!")) else "."
    return f"“{linked}{punctuation}”"


def append_resource_links(fields: dict[str, str]) -> str:
    links: list[str] = []
    doi = fields.get("doi", "")
    if doi:
        links.append(markdown_link("DOI", f"https://doi.org/{doi}"))
    code = fields.get("code", "")
    if code:
        links.append(markdown_link("Code", code))
    slides = fields.get("slides", "")
    if slides:
        links.append(markdown_link("Slides", slides))
    manuscript = fields.get("manuscript", "")
    if manuscript:
        links.append(markdown_link("Manuscript", manuscript))
    return " " + " · ".join(links) if links else ""


def format_publication(entry: Entry) -> str:
    f = entry.fields
    authors = format_people(f.get("author", ""))
    title = quoted_title(f)
    year = f.get("year", "")
    links = append_resource_links(f)

    if entry.kind == "article":
        journal = f.get("journal", "")
        volume = f.get("volume", "")
        number = f.get("number", "")
        pages = f.get("pages", "")
        details: list[str] = []
        if volume:
            volume_text = f"**{volume}**"
            if number:
                volume_text += f"({number})"
            details.append(volume_text)
        if pages:
            details.append(pages)
        venue = f"*{journal}*" if journal else ""
        if details:
            venue += ", " + ", ".join(details)
        if year:
            venue += f" ({year})"
        return f"{authors}. {title} {venue}.{links}".strip()

    if entry.kind in {"incollection", "inbook"}:
        book = f.get("booktitle", "") or f.get("title", "")
        editor = format_people(f.get("editor", ""))
        publisher = f.get("publisher", "")
        venue = f"In *{book}*"
        if editor:
            venue += f", edited by {editor}"
        if publisher:
            venue += f". {publisher}"
        if year:
            venue += f", {year}"
        note = f.get("note", "")
        if note:
            venue += f". {note}"
        return f"{authors}. {title} {venue}.{links}".strip()

    return format_conference(entry)


def format_conference(entry: Entry) -> str:
    f = entry.fields
    authors = format_people(f.get("author", ""))
    title = quoted_title(f)
    event = f.get("booktitle", "") or f.get("eventtitle", "") or f.get("howpublished", "")
    location = f.get("location", "") or f.get("address", "")
    date = f.get("date", "") or f.get("year", "")
    note = f.get("note", "")
    details = []
    if event:
        details.append(f"*{event}*")
    if location:
        details.append(location)
    if date:
        details.append(date)
    text = f"{authors}. {title} " + ", ".join(details)
    if note:
        text += f". {note}"
    text += "." + append_resource_links(f)
    return text.strip()


def write_numbered_section(lines: list[str], heading: str, entries: list[Entry], formatter) -> None:
    lines.append(f"## {heading}")
    lines.append("")
    if not entries:
        lines.extend(["*No entries yet.*", ""])
        return
    for entry in sort_entries(entries):
        lines.append(f"1. {formatter(entry)}")
    lines.append("")


def build_publications() -> None:
    entries = parse_bibtex(BIB_DIR / "publications.bib")
    articles = [e for e in entries if e.kind == "article"]
    chapters = [e for e in entries if e.kind in {"incollection", "inbook"}]
    others = [e for e in entries if e not in articles and e not in chapters]
    lines = ["<!-- Generated from bibliography/publications.bib. Do not edit directly. -->", ""]
    write_numbered_section(lines, "Refereed journal articles", articles, format_publication)
    write_numbered_section(lines, "Book chapters", chapters, format_publication)
    if others:
        write_numbered_section(lines, "Other publications", others, format_publication)
    (OUT_DIR / "publications.md").write_text("\n".join(lines), encoding="utf-8")


def build_conferences() -> None:
    entries = parse_bibtex(BIB_DIR / "conferences.bib")
    order = [
        "Reviewed conferences",
        "Posters and other international publications",
        "Conference communications",
    ]
    grouped: dict[str, list[Entry]] = {heading: [] for heading in order}
    for entry in entries:
        category = entry.fields.get("category", "Conference communications")
        grouped.setdefault(category, []).append(entry)
    lines = ["<!-- Generated from bibliography/conferences.bib. Do not edit directly. -->", ""]
    for heading in order:
        write_numbered_section(lines, heading, grouped.get(heading, []), format_conference)
    for heading, group in grouped.items():
        if heading not in order:
            write_numbered_section(lines, heading, group, format_conference)
    (OUT_DIR / "conferences.md").write_text("\n".join(lines), encoding="utf-8")


def build_talks() -> None:
    entries = sort_entries(parse_bibtex(BIB_DIR / "talks.bib"))
    lines = [
        "<!-- Generated from bibliography/talks.bib. Do not edit directly. -->",
        "",
        "```{=html}",
        '<div class="talk-grid">',
    ]
    for entry in entries:
        f = entry.fields
        video_id = f.get("youtube", "")
        title = escape(f.get("title", "Untitled"))
        event = escape(f.get("eventtitle", ""))
        authors = escape(re.sub(r"\*", "", format_people(f.get("author", ""))))
        location = escape(f.get("location", ""))
        date = escape(f.get("date", "") or f.get("year", ""))
        note = escape(f.get("note", ""))
        lines.extend([
            '<article class="talk-card">',
            '  <div class="talk-video">',
            f'    <iframe src="https://www.youtube-nocookie.com/embed/{video_id}" title="{title}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '  </div>',
            f'  <h2>{title}</h2>',
        ])
        if event:
            lines.append(f'  <p class="talk-event">{event}</p>')
        meta = " · ".join(part for part in [authors, location, date] if part)
        if meta:
            lines.append(f'  <p class="talk-meta">{meta}</p>')
        if note:
            lines.append(f'  <p class="talk-note">{note}</p>')
        resource_links = []
        if f.get("manuscript"):
            resource_links.append(f'<a href="{escape(f["manuscript"], quote=True)}">Manuscript</a>')
        if f.get("slides"):
            resource_links.append(f'<a href="{escape(f["slides"], quote=True)}">Slides</a>')
        if resource_links:
            lines.append(f'  <p class="talk-links">{" · ".join(resource_links)}</p>')
        lines.append('</article>')
    lines.extend(["</div>", "```", ""])
    (OUT_DIR / "talks.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_publications()
    build_conferences()
    build_talks()
    print("Generated publications, conferences, and talks from BibTeX.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - useful CLI error reporting
        print(f"Bibliography generation failed: {exc}", file=sys.stderr)
        raise
