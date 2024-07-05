# Dnd Profile Manager

### Link to GitHub Repository

https://github.com/hynguyenduc/T2A2-API-Webserver-Project

## R2
##### The Problem 
Dnd was initially a pen and paper game that encouraged getting together with a group of friends and exploring fantasy worlds. Now, with modern day technologies, we are able to connect with many different groups of people and discover new adventures. However, as we grow old it becomes harder to manage our time and maintain consistent connection with all the new friendships we started and campaigns we have embarked on. This can lead to lost character sheets or mixing up our characters.

##### The Solution
My proposed solution is a web database that can hold all relevant information for users, their campaigns and the character they have created

## R3
Tasks are tracked with trello. The workload will be separated by sections and will be placed into 3 possible conditions: Initially tasks start in their respective section, then progress to a 'Working on' column then move onto a 'Finished' column. There was also daily stand-up reports on the class discord. 
##### Planning Phase
![](docs/Untitled1.png)
##### Day 1
![](docs/Untitled2.png)
##### Day 2
![](docs/Untitled3.png)
##### Day 3
![](docs/Untitled4.png)
##### Day 4
![](docs/Untitled5.png)
##### Day 5
![](docs/Untitled6.png)

## R4
3rd party python libraries and dependencies would include
Flask: Python library that serves as a "web framework": a tool for making web applications

Marshmallow: Package that converts complex SQLAlchemy models to Python data types, such as dicts (serialization) and converts dicts to SQLAlchemy models (deserialization). Flask-marshmallow is the interface that connects Flask to Marshmallow  

SQLalchemy: An ORM (Object Relational Mapping) that facilitates interaction between a database and a Flask built python application. It does this by mapping database schema (tables) and data to Python objects
Pros

    Less and cleaner code compared to embedded SQL.

    High level implementation, no need to worry about what's going on under the hood. Great support for tasks like connections, migrations, seeds etc.

    Implementation is more simple, no need to convert from table to object and vice versa. Easy to use and maintain.

    The code remains the same or minor changes if the database changes.

    MVC????

Cons

    First stages of ORM (learning and installing) can be time-consuming.

    You still need to know about database and SQL fundamentals, it's not a total abstraction.

    Complex queries may not be solved with ORMs and embedded SQL will be necessary.

Bcrypt: Adds another layer of password protection with a technique called Hashing. Define hashing????

Psycopg2: Popular Postgresql database adapter for Python

Werkzeug: Sub-package of Flask used here to handle BadRequest errors. 

Flask-jwt-extended: Allows the web server to create and interpret a JWT token to allow for greater security with Bearer-type authentication (via encryption)

## R5
Postgres → describe this, pros and cons of that database system and relationship db systems in general
PostgreSQL, as a robust relational database management system (RDBMS), shares many pros and cons typical of relational databases in general. Here’s a breakdown:
Pros of PostgreSQL and RDBMS in General:

    Structured Data Model: Relational databases enforce a structured approach to storing data, which helps ensure data integrity and consistency.

    ACID Compliance: Transactions in PostgreSQL (and most RDBMS) are ACID compliant, ensuring reliability and support for complex operations.

    Strong Consistency: RDBMS systems maintain strong consistency guarantees, meaning that once a transaction is committed, data is immediately and durably stored in a consistent state.

    Standardized Query Language (SQL): SQL is well-defined and widely supported across various relational databases, making it easier to learn and use compared to proprietary query languages.

    Data Integrity: Built-in constraints (such as foreign keys, unique constraints, etc.) ensure data integrity at the database level, preventing inconsistencies.

    Scalability: While traditionally thought to be less scalable than NoSQL databases, modern RDBMS like PostgreSQL have improved scalability features like partitioning, replication, and clustering.

    Community and Support: PostgreSQL has a large and active open-source community, providing extensive documentation, support forums, and third-party tools.

Cons of PostgreSQL and RDBMS in General:

    Scaling Limitations: While PostgreSQL and other RDBMS can scale vertically (by adding more resources to a single server), scaling horizontally across multiple servers can be more complex and may require careful architecture and setup.

    Schema Modifications: Altering the database schema in a live production environment can sometimes be challenging and requires careful planning to avoid downtime or data loss.

    Performance with Large Datasets: Although PostgreSQL performs well with large datasets, certain operations (especially complex joins or full-text searches) may require optimization or alternative strategies compared to NoSQL databases.

    Cost: Some commercial RDBMS solutions can be expensive, although PostgreSQL itself is open-source and free to use.

    Flexibility vs. Structure: The structured nature of RDBMS can sometimes be seen as a limitation when dealing with highly variable or rapidly changing data structures, where NoSQL databases might offer more flexibility.

    Learning Curve: While SQL is standardized, mastering the intricacies of relational databases, including normalization, indexing, and query optimization, can require significant learning and experience.

