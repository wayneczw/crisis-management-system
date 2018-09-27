-- DROP TABLE `USER`;
-- DROP TABLE `INCIDENT`;

CREATE TABLE IF NOT EXISTS `USER` (
	`id` INTEGER PRIMARY KEY,
	`name`	TEXT NOT NULL UNIQUE,
	`password`	TEXT NOT NULL
);

-- TESTING

-- INSERT INTO USER(name, password) values ('a', 'aa');
-- INSERT INTO USER(name, password) VALUES ('b', 'bb');

-- END TESTING



-- 27 Sept
-- things need to be checked
-- priority range and denotation
-- uniqueness of incident
-- type of assistance required
-- if an incident can be reported by a user for multiple times
-- how should we deal w handled incident (more abt logic than db)
-- desired automation



CREATE TABLE IF NOT EXISTS INCIDENT (
  `id`  INTEGER PRIMARY KEY,
  `name`  TEXT NOT NULL,
  `first_reported`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `location` TEXT NOT NULL,
  `report_cnt`  INTEGER NOT NULL DEFAULT(1),
  `priority_injuries` INTEGER NOT NULL CHECK(`priority_injuries` > 0 AND `priority_injuries` < 4),
  `priority_dangers`  INTEGER NOT NULL CHECK(`priority_dangers` > 0 AND `priority_dangers` < 4),
  `priority_help` INTEGER NOT NULL CHECK(`priority_help` > 0 AND `priority_help` < 4),
--   cond unchecked
  `assistance_required` INTEGER NOT NULL,
  CONSTRAINT `unq`  UNIQUE (
    `location`,
    `priority_injuries`,
    `priority_dangers`,
    `priority_help`,
    `assistance_required`
  )
);

-- TESTING

-- INSERT INTO `INCIDENT`(
--   name,
--   location,
--   priority_injuries,
--   priority_dangers,
--   priority_help,
--   assistance_required
-- ) VALUES (
--   'testing event',
--   '0x3f3f3f3f',
--   1,
--   1,
--   1,
--   1
-- );

-- END TESTING