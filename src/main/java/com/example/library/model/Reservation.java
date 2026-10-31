package com.example.library.model;

import java.time.LocalDateTime;

public class Reservation {
    private String id;
    private String bookId;
    private Member member;
    private LocalDateTime reservationTime;
    private boolean fulfilled;

    public Reservation() {}

    public Reservation(String id, String bookId, Member member) {
        this.id = id;
        this.bookId = bookId;
        this.member = member;
        this.reservationTime = LocalDateTime.now();
        this.fulfilled = false;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getBookId() { return bookId; }
    public void setBookId(String bookId) { this.bookId = bookId; }

    public Member getMember() { return member; }
    public void setMember(Member member) { this.member = member; }

    public LocalDateTime getReservationTime() { return reservationTime; }
    public void setReservationTime(LocalDateTime reservationTime) { this.reservationTime = reservationTime; }

    public boolean isFulfilled() { return fulfilled; }
    public void setFulfilled(boolean fulfilled) { this.fulfilled = fulfilled; }
}
