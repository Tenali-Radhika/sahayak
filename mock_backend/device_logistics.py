"""
Paytm Mock System 4c: Device & Logistics API (Soundbox)
"""

import uuid
from typing import Dict, Any, Optional
from mock_backend.mock_data import db


def get_device_status(merchant_id: str) -> Optional[Dict[str, Any]]:
    """Query Soundbox device telemetry, battery, and SIM health."""
    device = db.devices.get(merchant_id)
    if not device:
        return {
            "merchant_id": merchant_id,
            "device_id": f"SBX_4G_{merchant_id[-4:]}",
            "status": "NOT_FOUND",
            "reported_error": "NO_DEVICE_LINKED"
        }
    return device


def replace_device(merchant_id: str, device_id: str, fault_reason: str, delivery_speed: str = "EXPRESS_SAME_DAY") -> Dict[str, Any]:
    """Raise autonomous replacement order for faulty Soundbox."""
    order_id = f"REP_ORD_{uuid.uuid4().hex[:6].upper()}"
    new_serial = f"SBX_4G_{uuid.uuid4().hex[:5].upper()}"
    
    order = {
        "replacement_order_id": order_id,
        "merchant_id": merchant_id,
        "old_device_id": device_id,
        "new_device_serial": new_serial,
        "dispatch_status": "DISPATCHED_FROM_LOCAL_HUB",
        "carrier": "Blue Dart Express",
        "awb_number": f"BD_{uuid.uuid4().hex[:9].upper()}",
        "estimated_delivery": "Tomorrow before 2:00 PM"
    }
    
    db.replacement_orders[order_id] = order
    
    # Update device in mock DB
    if merchant_id in db.devices:
        db.devices[merchant_id]["status"] = "REPLACEMENT_IN_TRANSIT"
        db.devices[merchant_id]["active_order_id"] = order_id
        
    return order


def get_device_logistics(merchant_id: str, order_id: Optional[str] = None) -> Dict[str, Any]:
    """Fetch tracking information for replacement Soundbox."""
    if order_id and order_id in db.replacement_orders:
        order = db.replacement_orders[order_id]
        return {
            "order_id": order_id,
            "carrier": order["carrier"],
            "awb_number": order["awb_number"],
            "current_checkpoint": "Out for delivery - Local Hub",
            "delivery_agent_name": "Suresh K",
            "delivery_agent_phone": "+919845012345",
            "eta_human": order["estimated_delivery"]
        }
    
    # Default logistics tracking
    return {
        "order_id": order_id or "REP_ORD_LATEST",
        "carrier": "Blue Dart Express",
        "awb_number": "BD_882918201",
        "current_checkpoint": "Out for delivery - Local Hub",
        "delivery_agent_name": "Suresh K",
        "delivery_agent_phone": "+919845012345",
        "eta_human": "Tomorrow before 2:00 PM"
    }

