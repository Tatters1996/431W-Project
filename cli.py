import psycopg2
from psycopg2 import sql, DatabaseError


def connect_to_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432",
    )


def execute_query(query, is_select=False):
    connection = None
    print(query)
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query)

        if is_select:
            results = cursor.fetchall()
            for row in results:
                print(row)
        else:
            connection.commit()
            print("Query executed successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if connection is not None:
            connection.rollback()
    finally:
        if connection is not None:
            cursor.close()
            connection.close()


def main():
    print(
        """Select an operation:
    1. Insert Data
    2. Delete Data
    3. Update Data
    4. Search Data
    5. Aggregate Functions
    6. Sorting
    7. Joins
    8. Grouping
    9. Subqueries
    10. Transactions
    11. Error Handling
    12. Exit"""
    )

    choice = input("Enter choice (1-12): ")
    if choice == "1":
        # Example for inserting data, adjust based on actual use case
        table_name = input("Enter table name: ")
        columns = input("Enter columns (comma-separated): ")
        values = input("Enter values (comma-separated): ")
        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values})").format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(", ").join(map(sql.Identifier, columns.split(","))),
            values=sql.SQL(", ").join(map(sql.Literal, values.split(","))),
        )
        execute_query(query)

    elif choice == "2":
        # Example for deleting data
        table_name = input("Enter table name: ")
        condition = input("Enter condition (e.g., column=value): ")
        query = f"DELETE FROM {table_name} WHERE {condition};"
        execute_query(query)

    elif choice == "3":
        # Example for updating data
        table_name = input("Enter table name: ")
        updates = input("Enter updates (e.g., column=new_value): ")
        condition = input("Enter condition (e.g., column=value): ")
        query = f"UPDATE {table_name} SET {updates} WHERE {condition};"
        execute_query(query)

    elif choice == "4":
        # Example for searching data
        table_name = input("Enter table name: ")
        condition = input("Enter condition (e.g., column=value): ")
        query = f"SELECT * FROM {table_name} WHERE {condition};"
        execute_query(query, is_select=True)

    if choice == "5":
        # Example for aggregate functions
        table_name = input("Enter table name: ")
        column = input("Enter column name for aggregation: ")
        agg_function = input(
            "Enter aggregate function (e.g., SUM, AVG, COUNT, MIN, MAX): "
        )
        query = f"SELECT {agg_function}({column}) FROM {table_name};"
        execute_query(query, is_select=True)

    elif choice == "6":
        # Example for sorting
        table_name = input("Enter table name: ")
        column = input("Enter column name to sort by: ")
        order = input("Enter sort order (ASC or DESC): ")
        query = f"SELECT * FROM {table_name} ORDER BY {column} {order};"
        execute_query(query, is_select=True)

    elif choice == "7":
        # Example for joins
        table1 = input("Enter first table name: ")
        table2 = input("Enter second table name: ")
        key1 = input(f"Enter join key for {table1}: ")
        key2 = input(f"Enter join key for {table2}: ")
        query = f"SELECT * FROM {table1} INNER JOIN {table2} ON {table1}.{key1} = {table2}.{key2};"
        execute_query(query, is_select=True)

    elif choice == "8":
        # Example for grouping
        table_name = input("Enter table name: ")
        column = input("Enter column name to group by: ")
        query = f"SELECT {column}, COUNT(*) FROM {table_name} GROUP BY {column};"
        execute_query(query, is_select=True)

    elif choice == "9":
        # Example for subqueries
        table_name = input("Enter table name: ")
        column = input("Enter column name to match: ")
        subquery_table = input("Enter subquery table name: ")
        subquery_column = input("Enter subquery column name: ")
        query = f"SELECT * FROM {table_name} WHERE {column} IN (SELECT {subquery_column} FROM {subquery_table});"
        execute_query(query, is_select=True)

    elif choice == "10":
        # Example for transactions
        # For simplicity, let's assume the user knows to input SQL commands separated by ";"
        commands = input("Enter your transaction commands separated by ';': ").split(
            ";"
        )
        connection = connect_to_db()
        try:
            cursor = connection.cursor()
            for command in commands:
                cursor.execute(command.strip())
            connection.commit()
            print("Transaction completed successfully.")
        except DatabaseError as error:
            connection.rollback()
            print(f"Transaction failed. Error: {error}")
        finally:
            cursor.close()
            connection.close()

    elif choice == "11":
        print(
            "Error Handling is integrated within each operation via try-except blocks."
        )
    
    elif choice == "12":
        exit()


if __name__ == "__main__":
    while True:
        main()
