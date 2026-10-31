package com.example.library.repository;

import com.example.library.model.Book;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

public class BookRepository {
    private final Map<String, Book> storage = new ConcurrentHashMap<>();

    public Optional<Book> findById(String id) {
        return Optional.ofNullable(storage.get(id));
    }

    public void save(Book book) {
        storage.put(book.getId(), book);
    }

    public boolean exists(String id) {
        return storage.containsKey(id);
    }

    public void delete(String id) {
        storage.remove(id);
    }
}
