# FiatDock & SettleGrid MCP Distribution Listing Packet
**Asset:** Monetized Feed-Reader MCP Server (`codegeist-mcp` lineage).
**Date:** November 02, 2026 | **Operator:** Robert Ketler

---

## 1. FiatDock Listing Configuration (`fiatdock.yml`)
```yaml
name: feed-reader-mcp
display_name: High-Speed Web & RSS Feed Reader for AI Agents
description: Production-grade feed parser and content extractor for autonomous agents. Returns clean JSON markdown.
category: developer-tools
pricing:
  model: per_call
  unit_amount_usd: 0.01
  currency: USD
payout:
  network: base_mainnet
  wallet_address: '0x47bE0d5d7B8e86A45F24c6F1c4B952bC88E2368C'
endpoint:
  url: 'https://feed-reader-mcp.crescentic.net/sse'
  transport: sse
```

## 2. SettleGrid Listing Configuration (`settlegrid.json`)
```json
{
  "service_name": "agentic-feed-reader-pro",
  "description": "Multi-protocol accessible feed ingestion API. Supports Stripe Connect, Google AP2, and Coinbase x402.",
  "pricing_tier": {
    "per_call_usd": 0.01,
    "free_quota_monthly": 100,
    "take_rate_pct": 5.0
  },
  "supported_agent_auth": [
    "stripe_mpp",
    "coinbase_x402",
    "openai_acp",
    "google_ap2",
    "circle_nanopayments"
  ],
  "payout_account": {
    "method": "stripe_connect",
    "currency": "usd"
  }
}
```

## 3. Immediate Action Checklist
1. [ ] Log in to [fiatdock.com/sell](https://fiatdock.com/sell) with Base wallet and paste YAML manifest.
2. [ ] Submit `settlegrid.json` to SettleGrid Developer Portal ([settlegrid.ai](https://settlegrid.ai)).
3. [ ] Monitor initial micro-transactions across both platforms.