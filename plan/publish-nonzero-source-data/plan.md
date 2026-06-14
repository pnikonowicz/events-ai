# Publish Only Nonzero Source Data

## Goal

Copy staged source data from `data_working/<day>/<source>` to `data/<day>/<source>` only when that source returned a nonzero fetch count. If a source returns zero results, leave the existing live source directory unchanged.

## Relevant Files And Functions

- `web/fetch/main.py`
  - `publish(eventbrite_amount, meetup_amount, data_path)`
  - calls to `publish_working_data(...)`
- `common/fetch_amounts.py`
  - `publish_working_data(source_name, source_dir, destination_dir)`
- `common/paths.py`
  - `DataPath.dir()`
  - `Paths.DATA_DIR`
  - `Paths.TEMP_LOCAL_DIR`

## Implementation Tasks

1. Define `publish_working_data(source_name, source_dir, destination_dir)` clearly:
   - `source_name`: source directory name such as `eventbrite` or `meetup`
   - `source_dir`: working `DataPath` for the day, rooted at `data_working`
   - `destination_dir`: live data root, usually `Paths.DATA_DIR`
2. Resolve paths:
   - working source: `<source_dir.dir()>/<source_name>`
   - live day: `<destination_dir>/<source_dir.day>`
   - live source: `<destination_dir>/<source_dir.day>/<source_name>`
3. Validate that the working source directory exists before publishing.
4. Create the live day directory if needed.
5. Replace only the target live source directory:
   - remove `data/<day>/<source>`
   - copy `data_working/<day>/<source>` into that same location
6. Keep `publish(...)` responsible for deciding whether to publish based on nonzero counts.
7. Log skipped zero-result sources and successful source publications.

## Edge Cases

- Working source directory is missing despite a nonzero count: treat this as an error and do not delete the live source directory.
- Working source directory exists but has no `data.json`: treat this as suspicious; prefer failing or logging an error rather than replacing good live data.
- Destination day directory does not exist: create it.
- Destination source directory exists: replace only that source directory.
- One source has new data and the other returns zero: publish the successful source only and preserve the stale-but-valid live data for the zero-result source.
- Copy operation fails halfway: avoid deleting live data until validation passes; if practical, copy to a temporary destination and then swap.

## Verification

- Unit-test `publish_working_data(...)` using temporary directories:
  - nonzero source staging directory replaces only the matching live source
  - missing staging source does not delete live source
  - publishing `eventbrite` does not modify `meetup`
- Use the targeted provider/day fetch CLI to create fresh staging data for one provider when manually inspecting publish behavior:

  ```bash
  python web/fetch/main.py meetup today
  python web/fetch/main.py eventbrite today
  ```

  Targeted mode should stop after writing `data_working/<day>/<source>`, so any live `data/` changes during this verification should come from the publish helper or full workflow being tested, not from the targeted fetch itself.
- Manual filesystem check:

  ```bash
  find data_working -maxdepth 3 -type f
  find data -maxdepth 3 -type f
  ```

- Run the full fetch workflow or a callable workflow test with one source mocked or forced to zero and verify:
  - the zero-result source directory in `data/` remains unchanged
  - the nonzero source directory in `data/` is replaced

- Expected result:
  - live source data changes only when that specific source has new staged data
  - zero-result source fetches do not wipe live data
