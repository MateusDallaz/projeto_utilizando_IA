-- ============================================================
-- Migração 002 — Cria a tabela Usuario (login do sistema)
-- Os usuários são cadastrados direto no banco. As senhas NÃO
-- ficam neste arquivo, porque ele vai para o GitHub.
-- ============================================================

SET NAMES utf8mb4;
USE projeto_utilizando_ia;

CREATE TABLE IF NOT EXISTS Usuario (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    senha   VARCHAR(50) NOT NULL
) ENGINE=InnoDB;
