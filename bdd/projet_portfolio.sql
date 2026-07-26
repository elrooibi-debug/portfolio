-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : dim. 26 juil. 2026 à 21:26
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `projet_portfolio`
--

-- --------------------------------------------------------

--
-- Structure de la table `accounts`
--

CREATE TABLE `accounts` (
  `id_user` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Déchargement des données de la table `accounts`
--

INSERT INTO `accounts` (`id_user`, `username`, `password`) VALUES
(1, 'ibi', 'yaz2wu');

-- --------------------------------------------------------

--
-- Structure de la table `habits`
--

CREATE TABLE `habits` (
  `id_habit` int(11) NOT NULL,
  `Habits` varchar(255) DEFAULT NULL,
  `Done` tinyint(1) NOT NULL DEFAULT 0,
  `Times` int(11) NOT NULL DEFAULT 0,
  `Goal` int(11) NOT NULL DEFAULT 0,
  `last_checked_date` date DEFAULT NULL,
  `last_checked_month` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Déchargement des données de la table `habits`
--

INSERT INTO `habits` (`id_habit`, `Habits`, `Done`, `Times`, `Goal`, `last_checked_date`, `last_checked_month`) VALUES
(2, 'reading', 0, 1, 31, '2026-07-26', 7);

-- --------------------------------------------------------

--
-- Structure de la table `learning`
--

CREATE TABLE `learning` (
  `id_learning` int(11) NOT NULL,
  `nom_langage` varchar(255) DEFAULT NULL,
  `description` mediumtext DEFAULT NULL,
  `ressources` mediumtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Déchargement des données de la table `learning`
--

INSERT INTO `learning` (`id_learning`, `nom_langage`, `description`, `ressources`) VALUES
(1, 'Python', 'Python is one of the three most used programming languages. It can be used for everything: web development, data analysis, machine learning, ...', 'Habit tracker tuto : https://youtu.be/4pX5tOKTnNA');

-- --------------------------------------------------------

--
-- Structure de la table `project`
--

CREATE TABLE `project` (
  `id_project` int(11) NOT NULL,
  `name_project` varchar(255) NOT NULL,
  `language_info` varchar(255) DEFAULT NULL,
  `time` int(11) NOT NULL,
  `competences` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `to_do`
--

CREATE TABLE `to_do` (
  `id_tache` int(11) NOT NULL,
  `nom_tache` varchar(255) DEFAULT NULL,
  `temps_tache` varchar(50) DEFAULT NULL,
  `realise` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Déchargement des données de la table `to_do`
--

INSERT INTO `to_do` (`id_tache`, `nom_tache`, `temps_tache`, `realise`) VALUES
(1, 'Réviser le code Flask', '14:00', 1);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id_user`);

--
-- Index pour la table `habits`
--
ALTER TABLE `habits`
  ADD PRIMARY KEY (`id_habit`);

--
-- Index pour la table `learning`
--
ALTER TABLE `learning`
  ADD PRIMARY KEY (`id_learning`);

--
-- Index pour la table `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`id_project`);

--
-- Index pour la table `to_do`
--
ALTER TABLE `to_do`
  ADD PRIMARY KEY (`id_tache`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `habits`
--
ALTER TABLE `habits`
  MODIFY `id_habit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `learning`
--
ALTER TABLE `learning`
  MODIFY `id_learning` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `project`
--
ALTER TABLE `project`
  MODIFY `id_project` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `to_do`
--
ALTER TABLE `to_do`
  MODIFY `id_tache` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
