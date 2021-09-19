# Auth Server using Flask

Simple auth server built using Flask and PostgreSQL

## Setup

- Clone the repository

```bash
git clone https://github.com/SheethalBangera/Auth-Server.git
```

- Install dependencies
```bash
pip install -r requirements.txt
```

- Setup database

```sql
CREATE TABLE users(
    userId Varchar(100) Primary key,
    email VARCHAR(100) UNIQUE NOT NULL,
    password Varchar(128) NOT NULL,
    name Text,
    age int
);
```

- Run Server
```bash
python app.py
```