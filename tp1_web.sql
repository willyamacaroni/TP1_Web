-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 16, 2020 at 04:13 PM
-- Server version: 10.4.10-MariaDB
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tp1_web`
--

-- --------------------------------------------------------

--
-- Table structure for table `magasin`
--

DROP TABLE IF EXISTS `magasin`;
CREATE TABLE IF NOT EXISTS `magasin` (
  `magasinId` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  PRIMARY KEY (`magasinId`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `magasin`
--

INSERT INTO `magasin` (`magasinId`, `nom`) VALUES
(27, 'Carrefour'),
(26, 'Basse-Ville'),
(25, 'Centre-Ville'),
(24, 'Galeries'),
(23, 'Stoneham'),
(22, 'St-Augustin'),
(21, 'Fontaine'),
(11, 'Ville St-Laurent'),
(12, 'Lac St-Charles'),
(31, 'Lebourgneuf');

-- --------------------------------------------------------

--
-- Table structure for table `produit`
--

DROP TABLE IF EXISTS `produit`;
CREATE TABLE IF NOT EXISTS `produit` (
  `produitId` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `description` varchar(100) NOT NULL,
  `stock` int(11) NOT NULL,
  `coutant` decimal(10,2) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `format` varchar(25) NOT NULL,
  `prix` decimal(10,2) NOT NULL,
  `magasinId` int(11) DEFAULT NULL,
  `type` int(69) NOT NULL,
  `taxableFederal` tinyint(1) NOT NULL,
  `taxableProvincial` tinyint(1) NOT NULL,
  PRIMARY KEY (`produitId`),
  KEY `type` (`type`)
) ENGINE=MyISAM AUTO_INCREMENT=195 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `produit`
--

INSERT INTO `produit` (`produitId`, `nom`, `description`, `stock`, `coutant`, `active`, `format`, `prix`, `magasinId`, `type`, `taxableFederal`, `taxableProvincial`) VALUES
(149, '62757800274', 'Nutribar Poudre chocolat protéine', 75, '9.97', 1, '380 gr ', '8.00', NULL, 4, 0, 0),
(71, '62757800221-1221', 'Nutribar double chocolat', 38, '9.97', 1, '325 gr *** 6 unités', '8.00', 23, 4, 0, 0),
(72, '62757800543', 'Nutribar moka-amandes', 122, '9.97', 1, '390 gr *** 6 unités', '8.00', NULL, 2, 0, 0),
(73, '62757800225-1225', 'Nutribar Nouga au caramel', 48, '9.97', 1, '325 gr *** 6 unités', '8.00', NULL, 3, 0, 0),
(90, '62757800573', 'Nutribar Poudre chocolat suprême', 152, '9.97', 1, '530 gr', '8.00', NULL, 4, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `type`
--

DROP TABLE IF EXISTS `type`;
CREATE TABLE IF NOT EXISTS `type` (
  `typeId` int(69) NOT NULL AUTO_INCREMENT,
  `type` varchar(69) CHARACTER SET ascii NOT NULL,
  PRIMARY KEY (`typeId`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `type`
--

INSERT INTO `type` (`typeId`, `type`) VALUES
(4, 'chocolat'),
(2, 'moka'),
(3, 'caramel'),
(1, 'autre');

-- --------------------------------------------------------

--
-- Table structure for table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
CREATE TABLE IF NOT EXISTS `utilisateur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(69) CHARACTER SET ascii NOT NULL,
  `motDePasses` varchar(69) CHARACTER SET ascii NOT NULL,
  `admin` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom` (`nom`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `utilisateur`
--

INSERT INTO `utilisateur` (`id`, `nom`, `motDePasses`, `admin`) VALUES
(1, 'Willyam', '', 1),
(6, 'Dominik', '123', 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
