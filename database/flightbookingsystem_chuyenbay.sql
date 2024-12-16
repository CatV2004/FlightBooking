-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: flightbookingsystem
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chuyenbay`
--

DROP TABLE IF EXISTS `chuyenbay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chuyenbay` (
  `ma_chuyen_bay` varchar(10) NOT NULL,
  `may_bay` varchar(10) NOT NULL,
  `tuyen_bay` varchar(10) NOT NULL,
  `lich_bay` varchar(10) NOT NULL,
  `gia_chuyen_bay` float NOT NULL,
  `thoi_gian_di` datetime NOT NULL,
  `thoi_gian_den` datetime NOT NULL,
  PRIMARY KEY (`ma_chuyen_bay`),
  KEY `may_bay` (`may_bay`),
  KEY `tuyen_bay` (`tuyen_bay`),
  KEY `lich_bay` (`lich_bay`),
  CONSTRAINT `chuyenbay_ibfk_1` FOREIGN KEY (`may_bay`) REFERENCES `maybay` (`so_hieu_mb`),
  CONSTRAINT `chuyenbay_ibfk_2` FOREIGN KEY (`tuyen_bay`) REFERENCES `tuyenbay` (`ma_tuyen_bay`),
  CONSTRAINT `chuyenbay_ibfk_3` FOREIGN KEY (`lich_bay`) REFERENCES `lichbay` (`ma_LB`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chuyenbay`
--

LOCK TABLES `chuyenbay` WRITE;
/*!40000 ALTER TABLE `chuyenbay` DISABLE KEYS */;
INSERT INTO `chuyenbay` VALUES ('CB01','MB01','TB5947','LB01',2500000,'2024-11-30 16:00:00','2024-11-30 20:00:00'),('CB02','MB02','TB5977','LB02',5000000,'2024-11-30 15:00:00','2024-11-30 16:30:00');
/*!40000 ALTER TABLE `chuyenbay` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-25 16:21:51
