"""
Sahayak - Mock Database Seed Data
Canonical test merchants and initial system state.
"""

from typing import Dict, Any
from copy import deepcopy

# Initial DB seed state
INITIAL_DATA: Dict[str, Any] = {
    "merchants": {
        "M_1092": {
            "merchant_id": "M_1092",
            "business_name": "Sharma General Store",
            "owner_name": "Ramesh Sharma",
            "phone_number": "+919876543210",
            "registered_address": "Shop 14, Main Market, Indiranagar, Bengaluru",
            "tier": "GOLD",
            "is_fraud_flagged": false if False else False,
            "active_disputes": 0,
            "hardship_flag": False,
            "kyc_status": "VERIFIED",
            "daily_limit_inr": 200000.0,
            "monthly_limit_inr": 5000000.0
        },
        "M_4401": {
            "merchant_id": "M_4401",
            "business_name": "Patel Electronics",
            "owner_name": "Ananya Patel",
            "phone_number": "+919822334455",
            "registered_address": "Plot 88, Electronic City Phase 1, Bengaluru",
            "tier": "GOLD",
            "is_fraud_flagged": False,
            "active_disputes": 0,
            "hardship_flag": False,
            "kyc_status": "VERIFIED",
            "daily_limit_inr": 500000.0,
            "monthly_limit_inr": 10000000.0
        },
        "M_8819": {
            "merchant_id": "M_8819",
            "business_name": "Singh Traders",
            "owner_name": "Vikram Singh",
            "phone_number": "+919811223344",
            "registered_address": "Warehouse 4, APMC Yard, Yeshwanthpur, Bengaluru",
            "tier": "PLATINUM",
            "is_fraud_flagged": True,  # Fraud flag active for escalation demo
            "active_disputes": 1,
            "hardship_flag": False,
            "kyc_status": "VERIFIED",
            "daily_limit_inr": 1000000.0,
            "monthly_limit_inr": 20000000.0
        },
        "M_5510": {
            "merchant_id": "M_5510",
            "business_name": "Gupta Medical Hall",
            "owner_name": "Suresh Gupta",
            "phone_number": "+919844556677",
            "registered_address": "Near Civil Hospital, MG Road, Bengaluru",
            "tier": "SILVER",
            "is_fraud_flagged": False,
            "active_disputes": 0,
            "hardship_flag": False,
            "kyc_status": "PENDING_REVERIFICATION",
            "daily_limit_inr": 25000.0,
            "monthly_limit_inr": 500000.0
        }
    },
    "settlements": {
        "M_1092": {
            "settlement_id": "SET_99201",
            "batch_date": "2026-10-28",
            "amount_inr": 14250.00,
            "status": "DELAYED",
            "reason_code": "BANK_HOLIDAY",
            "description": "Settlement delayed due to clearing bank Diwali holiday.",
            "scheduled_retry_time": "2026-10-29T06:00:00+05:30",
            "eligible_for_instant_retry": True,
            "risk_hold": False
        },
        "M_4401": {
            "settlement_id": "SET_44102",
            "batch_date": "2026-10-28",
            "amount_inr": 8400.00,
            "status": "SETTLED",
            "reason_code": "NONE",
            "description": "Settled successfully via IMPS.",
            "scheduled_retry_time": None,
            "eligible_for_instant_retry": False,
            "risk_hold": False
        },
        "M_8819": {
            "settlement_id": "SET_88190",
            "batch_date": "2026-10-28",
            "amount_inr": 120000.00,  # > ₹50,000 Hard Limit
            "status": "DELAYED",
            "reason_code": "RISK_HOLD",
            "description": "Risk hold flagged: high-value velocity deviation.",
            "scheduled_retry_time": None,
            "eligible_for_instant_retry": False,
            "risk_hold": True
        }
    },
    "devices": {
        "M_1092": {
            "device_id": "SBX_4G_88291",
            "model": "Paytm Soundbox 3.0 (4G Voice)",
            "status": "ACTIVE",
            "battery_health": "GOOD_88_PERCENT",
            "sim_status": "ACTIVE_AIRTEL",
            "last_heartbeat": "2026-10-29T10:15:00+05:30",
            "reported_error": None
        },
        "M_4401": {
            "device_id": "SBX_4G_44019",
            "model": "Paytm Soundbox 3.0 (4G Voice)",
            "status": "HARDWARE_FAULT",
            "battery_health": "DEGRADED_14_PERCENT",
            "sim_status": "ACTIVE_JIO",
            "last_heartbeat": "2026-10-29T08:30:00+05:30",
            "reported_error": "SPEAKER_COIL_OPEN"
        }
    },
    "loans": {
        "M_1092": {
            "loan_account_id": "LOAN_PL_7721",
            "total_sanctioned_inr": 150000.00,
            "outstanding_balance_inr": 45000.00,
            "daily_deduction_inr": 350.00,
            "next_emi_amount_inr": 3200.00,
            "next_emi_due_date": "2026-10-30",  # Due tomorrow!
            "days_past_due": 0,
            "is_npa": False
        },
        "M_4401": {
            "loan_account_id": "LOAN_PL_4401",
            "total_sanctioned_inr": 200000.00,
            "outstanding_balance_inr": 10000.00,
            "daily_deduction_inr": 200.00,
            "next_emi_amount_inr": 2500.00,
            "next_emi_due_date": "2026-11-15",
            "days_past_due": 0,
            "is_npa": False
        }
    },
    "retry_jobs": {},
    "replacement_orders": {},
    "payment_links": {},
    "tickets": {},
    "nudges": []
}


class MockDatabase:
    """Thread-safe in-memory database with reset capabilities for test harnesses."""
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self._data = deepcopy(INITIAL_DATA)
        
    @property
    def merchants(self):
        return self._data["merchants"]
        
    @property
    def settlements(self):
        return self._data["settlements"]
        
    @property
    def devices(self):
        return self._data["devices"]
        
    @property
    def loans(self):
        return self._data["loans"]
        
    @property
    def retry_jobs(self):
        return self._data["retry_jobs"]
        
    @property
    def replacement_orders(self):
        return self._data["replacement_orders"]
        
    @property
    def payment_links(self):
        return self._data["payment_links"]
        
    @property
    def tickets(self):
        return self._data["tickets"]
        
    @property
    def nudges(self):
        return self._data["nudges"]


# Global database instance
db = MockDatabase()
