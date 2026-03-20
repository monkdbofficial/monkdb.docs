# Financial Protocol Ingest (FIX, FDC3, ITCH, OUCH)

<div class="feature-tags"><span class="gh-label gh-label-release">26.3.2</span><span class="gh-label">FIX</span><span class="gh-label">FDC3</span><span class="gh-label">ITCH</span><span class="gh-label">OUCH</span></div>

MonkDB includes protocol ingest plugin support via custom `COPY FROM` URI schemes.

## Supported schemes

- `fix://`
- `fdc3://`
- `itch://`
- `ouch://`

URI rule:

- Must use absolute local path
- Host component is not supported
- Example: `fix:///data/protocol-ingest/fix.log`

## FIX example

```sql
CREATE TABLE monkdb.fix_events (
  protocol STRING,
  beginString STRING,
  bodyLength STRING,
  msgType STRING,
  msgSeqNum STRING,
  senderCompId STRING,
  targetCompId STRING,
  sendingTime STRING,
  clOrdId STRING,
  orderId STRING,
  symbol STRING,
  side STRING,
  orderQty STRING,
  ordType STRING,
  price STRING,
  timeInForce STRING,
  execType STRING,
  ordStatus STRING,
  checkSum STRING,
  tags OBJECT(DYNAMIC)
) WITH (number_of_replicas = 0, column_policy = 'dynamic');

COPY monkdb.fix_events
FROM 'fix:///data/protocol-ingest/fix.log'
WITH (format='json', fix_delimiter='pipe')
RETURN SUMMARY;
```

`fix_delimiter` allowed values:

- `auto`
- `soh`
- `pipe`

`fix_delimiter` behavior and impact:

- `auto` (default):
  - Per line, MonkDB checks if `SOH` (`\u0001`) exists anywhere in the line.
  - If present, it parses using `SOH`; otherwise it parses using `|`.
  - Best default for mixed historical files and most migrations.
- `soh`:
  - Forces `SOH` delimiter parsing for all lines.
  - Use when the feed is guaranteed to be native FIX framing with `SOH`.
- `pipe`:
  - Forces `|` delimiter parsing for all lines.
  - Use for log exports where `SOH` was replaced by `|` for readability.

Operational notes:

- If delimiter mode does not match the actual input delimiter, parsing may still succeed but with degraded output
  (for example, only the first tag may be parsed correctly and remaining tags can collapse into one value).
- Invalid/non-FIX lines still fail through normal `COPY` error handling.
- For best data quality, choose `soh` or `pipe` when your source format is known and stable; otherwise use `auto`.

## FDC3 ingest

FDC3 ingest is supported through the `fdc3://` scheme.

Input model:

- Line-oriented JSON input (typically NDJSON).
- Empty lines are skipped.
- Each non-empty line is transformed into exactly one JSON object for `COPY`.

Line conversion behavior:

- If the input line is a JSON object:
  - `protocol: "fdc3"` is added only when missing.
  - existing fields (for example `type`, `id`, `src`) are preserved.
- If the input line is a non-object JSON value (array/string/number/bool/null):
  - output is wrapped as:
    - `protocol: "fdc3"`
    - `payload: <original_json_value>`
- Invalid JSON lines fail through normal `COPY` error handling.

Notes:

- Use `WITH (format='json')` for `COPY`.
- Absolute file paths are required in the URI.
- Glob patterns are supported through local file expansion (for example, `fdc3:///data/protocol-ingest/*.ndjson`).

Typical FDC3 context ingest:

```sql
CREATE TABLE monkdb.fdc3_events (
  protocol STRING,
  type STRING,
  id OBJECT(DYNAMIC),
  src STRING
) WITH (number_of_replicas = 0, column_policy = 'dynamic');

COPY monkdb.fdc3_events
FROM 'fdc3:///data/protocol-ingest/fdc3.ndjson'
WITH (format='json')
RETURN SUMMARY;
```

Example transformed output for a non-object input line:

- Input line: `[{"ticker":"AAPL"}]`
- Emitted JSON line: `{"protocol":"fdc3","payload":[{"ticker":"AAPL"}]}`

## ITCH ingest

ITCH ingest is supported through the `itch://` scheme.

Input framing requirements:

- 2-byte big-endian message length
- followed by message payload bytes

Each decoded ITCH payload is emitted as one JSON line and ingested through `COPY`.

Current typed decode coverage:

- `S` (System Event)
- `R` (Stock Directory)
- `A` (Add Order - No MPID Attribution)

Unknown ITCH message types are emitted with generic metadata and `payload_hex`.

Notes:

- Use `WITH (format='json')` for `COPY`.
- Price fields are emitted as fixed 4-decimal strings (for example, `123.4500`).

```sql
CREATE TABLE monkdb.itch_events (
  protocol STRING,
  message_type STRING,
  event_code STRING,
  stock STRING,
  shares LONG,
  price STRING,
  stock_locate INTEGER
) WITH (column_policy='dynamic');

COPY monkdb.itch_events
FROM 'itch:///data/protocol-ingest/itch.bin'
WITH (format='json')
RETURN SUMMARY;
```

## OUCH ingest

OUCH ingest is supported through the `ouch://` scheme.

Input framing requirements:

- 2-byte big-endian message length
- followed by message payload bytes

Each decoded OUCH payload is emitted as one JSON line and ingested through `COPY`.

Current typed decode coverage:

- `O` (Enter Order)
- `U` (Replace Order)
- `X` (Cancel Order)
- `A` (Order Accepted)

Unknown OUCH message types are emitted with generic metadata and `payload_hex`.

Notes:

- Use `WITH (format='json')` for `COPY`.
- Price fields are emitted as fixed 4-decimal strings (for example, `123.4500`).

```sql
CREATE TABLE monkdb.ouch_events (
  protocol STRING,
  message_type STRING,
  order_token STRING,
  side STRING,
  shares LONG,
  stock STRING,
  price STRING,
  cancel_shares LONG
) WITH (column_policy='dynamic');

COPY monkdb.ouch_events
FROM 'ouch:///data/protocol-ingest/ouch.bin'
WITH (format='json')
RETURN SUMMARY;
```
