package com.example.library.model;

import java.time.LocalDate;

public class Member {
    private String id;
    private String name;
    private String email;
    private MemberTier tier;
    private LocalDate joinedDate;
    private int activeLoanCount;

    public Member() {}

    public Member(String id, String name, String email, MemberTier tier, LocalDate joinedDate) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.tier = tier;
        this.joinedDate = joinedDate;
        this.activeLoanCount = 0;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public MemberTier getTier() { return tier; }
    public void setTier(MemberTier tier) { this.tier = tier; }

    public LocalDate getJoinedDate() { return joinedDate; }
    public void setJoinedDate(LocalDate joinedDate) { this.joinedDate = joinedDate; }

    public int getActiveLoanCount() { return activeLoanCount; }
    public void setActiveLoanCount(int activeLoanCount) { this.activeLoanCount = activeLoanCount; }
}
