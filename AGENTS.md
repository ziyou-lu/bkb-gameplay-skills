# Repository-specific instructions

- Keep public game-effect knowledge only. Do not add personal accounts, registration details, authentication data, private research notes or copied videos/audio.
- Read catalog.json and sources/posts.json before adding a skill. Normalize Instagram source IDs across URL routes; merge existing mechanisms instead of one file per post.
- Shared mechanisms have one owner. Scene skills compose them by links. A new parameter, creator or visual style is normally an update, not a new skill.
- Preserve provenance and uncertainty. Caption/author text is not audio verification, shown code is not executed code, visual shape is not damage logic. Never reconstruct missing steps from a different post.
- Treat supplied parameters as source-specific examples. Do not invent universal defaults.
- Changes to evidence must update both source and catalog references. Refresh the derived index with python scripts/update_index.py, then run python scripts/validate.py and python -m unittest discover -s tests -v, then inspect the diff.
- Respect existing history and unrelated content during integration. Never force-push this preparation package. Report local preparation, commit, push and remote verification separately.
