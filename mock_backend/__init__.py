"""
Paytm Mock System Package
Exposing all 6 API surfaces and seed database.
"""

from mock_backend.mock_data import db, MockDatabase
from mock_backend.merchant_kyc import (
    get_merchant_profile,
    get_kyc_status,
    resend_kyc_link,
    update_kyc_status
)
from mock_backend.settlement import (
    get_settlement_status,
    retry_settlement,
    confirm_settlement_retry,
    resync_transaction
)
from mock_backend.device_logistics import (
    get_device_status,
    replace_device,
    get_device_logistics
)
from mock_backend.loan_emi import (
    get_loan_status,
    get_emi_details,
    send_emi_payment_link
)
from mock_backend.crm_ticketing import (
    create_crm_ticket,
    escalate_ticket_to_human,
    get_ticket_status
)
from mock_backend.sales_outreach import (
    send_payment_link,
    get_payment_link_status,
    trigger_nudge
)

__all__ = [
    "db",
    "MockDatabase",
    "get_merchant_profile",
    "get_kyc_status",
    "resend_kyc_link",
    "update_kyc_status",
    "get_settlement_status",
    "retry_settlement",
    "confirm_settlement_retry",
    "resync_transaction",
    "get_device_status",
    "replace_device",
    "get_device_logistics",
    "get_loan_status",
    "get_emi_details",
    "send_emi_payment_link",
    "create_crm_ticket",
    "escalate_ticket_to_human",
    "get_ticket_status",
    "send_payment_link",
    "get_payment_link_status",
    "trigger_nudge"
]

