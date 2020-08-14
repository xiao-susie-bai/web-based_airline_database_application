-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 15, 2019 at 07:56 PM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airticket_reservation_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`name`) VALUES
('China Southern');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `username` varchar(20) NOT NULL,
  `password` char(32) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `airline_name` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `birth_date`, `airline_name`) VALUES
('AirlineStaff', 'e2fc714c4727ee9395f324cd2e7f331f', 'Roe', 'Zhang', '1978-05-25', 'China Southern');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airline` varchar(20) NOT NULL,
  `airplane_ID` varchar(20) NOT NULL,
  `seat_capacity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline`, `airplane_ID`, `seat_capacity`) VALUES
('China Southern', '1', 4),
('China Southern', '2', 4),
('China Southern', '3', 50);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `name` varchar(20) NOT NULL,
  `city` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`name`, `city`) VALUES
('BEI', 'Beijing'),
('BOS', 'Boston'),
('HKA', 'Hong Kong'),
('JFK', 'NYC'),
('LAX', 'Los Angeles'),
('PVG', 'Shanghai'),
('SFO', 'San Francisco'),
('SZX', 'Shenzhen');

-- --------------------------------------------------------

--
-- Stand-in structure for view `all_flight_price`
-- (See below for the actual view)
--
CREATE TABLE `all_flight_price` (
`airline` varchar(20)
,`flight_ID` varchar(20)
,`departure_time` timestamp
,`price` decimal(12,1)
);

-- --------------------------------------------------------

--
-- Table structure for table `booking_agency`
--

CREATE TABLE `booking_agency` (
  `email` varchar(20) NOT NULL,
  `password` char(32) DEFAULT NULL,
  `booking_agent_ID` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `booking_agency`
--

INSERT INTO `booking_agency` (`email`, `password`, `booking_agent_ID`) VALUES
('ctrip@agent.com', 'e19d5cd5af0378da05f63f891c7467af', '1'),
('expedia@agent.com', 'e19d5cd5af0378da05f63f891c7467af', '2');

-- --------------------------------------------------------

--
-- Stand-in structure for view `customer_ticket_count`
-- (See below for the actual view)
--
CREATE TABLE `customer_ticket_count` (
`airline` varchar(20)
,`email` varchar(20)
,`name` varchar(20)
,`phone_number` varchar(20)
,`birth_date` date
,`passport_country` varchar(20)
,`city` varchar(20)
,`total_ticket_purchased` bigint(21)
);

-- --------------------------------------------------------

--
-- Table structure for table `customer_to_purchase`
--

CREATE TABLE `customer_to_purchase` (
  `email` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `airline` varchar(20) NOT NULL,
  `flight_ID` varchar(20) NOT NULL,
  `base_price` int(11) DEFAULT NULL,
  `departure_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `arrival_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `airplane_ID` varchar(20) DEFAULT NULL,
  `departure_airport` varchar(20) DEFAULT NULL,
  `arrival_airport` varchar(20) DEFAULT NULL,
  `flight_status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline`, `flight_ID`, `base_price`, `departure_time`, `arrival_time`, `airplane_ID`, `departure_airport`, `arrival_airport`, `flight_status`) VALUES
('China Southern', '102', 300, '2019-04-12 05:25:25', '2019-04-12 08:50:25', '3', 'SFO', 'LAX', 'on-time'),
('China Southern', '104', 300, '2019-05-12 05:25:25', '2019-05-12 08:50:25', '3', 'PVG', 'HKA', 'on-time'),
('China Southern', '106', 350, '2019-03-12 05:25:25', '2019-03-12 08:50:25', '3', 'SFO', 'LAX', 'delayed'),
('China Southern', '134', 300, '2019-01-12 05:25:25', '2019-01-12 08:50:25', '3', 'JFK', 'BOS', 'delayed'),
('China Southern', '206', 400, '2019-06-12 05:25:25', '2019-06-12 08:50:25', '2', 'SFO', 'LAX', 'on-time'),
('China Southern', '207', 300, '2019-07-12 05:25:25', '2019-07-12 08:50:25', '2', 'LAX', 'SFO', 'on-time'),
('China Southern', '296', 3000, '2019-06-01 05:25:25', '2019-06-01 08:50:25', '1', 'PVG', 'SFO', 'on-time'),
('China Southern', '715', 500, '2019-04-28 02:25:25', '2019-04-28 05:50:25', '1', 'PVG', 'BEI', 'delayed'),
('China Southern', '839', 300, '2018-10-12 05:25:25', '2018-10-12 08:50:25', '3', 'SZX', 'BEI', 'on-time');

-- --------------------------------------------------------

--
-- Table structure for table `flight_search_result`
--

CREATE TABLE `flight_search_result` (
  `airline` varchar(20) DEFAULT NULL,
  `flight_ID` varchar(20) DEFAULT NULL,
  `departure_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `arrival_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `departure_airport` varchar(20) DEFAULT NULL,
  `arrival_airport` varchar(20) DEFAULT NULL,
  `flight_status` varchar(20) DEFAULT NULL,
  `price` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `flight_to_purchase`
--

CREATE TABLE `flight_to_purchase` (
  `airline` varchar(20) DEFAULT NULL,
  `flight_ID` varchar(20) DEFAULT NULL,
  `departure_airport` varchar(20) DEFAULT NULL,
  `arrival_airport` varchar(20) DEFAULT NULL,
  `departure_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `arrival_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `price` int(11) DEFAULT NULL,
  `flight_status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Stand-in structure for view `flight_with_city`
