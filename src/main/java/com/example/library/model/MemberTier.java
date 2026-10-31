package com.example.library.model;

public enum MemberTier {
    REGULAR(1),
    PREMIUM(2),
    VIP(3);

    private final int priority;

    MemberTier(int priority) {
        this.priority = priority;
    }

    public int getPriority() {
        return priority;
    }
}
