import psycopg2
#from config import config


def create_tables():
    """ create tables in the PostgreSQL catalog database"""
    commands = (
        """
        CREATE TABLE users (user_id serial PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                picture VARCHAR(255));
        """,
        """ CREATE TABLE categories (id integer PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                user_id integer,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE);
        """,
        """
        CREATE TABLE products (id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                description VARCHAR(255),
                price CHAR(6),
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
                ON UPDATE CASCADE ON DELETE CASCADE,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE);
        """)
    conn = None
    try:
        # read the connection parameters
        # params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname="catalog", user="catalog", password="catalog")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
