USE vehicle_rental;

CREATE DATABASE  IF NOT EXISTS `vehicle_rental` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `vehicle_rental`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: vehicle_rental
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `CustomerName` varchar(255) NOT NULL,
  `ContactNumber` varchar(15) NOT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Victor Dato-on','09123456789'),(2,'Zuriel Montallana','09435095326'),(3,'Audey Orcajada','09925111676'),(4,'Alice Guo','09783798856'),(5,'Bato Dela Rosa','09812844613'),(6,'Rodrigo Lanuza III','09941230941'),(7,'Mark Vincent Santos','09480781771'),(8,'Mar Roxas','09793801190'),(9,'Riza Hontiveros','09409682465'),(10,'Willy Wonka','09005347279'),(11,'Chiz Escudero','09009007581'),(12,'John Doe','09072853825'),(13,'Bini Maloi','09133282771'),(14,'Bini Jhoanna','09188222963'),(15,'Bini Mikha','09310259178'),(16,'Data Base','09423721694'),(17,'My Sql','09217931794'),(18,'Helen Dato-on','09475168714'),(19,'Clifford Valdeztamon','09459012821'),(20,'Vhong Navarro','09899557821');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rentals`
--

DROP TABLE IF EXISTS `rentals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rentals` (
  `RentalID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int NOT NULL,
  `VehicleID` int NOT NULL,
  `RentalStatus` varchar(50) NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL,
  PRIMARY KEY (`RentalID`),
  KEY `CustomerID_idx` (`CustomerID`),
  KEY `VehicleID_idx` (`VehicleID`),
  CONSTRAINT `CustomerID` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`),
  CONSTRAINT `VehicleID` FOREIGN KEY (`VehicleID`) REFERENCES `vehicles` (`VehicleID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rentals`
--

LOCK TABLES `rentals` WRITE;
/*!40000 ALTER TABLE `rentals` DISABLE KEYS */;
INSERT INTO `rentals` VALUES (1,1,1,'Confirmed','2024-01-05','2024-06-14'),(2,2,2,'Confirmed','2024-01-10','2024-02-14'),(3,3,3,'Cancelled','2024-01-11','2024-02-03'),(4,4,4,'Confirmed','2024-01-04','2024-01-29'),(5,5,5,'Cancelled','2024-01-20','2024-03-25'),(6,6,6,'Confirmed','2024-01-15','2024-04-17'),(7,7,7,'Confirmed','2024-01-21','2024-02-26'),(8,8,8,'Confirmed','2024-02-12','2024-05-04'),(9,9,9,'Cancelled','2024-02-28','2024-04-10'),(10,10,10,'Cancelled','2024-03-14','2024-06-11'),(11,11,11,'Cancelled','2024-02-20','2024-03-04'),(12,12,12,'Confirmed','2024-04-01','2024-04-20'),(13,13,13,'Confirmed','2024-03-30','2024-04-30'),(14,14,14,'Confirmed','2024-03-21','2024-05-16'),(15,15,15,'Confirmed','2024-04-24','2024-04-28'),(16,16,16,'Confirmed','2024-01-13','2024-02-16'),(17,17,17,'Confirmed','2024-01-30','2024-02-09'),(18,18,18,'Cancelled','2024-03-17','2024-03-23'),(19,19,19,'Cancelled','2024-02-17','2024-02-20'),(20,20,20,'Confirmed','2024-04-28','2024-05-21');
/*!40000 ALTER TABLE `rentals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicles`
--

DROP TABLE IF EXISTS `vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicles` (
  `VehicleID` int NOT NULL AUTO_INCREMENT,
  `ManufacturerVehicle` varchar(255) NOT NULL,
  `VehicleModel` varchar(50) NOT NULL,
  `DailyRate` decimal(10,2) NOT NULL,
  PRIMARY KEY (`VehicleID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicles`
--

LOCK TABLES `vehicles` WRITE;
/*!40000 ALTER TABLE `vehicles` DISABLE KEYS */;
INSERT INTO `vehicles` VALUES (1,'Ford','Ranger',6000.00),(2,'Ford','Raptor',7500.00),(3,'Ford','Mustang GT',10000.00),(4,'Lamborghini','Urus',15000.00),(5,'Lamborghini','Reventón',30000.00),(6,'Lamborghini','Gallardo',20000.00),(7,'Land Rover','Range Rover SE',5000.00),(8,'Land Rover','Defender 90 SE',5000.00),(9,'Honda','Beat',2500.00),(10,'Honda','Click125',3000.00),(11,'Honda','XRM125 DS',3500.00),(12,'Honda','TMX125',2000.00),(13,'Suzuki','Skydrive Sport',2500.00),(14,'Suzuki','Burgman Street',4000.00),(15,'Suzuki','Raider R150 Carb',5500.00),(16,'Yamaha','Mio Gear',2000.00),(17,'Yamaha','NMAX',3500.00),(18,'Yamaha','Sniper155',5500.00),(19,'BMW','M3 GTR',25000.00),(20,'Subaru','BRZ',15500.00);
/*!40000 ALTER TABLE `vehicles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'vehicle_rental'
--

--
-- Dumping routines for database 'vehicle_rental'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-26 22:37:07
