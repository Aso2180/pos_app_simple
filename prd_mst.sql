-- MySQL dump 10.13  Distrib 8.4.4, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_app_db
-- ------------------------------------------------------
-- Server version	8.4.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `prd_mst`
--

DROP TABLE IF EXISTS `prd_mst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prd_mst` (
  `PRD_ID` int NOT NULL COMMENT '蝠・刀ID:PK',
  `CODE` char(13) NOT NULL COMMENT '蝠・刀繧ｳ繝ｼ繝・Unique蛻ｶ邏・ｒ莉倥￠繧・,
  `NAME` varchar(50) NOT NULL COMMENT '蝠・刀蜷・,
  `PRICE` int NOT NULL COMMENT '蝠・刀蜊倅ｾ｡',
  PRIMARY KEY (`PRD_ID`),
  UNIQUE KEY `IDX_PRD_CODE` (`CODE`),
  UNIQUE KEY `IDX_PRD_NAME` (`NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='蝠・刀繝槭せ繧ｿ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prd_mst`
--

LOCK TABLES `prd_mst` WRITE;
/*!40000 ALTER TABLE `prd_mst` DISABLE KEYS */;
/*!40000 ALTER TABLE `prd_mst` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-10 14:48:32
