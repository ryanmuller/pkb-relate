# PKB Relate

## Usage

1. Clone this repository
2. Create a sqlite3 database with the format used in ryanmuller/pkb-demos
3. Modify `lsi.py` to point to your database
4. Install requirements: `pip install -r requirements.txt`
5. Train the document similar server: `python lsi.py`
6. Run the demo: `python app.py 8080`
7. Access the demo in your browser: http://localhost:8080
