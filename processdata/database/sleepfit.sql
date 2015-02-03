-- MoodMon 
-- 
-- Version 1.0 (Nov. 2, 2014) 
-- Umass Lowell, Computer Science
--
-- khuang@cs.uml.edu

--
-- Table structure for table `sensingdata` 
--

DROP TABLE IF EXISTS `sensingdata`;
CREATE TABLE `sensingdata` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '0',
    `createTime` timestamp NOT NULL default 0,
    `trackDate` char(40) default NULL,
    `movement` smallint unsigned default 0,
    `illuminanceMax` float default 0,
    `illuminanceMin` float default 0,
    `illuminanceAvg` float default 0,
    `illuminanceStd` float default 0,
    `decibelMax` float default 0,
    `decibelMin` float default 0,
    `decibelAvg` float default 0,
    `decibelStd` float default 0,
    `isCharging` tinyint unsigned default 0,
    `powerLevel` float default 1.0,
    `proximity` float default 1.0,
    `ssid` mediumtext default '',
    `appUsage` mediumtext default '',
    `roomId` int unsigned NOT NULL default '0',
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 
-- Table structure for table `sleeplogger`
--

DROP TABLE IF EXISTS `sleeplogger`;
CREATE TABLE `sleeplogger` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '0',
    `createTime` timestamp NOT NULL default 0,
    `trackDate` char(40) default '',
    `sleepTime` timestamp default 0,
    `wakeupTime` timestamp default 0,
    `napTime` SMALLINT UNSIGNED default 0,
    `quality` tinyint unsigned default 3,
    `finished` tinyint unsigned default 0,
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 
-- Table structure for table `sysevents`
-- 

DROP TABLE IF EXISTS `sysevents`;
CREATE TABLE `sysevents` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '0',
    `createTime` timestamp NOT NULL default 0,
    `trackDate` char(40) default '',
    `eventType` tinyint unsigned default 0,
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 
-- Table structure for table `movementraw`
--

DROP TABLE IF EXISTS `movementraw`;
CREATE TABLE `movementraw` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '0',
    `createTime` timestamp NOT NULL default 0,
    `data` mediumtext default '',
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 
-- Table structure for table `soundtraw`
--

DROP TABLE IF EXISTS `soundraw`;
CREATE TABLE `soundraw` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '0',
    `createTime` timestamp NOT NULL default 0,
    `data` mediumtext default '',
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 
-- Table structure for table `lightraw`
--

DROP TABLE IF EXISTS `lightraw`;
CREATE TABLE `lightraw` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '0',
    `createTime` timestamp NOT NULL default 0,
    `data` mediumtext default '',
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 
-- Table structure for table `proximityraw`
--

DROP TABLE IF EXISTS `proximityraw`;
CREATE TABLE `proximityraw` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '0',
    `createTime` timestamp NOT NULL default 0,
    `data` mediumtext default '',
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `ID` smallint unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '',
    `UUID` char(128) NOT NULL default '',
    `age` smallint unsigned default '18',
    `gender` char(32) default 'Male',
    `racial` char(32) default 'A',
    `sleepHours` float default '8.0',
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- 
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
CREATE TABLE `rooms` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '',
    `wifi` mediumtext default '',
    PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


--
-- Table structure for table `lifestyleraw`
--

DROP TABLE IF EXISTS `lifestyleraw`;
CREATE TABLE `lifestyleraw` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '',
    `trackDate` char(40) default '',
    `createTime` timestamp NOT NULL default 0,
    `type` char(64) NOT NULL default '',
    `typeId` smallint unsigned NOT NULL default 0,
    `logTime` timestamp NOT NULL default 0,
    `selection` smallint unsigned NOT NULL default 0,
    `note` mediumtext default '',
    PRIMARY KEY (`ID`, `CID`) 
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


--
-- Table structure for table `dailylog`
-- 

DROP TABLE IF EXISTS `dailylog`;
CREATE TABLE `dailylog` (
    `ID` int unsigned NOT NULL auto_increment,
    `CID` char(128) NOT NULL default '',
    `trackDate` char(40) default '',
    `createTime` timestamp NOT NULL default 0,
    `numAwakenings` smallint unsigned default 0,
    `timeAwake` smallint unsigned default 0,
    `timeToSleep` smallint unsigned default 0,
    `quality` tinyint unsigned default 0,
    `restored` tinyint unsigned default 0,
    `stress` tinyint unsigned default 0,
    `depression` tinyint unsigned default 0,
    `fatigue` tinyint unsigned default 0,
    `sleepiness` tinyint unsigned default 0,
    PRIMARY KEY (`ID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;







