# Step 1: Fetch Sources Into Working Data

## Goal

Fetch each source into `data_working/<day>/<source>` instead of writing directly to `data/<day>/<source>`.

This step only stages source fetch output. It should not publish staged data, rebuild derived files in `data/`, or update fetch counts.

## Relevant Files And Functions

- `common/paths.py`
  - `Paths.DATA_DIR`
  - `Paths.TEMP_LOCAL_DIR`
  - `DataPath`
- `web/fetch/main.py`
  - creation of `DataPath` instances for `Today`, `Tomorrow`, and `Friday`
  - calls to `fetch_eventbrite(...)` and `fetch_meetup(...)`
- `fetch/eventbrite/get_data.py`
  - `fetch(query_date, data_path)`
  - writes under `os.path.join(data_path.dir(), "eventbrite")`
- `fetch/meetup/get_data.py`
  - `fetch(query_date, data_path)`
  - writes under `os.path.join(data_path.dir(), "meetup")`

## Implementation Tasks

1. Keep `Paths.TEMP_LOCAL_DIR` as the canonical staging root, pointing at `<project>/data_working`.
2. Ensure `DataPath(day, base_dir=...)` reliably resolves `dir()` to `<base_dir>/<day>`.
3. In `web/fetch/main.py`, construct fetch paths with `DataPath(QueryDate.<Day>.day(), Paths.TEMP_LOCAL_DIR)`.
4. Pass those working `DataPath` objects to both source fetchers.
5. Keep source fetchers path-agnostic: they should continue deriving their own source directory as `os.path.join(data_path.dir(), "<source>")`.
6. Do not change the default `DataPath(day)` behavior for server reads; the default should continue pointing at `Paths.DATA_DIR`.
7. Ensure source fetchers clean or replace only their own working source directory, not the full day directory and not `data/`.

## Edge Cases

- A source returns zero results: the source may leave an empty `data_working/<day>/<source>` directory or partial raw files, but this step must not publish it.
- One source succeeds and the other fails: each source should be isolated under its own staging directory.
- Existing live data exists in `data/<day>`: this step must not modify it.
- Existing staged data exists in `data_working/<day>/<source>`: the fetcher should remove or overwrite only that source directory before writing fresh results.
- Friday is skipped on Thursday or Friday: no `data_working/friday` fetch output should be required in that path.

## Verification

- Prefer the targeted provider/day fetch CLI from Step 5 when smoke-testing a single provider without running publish, derived-data rebuild, or fetch-count updates:

  ```bash
  python web/fetch/main.py meetup today
  python web/fetch/main.py eventbrite today
  ```

- Use the no-argument fetch only when verifying the full default multi-day, both-provider fetch path:

  ```bash
  python web/fetch/main.py
  ```

- Confirm source output exists under the staging root:

  ```bash
  find data_working -maxdepth 3 -type f
  ```

- Confirm the live source directories were not touched by this step:

  ```bash
  git diff -- data
  ```

- Confirm path behavior directly:

  ```bash
  python - <<'PY'
  from common.paths import DataPath, Paths
  print(DataPath("today", Paths.TEMP_LOCAL_DIR).dir())
  print(DataPath("today").dir())
  PY
  ```

- Expected result:
  - staged source files are written under `data_working/<day>/eventbrite` and `data_working/<day>/meetup`
  - targeted CLI fetches write only the requested provider under `data_working/<day>/<source>`
  - default app reads still point at `data/<day>`
  - no publishing or fetch count behavior is introduced by this step
