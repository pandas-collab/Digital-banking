package com.corebanking.backend.ledger;

import com.corebanking.backend.ledger.model.LedgerRowDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.Map;
import java.util.UUID;

@Service
public class LedgerService {

    private static final Logger logger = LoggerFactory.getLogger(LedgerService.class);

    private final JdbcTemplate jdbcTemplate;
    private final ObjectMapper objectMapper;

    public LedgerService(JdbcTemplate jdbcTemplate, ObjectMapper objectMapper) {
        this.jdbcTemplate = jdbcTemplate;
        this.objectMapper = objectMapper;
    }

    @Transactional
    public UUID appendEvent(String eventType, BigDecimal amount, UUID fromAccount, UUID toAccount, Map<String, Object> metadata) {
        // Validation
        if (eventType == null || eventType.trim().isEmpty()) {
            throw new IllegalArgumentException("eventType must not be null or empty");
        }
        if (amount == null) {
            throw new IllegalArgumentException("amount must not be null");
        }
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("amount must be positive");
        }
        if (metadata == null) {
            throw new IllegalArgumentException("metadata must not be null");
        }

        try {
            String metadataJson = objectMapper.writeValueAsString(metadata);
            UUID generatedId = UUID.randomUUID();

            jdbcTemplate.update(
                    "INSERT INTO ledger (id, event_type, amount, from_account, to_account, metadata) VALUES (?, ?, ?, ?, ?, ?::jsonb)",
                    generatedId, eventType, amount, fromAccount, toAccount, metadataJson
            );

            logger.info("Appended ledger event: id={}, type={}, amount={}", generatedId, eventType, amount);
            return generatedId;
        } catch (Exception e) {
            throw new LedgerException("Failed to append ledger event", e);
        }
    }
}
