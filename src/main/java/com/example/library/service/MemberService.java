package com.example.library.service;

import com.example.library.exception.MemberNotFoundException;
import com.example.library.model.Member;
import com.example.library.model.MemberTier;
import com.example.library.repository.MemberRepository;

import java.time.LocalDate;
import java.util.UUID;

public class MemberService {
    private final MemberRepository memberRepository;

    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    public Member registerMember(String name, String email, MemberTier tier) {
        String id = UUID.randomUUID().toString();
        Member member = new Member(id, name, email, tier, LocalDate.now());
        memberRepository.save(member);
        return member;
    }

    public Member getMember(String memberId) {
        return memberRepository.findById(memberId)
                .orElseThrow(() -> new MemberNotFoundException("Member with ID " + memberId + " not found"));
    }

    public void updateTier(String memberId, MemberTier newTier) {
        Member member = getMember(memberId);
        member.setTier(newTier);
        memberRepository.save(member);
    }
}
