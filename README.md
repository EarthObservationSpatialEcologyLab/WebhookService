# Webhook Service Submodule

I chose to go with a standalone service as it doesn't necessarily fit into the responsibilities of the backend of the dashboard app. Logical JSON handling only exists within the input handling trigger in the postgres database for a single source of truth for rules + to reduce overhead of ingress on the system hosting the docker.

<img width="382" height="283" alt="image" src="https://github.com/user-attachments/assets/396345be-ab6d-4020-b36b-6c6667494d92" />

## Quick Start
To start the service, first create a `.env` file with the following contents:
```env
  DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=verify-ca
  CA_CERT=<contents of ca.pem>
  WEBHOOK_SECRET=<secret>

```
Then:
`docker compose up --build`

The service will then be started at the port specified in the docker files.

*Note* The easiest way to expose to the internet was using the service [Render](https://render.com/)

## Components

### main.py
Home of the endpoints, currently only offloads logic to helpers.

### hardwarioCon.py : hardwario connector helper
Currently a passthrough as no logic is needed with the current development webhook setup (June 16, 2026).

### bluesCon.py : placeholder file for future endpoint logic handling
Not yet integrated.

### dbCon.py : Postgres connector helper
Contains the environment variable calls for the db and a method to insert the JSON directly into a raw input table.

## TODO:
- [ ]   Add docker compose reference in main dashboard (IoTDashboardFrontendBackend)
- [ ]   Expose the latest state of the input trigger as a text response (bash script)
- [ ]   Validate system with unit + integration tests
