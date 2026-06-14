# Step 4: Update Fetch Counts Only With New Data

## Goal

Update `data/fetch_amounts.json` only for sources that returned nonzero totals across the fetch run. If a source returns zero total results, preserve the previous displayed count for that source.

## Relevant Files And Functions

- `web/fetch/main.py`
  - total count aggregation for Eventbrite and Meetup
  - final calls to write fetch amounts
- `common/fetch_amounts.py`
  - `read_fetch_amounts_from_file(fetch_amount_file)`
  - `write_total_eventbrite_amount_to_file(fetch_amount_file, total_eventbrite_amount)`
  - `write_total_meetup_amount_to_file(fetch_amount_file, total_meetup_amount)`
  - `write_fetch_amounts_to_file(...)`
- `web/server/main.py`
  - `/api/fetch_amounts` or equivalent route that reads `Paths.FETCH_AMOUNTS`
- `web/static/query_entry.html`
  - count display behavior

## Implementation Tasks

1. Keep per-source total aggregation in `web/fetch/main.py`.
2. Preserve the existing count for any source with a total of `0`.
3. Update only the source field with a nonzero total.
4. Handle missing `fetch_amounts.json` by defaulting to:

   ```json
   {
     "eventbrite": 0,
     "meetup": 0
   }
   ```

5. Consider replacing source-specific write functions with one helper that updates a dictionary of nonzero source totals atomically.
6. Ensure writes create the parent `data/` directory if needed.
7. Keep count updates independent from source publish failures unless the workflow decides that counts should reflect only successfully published data.
8. Prefer writing counts after all day-level fetch and publish work completes.

## Edge Cases

- `fetch_amounts.json` is missing: create it with defaults plus any nonzero updates.
- `fetch_amounts.json` is malformed: fail clearly or recreate from defaults, depending on desired operational behavior.
- Eventbrite succeeds and Meetup returns zero: update `eventbrite`, preserve previous `meetup`.
- Meetup succeeds and Eventbrite returns zero: update `meetup`, preserve previous `eventbrite`.
- Both return zero: preserve the whole file and return a nonzero process exit as the current workflow does.
- Source fetch returns nonzero but publish fails: avoid displaying a count for data that was not actually published, unless the team explicitly wants fetch counts rather than published counts.

## Verification

- Unit-test count updates with temporary files:
  - existing counts plus `eventbrite=10`, `meetup=0` preserves old Meetup count
  - existing counts plus `eventbrite=0`, `meetup=12` preserves old Eventbrite count
  - both zero preserves both
  - missing file is initialized
- Use the targeted provider/day fetch CLI from Step 5 to verify provider fetches without changing `data/fetch_amounts.json`:

  ```bash
  cat data/fetch_amounts.json
  python web/fetch/main.py meetup today
  cat data/fetch_amounts.json
  ```

  The before and after count files should match because targeted mode stops before total aggregation and count updates.
- Manual check:

  ```bash
  cat data/fetch_amounts.json
  python web/fetch/main.py
  cat data/fetch_amounts.json
  ```

- If practical, mock fetch totals in `web/fetch/main.py` tests rather than making network calls.
- Expected result:
  - UI counts do not drop to zero because of a transient source failure
  - counts only change when new data exists for that source
