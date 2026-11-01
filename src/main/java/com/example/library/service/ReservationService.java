package com.example.library.service;

import com.example.library.model.Member;
import com.example.library.model.Reservation;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class ReservationService {
    private final Map<String, PriorityQueue<Reservation>> bookQueues = new ConcurrentHashMap<>();

    /**
     * Initializes priority queue for a book reservation list.
     * Higher tier members (VIP > PREMIUM > REGULAR) get higher priority in reservation queue.
     */
    public Reservation enqueueReservation(String bookId, Member member) {
        if (bookId == null || member == null) {
            throw new IllegalArgumentException("Book ID and member cannot be null");
        }

        PriorityQueue<Reservation> queue = bookQueues.computeIfAbsent(bookId, k ->
            new PriorityQueue<>((r1, r2) -> {
                int p2 = r2.getMember().getTier().getPriority();
                int p1 = r1.getMember().getTier().getPriority();
                if (p1 != p2) {
                    return Integer.compare(p2, p1); // higher priority first
                }
                return r1.getReservationTime().compareTo(r2.getReservationTime());
            })
        );

        Reservation res = new Reservation(UUID.randomUUID().toString(), bookId, member);
        queue.offer(res);
        return res;
    }

    public Optional<Reservation> peekNextReservation(String bookId) {
        PriorityQueue<Reservation> queue = bookQueues.get(bookId);
        return queue != null ? Optional.ofNullable(queue.peek()) : Optional.empty();
    }

    public Optional<Reservation> fulfillNextReservation(String bookId) {
        PriorityQueue<Reservation> queue = bookQueues.get(bookId);
        if (queue != null && !queue.isEmpty()) {
            Reservation res = queue.poll();
            if (res != null) {
                res.setFulfilled(true);
                return Optional.of(res);
            }
        }
        return Optional.empty();
    }

    public int getQueueLength(String bookId) {
        PriorityQueue<Reservation> queue = bookQueues.get(bookId);
        return queue != null ? queue.size() : 0;
    }
}
