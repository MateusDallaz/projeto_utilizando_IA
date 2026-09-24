-- ============================================================
-- Dados de exemplo para desenvolvimento — tabela clientes
-- Não executar em produção.
-- ============================================================
SET NAMES utf8mb4;
USE projeto_utilizando_ia;

INSERT INTO clientes (nome, email, telefone, cidade) VALUES
    ('João Silva',     'joao.silva@email.com',     '(47) 99999-1111', 'Rio do Sul'),
    ('Maria Souza',    'maria.souza@email.com',    '(47) 98888-2222', 'Blumenau'),
    ('Carlos Pereira', 'carlos.pereira@email.com', '(48) 97777-3333', 'Florianópolis');
