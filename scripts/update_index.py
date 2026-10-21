#!/usr/bin/env python3
"""Refresh only the derived public source index after editing posts.json."""
import json
from pathlib import Path
from validate import render_source_index

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    posts = json.loads((root / 'sources/posts.json').read_text())['posts']
    (root / 'sources/INDEX.md').write_text(render_source_index(posts))
    print('Updated sources/INDEX.md from sources/posts.json')
