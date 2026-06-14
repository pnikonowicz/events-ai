# Source

A source is an upstream event provider that fetches raw event data into the project.

Current sources:

- `eventbrite`
- `meetup`

Source data is stored under a day-specific provider directory:

```text
<root>/<day>/<source>
```

For live data, `<root>` is `data`:

```text
data/today/eventbrite
data/today/meetup
```

For staged fetch output, `<root>` is `data_working`:

```text
data_working/today/eventbrite
data_working/today/meetup
```

Each source owns only its own source directory. A fetch, cleanup, publish, or validation operation for one source must not remove or overwrite another source's directory for the same day.
