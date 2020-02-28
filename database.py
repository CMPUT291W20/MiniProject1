import sqlite3

def connect(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()
    return conn, cur

def drop_tables(cur):
    cur.execute("drop table if exists previews;")
    cur.execute("drop table if exists reviews;")
    cur.execute("drop table if exists bid;")
    cur.execute("drop table if exists sales;")
    cur.execute("drop table if exists products;")
    cur.execute("drop table if exists users;")

def define_tables(conn, cur):
    user_table = '''
                create table users (
                    email		char(20),
                    name		char(16),
                    pwd		char(4),
                    city		char(15),
                    gender	char(1),
                    primary key (email)
                    );
                '''

    product_table = '''
                create table products (
                    pid		char(4),
                    descr		char(20),
                    primary key (pid)
                    );
                '''

    sales_table = '''
                create table sales (
                    sid		char(4),
                    lister	char(20) not null,
                    pid		char(4),
                    edate		date,
                    descr		char(25),
                    cond		char(10),
                    rprice	int,
                    primary key (sid),
                    foreign key (lister) references users,
                    foreign key (pid) references products
                    );
                '''
    
    bids_table = '''
                create table bids (
                    bid		char(20), 
                    bidder	char(20) not null,
                    sid		char(4) not null, 
                    bdate 	date, 
                    amount	float,
                    primary key (bid),
                    foreign key (bidder) references users,
                    foreign key (sid) references sales
                    );
                '''
    
    reviews_table = '''
                    create table reviews (
                        reviewer	char(20), 
                        reviewee	char(20), 
                        rating	float, 
                        rtext		char(20), 
                        rdate		date,
                        primary key (reviewer, reviewee),
                        foreign key (reviewer) references users,
                        foreign key (reviewee) references users
                        );
                    '''

    previews_table = '''
                create table previews (
                    rid		int,
                    pid		char(4),
                    reviewer	char(20) not null,
                    rating	float,
                    rtext		char(20),
                    rdate		date,
                    primary key (rid),
                    foreign key (pid) references products,
                    foreign key (reviewer) references users
                    );
                '''

    cur.execute(user_table)
    cur.execute(product_table)
    cur.execute(sales_table)
    cur.execute(bids_table)
    cur.execute(reviews_table)
    cur.execute(previews_table)
    conn.commit()