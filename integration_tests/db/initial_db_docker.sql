CREATE TABLE IF NOT EXISTS profile(
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT now(),
  modified TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS team(
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  created TIMESTAMP NOT NULL DEFAULT now(),
  modified TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS country(
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  created TIMESTAMP NOT NULL DEFAULT now(),
  modified TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS "user"(
  id SERIAL PRIMARY KEY,
  profile_id INTEGER NOT NULL,
  country_id INTEGER NOT NULL,
  name VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL UNIQUE,
  pw VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  created TIMESTAMP NOT NULL DEFAULT now(),
  modified TIMESTAMP NOT NULL DEFAULT now(),
  FOREIGN KEY (profile_id) REFERENCES profile(id),
  FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE TABLE IF NOT EXISTS user_team(
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  team_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES "user"(id),
  FOREIGN KEY (team_id) REFERENCES team(id)
);

CREATE TABLE IF NOT EXISTS token(
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  token VARCHAR(64) NOT NULL UNIQUE,
  created TIMESTAMP NOT NULL DEFAULT now(),
  modified TIMESTAMP NOT NULL DEFAULT now(),
  FOREIGN KEY (user_id) REFERENCES "user"(id)
);

insert into profile(name) values('profile 1');
insert into country(name) values('Suisse');
insert into "user" (profile_id, country_id, name, username, pw, email) values(1,1,'Foo Bar','foo','foo','foo@bar.com');
