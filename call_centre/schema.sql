-- drop statements are only for testing purpose

DROP TABLE IF EXISTS `USER`;
DROP TABLE IF EXISTS `INCIDENT`;
DROP TABLE IF EXISTS `CONTACT`;
DROP TABLE IF EXISTS `REPORT`;

CREATE TABLE IF NOT EXISTS CONTACT (
  `id`  INTEGER PRIMARY KEY,
  `number`  TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS INCIDENT (
  `id`  INTEGER PRIMARY KEY,
  `name`  TEXT NOT NULL,
  `first_reported`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `location` TEXT NOT NULL,
  `report_cnt`  INTEGER NOT NULL DEFAULT(1),
  `priority_injuries` INTEGER NOT NULL CHECK(`priority_injuries` > 0 AND `priority_injuries` < 4),
  `priority_dangers`  INTEGER NOT NULL CHECK(`priority_dangers` > 0 AND `priority_dangers` < 4),
  `priority_help` INTEGER NOT NULL CHECK(`priority_help` > 0 AND `priority_help` < 4),
  `assistance_required` INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS REPORT (
  `cid` INTEGER NOT NULL,
  `iid` INTEGER NOT NULL,
  FOREIGN KEY(`cid`) REFERENCES CONTACT(`id`),
  FOREIGN KEY(`iid`) REFERENCES INCIDENT(`id`),
  CONSTRAINT `unq` UNIQUE (
    `cid`,
    `iid`
  )
);
