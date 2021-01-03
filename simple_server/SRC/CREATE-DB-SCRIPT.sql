
-- Create main tables:

CREATE TABLE Film IF NOT EXISTS NAME_DB (
	id          INT,
	Title       VARCHAR(100) NOT NULL,
	Year        INT,
	Runtime     VARCHAR(50),
	Rating      FLOAT,
	Language    VARCHAR(100),
	Country     VARCHAR(100),

PRIMARY KEY(id)
) ENGINE = INNODB ;

CREATE TABLE Actors IF NOT EXISTS NAME_DB (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE Director IF NOT EXISTS NAME_DB (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE Genre IF NOT EXISTS NAME_DB (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE Production IF NOT EXISTS NAME_DB (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE Writer IF NOT EXISTS NAME_DB (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

-- Create intermediate tables:

CREATE TABLE Film_Actors IF NOT EXISTS NAME_DB (
	Film_id          INT,
	Actor_id         INT,

FOREIGN KEY(Film_id),
FOREIGN KEY(Actor_id)
) ENGINE=INNODB;

CREATE TABLE Film_Director IF NOT EXISTS NAME_DB (
	Film_id             INT,
	Director_id         INT,

FOREIGN KEY(Film_id),
FOREIGN KEY(Director_id)
) ENGINE=INNODB;

CREATE TABLE Film_Genre IF NOT EXISTS NAME_DB (
	Film_id          INT,
	Genre_id         INT,

FOREIGN KEY(Film_id),
FOREIGN KEY(Genre_id)
) ENGINE=INNODB;

CREATE TABLE Film_Production IF NOT EXISTS NAME_DB (
	Film_id               INT,
	Production_id         INT,

FOREIGN KEY(Film_id),
FOREIGN KEY(Production_id)
) ENGINE=INNODB;

CREATE TABLE Film_Writer IF NOT EXISTS NAME_DB (
	Film_id          INT,
	Writer_id        INT,

FOREIGN KEY(Film_id),
FOREIGN KEY(Writer_id)
) ENGINE=INNODB;


-- Create indices:

CREATE FULLTEXT INDEX director_name_index ON Director(fullName);

CREATE INDEX actor_id_index ON Film_Actors(Actor_id) USING BTREE;

CREATE INDEX writer_id_index ON Film_Writer(Writer_id) USING BTREE;

CREATE INDEX director_id_index ON Film_Director(Director_id) USING BTREE;


--- create fulltext index
--- create index
--- define primary keys and foreign keys