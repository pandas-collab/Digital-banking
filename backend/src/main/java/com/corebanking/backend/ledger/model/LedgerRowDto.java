package com.corebanking.backend.ledger.model;

import java.time.OffsetDateTime;
import java.util.Map;
import java.util.UUID;

public class LedgerRowDto {
    public UUID ledgerId;
    public String eventType;
    public java.math.BigDecimal amount;
    public UUID fromAccountId;
    public UUID toAccountId;
    public Map<String, Object> metadata;
    public OffsetDateTime createdAt;
}
