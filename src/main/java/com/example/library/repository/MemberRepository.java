package com.example.library.repository;

import com.example.library.model.Member;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

public class MemberRepository {
    private final Map<String, Member> storage = new ConcurrentHashMap<>();

    public Optional<Member> findById(String id) {
        return Optional.ofNullable(storage.get(id));
    }

    public void save(Member member) {
        storage.put(member.getId(), member);
    }

    public boolean exists(String id) {
        return storage.containsKey(id);
    }
}
