import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from db import get_session  # import the actual session factory
import models.policy as policy_model
import models.account as account_model
from ledger_service import create_ledger_transfer  # standard ledger flow

scheduler = BackgroundScheduler()
scheduler.start()
logger = logging.getLogger(__name__)

def create_premium_job(policy_id: int):
    session: Session = get_session()
    try:
        policy = session.get(policy_model.Policy, policy_id)
        if not policy:
            return

        account = session.get(account_model.Account, policy.account_id)
        if not account:
            logger.warning("Defaulter: account_id=%s not found", policy.account_id)
            return

        if account.balance < policy.premium_monthly:
            logger.warning(
                "Defaulter: account_id=%s balance=%s < premium=%s",
                account.id,
                account.balance,
                policy.premium_monthly,
            )
            return

        create_ledger_transfer(
            from_account_id=account.id,
            to_account_id=0,  # Insurance-company placeholder
            amount=float(policy.premium_monthly),
            note="Premium for policy {}".format(policy.id),
            session=session,
            entity_type="premium",
            entity_id=policy.id,
        )

        policy.next_premium_date += timedelta(days=30)
        session.commit()
        logger.info("Deducted premium for policy_id=%s", policy.id)
    except Exception as e:
        logger.exception("Premium deduction failed: %s", e)
    finally:
        session.close()

def register_policy_for_premium(policy_id: int, session_factory):
    global scheduler
    if not scheduler.running:
        scheduler.start()
    scheduler.add_job(
        create_premium_job,
        "cron",
        day="*",
        hour=0,
        minute=1,
        args=[policy_id],
        id=f"premium-{policy_id}",
        replace_existing=True,
    )
