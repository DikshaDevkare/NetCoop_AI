import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.protocols.schemas import AgentMessageSchema
from app.protocols.validator import validate_agent_message

class BaseAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    def create_message(
        self,
        receiver: str,
        message_type: str,
        payload: Dict[str, Any],
        incident_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Creates a standardized NetCoop Agent Protocol message."""
        msg_dict = {
            "message_id": f"MSG-{uuid.uuid4().hex[:8].upper()}",
            "incident_id": incident_id,
            "sender": self.agent_name,
            "receiver": receiver,
            "message_type": message_type,
            "schema_version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        is_valid, errors, normalized_payload = validate_agent_message(msg_dict)
        if not is_valid:
            print(f"[{self.agent_name}] Warning: message validation warnings: {errors}")
        msg_dict["payload"] = normalized_payload
        return msg_dict

    def analyze(self, telemetry_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError("Each diagnostic agent must implement analyze()")
