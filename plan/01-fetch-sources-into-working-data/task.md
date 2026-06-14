# Step 1: Fetch Sources Into Working Data Tasks

- [ ] Keep `Paths.TEMP_LOCAL_DIR` as the canonical staging root.
  - Ensure it points at `<project>/data_working`.
  - Do not introduce a second staging constant or alternate working-data root.

- [ ] Verify `DataPath` supports explicit base directories.
  - Ensure `DataPath(day, base_dir=...)` resolves `dir()` to `<base_dir>/<day>`.
  - Preserve the default `DataPath(day)` behavior so server reads continue using `Paths.DATA_DIR`.

- [ ] Update full fetch orchestration to use working paths.
  - In `web/fetch/main.py`, construct fetch paths with `DataPath(QueryDate.<Day>.day(), Paths.TEMP_LOCAL_DIR)`.
  - Apply this to `Today`, `Tomorrow`, and `Friday` wherever those fetch paths are created.
  - Pass the working `DataPath` objects to both source fetchers.

- [ ] Keep source fetchers path-agnostic and source-scoped.
  - Leave provider output rooted at `os.path.join(data_path.dir(), "<source>")`.
  - Ensure Eventbrite only cleans or replaces `data_working/<day>/eventbrite` for a staged fetch.
  - Ensure Meetup only cleans or replaces `data_working/<day>/meetup` for a staged fetch.
  - Do not remove or overwrite the full day directory or another source directory.

- [ ] Keep this step limited to staging fetched source data.
  - Do not publish staged data into `data/`.
  - Do not rebuild derived files in `data/`.
  - Do not create embeddings.
  - Do not update fetch counts.

- [ ] Cover path behavior with focused tests or direct verification.
  - Verify `DataPath("today", Paths.TEMP_LOCAL_DIR).dir()` points under `data_working/today`.
  - Verify `DataPath("today").dir()` still points under `data/today`.
  - Verify provider fetch calls receive working `DataPath` objects.

- [ ] Smoke-test staged source output.
  - Prefer the targeted provider/day fetch CLI from Step 5:
    - `python web/fetch/main.py meetup today`
    - `python web/fetch/main.py eventbrite today`
  - Use `python web/fetch/main.py` only for the full default multi-day, both-provider path.
  - Confirm source output appears under `data_working/<day>/<source>`.

- [ ] Confirm live data is untouched by this step.
  - Check `git diff -- data`.
  - Ensure existing `data/<day>` source directories are not modified by staging fetches.

- [ ] Preserve existing Friday skip behavior.
  - Keep the existing Thursday or Friday skip logic intact.
  - Do not require `data_working/friday` output when Friday fetches are skipped.
