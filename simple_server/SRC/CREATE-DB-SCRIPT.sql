
-- Create main tables:

CREATE TABLE Film (
	id          INT,
	Title       VARCHAR(100) NOT NULL,
	Year        INT,
	Runtime     VARCHAR(50),
	Rating      FLOAT,
	Language    VARCHAR(100),
	Country     VARCHAR(200),

PRIMARY KEY(id)
) ENGINE = INNODB ;

CREATE TABLE Actor (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE Director (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE Genre (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE Production (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE Writer (
	id          INT,
	fullName    VARCHAR(100) NOT NULL,

PRIMARY KEY(id)
) ENGINE=INNODB;

-- Create intermediate tables:

CREATE TABLE Film_Actor (
	Film_id          INT,
	Actor_id         INT,

FOREIGN KEY(Film_id) REFERENCES Film(id),
FOREIGN KEY(Actor_id) REFERENCES Actor(id)
) ENGINE=INNODB;

CREATE TABLE Film_Director (
	Film_id             INT,
	Director_id         INT,

FOREIGN KEY(Film_id) REFERENCES Film(id),
FOREIGN KEY(Director_id) REFERENCES Director(id)
) ENGINE=INNODB;

CREATE TABLE Film_Genre (
	Film_id          INT,
	Genre_id         INT,

FOREIGN KEY(Film_id) REFERENCES Film(id),
FOREIGN KEY(Genre_id) REFERENCES Genre(id)
) ENGINE=INNODB;

CREATE TABLE Film_Production (
	Film_id               INT,
	Production_id         INT,

FOREIGN KEY(Film_id) REFERENCES Film(id),
FOREIGN KEY(Production_id) REFERENCES Production(id)
) ENGINE=INNODB;

CREATE TABLE Film_Writer (
	Film_id          INT,
	Writer_id        INT,

FOREIGN KEY(Film_id) REFERENCES Film(id),
FOREIGN KEY(Writer_id) REFERENCES Writer(id)
) ENGINE=INNODB;


-- Create indices:

CREATE FULLTEXT INDEX director_name_index ON Director(fullName);

CREATE INDEX actor_id_index ON Film_Actor(Actor_id) USING BTREE;

CREATE INDEX writer_id_index ON Film_Writer(Writer_id) USING BTREE;

CREATE INDEX director_id_index ON Film_Director(Director_id) USING BTREE;


-- create fulltext index
-- create index
-- define primary keys and foreign keys