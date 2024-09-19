CREATE DATABASE `db_empresa`;
USE `db_empresa`;

CREATE TABLE IF NOT EXISTS tb_usucionarios (
    usu_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    usu_matricula TEXT NOT NULL,
    usu_email TEXT NOT NULL,
    usu_senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_exercicios (
    exe_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    exe_nome TEXT NOT NULL,
    exe_descricao TEXT NOT NULL, 
    exe_usu_id INT NOT NULL,
    FOREIGN KEY (exe_usu_id) REFERENCES tb_usucionarios(usu_id)
);