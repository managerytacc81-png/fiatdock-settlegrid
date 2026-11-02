"""
Unit tests for FiatDock & SettleGrid MCP Gateway
"""

import base64
import json
import time
import unittest
from mcp_monetization_gateway import (
    FiatDockx402Verifier,
    SettleGridMiddleware,
    MonetizedFeedReaderService
)

class TestMCPGateway(unittest.TestCase):
    def test_unauthenticated_request_triggers_402(self):
        resp = MonetizedFeedReaderService.execute_read_feed("https://example.com/rss.xml")
        self.assertEqual(resp["status_code"], 402)
        self.assertEqual(resp["status"], "PAYMENT_REQUIRED")
        self.assertIn("supported_payment_rails", resp)

    def test_valid_x402_payment_proof(self):
        valid_payload = {
            "tx_hash": "0xabc123456789def",
            "amount_usd": 0.05,
            "network": "base_mainnet",
            "timestamp": int(time.time())
        }
        b64_proof = base64.b64encode(json.dumps(valid_payload).encode("utf-8")).decode("utf-8")

        valid, msg = FiatDockx402Verifier.verify_payment_proof(b64_proof, 0.01)
        self.assertTrue(valid)

        # Test service execution with proof
        resp = MonetizedFeedReaderService.execute_read_feed("https://example.com/rss.xml", x402_proof=b64_proof)
        self.assertEqual(resp["status"], "SUCCESS")
        self.assertIn("FiatDock", resp["settled_via"])

    def test_insufficient_x402_payment(self):
        short_payload = {
            "tx_hash": "0xabc123456789def",
            "amount_usd": 0.005,
            "network": "base_mainnet"
        }
        b64_proof = base64.b64encode(json.dumps(short_payload).encode("utf-8")).decode("utf-8")
        valid, msg = FiatDockx402Verifier.verify_payment_proof(b64_proof, 0.01)
        self.assertFalse(valid)
        self.assertIn("Insufficient payment", msg)

    def test_valid_settlegrid_token(self):
        header_b64 = base64.urlsafe_b64encode(b'{"alg":"HS256"}').decode("utf-8").rstrip("=")
        payload = {
            "agent_id": "agent_alpha_01",
            "rail": "stripe_mpp",
            "exp": int(time.time()) + 3600
        }
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8").rstrip("=")
        token = f"Bearer sg_test.{payload_b64}.mocksignature"

        verifier = SettleGridMiddleware()
        valid, msg = verifier.verify_agent_token(token)
        self.assertTrue(valid)

        resp = MonetizedFeedReaderService.execute_read_feed("https://example.com/rss.xml", auth_token=token)
        self.assertEqual(resp["status"], "SUCCESS")
        self.assertIn("SettleGrid", resp["settled_via"])

if __name__ == "__main__":
    unittest.main()
