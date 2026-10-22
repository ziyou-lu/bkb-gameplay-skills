# Repository-specific instructions

- Keep public game-effect knowledge only. Do not add personal accounts, registration details, authentication data, private research notes or copied videos/audio.
- Read catalog.json and sources/posts.json before adding a skill. Normalize Instagram source IDs across URL routes; merge existing mechanisms instead of one file per post.
- Shared mechanisms have one owner. Scene skills compose them by links. A new parameter, creator or visual style is normally an update, not a new skill. The same broad category does not imply the same workflow: compare trigger, inputs, state transitions and failure acceptance before merging. Register task_routes and reviewed distinct_from boundaries; keep compatibility navigation when moving an owner. Evidence-only notes must not be advertised as complete implementation capabilities.
- Preserve provenance and uncertainty. Caption/author text is not audio verification, shown code is not executed code, visual shape is not damage logic. Never reconstruct missing steps from a different post.
- Treat supplied parameters as source-specific examples. Do not invent universal defaults.
- Changes to evidence must update both source and catalog references. Refresh the derived index with python scripts/update_index.py, then run python scripts/validate.py and python -m unittest discover -s tests -v, then inspect the diff.
- Respect existing history and unrelated content during integration. Never force-push this preparation package. Report local preparation, commit, push and remote verification separately.

- The primary consumer is a game-creation Agent. SKILL.md must provide task triggers, required inputs/preconditions, concrete implementation decisions and sequence, mechanism-specific tuning, observable acceptance and relevant failure recovery. Do not replace executable guidance with research narration or a generic template.
- Keep creator attribution, repost chains, source IDs, observations, unknowns and source-specific parameter claims in references/sources.md and sources/posts.json. Every catalog skill has evidence_path. Entry points link that reference only when provenance is needed; do not embed source IDs, platform links or repeated evidence disclaimers in runtime instructions.
- Distinguish source-supported mechanisms from generalized implementation choices in the reference layer. Keep engineering constraints in the execution flow. Never claim candidate algorithms, project parameters or proposed acceptance checks were source-verified or already tested.
