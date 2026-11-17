CREATE DATABASE IF NOT EXISTS sistema_gimnasio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_gimnasio;

CREATE TABLE IF NOT EXISTS miembros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    plan VARCHAR(50) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO miembros (nombre, telefono, plan, estado) VALUES
('Carlos Mendoza', '555-1234', 'Mensual VIP', 'Activo'),
('Ana Sofía Ruiz', '555-5678', 'Trimestral', 'Activo'),
('Luis Fernando Torres', '555-9012', 'Mensual Básico', 'Vencido');
