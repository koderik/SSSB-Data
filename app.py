from talisman import Talisman
from flask import Flask, request, render_template
import json
import psycopg2
import os
import pdf_scrape
import appartment_analytics

app = Flask(__name__)

# add script.js
csp = {
    'script_src': [
        '\'self\'',
    ],

}
talisman = Talisman(app, force_https=True, content_security_policy=csp)

<<<<<<< HEAD
@app.route("/analytics")
def analytics():
    DATABASE_URL = os.environ["DATABASE_URL"]
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    cur.execute("SELECT * FROM sssbdata_closed")
    rows = cur.fetchall()
    cur.close()
    data = appartment_analytics.analyze(rows)
    return render_template("analytics.html", rows=json.dumps(data))
=======
>>>>>>> parent of f473f24 (feat: :sparkles: added hidden content)

# Add second route for /old to show old data
@app.route("/old")
def old():
    DATABASE_URL = os.environ["DATABASE_URL"]
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    cur.execute("SELECT * FROM sssbdata_closed")
    rows = cur.fetchall()
    cur.close()
    return render_template("old.html", rows=json.dumps(rows))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['pdf']
        if uploaded_file and uploaded_file.content_type == 'application/pdf':
            try:
                merit = pdf_scrape.get_merit(uploaded_file)
                print(merit)
                return render_template('merit.html', merit=merit)
            except:
                error = "Invalid PDF. Please upload a valid transcript PDF without grade distribution."
                return render_template('merit.html', error=error)
        else:
            error = "Invalid file type. Please upload a PDF."
            return render_template('merit.html', error=error)

    print("Fetcing data from database...")
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(
        DATABASE_URL, sslmode='require')
    # Create a cursor object
    cur = conn.cursor()
    # Execute a SELECT statement to retrieve all rows from the table
    cur.execute("SELECT * FROM sssbdata")

    # Fetch all the rows as a list of tuples
    rows = cur.fetchall()

    cur.close()
    conn.close()
    try:
        return render_template("./index.html", rows=json.dumps(rows))

    except Exception as e:
        return str(e)
    

@app.route('/merit', methods=['GET', 'POST'])
def merit():
    return render_template('merit.html')



if __name__ == '__main__':
    # run debug mode
    #app.run(debug=True)
    app.run()
