-- drop statements are only for testing purpose:
-- DROP TABLE IF EXISTS `INCIDENT_REPORT`;



CREATE TABLE IF NOT EXISTS INCIDENT_REPORT (
  `id`  INTEGER PRIMARY KEY,
  `first_reported`  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name`  TEXT NOT NULL,
  `mobile_number`  TEXT NOT NULL,
  `location` TEXT NOT NULL,
  `assistance_required` INTEGER NOT NULL,
  `description`  TEXT NOT NULL,
  `priority_injuries` INTEGER NOT NULL CHECK(`priority_injuries` > 0 AND `priority_injuries` < 11),
  `priority_dangers`  INTEGER NOT NULL CHECK(`priority_dangers` > 0 AND `priority_dangers` < 11),
  `priority_help` INTEGER NOT NULL CHECK(`priority_help` > 0 AND `priority_help` < 11),
  `report_status`  INTEGER NOT NULL CHECK(`report_status` > 0 AND `report_status` < 4),
  `is_first_such_incident`  INTEGER NOT NULL DEFAULT(1)
);

