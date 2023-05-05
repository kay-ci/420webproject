#420WebProject
    https://gitlab.com/server-side-programming/420webproject.git
##Group Members List
1. Simona Georgiana Dragomir
2. Jimmy Xu, 2138599
3. Kayci Nicole Davila, 2141560
4. Hernan Mathias Farina Forster

##Development Setup Steps
1. Install Python 3.7 or greater
2. Create a virtual environment (python -m venv .venv)
3. Activate virtual environment (.venv/scripts/activate)
4. Install requirements (pip install -r requirements.txt)
5. Setup DB credentials (environment variables DBUSER and DBPWD)
6. Make sure you are on the Dawson network (VPN, local connection)
7. Run schema.sql to set up the database
8. Run the application flask --app ProjectApp --debug run

##Deployment Setup steps
1. Install Python 3.7 or greater
2. Create a virtual environment (python -m venv .venv)
3. Activate virtual environment (.venv/scripts/activate)
4. Install requirements (pip install -r requirements.txt)
5. Setup DB credentials (environment variables DBUSER and DBPWD)
6. Make sure you are on the Dawson network (VPN, local connection)
7. Run schema.sql to set up the database
8. Run command gunicorn -b 0.0.0.0:8000 'ProjectApp:create_app()'
