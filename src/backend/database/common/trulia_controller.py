import psycopg
from backend.database.dao.TruliaHouseListingDAO import TruliaHouseListingDAO
from backend.database.services.TruliaHouseListingService import TruliaHouseListingService
from dotenv import load_dotenv
from backend.database.common.DatabaseConnectionPool import DatabaseConnectionPool
import os


# load_dotenv()
# pool = DatabaseConnectionPool(connectionString=os.getenv('CONNECTION_STRING'))
# with pool.managed_connection_cursor(disableAutoCommit=True) as cursor:
#     truliaHouseListingDAO = TruliaHouseListingDAO(cursor)
#     truliaHouseListingService = TruliaHouseListingService(truliaHouseListingDAO)

# # Create a cursor object
# cur = dbConnection.cursor()

# # Execute a query
# cur.execute("SELECT * FROM playing_with_neon")
# column_headers = [desc[0] for desc in cur.description]

# # Print column headers
# print(column_headers)
# rows = cur.fetchall()

# for row in rows:
#     print(row)

# # Close the cursor and connection
# cur.close()
# dbConnection.close()