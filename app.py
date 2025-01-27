from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_number TEXT,
        contractor_name TEXT,
        contract_number TEXT,
        award_date TEXT,
        original_amount REAL,
        revised_amount REAL,
        committed_dbe REAL,
        report_date TEXT,
        final_report TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id INTEGER,
        vendor_name TEXT,
        contract_type TEXT,
        original_amount REAL,
        award_date TEXT,
        certified_dbe TEXT,
        paid_this_period REAL,
        paid_to_date REAL,
        FOREIGN KEY(report_id) REFERENCES reports(id)
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Collect data from the form
        project_number = request.form['project_number']
        contractor_name = request.form['contractor_name']
        contract_number = request.form['contract_number']
        award_date = request.form['award_date']
        original_amount = request.form['original_amount']
        revised_amount = request.form['revised_amount']
        committed_dbe = request.form['committed_dbe']
        report_date = request.form['report_date']
        final_report = request.form['final_report']

        # Save report data
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO reports (
            project_number, contractor_name, contract_number, award_date,
            original_amount, revised_amount, committed_dbe, report_date, final_report
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (project_number, contractor_name, contract_number, award_date,
                   original_amount, revised_amount, committed_dbe, report_date, final_report))
        report_id = c.lastrowid

        # Save payment data
        for i in range(10):  # Assuming a max of 10 rows for simplicity
            vendor_name = request.form.get(f'vendor_name_{i}')
            if not vendor_name:
                continue
            contract_type = request.form.get(f'contract_type_{i}')
            original_amount = request.form.get(f'original_amount_{i}')
            award_date = request.form.get(f'award_date_{i}')
            certified_dbe = request.form.get(f'certified_dbe_{i}')
            paid_this_period = request.form.get(f'paid_this_period_{i}')
            paid_to_date = request.form.get(f'paid_to_date_{i}')
            
            c.execute('''INSERT INTO payments (
                report_id, vendor_name, contract_type, original_amount, award_date,
                certified_dbe, paid_this_period, paid_to_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (report_id, vendor_name, contract_type, original_amount, award_date,
                       certified_dbe, paid_this_period, paid_to_date))
        
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('submit.html')

@app.route('/reports')
def reports():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reports')
    reports_data = c.fetchall()
    conn.close()
    return render_template('reports.html', reports=reports_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
