import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain import OpenAI
from db_connector import connect
import pandas as pd

load_dotenv()

def abba(input):
    prompt_template = PromptTemplate(input_variables=["input"], template = '''Given below are the table structures in analytics database raw schema in snowflake cloud database
            1. Brands
            - brand_id (Primary Key)
            - brand_name

            2. Categories
            - category_id (Primary Key)
            - category_name

            3. Customers
            - customer_id (Primary Key)
            - first_name
            - last_name
            - phone

            4. OrderItem
            - item_id (Primary Key)
            - order_id (Foreign Key refrencing Order)
            - product_id (Foreign Key referencing Product)
            - quantity
            - list_price
            - discount

            5. Orders
            - order_id (Primary Key)
            - customer_id (Foreign Key referencing Customer)
            - order_status
            - order_date
            - required_date
            - shipped_date
            - store_id (Foreign Key referencing Stores)
            - staff_id (Foreign Key referencing Staff)
            
            6. Products
            - product_id (Primary Key)
            - product_name (Foreign Key referencing User)
            - brand_id (Foreign Key referencing Brands)
            - category_id (Foreign Key referencing Category)
            - model_year
            - list_price

            7. Staffs
            - staff_id (Primary Key)
            - first_name (Foreign Key referencing User)
            - last_name
            - email
            - phone
            - active
            - store_id (Foreign Key referencing Stores)

            8. Stocks
            - store_id (Primary Key)
            - product_id (Foreign Key referencing Products)
            - quantity
            
            9. Stores
            - store_id (Primary Key)
            - store_name
            - phone
            - email
            - street
            - city
            - state
            - zip_code
                  take user questions and response back with sql query.
              example : 
              user question : How many orders where placed by customer A
              your generated sql query : SELECT COUNT(*) AS num_orders FROM Orders o JOIN Customers c ON o.customer_id = c.customer_id WHERE c.first_name = 'Customer' AND c.last_name = 'A';
              example :
              user question : what are the top 10 products of brands , bought by users
              your generated sql query : SELECT p.product_id, p.product_name, b.brand_name, COUNT(oi.item_id) AS num_items_bought FROM Orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN Products p ON oi.product_id = p.product_id JOIN Brands b ON p.brand_id = b.brand_id GROUP BY p.product_id, p.product_name, b.brand_name ORDER BY num_items_bought DESC LIMIT 10;
              user question : {input}
              your generated sql query : ''')

    llm = OpenAI(temperature=0.9)
    final_prompt = prompt_template.format(input=input)
    response = llm(prompt=final_prompt)
    cursor = connect()
    cursor.execute(response)
    query_results = cursor.fetchall()
     # Get column names from the cursor description
    column_names = [col[0] for col in cursor.description]

    # Create a Pandas DataFrame
    data_frame = pd.DataFrame(query_results, columns=column_names)

    # Print the DataFrame
    #print(data_frame)
    return data_frame

def main():
    st.title("Ask your Database")
    query = st.text_input("Enter your question")
    if query: 
        output = abba(query)
        st.write(output)

if __name__ == "__main__":
    main()