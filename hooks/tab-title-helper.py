#!/usr/bin/env python3
"""Extract a short title from a Cortex Code hook JSON payload."""
import sys
import json
import re


def extract_prompt(data):
    """Try every known field path to find the user's prompt text."""
    # Direct top-level fields
    for key in ('prompt', 'content', 'message', 'text', 'input', 'query'):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()

    # Nested under tool_input
    ti = data.get('tool_input')
    if isinstance(ti, str) and ti.strip():
        return ti.strip()
    if isinstance(ti, dict):
        for key in ('prompt', 'content', 'message', 'text', 'input', 'query'):
            val = ti.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()

    # Nested under hook_input
    hi = data.get('hook_input')
    if isinstance(hi, dict):
        for key in ('prompt', 'content', 'message', 'text', 'input'):
            val = hi.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()

    # Last resort: find the longest string value in the payload
    strings = []

    def find_strings(obj, depth=0):
        if depth > 3:
            return
        if isinstance(obj, str) and len(obj) > 10:
            strings.append(obj)
        elif isinstance(obj, dict):
            for v in obj.values():
                find_strings(v, depth + 1)
        elif isinstance(obj, list):
            for v in obj:
                find_strings(v, depth + 1)

    find_strings(data)
    if strings:
        return max(strings, key=len)

    return ''


def make_title(text):
    """Clean up prompt text into a short, meaningful tab title."""
    # Normalize whitespace
    text = ' '.join(text.split())

    # Strip conversational filler (keep action verbs like run, create, build)
    filler_patterns = [
        r'^(hey|hi|hello|yo|ok|okay|so|well|alright|sure|thanks|thank you|thx),?\s*',
        r'^(please|pls|plz|kindly)\s+',
        r'^(can you|could you|would you|will you|do you mind)\s+',
        r"^(help me to|help me|i want to|i need to|i'd like to|i would like to)\s+",
        r'^(go ahead and|try to|try and|make sure to|make sure you)\s+',
    ]
    for pat in filler_patterns:
        text = re.sub(pat, '', text, flags=re.IGNORECASE)

    # Remove code blocks (bad titles)
    text = re.sub(r'```[\s\S]*?```', ' ', text)
    text = re.sub(r'`[^`]+`', '', text)

    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)

    # Clean trailing punctuation fragments
    text = re.sub(r'\s*[:;,]\s*$', '', text)
    text = re.sub(r'\s*[:;,](?=\s|$)', ' ', text)

    # Collapse whitespace
    text = ' '.join(text.split()).strip()

    # Take first sentence if there are multiple
    first_sentence = re.split(r'[.!?\n]', text)[0].strip()
    if len(first_sentence) > 15:
        text = first_sentence

    # Truncate to ~60 chars at a word boundary
    if len(text) > 60:
        text = text[:60].rsplit(' ', 1)[0].rstrip('.,;:') + '...'

    # Capitalize first letter, preserve rest
    if text:
        text = text[0].upper() + text[1:]

    # Fallback
    if not text or len(text) < 3:
        text = 'New Session'

    return text


if __name__ == '__main__':
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    prompt = extract_prompt(data)
    if not prompt:
        sys.exit(0)

    title = make_title(prompt[:300])
    print(title)
