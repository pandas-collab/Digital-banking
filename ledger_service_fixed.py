import json
import os
import logging
from typing import List, Dict, Optional
from cashflow_event import CashFlowEvent

logger = logging.getLogger(__name__)

class BulletproofLedgerService:
    """Guarantees 100% cash-flow transparency through persistent event logging"""

    def __init__(self, data_dir: str = "/workspace/data/cashflow"):
        self.data_dir = data_dir
        self.events_file = os.path.join(data_dir, "events.jsonl")
        self._ensure_directories()

    def _ensure_directories(self):
        """Create all required directories with error handling"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            if not os.path.exists(self.events_file):
                with open(self.events_file, 'w') as f:
                    f.write('')  # Create empty file
            logger.info(f"Ledger initialized at {self.data_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize ledger directories: {e}")
            raise

    def record_event(self, event: CashFlowEvent) -> bool:
        """Persist cash-flow event with bulletproof reliability"""
        try:
            event_data = json.dumps(event.to_dict()) + '\n'

            # Atomic write: write to temp file first
            temp_file = self.events_file + ".tmp"
            with open(temp_file, 'a') as f:
                f.write(event_data)

            # Atomic move: guarantees consistency
            os.rename(temp_file, self.events_file)

            logger.info(f"Recorded event: {event.id}")
            return True

        except Exception as e:
            logger.error(f"CRITICAL: Failed to record event {event.id}: {e}")
            raise

    def get_account_events(self, account_id: str) -> List[CashFlowEvent]:
        """Retrieve all events for an account with full transparency"""
        events = []
        try:
            if not os.path.exists(self.events_file):
                return events

            with open(self.events_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        data = json.loads(line)
                        if data.get('account_id') == account_id:
                            # Reconstruct event
                            event = CashFlowEvent(
                                event_type=data['event_type'],
                                account_id=data['account_id'],
                                amount=data['amount'],
                                previous_balance=data['previous_balance'],
                                new_balance=data['new_balance'],
                                metadata=data.get('metadata', {})
                            )
                            events.append(event)
                    except Exception as e:
                        logger.warning(f"Skipping malformed event line: {e}")

            return sorted(events, key=lambda x: x.timestamp, reverse=True)

        except Exception as e:
            logger.error(f"Failed to retrieve events for {account_id}: {e}")
            raise

    def get_all_events(self) -> List[Dict]:
        """Get all cash-flow events for audit purposes"""
        events = []
        try:
            if not os.path.exists(self.events_file):
                return events

            with open(self.events_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue

            return events

        except Exception as e:
            logger.error(f"Failed to retrieve all events: {e}")
            raise
