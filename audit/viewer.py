"""
Sahayak - Audit Viewer
Visualizer for the live demo and judge inspections.
"""

from typing import List, Optional
from audit.writer import audit_writer
from audit.schema import AuditEntry
from rich.console import Console
from rich.table import Table

console = Console()


def display_audit_trail(session_id: Optional[str] = None):
    """Pretty-print the audit trail table using Rich."""
    entries: List[AuditEntry] = audit_writer.get_entries(session_id)
    integrity = audit_writer.verify_integrity()
    
    table = Table(title=f"Sahayak Cryptographic Audit Trail (Integrity: {'VALID ✅' if integrity else 'TAMPERED ❌'})")
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Timestamp", style="magenta")
    table.add_column("Event Type", style="green")
    table.add_column("State", style="yellow")
    table.add_column("Merchant", style="blue")
    table.add_column("Hash (SHA-256)", style="dim")
    
    for e in entries[-10:]:  # Display last 10 entries
        table.add_row(
            str(e.index),
            e.timestamp.split("T")[1][:8],
            e.event_type.value,
            e.state,
            e.merchant_id,
            e.hash[:16] + "..."
        )
        
    console.print(table)


def get_live_audit_feed(limit: int = 20) -> List[dict]:
    """Return JSON serializable audit entries for web UI streaming."""
    entries = audit_writer.get_entries()
    return [e.model_dump() for e in entries[-limit:]]
