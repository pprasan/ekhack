CRATE DATABASE `emirates`;

USE `emirates`;

CREATE TABLE `tweets` (
  `country_code` varchar(5) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `sentiment` varchar(30) NOT NULL,
  KEY `k_created_at` (`created_at`),
  KEY `k_country_code` (`country_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


select country_code,
sum(case when sentiment='positive' then 1 else 0 end) as pos,
sum(case when sentiment='negative' then 1 else 0 end) as neg,
sum(case when sentiment='neutral' then 1 else 0 end) as neu
from tweets
group by 1
