-- Active: 1709767233807@@127.0.0.1@3306


-- Create the main_categories table
CREATE TABLE main_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_category TEXT UNIQUE COLLATE NOCASE
);

-- Create the sub_categories table
CREATE TABLE sub_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sub_category TEXT COLLATE NOCASE,
    main_category_id INTEGER,
    FOREIGN KEY (main_category_id) REFERENCES main_categories (id)
);


-- Insert rows into main_categories table
INSERT INTO main_categories (main_category) VALUES ('Groceries');
INSERT INTO main_categories (main_category) VALUES ('Medico');
INSERT INTO main_categories (main_category) VALUES ('Subscriptions');
INSERT INTO main_categories (main_category) VALUES ('E-provisions');
INSERT INTO main_categories (main_category) VALUES ('Cash-transfers');
INSERT INTO main_categories (main_category) VALUES ('Food-orders');
INSERT INTO main_categories (main_category) VALUES ('Others');


-- Insert rows into sub_categories table
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Kaya', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Kaufland', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Aldi', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Rewe', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Marktkauf', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('DM', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Netto', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('TEDI', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Lidl', 1);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Jaffna', 1); 
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Rossmann', 1);

INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Apotheke', 2);

INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('CHATGPT', 3);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('GOOGLE', 3);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('OPENAI', 3);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('AMZNPrime DE', 3);


INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Amazon', 4);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Myntra', 4);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Uber', 4); 
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Butlers', 4);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('AMZN MKTP DE', 4);

INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('paypal', 5);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('wise', 5);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('paysend', 5);

INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('BURGER KING', 6);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('INDIAN PALACE', 6);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Swiggy', 6);
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('SUBWAY', 6); 
INSERT INTO sub_categories (sub_category, main_category_id) VALUES ('Barlin Doner', 6);







DELETE FROM sub_categories WHERE sub_category = 'AMZN';


UPDATE sub_categories
SET sub_category = 'SumUp *Barlin Doner'
WHERE id = 29;

DROP table main_categories
DROP table sub_categories

