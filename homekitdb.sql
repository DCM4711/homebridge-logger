# ************************************************************
# Sequel Ace SQL dump
# Version 20067
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# Host: 192.168.1.249 (MySQL 8.0.37-0ubuntu0.20.04.3)
# Database: homekitdb
# Generation Time: 2024-07-20 12:39:35 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table Devices_tbl
# ------------------------------------------------------------

CREATE TABLE `Devices_tbl` (
  `index` int DEFAULT NULL,
  `Device` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `FriendlyName` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Description` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `UUID` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Location` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Source` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`Device`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



# Dump of table HS100_tbl
# ------------------------------------------------------------

CREATE TABLE `HS100_tbl` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ServerTimestamp` timestamp NULL DEFAULT NULL,
  `Device` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Battery` float DEFAULT NULL,
  `Energy` float DEFAULT NULL,
  `Switch` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Illuminance` float DEFAULT NULL,
  `AtmosphericPressure` float DEFAULT NULL,
  `Temperature` float DEFAULT NULL,
  `Occupancy` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `TVChannelNumber` float DEFAULT NULL,
  `TVChannelName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Device` (`Device`),
  KEY `ServerTimestamp` (`ServerTimestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



# Dump of table Shelly_tbl
# ------------------------------------------------------------

CREATE TABLE `Shelly_tbl` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ServerTimestamp` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `Device` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Battery` float DEFAULT NULL,
  `Energy` float DEFAULT NULL,
  `Switch` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Temperature` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Device` (`Device`),
  KEY `ServerTimestamp` (`ServerTimestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



# Dump of table WebOSTV_tbl
# ------------------------------------------------------------

CREATE TABLE `WebOSTV_tbl` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ServerTimestamp` timestamp NULL DEFAULT NULL,
  `Device` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Battery` float DEFAULT NULL,
  `Energy` float DEFAULT NULL,
  `Switch` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `TVChannelNumber` float DEFAULT NULL,
  `TVChannelName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Device` (`Device`),
  KEY `ServerTimestamp` (`ServerTimestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



# Dump of table Zibee2MQTT_tbl
# ------------------------------------------------------------

CREATE TABLE `Zibee2MQTT_tbl` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ServerTimestamp` timestamp NULL DEFAULT NULL,
  `Device` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Battery` float DEFAULT NULL,
  `Energy` float DEFAULT NULL,
  `Switch` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Illuminance` float DEFAULT NULL,
  `AtmosphericPressure` float DEFAULT NULL,
  `Humidity` float DEFAULT NULL,
  `Temperature` float DEFAULT NULL,
  `Occupancy` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Contact` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Vibration` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Leak` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Device` (`Device`),
  KEY `ServerTimestamp` (`ServerTimestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



# Dump of table log_tbl
# ------------------------------------------------------------

CREATE TABLE `log_tbl` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `Source` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `UUID` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ClientTimestamp` timestamp NULL DEFAULT NULL,
  `ServerTimestamp` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `Home` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Room` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Name` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Characteristic` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Value` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `UUID` (`UUID`),
  KEY `Timestamp` (`ClientTimestamp`),
  KEY `Room` (`Room`),
  KEY `Home` (`Home`),
  KEY `Characteristic` (`Characteristic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
