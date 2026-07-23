-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : jeu. 23 juil. 2026 à 18:46
-- Version du serveur : 5.7.24
-- Version de PHP : 8.3.1

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
CREATE DATABASE IF NOT EXISTS `projet_portfolio` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `projet_portfolio`;

-- --------------------------------------------------------

--
-- Structure de la table `habits`
--

DROP TABLE IF EXISTS `habits`;
CREATE TABLE `habits` (
  `Habits` varchar(255) DEFAULT NULL,
  `Done` tinyint(1) NOT NULL,
  `Times` int(11) NOT NULL,
  `Goal` int(11) NOT NULL,
  `id_habit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `habits`
--

INSERT INTO `habits` (`Habits`, `Done`, `Times`, `Goal`, `id_habit`) VALUES
('lecture quran', 0, 0, 31, 1);

-- --------------------------------------------------------

--
-- Structure de la table `learning`
--

DROP TABLE IF EXISTS `learning`;
CREATE TABLE `learning` (
  `id_learning` int(11) NOT NULL,
  `nom_langage` varchar(255) DEFAULT NULL,
  `description` mediumtext,
  `ressources` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `learning`
--

INSERT INTO `learning` (`id_learning`, `nom_langage`, `description`, `ressources`) VALUES
(1, 'Python', 'Python is one of the three most used programming languages. It can be used for everything: web developpement, data analysis, machine learning, ...', 'Habit tracker tuto : https://youtu.be/4pX5tOKTnNA');

-- --------------------------------------------------------

--
-- Structure de la table `project`
--

DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `name_project` varchar(255) NOT NULL,
  `language_info` varchar(255) DEFAULT NULL,
  `time` int(11) NOT NULL,
  `competences` varchar(255) NOT NULL,
  `id_project` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `to_do`
--

DROP TABLE IF EXISTS `to_do`;
CREATE TABLE `to_do` (
  `id_tache` int(11) NOT NULL,
  `nom_tache` varchar(255) DEFAULT NULL,
  `temps_tache` datetime DEFAULT NULL,
  `realise` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Index pour les tables déchargées
--

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
-- AUTO_INCREMENT pour la table `habits`
--
ALTER TABLE `habits`
  MODIFY `id_habit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
  MODIFY `id_tache` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
