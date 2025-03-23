from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage

import os

user_id = "user_id"

# Get tools
@tool
def get_name(user_id: str):
    """Returns the name stored in a database associated with a user_id.

    Args:
        -user_id: the id of the calling user in strings

    Returns:
        The name of the calling user or error if the calling user's id is not registered in the database
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute(f"SELECT name FROM users WHERE id = '{user_id}'")
        row = cursor.fetchone()
            
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        return f"ERROR MESSAGE: {user_id} is not registered with the database"

@tool
def get_assets(user_id: str):
    """Returns the financial assets owned by the calling user identified with a user_id from a database.

    Args:
        -user_id: the id of the calling user in strings

    Returns:
        A list of assets owned by the calling user or error if the calling user's id is not registered in the database
        
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        results = []
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute(f"SELECT id, amount, description, type FROM assets WHERE user_id = '{user_id}'")
        rows = cursor.fetchall()
        
        for row in rows:
            obj = {}
            obj["asset_id"] = row[0]
            obj["asset_amount"] = row[1]
            obj["asset_description"] = row[2]
            obj["asset_type"] = row[3]
            results.append(obj)
            
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

@tool
def get_goals(user_id: str):
    """Returns the financial goals set by the calling user identified with a user_id from a database.

    Args:
        -user_id: the id of the calling user in strings

    Returns:
        A list of financial goals set by the calling user or error if the calling user's id is not registered in the database
        
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        results = []
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute(f"SELECT id, description FROM goals WHERE user_id = '{user_id}'")
        rows = cursor.fetchall()
        
        for row in rows:
            obj = {}
            obj["goal_id"] = row[0]
            obj["goal_description"] = row[1]
            results.append(obj)
            
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

@tool
def get_transactions(user_id: str):
    """Returns the past transactions made by the calling user identified with a user_id from a database.

    Args:
        -user_id: the id of the calling user in strings

    Returns:
        A list of transactions made by the calling user or error if the calling user's id is not registered in the database
        
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        results = []
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute(f"SELECT id FROM accounts WHERE user_id = '{user_id}'")
        accounts = cursor.fetchall()
        
        for account in accounts:
            account_id = account[0]
            cursor.execute(f"SELECT id, category, amount, description, date FROM transactions WHERE account_id = {account_id}")
            transactions = cursor.fetchall()
            for transaction in transactions:
                obj = {}
                obj["id"] = transaction[0]
                obj["category"] = transaction[1]
                obj["amount"] = transaction[2]
                obj["description"] = transaction[3]
                obj["date"] = transaction[4]
                results.append(obj)
        
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

@tool
def get_accounts(user_id: str):
    """Returns all the banking accounts owned by the calling user identified with a user_id from a database.

    Args:
        -user_id: the id of the calling user in strings

    Returns:
        A list of banking accounts owned by the calling user or error if the calling user's id is not registered in the database
        
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        results = []
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute(f"SELECT user_id, type, balance, institution FROM accounts WHERE user_id = '{user_id}'")
        rows = cursor.fetchall()
        
        for row in rows:
            obj = {}
            obj["user_id"] = row[0]
            obj["account_type"] = row[1]
            obj["account_balance"] = row[2]
            obj["account_institution"] = row[3]
            results.append(obj)
            
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

@tool
def get_current_time():
    """Gets the current date and time.

    Args:
        None

    Returns:
        The current date and time.
        
    """
    try:
        from datetime import datetime

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return "Current time: " + current_time
    except Exception as e:
        return f"ERROR MESSAGE: {e}"
    
# Create tools
@tool
def create_user(user_id: str, name: str):
    """Asks the user for its name to register the user to the database.

    Args:
        -user_id: the id of the calling user in strings
        -name: the name of the calling user

    Returns:
        A message indicating whether the user has successfully been registered.
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, name))
        conn.commit()
            
        cursor.close()
        conn.close()
        return f"SUCCESS MESSAGE: user {user_id} with name f{name} has successfully been registered."
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

@tool
def create_goal(user_id: str, description: str):
    """Stores the calling user's financial goal to the database using the user id..

    Args:
        -user_id: the id of the calling user in strings
        -description: the description of the calling user's financial goals

    Returns:
        A message indicating whether the goal has successfully been stored.
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute("INSERT INTO goals (user_id, description) VALUES (%s, %s)", (user_id, description))
        conn.commit()
            
        cursor.close()
        conn.close()
        return f"SUCCESS MESSAGE: user {user_id}'s goal has successfully been registered."
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

@tool
def create_account(user_id: str, account_type: str, balance: float, institution:str):
    """Creates a new banking account for the calling user in the database.

    Args:
        -user_id: the id of the calling user in strings
        -account_type: the type of the banking account: checking, savings, etc.
        -balance: the balance in dollars that the banking account starts with
        -institution: the institution that the banking account belongs to

    Returns:
        A message indicating whether the bought asset has successfully been stored.
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute("INSERT INTO accounts (user_id, type, balance, institution) VALUES (%s, %s, %s, %s)", (user_id, account_type, balance, institution))
        conn.commit()
            
        cursor.close()
        conn.close()
        return f"SUCCESS MESSAGE: user {user_id}'s newly created account has successfully been registered."
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

@tool
def create_asset(user_id: str, amount: float, description: str, asset_type:str):
    """Stores the asset that the calling user has just bought to the database. Examples of assets would be ETFs, stocks, bonds, etc but not daily purchases.

    Args:
        -user_id: the id of the calling user in strings
        -amount: the amount of this asset in dollars that the user has purchased
        -description: the description of the asset bought
        -asset_type: the type of the asset bought

    Returns:
        A message indicating whether the bought asset has successfully been stored.
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute("INSERT INTO assets (user_id, amount, description, type) VALUES (%s, %s, %s, %s)", (user_id, amount, description, asset_type))
        conn.commit()
            
        cursor.close()
        conn.close()
        return f"SUCCESS MESSAGE: user {user_id}'s newly purchased asset has successfully been registered."
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

@tool
def create_transaction(account_id: str, category: str, amount: float, description: str, date: str):
    """Stores the transaction that the calling user has just made to the database. Transactions include any spending of money or earning of money.

    Args:
        -account_id: the id of the account that the transaction is made from or to
        -category: the category of the transaction: income, expense, entertainment, food, grocery, etc.
        -amount: the amount of dollars involved in this transaction
        -description: the description of this transaction
        -date: the date of where the transaction is made

    Returns:
        A message indicating whether the transaction has successfully been stored.
    """
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user="root",
            database="plan_wise"
        )
        cursor = conn.cursor()
        # Retrieve data
        cursor.execute("INSERT INTO transactions (account_id, category, amount, description, date) VALUES (%s, %s, %s, %s, %s)", (account_id, category, amount, description, date))
        conn.commit()
            
        cursor.close()
        conn.close()
        return f"SUCCESS MESSAGE: new transaction has successfully been registered into {account_id}."
    except Exception as e:
        return f"ERROR MESSAGE: {e}"

def get_agent():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    tools = [get_name, get_assets, get_goals, get_transactions, get_accounts, get_current_time, create_user, create_account, create_goal, create_asset]

    prompt = f"""
    You are a helpful assistant and financial expert who helps students with financial planning and portfolio management.
    You will provide financial advice because you know that your users will act at their own risk.
    You may not need to use tools for every query - the user may just want to chat!"
    You are currently serving user with id {user_id}.
    """

    memory = MemorySaver()
    agent = create_react_agent(model, tools, prompt=prompt, checkpointer=memory)

    return agent