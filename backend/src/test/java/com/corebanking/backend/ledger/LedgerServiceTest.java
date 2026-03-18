package com.corebanking.backend.ledger;

import com.corebanking.backend.ledger.model.LedgerRowDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(classes = {LedgerService.class, ObjectMapper.class})
@ActiveProfiles("test")
class LedgerServiceTest {

    @Autowired
    private LedgerService ledgerService;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Test
    @Transactional
    void testHappyPathInsert() {
        UUID from = UUID.randomUUID();
        UUID to = UUID.randomUUID();
        UUID id = ledgerService.appendEvent("transfer", BigDecimal.valueOf(100.50), from, to, Map.of("note", "test"));
        assertNotNull(id);

        List<LedgerRowDto> rows = jdbcTemplate.query(
                "SELECT id as ledger_id, event_type, amount, from_account, to_account, metadata, created_at FROM ledger WHERE id = ?",
                (rs, rowNum) -> {
                    LedgerRowDto dto = new LedgerRowDto();
                    dto.ledgerId = UUID.fromString(rs.getString("ledger_id"));
                    dto.eventType = rs.getString("event_type");
                    dto.amount = rs.getBigDecimal("amount");
                    dto.fromAccountId = rs.getObject("from_account", UUID.class);
                    dto.toAccountId = rs.getObject("to_account", UUID.class);
                    try {
                        dto.metadata = objectMapper.readValue(rs.getString("metadata"), Map.class);
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                    dto.createdAt = rs.getTimestamp("created_at").toInstant().atOffset(java.time.ZoneOffset.UTC);
                    return dto;
                },
                id
        );
        assertEquals(1, rows.size());
        assertEquals(BigDecimal.valueOf(100.50).setScale(4), rows.get(0).amount);
        assertEquals("test", rows.get(0).metadata.get("note"));
    }

    @Test
    void testNullEventTypeFails() {
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
                ledgerService.appendEvent(null, BigDecimal.TEN, null, null, Map.of()));
        assertTrue(ex.getMessage().contains("eventType"));
    }

    @Test
    void testEmptyEventTypeFails() {
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
                ledgerService.appendEvent(" ", BigDecimal.TEN, null, null, Map.of()));
        assertTrue(ex.getMessage().contains("eventType"));
    }

    @Test
    void testNegativeAmountFails() {
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
                ledgerService.appendEvent("transfer", BigDecimal.valueOf(-5), null, null, Map.of()));
        assertTrue(ex.getMessage().contains("positive"));
    }

    @Test
    void testNullMetadataFails() {
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
                ledgerService.appendEvent("transfer", BigDecimal.TEN, null, null, null));
        assertTrue(ex.getMessage().contains("metadata"));
    }
}
