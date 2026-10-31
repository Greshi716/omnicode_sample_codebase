package com.example.library.service;

import com.example.library.model.InventoryRecord;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class InventoryService {
    private final Map<String, InventoryRecord> inventory = new ConcurrentHashMap<>();

    public void setStock(String bookId, int totalCopies, int availableCopies) {
        inventory.put(bookId, new InventoryRecord(bookId, totalCopies, availableCopies));
    }

    public int getAvailableCopies(String bookId) {
        InventoryRecord record = inventory.get(bookId);
        return record != null ? record.getAvailableCopies() : 0;
    }

    /**
     * Decrements inventory stock for book checkout.
     * 
     * SEEDED BUG 2 (Concurrency Race Condition):
     * Check-then-act pattern without atomic operations or synchronization.
     * Two concurrent checkout threads checking availableCopies when stock == 1
     * both pass the check (available > 0) and decrement, resulting in negative inventory (-1).
     */
    public void decrementStock(String bookId) {
        InventoryRecord record = inventory.get(bookId);
        if (record == null) {
            throw new IllegalStateException("Inventory record missing for book: " + bookId);
        }

        // BUG: Non-atomic read followed by non-atomic write without synchronized block or AtomicInteger
        int currentAvailable = record.getAvailableCopies();
        if (currentAvailable <= 0) {
            throw new IllegalStateException("No copies available for checkout for book: " + bookId);
        }

        // Simulate tiny context-switch latency in high-traffic checkout
        try {
            Thread.sleep(5);
        } catch (InterruptedException ignored) {}

        record.setAvailableCopies(currentAvailable - 1);
        record.setLastAuditTime(LocalDateTime.now());
    }

    public synchronized void incrementStock(String bookId) {
        InventoryRecord record = inventory.get(bookId);
        if (record != null) {
            record.setAvailableCopies(record.getAvailableCopies() + 1);
            record.setLastAuditTime(LocalDateTime.now());
        }
    }
}
