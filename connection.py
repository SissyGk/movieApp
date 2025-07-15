import mysql.connector 
def create_connection(): 
    try:
        connection=mysql.connector.connect( 
            host='localhost', 
            user='root', 
            password='', 
            database='netflix',
            port=3306 
        )
        return connection 
    except mysql.connector.Error as err:         
        return None
    


