# System Prerequisites

## Linux limits

For production Linux installations, configure process limits for the MonkDB user (and root/superuser if required by your environment):

- File descriptors: soft/hard `unlimited`
- Memory lock: soft/hard `unlimited`
- Threads: soft/hard `4096`
- Virtual memory (Linux): soft/hard `unlimited`
- `vm.max_map_count` (Linux): `262144`

Typical files:

- `/etc/security/limits.conf`
- `/etc/sysctl.conf` or `/etc/sysctl.d/*.conf`

Example:

```conf
# /etc/security/limits.conf
monkdb soft nofile unlimited
monkdb hard nofile unlimited
monkdb soft memlock unlimited
monkdb hard memlock unlimited
monkdb soft nproc 4096
monkdb hard nproc 4096
monkdb soft as unlimited
monkdb hard as unlimited
```

```conf
# /etc/sysctl.d/99-monkdb.conf
vm.max_map_count=262144
```

Apply sysctl changes:

```bash
sudo sysctl --system
```

## JVM and heap

MonkDB is JVM-based. Set heap via `MONKDB_HEAP_SIZE`.

- Start with about 25% of machine RAM.
- Keep heap between `1GB` and about `30.5GB` for Compressed Oops efficiency.
- If `bootstrap.memory_lock: true` is used, ensure `memlock` limits permit lock.

## Swap

Avoid swap for MonkDB processes. Prefer:

- `bootstrap.memory_lock: true`
- Host-level swap tuning/disabling per your ops policy

## Network and ports

Default ports commonly used:

- HTTP: `6000`
- PGWire: `5432`
- Transport: `6100`

Use firewall rules and TLS in production.

## `psql` client installation

Install `psql` client on any machine from which you run SQL administration or tests.

### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install -y postgresql-client
```

### RHEL / CentOS / Rocky / AlmaLinux

```bash
sudo dnf install -y postgresql
```

### macOS (Homebrew)

```bash
brew install libpq
brew link --force libpq
```

### Verify

```bash
psql --version
```
