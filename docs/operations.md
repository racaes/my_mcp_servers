# Runtime Operations

## Health checks

- **STDIO transport**: rely on process exit code (`0` indicates success). Use the
  `tests/test_health_endpoints.py::test_stdio_launch_handles_missing_binary`
  scenario as a template for asserting failure modes.
- **HTTP transport**: probe `GET /status` (implemented in
  `servers/markitdown/app.py`) for liveness. Expect `{"status": "ok"}` while the
  server is healthy.

## Logging

- Configure log level and file destination via `servers/markitdown/config.toml`.
- Enable file logging by pointing `logging.file` to a writable path (defaults to
  `logs/markitdown.log`).
- Logs streamed from the underlying STDIO process are tagged as `stdout` or
  `stderr` for quick triage.

## Error handling

- The STDIO launcher forwards non-zero exit codes to the caller, allowing VS Code
  or supervising processes to react appropriately.
- HTTP conversion errors return `500` with an explanatory message when the
  `markitdown` dependency is misconfigured.
- All launch scripts surface exceptions via non-zero exit codes, making them
  shell-friendly for automation.

## Observability roadmap

- Add structured logging (`jsonlogger` or `structlog`) for machine-parsable
  output.
- Emit metrics counters (successful conversions, failures) via StatsD or
  Prometheus once adoption grows.
- Integrate optional OpenTelemetry exporters for traceability across multiple
  MCP servers.
