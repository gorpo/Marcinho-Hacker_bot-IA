-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Tempo de geração: 08/07/2020 às 20:29
-- Versão do servidor: 10.3.22-MariaDB-1ubuntu1
-- Versão do PHP: 7.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `marcinho_bot`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `comandos`
--

CREATE TABLE `comandos` (
  `id` int(11) NOT NULL,
  `tipo` varchar(5000) DEFAULT NULL,
  `comando` varchar(5000) DEFAULT NULL,
  `resposta` varchar(5000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Despejando dados para a tabela `comandos`
--

INSERT INTO `comandos` (`id`, `tipo`, `comando`, `resposta`) VALUES
(1, 'texto', 'cadastra', 'teu cu'),
(5, 'texto', 'vsf', 'jahsjdhasd'),
(6, 'imagem', 'vanessinha', 'AgACAgEAAx0CViT8vwABBfYTXwWFaEheYX1VZ9f6Atm0VA4nAAFvAAKUqDEbFTApRGHyfQ4zqaIe8tpuBgAEAQADAgADbQADuAYDAAEaBA'),
(7, 'texto', 'teste', 'a'),
(8, 'imagem', 'cloroquina', 'AgACAgEAAx0CViT8vwABBfmgXwX79TlawhsOlvI_ISn4yGvP61wAArOoMRsVMDFEEsvB-_3MPDw2um4GAAQBAAMCAANtAAOyqQMAARoE');

-- --------------------------------------------------------

--
-- Estrutura para tabela `perguntas`
--

CREATE TABLE `perguntas` (
  `id` int(11) NOT NULL,
  `usuario` varchar(5000) DEFAULT NULL,
  `pergunta` varchar(5000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Despejando dados para a tabela `perguntas`
--

INSERT INTO `perguntas` (`id`, `usuario`, `pergunta`) VALUES
(1, '@GorpoOrko', 'e o audio?'),
(2, '@GorpoOrko', 'n pego?'),
(3, '@vladtcxs', '@GorpoOrko ciclone já chegou aí ?'),
(4, '@Odeiobot', 'Seu pau tá melhor?'),
(5, '@Spexs', 'Jnr, [08/07/2020 15:53]\n[Em resposta a Luix]\nQual nome dela? \nTem insta?\n\nLuix, [08/07/2020 15:53]\n[Em resposta a Jnr]\nTambém quero saber\n\nJnr, [08/07/2020 15:53]\nNao\nVoce nao ta entendendo.\n\nJnr, [08/07/2020 15:54]\nEu realmente preciso do insta dela'),
(6, '@Spexs', 'Qual nome dela? \nTem insta?'),
(7, '@Spexs', 'Vai comprar conteúdo, eh?');

--
-- Índices de tabelas apagadas
--

--
-- Índices de tabela `comandos`
--
ALTER TABLE `comandos`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `perguntas`
--
ALTER TABLE `perguntas`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de tabelas apagadas
--

--
-- AUTO_INCREMENT de tabela `comandos`
--
ALTER TABLE `comandos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `perguntas`
--
ALTER TABLE `perguntas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
