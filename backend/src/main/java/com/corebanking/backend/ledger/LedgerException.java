package com.corebanking.backend.ledger;

public class LedgerException extends RuntimeException {
    public LedgerException(String msg, Throwable cause) {
        super(msg, cause);
    }
}
