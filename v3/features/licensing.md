# License Management

<div class="feature-tags"><span class="gh-label">Licensing</span><span class="gh-label">Cluster Operations</span></div>

MonkDB licensing can be managed through SQL and monitored through `sys.cluster` license fields.

## Apply license key

```sql
SET LICENSE KEY 'MONK1....';
```

## Inspect license status

```sql
SELECT
  "license"['status'],
  "license"['valid'],
  "license"['allowed_nodes'],
  "license"['current_nodes'],
  "license"['error']
FROM sys.cluster;
```

## Deployment runbooks

- [License Provisioning for Larger Clusters](../operations/license-provisioning-large-cluster.md)

## Relevant settings

- `license.key`
- `license.expiry_grace`
- `license.block_when_oversized`

## Enforcement modes

`sys.cluster.license.enforcement` indicates effective mode:

- `normal`
- `read_only`
- `admin_only`
