# Java Flight Recorder (JFR)

Use JFR for deep JVM/runtime analysis with low overhead.

## Start recordings with `jcmd`

```bash
jcmd <pid> JFR.start duration=60s filename=/data/recording1.jfr
jcmd <pid> JFR.start duration=300s filename=/data/recording2.jfr settings=profile
```

## When to use

- Intermittent latency spikes.
- GC pauses not explained by basic metrics.
- CPU hotspots and lock contention.

## Recommended practice

- Capture short focused recordings under realistic load.
- Correlate recording window with query/system telemetry from `sys.jobs*` and `sys.operations*`.
