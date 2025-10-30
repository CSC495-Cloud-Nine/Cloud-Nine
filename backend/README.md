Cloud9 demo backend
===================

This is a minimal Node.js HTTP server used in the demo to accept registration requests.

How it works
- The server exposes POST /api/register which accepts JSON: { firstName, lastName, age, email, password }
- Password is hashed with a random salt using Node's built-in crypto.scryptSync and stored in `users.json`.
- `users.json` is a simple JSON array used as a placeholder storage. Replace this with your real database later.

Run locally
---------
1. Make sure you have Node.js (>=12) installed.
2. From the project root, start the server:

   node backend/server.js

3. The server listens on port 3000 by default. Register by POSTing to:

   http://localhost:3000/api/register

Notes & next steps
- This is intentionally dependency-free. For production, replace the storage layer with a proper DB (Postgres, MongoDB, etc.).
- Use HTTPS in production. This demo sends passwords over HTTP only for local convenience.
- Consider adding input sanitization, rate-limiting, and email verification in a real system.
