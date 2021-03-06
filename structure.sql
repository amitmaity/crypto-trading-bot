-- -------------------------------------------------------------
-- TablePlus 3.12.4(360)
--
-- https://tableplus.com/
--
-- Database: crypto_trading_bot
-- Generation Time: 2021-02-28 22:19:42.6660
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


DROP TABLE IF EXISTS `buy_transactions`;
CREATE TABLE `buy_transactions` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) unsigned DEFAULT NULL,
  `client_order_id` varchar(255) DEFAULT NULL,
  `order_quantity` decimal(16,10) DEFAULT NULL,
  `order_price` decimal(16,10) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `fill_price` decimal(16,10) DEFAULT NULL,
  `fill_quantity` decimal(16,10) DEFAULT NULL,
  `commission` decimal(16,10) DEFAULT NULL,
  `timestamp` int(12) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `config_name` varchar(64) NOT NULL,
  `config_value` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `price_data`;
CREATE TABLE `price_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `price` decimal(16,10) DEFAULT NULL,
  `low` decimal(16,10) DEFAULT NULL,
  `high` decimal(16,10) DEFAULT NULL,
  `timestamp` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sell_transactions`;
CREATE TABLE `sell_transactions` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `buy_order_ref` bigint(20) unsigned DEFAULT NULL,
  `order_id` bigint(20) unsigned DEFAULT NULL,
  `client_order_id` varchar(255) DEFAULT NULL,
  `order_quantity` decimal(16,10) DEFAULT NULL,
  `order_price` decimal(16,10) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `fill_price` decimal(16,10) DEFAULT NULL,
  `fill_quantity` decimal(16,10) DEFAULT NULL,
  `commission` decimal(16,10) DEFAULT NULL,
  `timestamp` int(12) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `config` (`config_name`, `config_value`) VALUES
('quote_coin', 'BTC'),
('base_coin', 'BNB'),
('buy_price_diff_percentage', '0.5'),
('sell_price_diff_percentage', '0.3'),
('price_range_minutes', '60'),
('buy_price_diff_percentage_from_24hr_high', '0.8'),
('quote_coin_usage_per_transaction', '0.0001'),
('coin_quantity_precision', '2');



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;