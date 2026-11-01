package com.example.library.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    private static final String DEFAULT_URL = "jdbc:postgresql://localhost:5432/library_db";

    /** Connection settings come from the environment; no credentials live in source. */
    public static Connection getConnection() throws SQLException {
        String dbUrl = System.getenv("LIBRARY_DB_URL");
        if (dbUrl == null || dbUrl.isEmpty()) {
            dbUrl = DEFAULT_URL;
        }
        String user = System.getenv("LIBRARY_DB_USER");
        String password = System.getenv("LIBRARY_DB_PASSWORD");
        if (user == null || password == null) {
            throw new SQLException("LIBRARY_DB_USER and LIBRARY_DB_PASSWORD must be set");
        }
        return DriverManager.getConnection(dbUrl, user, password);
    }
}