In summary, PostgreSQL and relational databases like it excel in providing strong consistency, data integrity, and a well-supported querying language. However, they may require careful planning for scalability and schema modifications, especially in large-scale or rapidly evolving systems. Choosing between PostgreSQL and other database systems often depends on specific project requirements, data structure, scalability needs, and the development team's expertise.

## R6
SQLAlchemy → describe, features, what it does, and how you’re going to use it 
SQLAlchemy is a popular Python SQL toolkit and Object-Relational Mapping (ORM) library that provides a flexible and high-level interface for interacting with relational databases. Here’s an overview of what SQLAlchemy does and its key features:
What SQLAlchemy Does:

    ORM (Object-Relational Mapping):
        SQLAlchemy allows developers to define database models as Python classes (objects). These classes represent tables in the database, where attributes of the class correspond to columns in the table.
        By using ORM, developers can work with database records as Python objects, abstracting away much of the SQL syntax and database-specific details.

    Database Connectivity:
        SQLAlchemy supports multiple database backends including PostgreSQL, MySQL, SQLite, Oracle, and more. It provides a consistent API regardless of the underlying database, allowing developers to switch databases easily.

    SQL Expression Language:
        SQLAlchemy provides a SQL expression language that allows users to write SQL queries in a Pythonic way, using Python constructs rather than raw SQL strings.
        This makes it easier to dynamically construct SQL queries and leverage the power of Python for complex database operations.

    Transaction Management:
        SQLAlchemy supports transaction management, allowing developers to manage database transactions explicitly. This ensures data integrity and consistency, following the ACID properties (Atomicity, Consistency, Isolation, Durability).

    Schema Migration:
        SQLAlchemy includes tools for schema migration and versioning. Developers can define database schema changes as Python scripts (migrations) and apply them to databases easily, facilitating database schema evolution over time.

    Query Building:
        SQLAlchemy provides a powerful Query API that allows developers to build complex database queries using method chaining and Pythonic constructs. Queries can be composed dynamically based on application logic.

    Integration with Flask and Other Frameworks:
        SQLAlchemy is commonly used with web frameworks like Flask and Django, integrating seamlessly with these frameworks to provide database support and ORM capabilities.

Key Features of SQLAlchemy:

    Declarative Syntax: SQLAlchemy allows developers to define database models using a declarative syntax, where Python classes map directly to database tables and columns.

    Session Management: SQLAlchemy manages database sessions, providing a unit of work pattern where changes to objects are tracked and committed to the database in a transactional manner.

    Relationship Management: SQLAlchemy supports relationships between database tables, including one-to-one, one-to-many, and many-to-many relationships. These are defined using object attributes, facilitating data retrieval and manipulation.

    Query Optimization: SQLAlchemy includes tools for query optimization and performance tuning, allowing developers to fine-tune database queries to improve application performance.

    Flexibility: SQLAlchemy provides flexibility in how developers interact with databases. While it encourages the use of ORM for simplicity, it also allows direct SQL execution when necessary, providing a balance between abstraction and control.

Overall, SQLAlchemy simplifies database interactions in Python applications by providing a powerful ORM, SQL expression language, and tools for database management and query optimization. Its flexibility and extensive feature set make it a popular choice for developers working with relational databases in Python projects.

## R7
Focus on db design before coding is done, just initial db design (some extra bit i missed) → pure design, no reference to code, python, sql, alchemy, etc 

## R8
Why did you structure that way, ie. why are the ‘relationships’ structured that way? Does it make it easier to code something if structured that way? Ie. explain the models that sit on top of the design (alchemy models) → more on alchemy models, relationships and the coding

## R9
Explain each endpoint, description is the minimum, must also give example, such as with sent header, sent body, sent url, with such restful parameters, sent request, what are the given responses
Http verb
Path or route
Body / header: includes JWT token
Response

Need to justify why you deviated from ERD, if you ever did
Normalization process (3rd normal form)
Use Alchemy
Error handling

Does not need to be a large database set
At least 3 tables that are related 
Need to get ideas signed off on
All link out should include a link and screenshot



