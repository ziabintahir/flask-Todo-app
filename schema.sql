--schema.sql
--
-- Purpose:
-- This file defines the database schema (DDL) for the
-- To-Do application using raw SQL.
--
-- NOTE:
-- The application initializes the database schema
-- programmatically at runtime using the same SQL
-- (CREATE TABLE IF NOT EXISTS) to ensure consistency
-- across development, testing (pytest), and deployment.
--
-- This file is kept for:
-- 1. Documentation of database structure
-- 2. Reference for reviewers
-- 3. Manual initialization if required
--
-- ORM IS NOT USED as per assignment instructions.

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    status TEXT CHECK(status IN ('pending','completed')) DEFAULT 'pending'
);
