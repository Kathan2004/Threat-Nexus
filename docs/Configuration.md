# Configuration

Local configuration lives in `.env` at the root of the `threat-nexus` project.

Use `.env.example` as the template:

```bash
cp .env.example .env
```

Then edit `.env` and fill in the values you have.

## Important Files

- `.env`: your local real config. This may contain secrets.
- `.env.example`: safe template showing every supported variable.
- `core/config/settings.py`: Python settings model that reads the `.env` values.

## Required Core Config

These are needed for the platform itself:

- `JWT_SECRET`: secret used to sign API tokens. Required outside development, minimum 32 characters.
- `ADMIN_USERNAME` / `ADMIN_PASSWORD`: first admin account, created only when no users exist.
- `GRAFANA_ADMIN_PASSWORD`: Grafana admin password used by docker compose.
- `MONGODB_URI`: MongoDB connection string.
- `MONGODB_DATABASE`: MongoDB database name.
- `REDIS_URL`: Redis connection string.

## Optional Distribution Config

These are needed only if you want Discord publishing:

- `DISCORD_TOKEN`
- `DISCORD_GUILD_ID`

## Optional AI Config

Fill one or more if you want AI enrichment:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `ANTHROPIC_API_KEY`

If none are set, the backend uses the deterministic fallback enrichment provider.

## Source Plugin Config

Each source has an `*_ENABLED` flag plus source-specific credentials.

Public sources can be enabled without API keys where supported:

- `CISA_KEV_ENABLED=true`
- `NVD_ENABLED=true`
- `URLHAUS_ENABLED=true`
- `MALWAREBAZAAR_ENABLED=true`
- `RANSOMWARE_LIVE_ENABLED=true`

Commercial, authenticated, or self-hosted sources need extra config:

- VirusTotal: `VIRUSTOTAL_API_KEY`
- GreyNoise: `GREYNOISE_API_KEY`
- AbuseIPDB: `ABUSEIPDB_API_KEY`
- Shodan: `SHODAN_API_KEY`
- Censys: `CENSYS_API_ID`, `CENSYS_API_SECRET`
- GitHub: `GITHUB_TOKEN`
- Reddit: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`
- MISP: `MISP_BASE_URL`, `MISP_API_KEY`
- OpenCTI: `OPENCTI_BASE_URL`, `OPENCTI_TOKEN`
- IntelOwl: `INTELOWL_BASE_URL`, `INTELOWL_TOKEN`
- AlienVault OTX: `OTX_API_KEY`

## Runtime Collection Behavior

Collector plugins now receive runtime source settings before every collection run.

The collector runner:

1. Loads source records from MongoDB collection `source_configs`.
2. Applies the matching config to each discovered plugin by plugin name.
3. Skips disabled plugins.
4. Skips enabled plugins that are missing required credentials.
5. Uses configured base URLs and credentials for HTTP collection.
6. Reports missing credentials or unhealthy endpoints through plugin health checks.

If no source record exists yet, the backend uses the defaults from `core/services/source_config.py`.

## Frontend Settings

The frontend has a Settings page at `/settings`.

The page talks to these backend endpoints:

- `GET /settings/sources`: list source configuration status.
- `PUT /settings/sources/{source_id}`: update one source.

Secrets are write-only through the API. The backend stores which credential names are configured, but it does not return secret values to the browser.

This admin settings store is separate from `.env`. Use `.env` for boot-time platform settings such as MongoDB, Redis, JWT, Discord, and AI provider keys. Use the frontend settings page for source plugin credentials that operators may rotate from the UI.

The current implementation stores source credentials in MongoDB. For production, put MongoDB on encrypted storage and plan a follow-up change to envelope-encrypt secret values with KMS or Vault.
