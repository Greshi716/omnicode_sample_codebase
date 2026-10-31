package com.example.library.model;

import java.time.LocalDateTime;

public class InventoryRecord {
    private String bookId;
    private int totalCopies;
    private int availableCopies;
    private LocalDateTime lastAuditTime;

    public InventoryRecord() {}

    public InventoryRecord(String bookId, int totalCopies, int availableCopies) {
        this.bookId = bookId;
        this.totalCopies = totalCopies;
        this.availableCopies = availableCopies;
        this.lastAuditTime = LocalDateTime.now();
    }

    public String getBookId() { return bookId; }
    public void setBookId(String bookId) { this.bookId = bookId; }

    public int getTotalCopies() { return totalCopies; }
    public void setTotalCopies(int totalCopies) { this.totalCopies = totalCopies; }

    public int getAvailableCopies() { return availableCopies; }
    public void setAvailableCopies(int availableCopies) { this.availableCopies = availableCopies; }

    public LocalDateTime getLastAuditTime() { return lastAuditTime; }
    public void setLastAuditTime(LocalDateTime lastAuditTime) { this.lastAuditTime = lastAuditTime; }
}
