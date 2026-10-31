package com.example.library.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    private static final String DEFAULT_URL = "jdbc:postgresql://localhost:5432/library_db";
    private static final String USER = "postgres";
    private static final String PASS = "postgres";

    public static Connection getConnection() throws SQLException {
        String dbUrl = System.getenv("LIBRARY_DB_URL");
        if (dbUrl == null || dbUrl.isEmpty()) {
            dbUrl = DEFAULT_URL;
        }
        return DriverManager.getConnection(dbUrl, USER, PASS);
    }
}
