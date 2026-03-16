# Security, Authentication, RBAC

## Authentication model

MonkDB supports authenticated access across SQL endpoints with host-based/auth provider configuration.

Production guidance:

- Avoid broad trust authentication in production.
- Use strong password/cert-based flows.
- Restrict local development shortcuts to non-production profiles.

## Authorization model (RBAC)

Privileges are granted to users/roles with scope controls.

Core privilege families:

- `DQL` (read/query)
- `DML` (insert/update/delete/copy from)
- `DDL` (create/alter/drop)
- `AL` (administrative operations)

## Users and roles

Common lifecycle commands:

- `CREATE USER`, `ALTER USER`, `DROP USER`
- `CREATE ROLE`, `ALTER ROLE`, `DROP ROLE`
- `GRANT`, `REVOKE`, `DENY`

## Row and column governance

MonkDB governance policies provide:

- Row filtering (`scope='row_filter'`)
- Column masking (`scope='column_mask'`)

This gives policy-based row-level and column-level control without application-only filtering.

## Secure communications

Enable TLS/SSL for:

- HTTP endpoint
- PGWire endpoint
- Inter-node transport channel

Use mTLS for stricter node/client identity enforcement where required.

## Hardening checklist

- Disable default/trust auth modes in production.
- Enforce least-privilege grants.
- Separate admin users from app users.
- Rotate passwords/certs.
- Audit high-risk statements and privilege changes.
- Gate local FDW access (`fdw.allow_local=false` unless required).
