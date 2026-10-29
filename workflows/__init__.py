"""
Sahayak Workflows Package
"""

from workflows.compound_demo import run_compound_call
from workflows.cs.settlement_delay import run_settlement_workflow
from workflows.cs.soundbox_failure import run_soundbox_workflow
from workflows.cs.failed_payment import run_failed_payment_workflow
from workflows.cs.emi_kyc import run_emi_kyc_workflow
from workflows.sales.emi_reminder import trigger_proactive_emi_reminder
from workflows.sales.usage_nudge import trigger_soundbox_upgrade_nudge
from workflows.sales.loan_followup import trigger_loan_followup

__all__ = [
    "run_compound_call",
    "run_settlement_workflow",
    "run_soundbox_workflow",
    "run_failed_payment_workflow",
    "run_emi_kyc_workflow",
    "trigger_proactive_emi_reminder",
    "trigger_soundbox_upgrade_nudge",
    "trigger_loan_followup"
]
