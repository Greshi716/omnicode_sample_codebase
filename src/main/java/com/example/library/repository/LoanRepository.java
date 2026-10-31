package com.example.library.repository;

import com.example.library.model.Loan;
import com.example.library.model.LoanStatus;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

public class LoanRepository {
    private final Map<String, Loan> storage = new ConcurrentHashMap<>();

    public Optional<Loan> findById(String id) {
        return Optional.ofNullable(storage.get(id));
    }

    public void save(Loan loan) {
        storage.put(loan.getId(), loan);
    }

    public List<Loan> findActiveLoansByMember(String memberId) {
        return storage.values().stream()
                .filter(l -> l.getMemberId().equals(memberId) && l.getStatus() == LoanStatus.ACTIVE)
                .collect(Collectors.toList());
    }
}
