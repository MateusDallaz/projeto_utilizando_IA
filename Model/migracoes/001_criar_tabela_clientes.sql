-- ============================================================
-- Migração 001 — Cria o banco e a tabela clientes
-- Regra: migrações já executadas NUNCA são editadas.
--        Qualquer mudança vira um novo arquivo (002_..., 003_...).
-- ============================================================

-- Garante que acentos (ã, ç, é...) sejam gravados corretamente
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS projeto_utilizando_ia
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE projeto_utilizando_ia;

CREATE TABLE IF NOT EXISTS clientes (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    telefone      VARCHAR(20),
    cidade        VARCHAR(100),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
