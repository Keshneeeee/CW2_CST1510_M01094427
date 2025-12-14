import pandas as pd #Import the pandas library
from week_8.app.data.db import connect_database #Import the function to connect to the database
#Function to count the incidents by types
def get_incidents_by_type_count(conn=None):
    #Determines if the connection should be closed after query
    close = False
    if conn is None:
        #If there is no connection. create one and mark it to close after query
        conn = connect_database() #Connect to database
        close = True
    #SQL query to count group by type, sort by count, starting by descending order
    query = """
    Select incident_type, count(*) as count
    from cyber_incidents
    group by incident_type
    order by count DESC
    """
    #Execute the SQL query directly in the pandas dataframe
    df = pd.read_sql_query(query, conn)
    if close:
        conn.close()
    return df #Return the dataframe with incidents data counts

#Function to count incidents by severity status
def get_high_severity_status(conn=None):
    close = False
    if conn is None:
        conn = connect_database()
        close = True
    #SQL query to count incidents by severity status, starting by descending order
    query = """
    Select status, count(*) as count
    from cyber_incidents
    where severity = 'High'
    group by status
    order by count DESC
    """
    #Execute SQL query directly in the pandas data frame
    df = pd.read_sql_query(query, conn)
    if close:
        conn.close()
    return df #Return the data frame with incidents data counts

#Function to count incidents by types with many cases
def get_incident_type_with_many_cases(conn, min_counts):
    #SQL query to count incident types starting by descending order
    query = """
    Select incident_type, count(*) as count
    from cyber_incidents
    group by incident_type
    having count(*) as count
    order by count DESC
    """
    #Execute SQL query directly in the pandas data frame
    df = pd.read_sql_query(query, conn)
    return df #Return the data frame with incidents data counts

#Function to retrieve datasets grouped by uploader
def get_datasets_by_uploader(conn=None):
    close = False
    if conn is None:
        conn = connect_database()
        close = True
    #SQL query to count uploader, sorted in descending order
    query = """
    Select uploaded_by, count(*) as count
    from datasets_metadata
    group by uploaded_by
    order by count DESC
    """
    df = pd.read_sql_query(query, conn) #Execute the query into a pandas dataframe
    if close:
        conn.close()
    return df #Return results in the dataframe

#Function to retrieve large datasets
def get_large_datasets(conn=None, min_rows=100000):
    close = False
    if conn is None:
        conn = connect_database()
        close = True
    #SQL Query to select name, rows and columns from large datasets. Use of '?' to prevent SQL injection
    query = """
    select name, rows, columns, uploaded_by
    from datasets_metadata
    where rows > ?
    order by rows DESC
    """
    #Execute SQL query and read into a pandas dataframe
    df = pd.read_sql_query(query, conn, params={"rows": min_rows})
    if close:
        conn.close()
    return df #Return results as a panne

#Function to retrieve datasets monthly
def get_datasets_upload_trends_monthly(conn):
    #Function to select the month and count the datasets. in descending order
    query = """
    select strftime('5y-%m', uploaded_date) as month, count(*) as count
    from datasets_metadata
    group by month
    order by month DESC
    """
    #Execute SQL query and read into a panda dataframe
    df = pd.read_sql_query(query, conn)
    return df #Return results as a panne

#Function to retrieve high priority tickets
def get_high_priority_tickets(conn=None):
    close = False
    if conn is None:
        conn = connect_database()
        close = True
    #SQL query to select ticket's priority
    query = """
    select *
    from it_tickets
    where priority = 'High'
    order by ticket_id ASC
    """
    #Execute SQL query and read into pandas dataframe
    df = pd.read_sql_query(query, conn)
    if close:
        conn.close()
    return df

#Function to get ticket status by high priority
def get_high_priority_tickets_by_status(conn):
    #SQL query to select status, read from descending order
    query = """
    select status, count(*) as count
    from it_tickets
    where status = 'High'
    group by status
    order by count DESC
    """
    #Execute SQL query and read into pandas dataframe
    df = pd.read_sql_query(query, conn)
    return df

#Function to retrieve ticket status by resolution with minimum resolution time is 24 hours
def get_slow_resolution_tickets_by_status(conn, min_resolution_time =24):
    #SQL query to select status resolution time and read it from descending order
    query = """
    select status, AVG(resolution_time_hours) as avg_resolution
    from it_tickets
    group by status
    order by count DESC
    """
    df = pd.read_sql_query(query, conn, params={"avg_resolution": min_resolution_time})
    return df

#Function to retrieve average resolution time by staff
def get_avg_resolution_by_staff(conn=None):
    close = False
    if conn is None:
        conn = connect_database()
        close = True
    #SQL query to select average resolution time
    query = """
    select assigned_to, AVG(resolution_time_hours) as avg_resolution_time
    from it_tickets
    where resolution_time_hours is not null
    group by assigned_to
    order by avg_resolution_time DESC
    """
    #Execute sql quesry and read results in pandas dataframe
    df = pd.read_sql_query(query, conn)
    if close:
        conn.close()
    return df #Return results in panne

#Function to retrieve resolution tickets, with atleast 24 hours
def get_slow_resolution_tickets(conn, min_resolution_time =24):
    #SQL query to select resultion time from tickets in descending order. use of '?' to prevent SQL injection
    query = """
    select *
    from it_tickets
    where resolution_time_hours > ?
    order by resolution_time_hours DESC
    """
    df = pd.read_sql_query(query, conn, params={"avg_resolution": min_resolution_time})
    return df






