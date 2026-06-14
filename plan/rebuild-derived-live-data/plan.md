# Rebuild Derived Live Data After Publishing

## Goal

After publishing any nonzero source data for a day, rebuild the derived live files in `data/<day>` from the currently published source directories:

- `joined.json`
- `unique.json`
- `data.embeddings.json`

Derived files should represent the final live source mix, including newly published source data and preserved source data for any zero-result source.

## Relevant Files And Functions

- `web/fetch/main.py`
  - `embed_all_event_data(data_path)`
  - current call order around fetch, embed, and publish
- `fetch/collect.py`
  - `collect_all_data(data_path)`
- `fetch/unique.py`
  - `unique(data_path, threshold)`
- `ai/json_data_to_embeddings.py`
  - `data_to_embeddings(data_path)`
- `common/paths.py`
  - `DataPath`
  - `Paths.DATA_DIR`
  - `Paths.TEMP_LOCAL_DIR`

## Implementation Tasks

1. Change the workflow so source fetchers write to `data_working`, then source publishing updates `data`, then derived files are rebuilt in `data`.
2. Introduce a clear helper, for example `rebuild_live_event_data(day)`, that creates `DataPath(day, Paths.DATA_DIR)` and calls:
   - `collect_all_data(live_data_path)`
   - `unique(live_data_path, .60)`
   - `data_to_embeddings(live_data_path)`
3. Call the rebuild helper only after at least one source was published for that day.
4. Ensure `collect_all_data(...)` reads only source-level `data.json` files, or otherwise prevent it from accidentally aggregating derived files.
5. Ensure stale derived files are overwritten or removed when rebuilding.
6. Keep staging-derived files out of the serving path unless they are useful for debugging; serving should continue reading from `data/<day>`.
7. Decide how to handle missing embedding secrets:
   - current behavior logs a warning and returns `0`
   - this should not block source publishing or `joined.json`/`unique.json` generation

## Edge Cases

- Only one source publishes: rebuild derived files from the newly published source plus preserved live data from the other source.
- No source publishes for a day: do not rebuild derived files, because live source data did not change.
- `data/<day>` does not exist before first successful publish: publishing should create it, then rebuild should generate derived files.
- `unique.json` has no rows: embeddings should be removed or left absent according to existing `data_to_embeddings(...)` behavior.
- Missing Google API key: `data.embeddings.json` may not be created, but `joined.json` and `unique.json` should still be valid.
- `collect_json_data(...)` walks nested directories: make sure it does not ingest `joined.json`, `unique.json`, or unrelated `data.json` files outside source directories.

## Verification

- Add tests or a temporary-directory harness that creates:
  - live `eventbrite/data.json`
  - live `meetup/data.json`
  - staged replacement for one source
  - then publishes and rebuilds
- Use the targeted provider/day fetch CLI only to refresh one provider's staged source data for manual publish/rebuild testing:

  ```bash
  python web/fetch/main.py meetup today
  python web/fetch/main.py eventbrite today
  ```

  Targeted mode should not collect, dedupe, embed, or publish by itself.
- Verify `joined.json` includes both the newly published source and the preserved source.
- Verify `unique.json` is regenerated after `joined.json`.
- Verify `data.embeddings.json` is regenerated when a Google API key is available, or that a warning is logged and the workflow continues when it is not.
- Manual check:

  ```bash
  python web/fetch/main.py
  ls data/*/joined.json data/*/unique.json
  ```

- Expected result:
  - derived live files always match the live source directories after a successful publish
  - derived files are not rebuilt from incomplete staging data when one source returned zero
