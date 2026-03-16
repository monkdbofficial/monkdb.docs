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

## FDC3 example

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

## ITCH / OUCH note

ITCH and OUCH readers expect framed binary input (2-byte length-prefixed messages).

```sql
COPY monkdb.itch_events FROM 'itch:///data/protocol-ingest/itch.bin' WITH (format='json') RETURN SUMMARY;
COPY monkdb.ouch_events FROM 'ouch:///data/protocol-ingest/ouch.bin' WITH (format='json') RETURN SUMMARY;
```