-- (See below for the actual view)
--
CREATE TABLE `flight_with_city` (
`airline` varchar(20)
,`flight_ID` varchar(20)
,`base_price` int(11)
,`departure_time` timestamp
,`arrival_time` timestamp
,`airplane_ID` varchar(20)
,`departure_airport` varchar(20)
,`arrival_airport` varchar(20)
,`flight_status` varchar(20)
,`departure_city` varchar(20)
,`arrival_city` varchar(20)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `flight_with_city_with_price`
-- (See below for the actual view)
--
CREATE TABLE `flight_with_city_with_price` (
`airline` varchar(20)
,`flight_ID` varchar(20)
,`departure_time` timestamp
,`base_price` int(11)
,`arrival_time` timestamp
,`airplane_ID` varchar(20)
,`departure_airport` varchar(20)
,`arrival_airport` varchar(20)
,`flight_status` varchar(20)
,`departure_city` varchar(20)
,`arrival_city` varchar(20)
,`price` decimal(12,1)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `flight_with_normal_price`
-- (See below for the actual view)
--
CREATE TABLE `flight_with_normal_price` (
`airline` varchar(20)
,`flight_ID` varchar(20)
,`departure_time` timestamp
,`price` int(11)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `flight_with_over_booked_price`
-- (See below for the actual view)
--
CREATE TABLE `flight_with_over_booked_price` (
`airline` varchar(20)
,`flight_ID` varchar(20)
,`departure_time` timestamp
,`price` decimal(12,1)
);

-- --------------------------------------------------------

--
-- Table structure for table `latest_flight_purchased`
--

CREATE TABLE `latest_flight_purchased` (
  `airline` varchar(20) DEFAULT NULL,
  `flight_ID` varchar(20) DEFAULT NULL,
  `departure_airport` varchar(20) DEFAULT NULL,
  `arrival_airport` varchar(20) DEFAULT NULL,
  `departure_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `arrival_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `flight_status` varchar(20) DEFAULT NULL,
  `ticket_ID` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `phone_number`
--

CREATE TABLE `phone_number` (
  `username` varchar(20) NOT NULL,
  `phone_number` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `phone_number`
--

INSERT INTO `phone_number` (`username`, `phone_number`) VALUES
('AirlineStaff', ' 44455556666'),
('AirlineStaff', '11122223333');

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `email_customer` varchar(20) NOT NULL,
  `ticket_ID` varchar(20) NOT NULL,
  `credit_or_debit` varchar(20) DEFAULT NULL,
  `card_number` varchar(20) DEFAULT NULL,
  `card_holder` varchar(20) DEFAULT NULL,
  `security_code` varchar(20) DEFAULT NULL,
  `expiration_card` date DEFAULT NULL,
  `date_purchase` date DEFAULT NULL,
  `time_purchase` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`email_customer`, `ticket_ID`, `credit_or_debit`, `card_number`, `card_holder`, `security_code`, `expiration_card`, `date_purchase`, `time_purchase`) VALUES
('testcustomer@nyu.edu', '1111111111111', 'credit', '1111222233334444', 'Test Customer 1', '101', '2023-03-01', '2019-03-12', '11:55:55'),
('testcustomer@nyu.edu', '1212121212121', 'credit', '1111222233334444', 'Test Customer 1', '101', '2023-03-01', '2019-04-05', '11:55:55'),
('testcustomer@nyu.edu', '1818181818181', 'credit', '1111222233334444', 'Test Customer 1', '101', '2023-03-01', '2019-04-25', '11:55:55'),
('testcustomer@nyu.edu', '2020202020202', 'credit', '1111222233334444', 'Test Customer 1', '101', '2023-03-01', '2019-02-12', '11:55:55'),
('testcustomer@nyu.edu', '5555555555555', 'credit', '1111222233334444', 'Test Customer 1', '101', '2023-03-01', '2019-04-28', '11:55:55'),
('testcustomer@nyu.edu', '6666666666666', 'credit', '1111222233334444', 'Test Customer 1', '101', '2023-03-01', '2019-03-05', '11:55:55'),
('user1@nyu.edu', '1515151515151', 'credit', '1111222233335555', 'User 1', '101', '2023-03-01', '2019-05-13', '11:55:55'),
('user1@nyu.edu', '1717171717171', 'credit', '1111222233335555', 'User 1', '101', '2023-03-01', '2019-03-11', '11:55:55'),
('user1@nyu.edu', '1919191919191', 'credit', '1111222233335555', 'User 1', '101', '2023-03-01', '2019-05-04', '11:55:55'),
('user1@nyu.edu', '2222222222222', 'credit', '1111222233335555', 'User 1', '101', '2023-03-01', '2019-03-11', '11:55:55'),
('user1@nyu.edu', '4444444444444', 'credit', '1111222233335555', 'User 1', '101', '2023-03-01', '2019-03-21', '11:55:55'),
('user2@nyu.edu', '1616161616161', 'credit', '1111222233335555', 'User 2', '101', '2023-03-01', '2019-04-19', '11:55:55'),
('user2@nyu.edu', '3333333333333', 'credit', '1111222233335555', 'User 2', '101', '2023-03-01', '2019-04-11', '11:55:55'),
('user3@nyu.edu', '1011011011011', 'credit', '1111222233335555', 'User 3', '101', '2023-03-01', '2018-10-23', '11:55:55'),
('user3@nyu.edu', '1414141414141', 'credit', '1111222233335555', 'User 3', '101', '2023-03-01', '2019-05-12', '11:55:55'),
('user3@nyu.edu', '7777777777777', 'credit', '1111222233335555', 'User 3', '101', '2023-03-01', '2019-02-03', '11:55:55'),
('user3@nyu.edu', '8888888888888', 'credit', '1111222233335555', 'User 3', '101', '2023-03-01', '2018-10-03', '11:55:55'),
('user3@nyu.edu', '9999999999999', 'credit', '1111222233335555', 'User 3', '101', '2023-03-01', '2019-02-03', '11:55:55');

-- --------------------------------------------------------

--
-- Table structure for table `purchase_for`
--

CREATE TABLE `purchase_for` (
  `ticket_ID` varchar(20) NOT NULL,
  `email_customer` varchar(20) NOT NULL,
  `email_agent` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `purchase_for`
--

INSERT INTO `purchase_for` (`ticket_ID`, `email_customer`, `email_agent`) VALUES
('1011011011011', 'user3@nyu.edu', 'expedia@agent.com'),
('1111111111111', 'testcustomer@nyu.edu', 'ctrip@agent.com'),
('1212121212121', 'testcustomer@nyu.edu', 'ctrip@agent.com'),
('1414141414141', 'user3@nyu.edu', 'ctrip@agent.com'),
('1717171717171', 'user1@nyu.edu', 'expedia@agent.com'),
('1818181818181', 'testcustomer@nyu.edu', 'ctrip@agent.com'),
('1919191919191', 'user1@nyu.edu', 'expedia@agent.com'),
('5555555555555', 'testcustomer@nyu.edu', 'ctrip@agent.com'),
('6666666666666', 'testcustomer@nyu.edu', 'ctrip@agent.com');

-- --------------------------------------------------------

--
-- Table structure for table `retail_customer`
--

CREATE TABLE `retail_customer` (
  `email` varchar(20) NOT NULL,
  `password` char(32) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `building_number` varchar(20) DEFAULT NULL,
  `street` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_country` varchar(20) DEFAULT NULL,
  `birth_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `retail_customer`
--

INSERT INTO `retail_customer` (`email`, `password`, `name`, `phone_number`, `building_number`, `street`, `city`, `state`, `passport_number`, `passport_expiration`, `passport_country`, `birth_date`) VALUES
('testcustomer@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'Test Customer 1', '12343214321', '1555', 'Century Avenue', 'Pudong', 'Shanghai', '54321', '2025-12-24', 'China', '1999-12-19'),
('user1@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'User 1', '12343224322', '1555', 'Century Avenue', 'Pudong', 'Shanghai', '54322', '2025-12-25', 'China', '1999-11-19'),
('user2@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'User 2', '12343234323', '1702', 'Century Avenue', 'Pudong', 'Shanghai', '54323', '2025-10-24', 'China', '1999-10-19'),
('user3@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'User 3', '12343244324', '1890', 'Century Avenue', 'Pudong', 'Shanghai', '54324', '2025-09-24', 'China', '1999-09-19');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_ID` varchar(20) NOT NULL,
  `sold_price` int(11) DEFAULT NULL,
  `airline` varchar(20) DEFAULT NULL,
  `flight_ID` varchar(20) DEFAULT NULL,
  `departure_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_ID`, `sold_price`, `airline`, `flight_ID`, `departure_time`) VALUES
('1011011011011', 300, 'China Southern', '134', '2019-01-12 05:25:25'),
('1111111111111', 300, 'China Southern', '102', '2019-04-12 05:25:25'),
('1212121212121', 500, 'China Southern', '715', '2019-04-28 02:25:25'),
('1414141414141', 400, 'China Southern', '206', '2019-06-12 05:25:25'),
('1515151515151', 400, 'China Southern', '206', '2019-06-12 05:25:25'),
('1616161616161', 400, 'China Southern', '206', '2019-06-12 05:25:25'),
('1717171717171', 300, 'China Southern', '207', '2019-07-12 05:25:25'),
('1818181818181', 300, 'China Southern', '207', '2019-07-12 05:25:25'),
('1919191919191', 3000, 'China Southern', '296', '2019-06-01 05:25:25'),
('2020202020202', 3000, 'China Southern', '296', '2019-06-01 05:25:25'),
('2222222222222', 300, 'China Southern', '102', '2019-04-12 05:25:25'),
('3333333333333', 300, 'China Southern', '102', '2019-04-12 05:25:25'),
('4444444444444', 300, 'China Southern', '104', '2019-05-12 05:25:25'),
('5555555555555', 300, 'China Southern', '104', '2019-05-12 05:25:25'),
('6666666666666', 350, 'China Southern', '106', '2019-03-12 05:25:25'),
('7777777777777', 350, 'China Southern', '106', '2019-03-12 05:25:25'),
('8888888888888', 300, 'China Southern', '839', '2018-10-12 05:25:25'),
('9999999999999', 360, 'China Southern', '102', '2019-04-12 05:25:25');

-- --------------------------------------------------------

--
-- Stand-in structure for view `ticket_sold_capacity`
-- (See below for the actual view)
--
CREATE TABLE `ticket_sold_capacity` (
`airline` varchar(20)
,`flight_ID` varchar(20)
,`departure_time` timestamp
,`num_ticket_sold` bigint(21)
,`seat_capacity` int(11)
,`percentage_sold` decimal(24,4)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `ticket_with_city`
-- (See below for the actual view)
--
CREATE TABLE `ticket_with_city` (
`airline` varchar(20)
,`flight_ID` varchar(20)
,`departure_time` timestamp
,`ticket_ID` varchar(20)
,`sold_price` int(11)
,`base_price` int(11)
,`arrival_time` timestamp
,`airplane_ID` varchar(20)
,`departure_airport` varchar(20)
,`arrival_airport` varchar(20)
,`flight_status` varchar(20)
,`departure_city` varchar(20)
,`arrival_city` varchar(20)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `ticket_with_purchase_customer_info`
-- (See below for the actual view)
--
CREATE TABLE `ticket_with_purchase_customer_info` (
`ticket_ID` varchar(20)
,`sold_price` int(11)
,`airline` varchar(20)
,`flight_ID` varchar(20)
,`departure_time` timestamp
,`email_customer` varchar(20)
,`credit_or_debit` varchar(20)
,`card_number` varchar(20)
,`card_holder` varchar(20)
,`security_code` varchar(20)
,`expiration_card` date
,`date_purchase` date
,`time_purchase` time
,`email` varchar(20)
,`password` char(32)
,`name` varchar(20)
,`phone_number` varchar(20)
,`building_number` varchar(20)
,`street` varchar(20)
,`city` varchar(20)
,`state` varchar(20)
,`passport_number` varchar(20)
,`passport_expiration` date
,`passport_country` varchar(20)
,`birth_date` date
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `ticket_with_purchase_info`
-- (See below for the actual view)
--
CREATE TABLE `ticket_with_purchase_info` (
`ticket_ID` varchar(20)
,`sold_price` int(11)
,`airline` varchar(20)
,`flight_ID` varchar(20)
,`departure_time` timestamp
,`email_customer` varchar(20)
,`credit_or_debit` varchar(20)
,`card_number` varchar(20)
,`card_holder` varchar(20)
,`security_code` varchar(20)
,`expiration_card` date
,`date_purchase` date
,`time_purchase` time
);

-- --------------------------------------------------------

--
-- Structure for view `all_flight_price`
--
DROP TABLE IF EXISTS `all_flight_price`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `all_flight_price`  AS  (select `flight_with_normal_price`.`airline` AS `airline`,`flight_with_normal_price`.`flight_ID` AS `flight_ID`,`flight_with_normal_price`.`departure_time` AS `departure_time`,`flight_with_normal_price`.`price` AS `price` from `flight_with_normal_price`) union (select `flight_with_over_booked_price`.`airline` AS `airline`,`flight_with_over_booked_price`.`flight_ID` AS `flight_ID`,`flight_with_over_booked_price`.`departure_time` AS `departure_time`,`flight_with_over_booked_price`.`price` AS `price` from `flight_with_over_booked_price`) ;

-- --------------------------------------------------------

--
-- Structure for view `customer_ticket_count`
--
DROP TABLE IF EXISTS `customer_ticket_count`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `customer_ticket_count`  AS  select `ticket`.`airline` AS `airline`,`retail_customer`.`email` AS `email`,`retail_customer`.`name` AS `name`,`retail_customer`.`phone_number` AS `phone_number`,`retail_customer`.`birth_date` AS `birth_date`,`retail_customer`.`passport_country` AS `passport_country`,`retail_customer`.`city` AS `city`,count(distinct `purchases`.`ticket_ID`) AS `total_ticket_purchased` from ((`purchases` join `ticket` on((`purchases`.`ticket_ID` = `ticket`.`ticket_ID`))) join `retail_customer` on((`purchases`.`email_customer` = `retail_customer`.`email`))) group by `ticket`.`airline`,`retail_customer`.`email` ;

-- --------------------------------------------------------

--
-- Structure for view `flight_with_city`
--
DROP TABLE IF EXISTS `flight_with_city`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `flight_with_city`  AS  (select `flight`.`airline` AS `airline`,`flight`.`flight_ID` AS `flight_ID`,`flight`.`base_price` AS `base_price`,`flight`.`departure_time` AS `departure_time`,`flight`.`arrival_time` AS `arrival_time`,`flight`.`airplane_ID` AS `airplane_ID`,`flight`.`departure_airport` AS `departure_airport`,`flight`.`arrival_airport` AS `arrival_airport`,`flight`.`flight_status` AS `flight_status`,`d`.`city` AS `departure_city`,`a`.`city` AS `arrival_city` from ((`flight` join `airport` `d`) join `airport` `a`) where ((`flight`.`departure_airport` = `d`.`name`) and (`flight`.`arrival_airport` = `a`.`name`))) ;

-- --------------------------------------------------------

--
-- Structure for view `flight_with_city_with_price`
--
DROP TABLE IF EXISTS `flight_with_city_with_price`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `flight_with_city_with_price`  AS  (select `flight_with_city`.`airline` AS `airline`,`flight_with_city`.`flight_ID` AS `flight_ID`,`flight_with_city`.`departure_time` AS `departure_time`,`flight_with_city`.`base_price` AS `base_price`,`flight_with_city`.`arrival_time` AS `arrival_time`,`flight_with_city`.`airplane_ID` AS `airplane_ID`,`flight_with_city`.`departure_airport` AS `departure_airport`,`flight_with_city`.`arrival_airport` AS `arrival_airport`,`flight_with_city`.`flight_status` AS `flight_status`,`flight_with_city`.`departure_city` AS `departure_city`,`flight_with_city`.`arrival_city` AS `arrival_city`,`all_flight_price`.`price` AS `price` from (`flight_with_city` left join `all_flight_price` on(((`flight_with_city`.`airline` = `all_flight_price`.`airline`) and (`flight_with_city`.`flight_ID` = `all_flight_price`.`flight_ID`) and (`flight_with_city`.`departure_time` = `all_flight_price`.`departure_time`))))) ;

-- --------------------------------------------------------

--
-- Structure for view `flight_with_normal_price`
--
DROP TABLE IF EXISTS `flight_with_normal_price`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `flight_with_normal_price`  AS  (select `flight_with_city`.`airline` AS `airline`,`flight_with_city`.`flight_ID` AS `flight_ID`,`flight_with_city`.`departure_time` AS `departure_time`,`flight_with_city`.`base_price` AS `price` from `flight_with_city` where (not((`flight_with_city`.`airline`,`flight_with_city`.`flight_ID`,`flight_with_city`.`departure_time`) in (select `ticket_sold_capacity`.`airline`,`ticket_sold_capacity`.`flight_ID`,`ticket_sold_capacity`.`departure_time` from `ticket_sold_capacity` where (`ticket_sold_capacity`.`percentage_sold` > 0.7))))) ;

-- --------------------------------------------------------

--
-- Structure for view `flight_with_over_booked_price`
--
DROP TABLE IF EXISTS `flight_with_over_booked_price`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `flight_with_over_booked_price`  AS  (select `flight_with_city`.`airline` AS `airline`,`flight_with_city`.`flight_ID` AS `flight_ID`,`flight_with_city`.`departure_time` AS `departure_time`,(`flight_with_city`.`base_price` * 1.2) AS `price` from `flight_with_city` where (`flight_with_city`.`airline`,`flight_with_city`.`flight_ID`,`flight_with_city`.`departure_time`) in (select `ticket_sold_capacity`.`airline`,`ticket_sold_capacity`.`flight_ID`,`ticket_sold_capacity`.`departure_time` from `ticket_sold_capacity` where (`ticket_sold_capacity`.`percentage_sold` > 0.7))) ;

-- --------------------------------------------------------

--
-- Structure for view `ticket_sold_capacity`
--
DROP TABLE IF EXISTS `ticket_sold_capacity`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ticket_sold_capacity`  AS  (select `ticket`.`airline` AS `airline`,`ticket`.`flight_ID` AS `flight_ID`,`ticket`.`departure_time` AS `departure_time`,count(`ticket`.`ticket_ID`) AS `num_ticket_sold`,`airplane`.`seat_capacity` AS `seat_capacity`,(count(`ticket`.`ticket_ID`) / `airplane`.`seat_capacity`) AS `percentage_sold` from ((`ticket` left join `flight` on(((`ticket`.`airline` = `flight`.`airline`) and (`ticket`.`flight_ID` = `flight`.`flight_ID`) and (`ticket`.`departure_time` = `flight`.`departure_time`)))) left join `airplane` on(((`ticket`.`airline` = `airplane`.`airline`) and (`flight`.`airplane_ID` = `airplane`.`airplane_ID`)))) group by `ticket`.`airline`,`ticket`.`flight_ID`,`ticket`.`departure_time`) ;

-- --------------------------------------------------------

--
-- Structure for view `ticket_with_city`
--
DROP TABLE IF EXISTS `ticket_with_city`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ticket_with_city`  AS  (select `ticket`.`airline` AS `airline`,`ticket`.`flight_ID` AS `flight_ID`,`ticket`.`departure_time` AS `departure_time`,`ticket`.`ticket_ID` AS `ticket_ID`,`ticket`.`sold_price` AS `sold_price`,`flight_with_city`.`base_price` AS `base_price`,`flight_with_city`.`arrival_time` AS `arrival_time`,`flight_with_city`.`airplane_ID` AS `airplane_ID`,`flight_with_city`.`departure_airport` AS `departure_airport`,`flight_with_city`.`arrival_airport` AS `arrival_airport`,`flight_with_city`.`flight_status` AS `flight_status`,`flight_with_city`.`departure_city` AS `departure_city`,`flight_with_city`.`arrival_city` AS `arrival_city` from (`ticket` join `flight_with_city` on(((`ticket`.`airline` = `flight_with_city`.`airline`) and (`ticket`.`flight_ID` = `flight_with_city`.`flight_ID`) and (`ticket`.`departure_time` = `flight_with_city`.`departure_time`))))) ;

-- --------------------------------------------------------

--
-- Structure for view `ticket_with_purchase_customer_info`
--
DROP TABLE IF EXISTS `ticket_with_purchase_customer_info`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ticket_with_purchase_customer_info`  AS  (select `ticket_with_purchase_info`.`ticket_ID` AS `ticket_ID`,`ticket_with_purchase_info`.`sold_price` AS `sold_price`,`ticket_with_purchase_info`.`airline` AS `airline`,`ticket_with_purchase_info`.`flight_ID` AS `flight_ID`,`ticket_with_purchase_info`.`departure_time` AS `departure_time`,`ticket_with_purchase_info`.`email_customer` AS `email_customer`,`ticket_with_purchase_info`.`credit_or_debit` AS `credit_or_debit`,`ticket_with_purchase_info`.`card_number` AS `card_number`,`ticket_with_purchase_info`.`card_holder` AS `card_holder`,`ticket_with_purchase_info`.`security_code` AS `security_code`,`ticket_with_purchase_info`.`expiration_card` AS `expiration_card`,`ticket_with_purchase_info`.`date_purchase` AS `date_purchase`,`ticket_with_purchase_info`.`time_purchase` AS `time_purchase`,`retail_customer`.`email` AS `email`,`retail_customer`.`password` AS `password`,`retail_customer`.`name` AS `name`,`retail_customer`.`phone_number` AS `phone_number`,`retail_customer`.`building_number` AS `building_number`,`retail_customer`.`street` AS `street`,`retail_customer`.`city` AS `city`,`retail_customer`.`state` AS `state`,`retail_customer`.`passport_number` AS `passport_number`,`retail_customer`.`passport_expiration` AS `passport_expiration`,`retail_customer`.`passport_country` AS `passport_country`,`retail_customer`.`birth_date` AS `birth_date` from (`ticket_with_purchase_info` join `retail_customer` on((`ticket_with_purchase_info`.`email_customer` = `retail_customer`.`email`)))) ;

-- --------------------------------------------------------

--
-- Structure for view `ticket_with_purchase_info`
--
DROP TABLE IF EXISTS `ticket_with_purchase_info`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ticket_with_purchase_info`  AS  (select `ticket`.`ticket_ID` AS `ticket_ID`,`ticket`.`sold_price` AS `sold_price`,`ticket`.`airline` AS `airline`,`ticket`.`flight_ID` AS `flight_ID`,`ticket`.`departure_time` AS `departure_time`,`purchases`.`email_customer` AS `email_customer`,`purchases`.`credit_or_debit` AS `credit_or_debit`,`purchases`.`card_number` AS `card_number`,`purchases`.`card_holder` AS `card_holder`,`purchases`.`security_code` AS `security_code`,`purchases`.`expiration_card` AS `expiration_card`,`purchases`.`date_purchase` AS `date_purchase`,`purchases`.`time_purchase` AS `time_purchase` from (`ticket` join `purchases` on((`ticket`.`ticket_ID` = `purchases`.`ticket_ID`)))) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airline`,`airplane_ID`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `booking_agency`
--
ALTER TABLE `booking_agency`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`airline`,`flight_ID`,`departure_time`),
  ADD KEY `airline` (`airline`,`airplane_ID`),
  ADD KEY `departure_airport` (`departure_airport`),
  ADD KEY `arrival_airport` (`arrival_airport`);

--
-- Indexes for table `phone_number`
--
ALTER TABLE `phone_number`
  ADD PRIMARY KEY (`username`,`phone_number`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
  ADD PRIMARY KEY (`email_customer`,`ticket_ID`),
  ADD KEY `ticket_ID` (`ticket_ID`);

--
-- Indexes for table `purchase_for`
--
ALTER TABLE `purchase_for`
  ADD PRIMARY KEY (`ticket_ID`,`email_customer`,`email_agent`),
  ADD KEY `email_customer` (`email_customer`),
  ADD KEY `email_agent` (`email_agent`);

--
-- Indexes for table `retail_customer`
--
ALTER TABLE `retail_customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_ID`),
  ADD KEY `airline` (`airline`,`flight_ID`,`departure_time`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`name`);

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline`) REFERENCES `airline` (`name`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline`) REFERENCES `airline` (`name`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`airline`,`airplane_ID`) REFERENCES `airplane` (`airline`, `airplane_ID`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`departure_airport`) REFERENCES `airport` (`name`),
  ADD CONSTRAINT `flight_ibfk_4` FOREIGN KEY (`arrival_airport`) REFERENCES `airport` (`name`);

--
-- Constraints for table `phone_number`
--
ALTER TABLE `phone_number`
  ADD CONSTRAINT `phone_number_ibfk_1` FOREIGN KEY (`username`) REFERENCES `airline_staff` (`username`);

--
-- Constraints for table `purchases`
--
ALTER TABLE `purchases`
  ADD CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`email_customer`) REFERENCES `retail_customer` (`email`),
  ADD CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`ticket_ID`) REFERENCES `ticket` (`ticket_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `purchase_for`
--
ALTER TABLE `purchase_for`
  ADD CONSTRAINT `purchase_for_ibfk_1` FOREIGN KEY (`email_customer`) REFERENCES `retail_customer` (`email`),
  ADD CONSTRAINT `purchase_for_ibfk_2` FOREIGN KEY (`email_agent`) REFERENCES `booking_agency` (`email`),
  ADD CONSTRAINT `purchase_for_ibfk_3` FOREIGN KEY (`ticket_ID`) REFERENCES `ticket` (`ticket_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`airline`) REFERENCES `airline` (`name`),
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`airline`,`flight_ID`,`departure_time`) REFERENCES `flight` (`airline`, `flight_ID`, `departure_time`) ON DELETE CASCADE ON UPDATE CASCADE;

DELIMITER $$
--
-- Events
--
CREATE DEFINER=`root`@`localhost` EVENT `update flight status` ON SCHEDULE EVERY 1 MINUTE STARTS '2019-05-12 00:00:00' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE flight
        SET flight_status = "On Time"
        WHERE flight_status = "Scheduled" AND departure_time < CURRENT_TIMESTAMP()$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
