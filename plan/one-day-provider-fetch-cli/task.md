# Step 5: One-Day Provider Fetch CLI Tasks

- [x] Add standard-library CLI parsing in `web/fetch/main.py`.
  - Support no arguments as the existing full fetch workflow.
  - Support exactly two targeted arguments: `<provider> <day>`.
  - Restrict provider choices to `meetup` and `eventbrite`.
  - Restrict day choices to `today`, `tomorrow`, and `friday`.

- [x] Refactor fetch orchestration into callable functions.
  - Keep the current full multi-day, both-provider behavior available as a callable helper.
  - Keep the `if __name__ == "__main__"` block thin.
  - Ensure no-argument execution still runs the current workflow unchanged.

- [x] Add targeted fetch orchestration.
  - Add a helper such as `fetch_one(provider, query_date)`.
  - Build the path with `DataPath(query_date.day(), Paths.TEMP_LOCAL_DIR)`.
  - Call only the selected provider fetch function.
  - Log the selected provider, day, and returned count.
  - Exit nonzero when the selected provider returns `0`.

- [x] Map CLI day values to existing `QueryDate` values.
  - `today` maps to `QueryDate.Today`.
  - `tomorrow` maps to `QueryDate.Tomorrow`.
  - `friday` maps to `QueryDate.Friday`.

- [x] Keep targeted mode isolated from derived workflows.
  - Do not collect or dedupe staged data.
  - Do not create embeddings.
  - Do not publish data.
  - Do not update total fetch amounts.
  - Do not change provider internals, `QueryDate`, output directory conventions, or fetch count helpers.
