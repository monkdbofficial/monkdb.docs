# DROP ANALYSER

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DDL and Administration |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires DDL/administrative privilege according to target object scope. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
DROP ANALYZER analyzer_ident;
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use during planned schema and runtime administration changes.
- Use in automation pipelines with environment-specific validation and rollback strategy.

## When Not to Use

- Avoid during incident windows unless the command is part of approved mitigation.
- Avoid schema changes in peak traffic windows without staged rollout.

## Common Errors and Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Permission denied / unauthorized | Missing privilege on object or cluster scope | Re-run with required grants or elevated admin role. |
| Analysis/parse error | Syntax variant or object shape mismatch | Compare with canonical syntax and object definition. |
| Runtime failure under load | Resource limits, breaker pressure, or node state transitions | Check `sys.jobs`, `sys.operations`, `sys.checks`, and retry after mitigation. |

## Cross-References

- [SQL Command Catalog](../08-command-catalog.md)
- [SQL Commands Index](./README.md)
- [SQL Reference Overview](../01-sql-reference.md)

## Detailed Reference
The `DROP ANALYZER` statement is used to remove a custom analyzer from the MonkDB cluster.

## SQL Statement

```sql
DROP ANALYZER analyzer_ident;
```

Where `analyzer_ident` is the name of the custom analyzer to be deleted.

## Description

Custom analyzers in MonkDB are user-defined components that process text for full-text search purposes. These analyzers typically consist of tokenizers, token filters, and character filters. Once created, they can be applied to full-text indices for tables. The `DROP ANALYZER` statement allows users to remove such analyzers when they are no longer needed.

When executed, the analyzer is removed from the cluster, and any full-text indices that depend on it will no longer function correctly unless reconfigured with another analyzer.

## Example

### Create a Custom Analyzer

```sql
CREATE ANALYZER firstname_synonyms (
    TOKENIZER lowercase,
    TOKEN_FILTERS (
        _ WITH (
            type = 'synonym',
            synonyms_path = 'synonyms-solr.txt'
        )
    )
);
```

The `CREATE ANALYZER` statement defines a new analyzer named `firstname_synonyms`, which uses a synonym file (synonyms-solr.txt) for token filtering.

### Drop the Custom Analyzer

```sql
DROP ANALYZER firstname_synonyms;
```

The `DROP ANALYZER` statement removes this analyzer from the cluster.

## Considerations

- Dropping an analyzer will affect any indices relying on it. Ensure that no active tables or queries depend on the analyzer before removing it.
- MonkDB does not support editing an existing analyzer directly. If modifications are required, you must drop the existing analyzer and recreate it with updated parameters
- If you attempt to drop an analyzer that does not exist, MonkDB will raise an error unless handled with additional logic (e.g., checking existence beforehand).

---

## See Also

- [Create an analyzer](./25_CREATE_ANALYSER.md)
