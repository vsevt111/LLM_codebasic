from sqlalchemy import create_engine
from dotenv import load_dotenv
from few_shot import FewShotPosts
import mysql.connector
import os
load_dotenv()
# initial data to mysql
db_password=os.getenv("DB_PASSWORD")
# Step 2: Create a SQLAlchemy engine to connect to the MySQL database
engine = create_engine(f"mysql+pymysql://root:{db_password}@localhost:3306/post_generator_llm")
def connect():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=db_password,
        database="post_generator_llm"
    )

    # mycursor = mydb.cursor()
    #
    # mycursor.execute(
    #     '''
    #     CREATE TABLE linkedin_posts (
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     text TEXT,
    #     engagement INT,
    #     influencer VARCHAR(100),
    #     line_count INT(255),
    #     language VARCHAR(255),
    #     tags VARCHAR(150),
    #     length VARCHAR(50))
    #     ''')
    # mycursor.close()
    mydb.close()
def initialize():
    fs = FewShotPosts()
    df = fs.df
    df['text']=df.text.str.encode('utf-8', 'ignore').str.decode('utf-8')

    df['tags']=df['tags'].apply(lambda x : ', '.join(x))
    try:

        # engine.connect()
        # Step 3: Convert the Pandas DataFrame to a format for MySQL table insertion
        df.to_sql(name='linkedin_posts', con=engine, if_exists='append', index=False)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # connect()
    initialize()