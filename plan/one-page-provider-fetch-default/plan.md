# Step 6: One-Page Provider Fetch Default

## Goal

When `web/fetch/main.py` fetches Meetup or Eventbrite data, each provider should fetch only one upstream results page by default.

The default should apply to both invocation modes:

```bash
python web/fetch/main.py
python web/fetch/main.py <meetup | eventbrite> <today | tomorrow | friday>
```

Keep the design open for an explicit future override, such as `max_pages`, without requiring callers to pass that value for the default one-page behavior.

## Relevant Files And Functions

- `web/fetch/main.py`
  - `fetch_all()`
  - `fetch_one(provider, query_date)`
  - calls to `fetch_eventbrite(...)` and `fetch_meetup(...)`
- `fetch/eventbrite/get_data.py`
  - `fetch(query_date, data_path)`
  - `fetch_from_eventbrite(target_day, raw_data_dir)`
  - `fetch_all_raw_html(target_day, number_of_pages)`
  - `get_number_of_pages_from_html(raw_html)`
- `fetch/meetup/get_data.py`
  - `fetch(query_date, data_path)`
  - `get_all_results(target_date, session=HTMLSession())`
- `tests/web/fetch/test_main_targeted_isolation.py`
  - orchestration tests for targeted and full fetch modes
- `tests/fetch/eventbrite/test_get_data_eventbrite.py`
  - Eventbrite pagination parsing coverage
- `tests/fetch/meetup/test_get_all_results.py`
  - Meetup cursor pagination coverage

## Implementation Tasks

1. Add an optional page limit parameter to both provider fetch entry points:
   - `fetch/eventbrite/get_data.py::fetch(query_date, data_path, max_pages=1)`
   - `fetch/meetup/get_data.py::fetch(query_date, data_path, max_pages=1)`
2. Thread the Eventbrite limit through `fetch_from_eventbrite(...)`.
   - Fetch page 1 once.
   - Continue writing page 1 to disk as the first raw result.
   - Do not refetch page 1 through `fetch_all_raw_html(...)`.
   - Fetch additional pages only when `max_pages > 1`.
   - Clamp the requested pages to the upstream `page_count` discovered from page 1.
3. Thread the Meetup limit through `get_all_results(...)`.
   - Treat one GraphQL request as one page.
   - Stop after the first request by default, even when `hasNextPage` is true.
   - Continue to stop early when the API returns no usable `data`.
4. Update `web/fetch/main.py` orchestration only if needed.
   - Existing calls should be able to rely on provider defaults.
   - If the implementation adds a shared constant, keep it near fetch orchestration and pass it explicitly to both providers.
5. Preserve existing output conventions.
   - Eventbrite still writes under `data_working/<day>/eventbrite`.
   - Meetup still writes under `data_working/<day>/meetup`.
   - Targeted mode still fetches only the selected provider and selected day.
6. Do not change collection, dedupe, embeddings, publishing, fetch count behavior, `QueryDate`, or source directory ownership rules.

## Edge Cases

- Eventbrite page 1 reports `page_count` greater than `1`: fetch only page 1 by default.
- Eventbrite page 1 reports `page_count` as `0`: keep the existing zero-result handling behavior.
- Eventbrite `max_pages` is higher than upstream `page_count`: fetch only available pages.
- Meetup first response has `hasNextPage: true`: fetch only the first GraphQL page by default.
- Meetup first response has no usable `data`: return an empty result list as it does now.
- `max_pages` is `None` or less than `1`: choose and document one behavior before implementation, preferably treating invalid limits as `1` to preserve the safer default.

## Verification

- Add provider-level unit tests that avoid network calls.
- Eventbrite tests should verify:
  - default `fetch_from_eventbrite(...)` returns and writes only page 1 when page 1 advertises multiple pages
  - `fetch_all_raw_html(...)` or the equivalent helper is not called for page 1 a second time
  - an explicit `max_pages=2` fetches page 1 and page 2 when both are available
- Meetup tests should verify:
  - default `get_all_results(...)` makes one request when `hasNextPage` is true
  - explicit `max_pages=2` makes two requests when cursors continue
  - zero or invalid page limits do not fetch unbounded pages
- Keep existing orchestration tests green to confirm full and targeted modes still dispatch the same providers and paths.
- Run the relevant test subset in the devcontainer:

  ```bash
  devcontainer exec --workspace-folder . python -m pytest tests/fetch/eventbrite tests/fetch/meetup tests/web/fetch
  ```

## Expected Result

- Full fetches and targeted fetches triggered through `web/fetch/main.py` fetch one upstream page per provider/day by default.
- The one-page default reduces network usage and runtime without changing output paths or downstream workflows.
- Provider internals still support a clear path to fetch more than one page explicitly in a future change or debugging workflow.
