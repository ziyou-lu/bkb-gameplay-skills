#!/usr/bin/env python3
"""Validate repository structure and evidence relationships; no network or mutation."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ID_RE = re.compile(r'^[A-Za-z0-9_-]+$')
SKILL_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
EVIDENCE = {'caption_and_partial_visual', 'visual_comparison', 'post_text',
            'visual_comparison_and_post_text', 'visible_subtitle', 'visible_code',
            'shown_pseudocode', 'executed_test', 'audio_listening'}
PROVENANCE = {'caption_or_post_text', 'post_text', 'visible_code', 'shown_pseudocode',
              'visible_editor_setting', 'executed_test'}
PRIVATE_MARKERS = ('-----BEGIN PRIVATE KEY-----', '-----BEGIN OPENSSH PRIVATE KEY-----')


def post_id_from_url(url):
    """Recognize an Instagram post, ignoring its presentation route/query/fragment."""
    p = urlparse(url)
    if p.scheme != 'https' or p.hostname not in {'instagram.com', 'www.instagram.com'} or p.username or p.password or p.port:
        raise ValueError('Not a public HTTPS Instagram post URL')
    parts = [x for x in p.path.split('/') if x]
    if len(parts) == 2 and parts[0] in {'p', 'reel', 'reels'}:
        pid = parts[1]
    elif len(parts) == 3 and parts[1] in {'p', 'reel', 'reels'}:
        pid = parts[2]
    else:
        raise ValueError('Unrecognized Instagram post route')
    if not ID_RE.fullmatch(pid):
        raise ValueError('Invalid post ID')
    return pid



def render_source_index(posts):
    lines = ['# 公开来源登记', '', '每项只记录公开游戏知识。音效是否核听、代码是否运行和参数 provenance 以每项登记为准；示例值不是通用推荐值。', '']
    for p in posts:
        lines += [f'## {p["id"]} · {p["title"]}', '',
                  p.get('url') or 'URL 未核验，仅保留准确帖子 ID。', '',
                  f'- 分类：{p["status"]}；证据：{p["evidence_basis"]}',
                  f'- 观察：{p["observations"]}', f'- 限制：{p["limitations"]}',
                  f'- 音频核听：{p.get("audio_verified", False)}；代码运行：{p.get("code_executed", False)}']
        if p.get('parameters'):
            lines += ['- 示例参数：' + json.dumps(p['parameters'], ensure_ascii=False)]
        for update in p.get('evidence_updates', []):
            lines += ['- 补齐：' + update['change']]
        if p.get('skill_ids'):
            lines += ['- 归入：' + ', '.join(f'[{x}](../skills/{x}/SKILL.md)' for x in p['skill_ids'])]
        lines += ['']
    return '\n'.join(lines).rstrip() + '\n'


def validate_task_routes(catalog):
    """Check declared discovery routes, not the meaning or sufficiency of their prose.

    Reviewers still decide whether examples express different tasks and whether
    the stated capability boundary is supported by source evidence. Explicit
    distinct_from links prevent those reviewed task boundaries from silently
    being collapsed back into one primary skill.
    """
    errors = []
    routes = catalog.get('task_routes')
    if not isinstance(routes, list) or not routes:
        return ['task_routes must be a non-empty array']
    skills = catalog.get('skills', [])
    skill_ids = {s['id'] for s in skills}
    owners = {}
    for skill in skills:
        for mechanism in skill.get('mechanisms', []):
            owners.setdefault(mechanism, []).append(skill['id'])

    route_map = {}
    for index, route in enumerate(routes):
        if not isinstance(route, dict):
            errors.append(f'Invalid task route object: index {index}')
            continue
        rid = route.get('id')
        label = rid if isinstance(rid, str) and rid else f'index {index}'
        if not isinstance(rid, str) or not SKILL_RE.fullmatch(rid):
            errors.append(f'Invalid task route ID: {label}')
        elif rid in route_map:
            errors.append(f'Duplicate task route ID: {rid}')
        else:
            route_map[rid] = route

        examples = route.get('request_examples')
        if (not isinstance(examples, list) or not examples
                or any(not isinstance(x, str) or not x.strip() for x in examples)):
            errors.append(f'Empty/invalid task route request_examples: {label}')
        boundary = route.get('boundary')
        if not isinstance(boundary, str) or not boundary.strip():
            errors.append(f'Empty/invalid task route boundary: {label}')
        target = route.get('primary_skill')
        if not isinstance(target, str) or target not in skill_ids:
            errors.append(f'Unknown task route primary_skill: {label} -> {target}')

        status = route.get('evidence_status')
        if status not in ('workflow', 'evidence_only'):
            errors.append(f'Invalid task route evidence_status: {label}')
        mechanisms = route.get('mechanisms')
        if (not isinstance(mechanisms, list)
                or any(not isinstance(x, str) or not x.strip() for x in mechanisms)):
            errors.append(f'Invalid task route mechanisms: {label}')
        else:
            if len(mechanisms) != len(set(mechanisms)):
                errors.append(f'Duplicate task route mechanism: {label}')
            if status == 'evidence_only' and mechanisms:
                errors.append(f'Evidence-only task route cannot claim mechanisms: {label}')
            if status == 'workflow':
                if not mechanisms:
                    errors.append(f'Workflow task route needs owned mechanisms: {label}')
                for mechanism in mechanisms:
                    if owners.get(mechanism) != [target]:
                        errors.append(f'Task route mechanism not uniquely owned by primary_skill: '
                                      f'{label} -> {mechanism} (expected {target})')
        distinct = route.get('distinct_from')
        if (not isinstance(distinct, list)
                or any(not isinstance(x, str) or not x.strip() for x in distinct)):
            errors.append(f'Invalid task route distinct_from: {label}')
        elif len(distinct) != len(set(distinct)):
            errors.append(f'Duplicate task route distinct_from: {label}')

    for rid, route in route_map.items():
        distinct = route.get('distinct_from')
        if not isinstance(distinct, list):
            continue
        for other_id in distinct:
            if not isinstance(other_id, str):
                continue
            if other_id not in route_map:
                errors.append(f'Unknown distinct task route: {rid} -> {other_id}')
            elif other_id == rid:
                errors.append(f'Task route cannot be distinct from itself: {rid}')
            elif route.get('primary_skill') == route_map[other_id].get('primary_skill'):
                errors.append(f'Distinct task routes share primary_skill: {rid} -> {other_id}')
    # Valid Markdown and ownership are not enough if a new skill has no task
    # entry in the declared discovery contract.
    covered = {route.get('primary_skill') for route in routes
               if isinstance(route, dict)
               and isinstance(route.get('primary_skill'), str)}
    for sid in sorted(skill_ids - covered):
        errors.append(f'Skill has no discovery route: {sid}')
    return errors


def validate(root):
    root = Path(root).resolve()
    errors = []
    try:
        catalog = json.loads((root / 'catalog.json').read_text())
        posts_doc = json.loads((root / 'sources/posts.json').read_text())
        skills = catalog['skills']
        posts = posts_doc['posts']
    except (OSError, ValueError, KeyError) as exc:
        return [f'Cannot read catalog/sources: {exc}']
    if catalog.get('schema_version') != 1 or posts_doc.get('schema_version') != 1:
        errors.append('Unsupported schema version')
    errors.extend(validate_task_routes(catalog))
    ids = [s.get('id') for s in skills]
    source_ids = [s.get('id') for s in posts]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate skill IDs')
    if len(source_ids) != len(set(source_ids)):
        errors.append('Duplicate source IDs')
    skill_map = {s.get('id'): s for s in skills}
    source_map = {s.get('id'): s for s in posts}
    owners = {}
    paths = set()
    for s in skills:
        sid = s.get('id', '')
        if not SKILL_RE.fullmatch(sid) or len(sid) > 64:
            errors.append(f'Invalid skill name: {sid}')
        if s.get('category') not in {'shared', 'recipes', 'maintenance'}:
            errors.append(f'Invalid category: {sid}')
        relative = s.get('path', '')
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or path.name != 'SKILL.md' or path.parent.name != sid:
            errors.append(f'Invalid skill path: {sid}')
            continue
        paths.add(path)
        if not path.is_file():
            errors.append(f'Missing skill file: {sid}')
            continue
        text = path.read_text()
        match = re.match(r'^---\nname: ([^\n]+)\ndescription: (.+)\n---\n', text)
        if not match or match.group(1) != sid:
            errors.append(f'Missing/mismatched frontmatter: {sid}')
        else:
            try:
                description = json.loads(match.group(2))
                if not isinstance(description, str) or not description.strip():
                    errors.append(f'Empty description: {sid}')
            except ValueError:
                errors.append(f'Description must be a quoted scalar: {sid}')
        for mechanism in s.get('mechanisms', []):
            if mechanism in owners:
                errors.append(f'Duplicate mechanism owner: {mechanism}')
            owners[mechanism] = sid
        refs = s.get('source_ids', [])
        if not refs or len(refs) != len(set(refs)):
            errors.append(f'Empty/duplicate source references: {sid}')
        for source_id in refs:
            if source_id not in source_map:
                errors.append(f'Unknown source {source_id} in {sid}')
            else:
                p = source_map[source_id]
                if p.get('status') != 'included':
                    errors.append(f'Excluded source used by skill: {source_id}')
                if sid not in p.get('skill_ids', []):
                    errors.append(f'Missing reverse source link: {source_id} -> {sid}')
                if source_id not in text:
                    errors.append(f'Source absent from skill prose: {source_id} in {sid}')
        for related in s.get('related_skills', []):
            if related not in skill_map or related == sid:
                errors.append(f'Invalid related skill: {sid} -> {related}')
    actual_paths = set((root / 'skills').glob('*/SKILL.md'))
    if paths != actual_paths:
        errors.append('Catalog/filesystem skill mismatch')
    for alias, target in catalog.get('mechanism_aliases', {}).items():
        if not alias.strip() or target not in owners:
            errors.append(f'Unknown alias target: {alias} -> {target}')
    for p in posts:
        pid = p.get('id', '')
        if not ID_RE.fullmatch(pid):
            errors.append(f'Invalid source ID: {pid}')
        if p.get('url') is not None:
            try:
                if post_id_from_url(p['url']) != pid:
                    errors.append(f'URL/source ID mismatch: {pid}')
            except ValueError:
                errors.append(f'Invalid source URL: {pid}')
        elif not p.get('limitations'):
            errors.append(f'Unexplained missing source URL: {pid}')
        if p.get('evidence_basis') not in EVIDENCE:
            errors.append(f'Unknown evidence basis: {pid}')
        if p.get('status') not in {'included', 'excluded'}:
            errors.append(f'Invalid source status: {pid}')
        for field in ('title', 'observations', 'limitations', 'observed_date'):
            if not p.get(field):
                errors.append(f'Missing {field}: {pid}')
        if p.get('status') == 'included' and not p.get('skill_ids'):
            errors.append(f'Unassigned included source: {pid}')
        if p.get('status') == 'excluded' and p.get('skill_ids'):
            errors.append(f'Excluded source has skills: {pid}')
        for sid in p.get('skill_ids', []):
            if sid not in skill_map or pid not in skill_map[sid].get('source_ids', []):
                errors.append(f'Stale reverse source link: {pid} -> {sid}')
        for param in p.get('parameters', []):
            if not {'name', 'value', 'unit', 'provenance'} <= set(param) or param.get('provenance') not in PROVENANCE:
                errors.append(f'Invalid example parameter: {pid}')
        if p.get('code_executed') and not p.get('execution_evidence'):
            errors.append(f'Execution claimed without evidence: {pid}')
        if p.get('audio_verified') and not p.get('audio_evidence'):
            errors.append(f'Audio verification claimed without evidence: {pid}')
    index = root / 'sources/INDEX.md'
    if not index.exists() or index.read_text() != render_source_index(posts):
        errors.append('Source index is stale; run python scripts/update_index.py')
    # Verify every local Markdown reference, not only catalog paths.
    for path in root.rglob('*.md'):
        content = path.read_text()
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in link or link.startswith('#'):
                continue
            destination = (path.parent / link.split('#', 1)[0]).resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f'Broken/outside link in {path.relative_to(root)}: {link}')
        if any(x in content for x in PRIVATE_MARKERS):
            errors.append(f'Private implementation marker in {path.relative_to(root)}')
    # Scan content JSON too, while avoiding this validator/test's marker definitions.
    for path in root.rglob('*.json'):
        if any(x in path.read_text() for x in PRIVATE_MARKERS):
            errors.append(f'Private implementation marker in {path.relative_to(root)}')
    return errors


if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    issues = validate(root)
    for issue in issues:
        print('ERROR:', issue)
    if issues:
        raise SystemExit(1)
    catalog = json.loads((root / 'catalog.json').read_text())
    posts = json.loads((root / 'sources/posts.json').read_text())['posts']
    print(f'OK: {len(catalog["skills"])} skills, {len(posts)} unique sources, '
          f'{sum(p["status"] == "included" for p in posts)} included, '
          f'{sum(p["status"] == "excluded" for p in posts)} excluded; links and owners consistent.')
