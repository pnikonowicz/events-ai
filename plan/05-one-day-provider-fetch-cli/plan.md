# Step 5: One-Day Provider Fetch CLI

## Goal

Add a targeted testing mode to `web/fetch/main.py`:

```bash
python web/fetch/main.py <meetup | eventbrite> <today | tomorrow | friday>
```

This mode fetches only the selected provider for the selected named day and stops there. It should not collect, dedupe, create embeddings, publish data, or update total fetch amounts.

Running `python web/fetch/main.py` with no arguments should keep the current full multi-day, both-provider behavior.

## Relevant Files And Functions

- `web/fetch/main.py`
  - current no-argument fetch orchestration
  - calls to `fetch_eventbrite(...)` and `fetch_meetup(...)`
  - creation of `DataPath(..., Paths.TEMP_LOCAL_DIR)`
- `fetch/target_date.py`
  - `QueryDate.Today`
  - `QueryDate.Tomorrow`
  - `QueryDate.Friday`
- `fetch/eventbrite/get_data.py`
  - `fetch(query_date, data_path)`
- `fetch/meetup/get_data.py`
  - `fetch(query_date, data_path)`

## Implementation Tasks

1. Add CLI argument parsing in `web/fetch/main.py` using the standard library, preferably `argparse`.
2. Support two invocation modes:
   - no arguments: run the existing full fetch workflow unchanged
   - two arguments: run targeted one-provider, one-day fetch mode
3. Accept exactly these targeted mode values:
   - provider: `meetup` or `eventbrite`
   - day: `today`, `tomorrow`, or `friday`
4. Map day strings to existing query date objects:
   - `today` -> `QueryDate.Today`
   - `tomorrow` -> `QueryDate.Tomorrow`
   - `friday` -> `QueryDate.Friday`
5. Add a small orchestration helper, for example `fetch_one(provider, query_date)`, that:
   - builds `DataPath(query_date.day(), Paths.TEMP_LOCAL_DIR)`
   - calls only the selected provider fetch function
   - logs the selected provider, day, and returned count
   - exits with status `1` if the selected provider returns `0`
6. Refactor the current `if __name__ == "__main__"` block into callable functions so normal fetch behavior and targeted fetch behavior can be tested without network calls.
7. Do not change provider internals, `QueryDate`, output directory conventions, embedding, dedupe, publish helpers, or fetch count helpers.

## Edge Cases

- Invalid provider: fail through argument parsing with a nonzero exit.
- Invalid day: fail through argument parsing with a nonzero exit.
- Only one targeted argument is provided: fail through argument parsing with a nonzero exit.
- Targeted fetch returns zero results: log the failure and exit nonzero.
- Targeted Eventbrite fetch should only write under `data_working/<day>/eventbrite`.
- Targeted Meetup fetch should only write under `data_working/<day>/meetup`.
- Existing no-argument behavior should still fetch both providers for today and tomorrow, and Friday when allowed by the existing weekday logic.

## Verification

- Add tests for CLI orchestration without network calls by monkeypatching provider fetch functions.
- Cover:
  - `eventbrite today` calls only Eventbrite with `QueryDate.Today` and a `data_working/today` path
  - `meetup friday` calls only Meetup with `QueryDate.Friday` and a `data_working/friday` path
  - no-argument invocation still dispatches the existing full fetch workflow
  - invalid provider exits nonzero
  - invalid day exits nonzero
  - targeted fetch returning `0` exits nonzero
- Run the relevant pytest subset:

  ```bash
  pytest tests/web/fetch tests/fetch/test_target_date.py
  ```

## Expected Result

- Developers can quickly fetch one provider for one named day while testing later plans:

  ```bash
  python web/fetch/main.py meetup today
  python web/fetch/main.py eventbrite friday
  ```

- Targeted mode writes only provider fetch output to `data_working/<day>/<source>`.
- Targeted mode does not modify derived live data, embeddings, published data, or fetch counts.
- Earlier plan verification should use targeted mode as the preferred live-provider smoke test, and reserve no-argument `python web/fetch/main.py` for full workflow checks that intentionally publish, rebuild derived data, and update counts.
- The existing full fetch command remains backward compatible:

  ```bash
  python web/fetch/main.py
  ```
