from flask import render_template, Flask, g  # Import Global Namespace.
# To provide access to the database throughout the application, import the global helper g from flask.

import sqlite3

# Database Path
# create a constant called PATH that contains the path to the already created database.
PATH = "db/jobs.sqlite"

app = Flask(__name__)


# Global Database Attribute
def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        # sqlite3 Row Factory
        # To make accessing data easier, after the if statement in open_connection:
        # Note: All rows returned from the database will be named tuples.
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Query Database Function
# Let’s create a function to make it easier to query the database.
def execute_sql(sql, values=(), commit=False, single=False):
    # Query Database Function Parameters
    # Add four parameters: sql, values, commit, and single.
    # Set the default of values to an empty tuple ().
    # Set the default of commit to False.
    # Set the default of single to False
    connection = open_connection()
    # Query Database Function Execute
    # In the body of execute_sql call the execute function on connection,
    # and pass in the sql and values variables. Assign the return value to a variable called cursor
    cursor = connection.execute(sql, values)
    # Query Database Function Results

    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results


# Close the Connection
# In order to make sure the database connection is closed when the app_context is torn down
@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, "_connection", None)
    if connection is not None:
        connection.close()


@app.route('/')
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, '
                       'employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)