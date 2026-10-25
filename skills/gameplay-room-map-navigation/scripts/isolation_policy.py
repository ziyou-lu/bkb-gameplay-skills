"""Library-authored map-only visibility-set candidate, not a renderer.

The caller supplies the latest base visibility after exploration and other
filters. The function cannot change world objects, records or the input set.
Session ownership, asynchronous loading and UI projection remain integration
responsibilities described in SKILL.md, not simulated by this pure function.
"""


def visible_room_ids(base_visible_ids, selected_room_id, *, isolated):
    """Return an immutable view; invalid isolated selection fails closed."""
    if not isinstance(isolated, bool):
        raise ValueError('isolated must be a boolean')
    if isinstance(base_visible_ids, (str, bytes)):
        raise ValueError('base_visible_ids must be a collection of room IDs')
    try:
        base = frozenset(base_visible_ids)
    except TypeError as exc:
        raise ValueError('base_visible_ids must contain hashable room IDs') from exc
    if any(not isinstance(rid, str) or not rid for rid in base):
        raise ValueError('room IDs must be nonempty strings')
    if selected_room_id is not None and (
            not isinstance(selected_room_id, str) or not selected_room_id):
        raise ValueError('selected_room_id must be a nonempty string or None')
    if not isolated:
        return base
    return frozenset({selected_room_id}) & base if selected_room_id else frozenset()
