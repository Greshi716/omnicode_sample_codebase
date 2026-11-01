package com.example.library.service;

import com.example.library.exception.BookNotFoundException;
import com.example.library.exception.LoanLimitExceededException;
import com.example.library.exception.MemberNotFoundException;
import com.example.library.model.Book;
import com.example.library.model.Loan;
import com.example.library.model.LoanStatus;
import com.example.library.model.Member;
import com.example.library.repository.BookRepository;
import com.example.library.repository.LoanRepository;
import com.example.library.repository.MemberRepository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.UUID;

public class LendingService {
    private static final int MAX_ACTIVE_LOANS = 5;
    private static final BigDecimal DAILY_OVERDUE_FINE = new BigDecimal("1.50");

    private final BookRepository bookRepository;
    private final MemberRepository memberRepository;
    private final LoanRepository loanRepository;
    private final InventoryService inventoryService;

    public LendingService(BookRepository bookRepository, MemberRepository memberRepository,
                          LoanRepository loanRepository, InventoryService inventoryService) {
        this.bookRepository = bookRepository;
        this.memberRepository = memberRepository;
        this.loanRepository = loanRepository;
        this.inventoryService = inventoryService;
    }

    public Loan checkoutBook(String memberId, String bookId, LocalDate checkoutDate) {
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new MemberNotFoundException("Member with ID " + memberId + " not found"));

        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new BookNotFoundException("Book with ID " + bookId + " not found"));

        List<Loan> activeLoans = loanRepository.findActiveLoansByMember(memberId);
        if (activeLoans.size() >= MAX_ACTIVE_LOANS) {
            throw new LoanLimitExceededException("Member has reached max active loan limit of " + MAX_ACTIVE_LOANS);
        }

        inventoryService.decrementStock(bookId);

        LocalDate dueDate = checkoutDate.plusDays(14);
        Loan loan = new Loan(UUID.randomUUID().toString(), bookId, memberId, checkoutDate, dueDate);
        loanRepository.save(loan);
        member.setActiveLoanCount(member.getActiveLoanCount() + 1);
        memberRepository.save(member);

        return loan;
    }

    public Loan returnBook(String loanId, LocalDate returnDate) {
        Loan loan = loanRepository.findById(loanId)
                .orElseThrow(() -> new IllegalArgumentException("Loan record not found: " + loanId));

        loan.setReturnDate(returnDate);
        loan.setStatus(LoanStatus.RETURNED);

        BigDecimal fine = calculateOverdueFine(loan, returnDate);
        loan.setFineAmount(fine);

        loanRepository.save(loan);
        inventoryService.incrementStock(loan.getBookId());

        memberRepository.findById(loan.getMemberId()).ifPresent(m -> {
            m.setActiveLoanCount(Math.max(0, m.getActiveLoanCount() - 1));
            memberRepository.save(m);
        });

        return loan;
    }

    /**
     * Calculates overdue fine for a returned book.
     */
    public BigDecimal calculateOverdueFine(Loan loan, LocalDate returnDate) {
        if (returnDate == null || loan.getDueDate() == null) {
            return BigDecimal.ZERO;
        }

        if (returnDate.isAfter(loan.getDueDate())) {
            long overdueDays = ChronoUnit.DAYS.between(loan.getDueDate(), returnDate) + 1;
            return DAILY_OVERDUE_FINE.multiply(BigDecimal.valueOf(overdueDays));
        }

        return BigDecimal.ZERO;
    }
}
