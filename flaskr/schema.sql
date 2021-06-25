drop table if exists userProfile;

create table userProfile(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username Text UNIQUE NOT NULL,
    msg INTEGER NOT NULL DEFAULT 0
);