# EShop rules for FR-02, FR-10 and FR-15

Use the actual requirement/API specification supplied by the user as the source of truth. The following is a compact routing aid for the HW06 version and must be reconciled with the tested commit.

## FR-02 – Login and account lockout

- Main endpoint: `POST /api/login` with `email` and `password`.
- Each failed login increments the counter by exactly 1.
- Three or more consecutive failures lock the account for 30 seconds.
- Error messages must not reveal inappropriate details.
- Successful login returns JWT; authenticated requests use `Authorization: Bearer <token>`.
- Model email/password partitions, the 0/1/2/3 attempt boundary, time boundary, reset after success, concurrency/replay if feasible, response schema and sensitive-field exclusion.

## FR-10 – Order state machine

- Admin transition endpoint: `PUT /api/admin/orders/:id/status`.
- User cancellation endpoint: `PUT /api/orders/:id/cancel`.
- Allowed path: `pending → confirmed → shipping → delivered`.
- Cancellation: `pending → canceled`, `confirmed → canceled`.
- `delivered` and `canceled` are final states.
- User cannot cancel `shipping`; admin actions must follow the state machine.
- Cover current × target × actor, and assert that rejected transitions leave state unchanged.

## FR-15 – Product CRUD

- API family: `GET /api/products`, `GET /api/products/:id`, `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id`.
- Name is required and at most 255 characters.
- Price is required and positive (`> 0`).
- Category is required and must exist.
- Mutations require valid authentication and `role=admin` under FR-12.
- Updating one product must not change any other product.
- Cover CRUD lifecycle, field partitions/boundaries, resource IDs, role/token matrix, injection/output handling, schema and cleanup.

## Applicable security routing

- SEC-01: password not stored plaintext; mostly FR-02/setup evidence, not directly provable only from login response.
- SEC-02: protected APIs require valid JWT.
- SEC-03: admin APIs enforce admin role, not token presence alone.
- SEC-04: user-controlled displayed data is safely escaped; API test can plant/observe data, but UI rendering evidence may be needed.
- SEC-05: database queries are parameterized; use behavioral injection tests without claiming implementation proof from one passing input.
- SEC-06 and SEC-07 are outside the selected feature scope unless shared behavior creates a justified cross-feature test.
