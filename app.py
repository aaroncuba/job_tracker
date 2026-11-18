from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection
import json

app = Flask(__name__)
app.secret_key = 'secret123'

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT COUNT(*) as total FROM companies')
    companies_count = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM jobs')
    jobs_count = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM applications')
    apps_count = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM contacts')
    contacts_count = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    stats = {
        'companies': companies_count,
        'jobs': jobs_count,
        'applications': apps_count,
        'contacts': contacts_count
    }
    return render_template('dashboard.html', stats=stats)

# Companies CRUD
@app.route('/companies')
def companies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies ORDER BY company_id DESC')
    company_list = cursor.fetchall()

    edit_data = None
    edit_id = request.args.get('edit_id')
    if edit_id:
        cursor.execute('SELECT * FROM companies WHERE company_id = %s', (edit_id,))
        edit_data = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('companies.html', companies=company_list, edit_data=edit_data)

@app.route('/companies/add', methods=['POST'])
def add_company():
    name = request.form.get('company_name', '').strip()
    if not name:
        flash('Company name is required.', 'error')
        return redirect(url_for('companies'))

    industry = request.form.get('industry', '').strip() or None
    website = request.form.get('website', '').strip() or None
    city = request.form.get('city', '').strip() or None
    state = request.form.get('state', '').strip() or None
    notes = request.form.get('notes', '').strip() or None

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO companies (company_name, industry, website, city, state, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (name, industry, website, city, state, notes))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Company added.', 'success')
    return redirect(url_for('companies'))

@app.route('/companies/update/<int:id>', methods=['POST'])
def update_company(id):
    name = request.form.get('company_name', '').strip()
    if not name:
        flash('Company name is required.', 'error')
        return redirect(url_for('companies', edit_id=id))

    industry = request.form.get('industry', '').strip() or None
    website = request.form.get('website', '').strip() or None
    city = request.form.get('city', '').strip() or None
    state = request.form.get('state', '').strip() or None
    notes = request.form.get('notes', '').strip() or None

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = '''
        UPDATE companies
        SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s
        WHERE company_id = %s
    '''
    cursor.execute(sql, (name, industry, website, city, state, notes, id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Company updated.', 'success')
    return redirect(url_for('companies'))

@app.route('/companies/delete/<int:id>', methods=['POST'])
def delete_company(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM companies WHERE company_id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Company deleted.', 'success')
    return redirect(url_for('companies'))

# Jobs CRUD
@app.route('/jobs')
def jobs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
        SELECT jobs.*, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.job_id DESC
    ''')
    job_list = cursor.fetchall()

    for j in job_list:
        if j['requirements']:
            skills = json.loads(j['requirements']) if isinstance(j['requirements'], str) else j['requirements']
            j['skills_text'] = ', '.join(skills)
        else:
            j['skills_text'] = ''

    cursor.execute('SELECT company_id, company_name FROM companies ORDER BY company_name')
    company_list = cursor.fetchall()

    edit_data = None
    edit_skills = ''
    edit_id = request.args.get('edit_id')
    if edit_id:
        cursor.execute('SELECT * FROM jobs WHERE job_id = %s', (edit_id,))
        edit_data = cursor.fetchone()
        if edit_data and edit_data['requirements']:
            skills = json.loads(edit_data['requirements']) if isinstance(edit_data['requirements'], str) else edit_data['requirements']
            edit_skills = ', '.join(skills)

    cursor.close()
    conn.close()
    return render_template('jobs.html', jobs=job_list, companies=company_list, edit_data=edit_data, edit_skills=edit_skills)

@app.route('/jobs/add', methods=['POST'])
def add_job():
    company_id = request.form.get('company_id')
    title = request.form.get('job_title', '').strip()
    if not company_id or not title:
        flash('Company and job title are required.', 'error')
        return redirect(url_for('jobs'))

    job_type = request.form.get('job_type')
    salary_min = request.form.get('salary_min') or None
    salary_max = request.form.get('salary_max') or None
    job_url = request.form.get('job_url', '').strip() or None
    date_posted = request.form.get('date_posted') or None

    raw_skills = request.form.get('requirements', '')
    skills_list = [s.strip() for s in raw_skills.split(',') if s.strip()]
    requirements_json = json.dumps(skills_list)

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (company_id, title, job_type, salary_min, salary_max, job_url, date_posted, requirements_json))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Job added.', 'success')
    return redirect(url_for('jobs'))

@app.route('/jobs/update/<int:id>', methods=['POST'])
def update_job(id):
    company_id = request.form.get('company_id')
    title = request.form.get('job_title', '').strip()
    if not company_id or not title:
        flash('Company and job title are required.', 'error')
        return redirect(url_for('jobs', edit_id=id))

    job_type = request.form.get('job_type')
    salary_min = request.form.get('salary_min') or None
    salary_max = request.form.get('salary_max') or None
    job_url = request.form.get('job_url', '').strip() or None
    date_posted = request.form.get('date_posted') or None

    raw_skills = request.form.get('requirements', '')
    skills_list = [s.strip() for s in raw_skills.split(',') if s.strip()]
    requirements_json = json.dumps(skills_list)

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = '''
        UPDATE jobs
        SET company_id = %s, job_title = %s, job_type = %s, salary_min = %s, salary_max = %s,
            job_url = %s, date_posted = %s, requirements = %s
        WHERE job_id = %s
    '''
    cursor.execute(sql, (company_id, title, job_type, salary_min, salary_max, job_url, date_posted, requirements_json, id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Job updated.', 'success')
    return redirect(url_for('jobs'))

@app.route('/jobs/delete/<int:id>', methods=['POST'])
def delete_job(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM jobs WHERE job_id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Job deleted.', 'success')
    return redirect(url_for('jobs'))

# Applications CRUD
@app.route('/applications')
def applications():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_id DESC
    ''')
    app_list = cursor.fetchall()

    for a in app_list:
        if a['interview_data']:
            data = json.loads(a['interview_data']) if isinstance(a['interview_data'], str) else a['interview_data']
            a['notes_text'] = data.get('notes', '')
        else:
            a['notes_text'] = ''

    cursor.execute('''
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.job_title
    ''')
    job_list = cursor.fetchall()

    edit_data = None
    edit_notes = ''
    edit_id = request.args.get('edit_id')
    if edit_id:
        cursor.execute('SELECT * FROM applications WHERE application_id = %s', (edit_id,))
        edit_data = cursor.fetchone()
        if edit_data and edit_data['interview_data']:
            data = json.loads(edit_data['interview_data']) if isinstance(edit_data['interview_data'], str) else edit_data['interview_data']
            edit_notes = data.get('notes', '')

    cursor.close()
    conn.close()
    return render_template('applications.html', applications=app_list, jobs=job_list, edit_data=edit_data, edit_notes=edit_notes)

@app.route('/applications/add', methods=['POST'])
def add_application():
    job_id = request.form.get('job_id')
    app_date = request.form.get('application_date')
    if not job_id or not app_date:
        flash('Job and application date are required.', 'error')
        return redirect(url_for('applications'))

    status = request.form.get('status', 'Applied')
    resume_version = request.form.get('resume_version', '').strip() or None
    cover_letter = int(request.form.get('cover_letter_sent', 0))
    notes = request.form.get('interview_notes', '').strip()
    interview_json = json.dumps({'notes': notes}) if notes else None

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (job_id, app_date, status, resume_version, cover_letter, interview_json))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Application added.', 'success')
    return redirect(url_for('applications'))

@app.route('/applications/update/<int:id>', methods=['POST'])
def update_application(id):
    job_id = request.form.get('job_id')
    app_date = request.form.get('application_date')
    if not job_id or not app_date:
        flash('Job and application date are required.', 'error')
        return redirect(url_for('applications', edit_id=id))

    status = request.form.get('status', 'Applied')
    resume_version = request.form.get('resume_version', '').strip() or None
    cover_letter = int(request.form.get('cover_letter_sent', 0))
    notes = request.form.get('interview_notes', '').strip()
    interview_json = json.dumps({'notes': notes}) if notes else None

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = '''
        UPDATE applications
        SET job_id = %s, application_date = %s, status = %s, resume_version = %s, cover_letter_sent = %s, interview_data = %s
        WHERE application_id = %s
    '''
    cursor.execute(sql, (job_id, app_date, status, resume_version, cover_letter, interview_json, id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Application updated.', 'success')
    return redirect(url_for('applications'))

@app.route('/applications/delete/<int:id>', methods=['POST'])
def delete_application(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM applications WHERE application_id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Application deleted.', 'success')
    return redirect(url_for('applications'))

# Contacts CRUD
@app.route('/contacts')
def contacts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.contact_id DESC
    ''')
    contact_list = cursor.fetchall()

    cursor.execute('SELECT company_id, company_name FROM companies ORDER BY company_name')
    company_list = cursor.fetchall()

    edit_data = None
    edit_id = request.args.get('edit_id')
    if edit_id:
        cursor.execute('SELECT * FROM contacts WHERE contact_id = %s', (edit_id,))
        edit_data = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('contacts.html', contacts=contact_list, companies=company_list, edit_data=edit_data)

@app.route('/contacts/add', methods=['POST'])
def add_contact():
    company_id = request.form.get('company_id')
    name = request.form.get('contact_name', '').strip()
    if not company_id or not name:
        flash('Company and contact name are required.', 'error')
        return redirect(url_for('contacts'))

    title = request.form.get('title', '').strip() or None
    email = request.form.get('email', '').strip() or None
    phone = request.form.get('phone', '').strip() or None
    linkedin = request.form.get('linkedin_url', '').strip() or None
    notes = request.form.get('notes', '').strip() or None

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (company_id, name, title, email, phone, linkedin, notes))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Contact added.', 'success')
    return redirect(url_for('contacts'))

@app.route('/contacts/update/<int:id>', methods=['POST'])
def update_contact(id):
    company_id = request.form.get('company_id')
    name = request.form.get('contact_name', '').strip()
    if not company_id or not name:
        flash('Company and contact name are required.', 'error')
        return redirect(url_for('contacts', edit_id=id))

    title = request.form.get('title', '').strip() or None
    email = request.form.get('email', '').strip() or None
    phone = request.form.get('phone', '').strip() or None
    linkedin = request.form.get('linkedin_url', '').strip() or None
    notes = request.form.get('notes', '').strip() or None

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = '''
        UPDATE contacts
        SET company_id = %s, contact_name = %s, title = %s, email = %s, phone = %s, linkedin_url = %s, notes = %s
        WHERE contact_id = %s
    '''
    cursor.execute(sql, (company_id, name, title, email, phone, linkedin, notes, id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Contact updated.', 'success')
    return redirect(url_for('contacts'))

@app.route('/contacts/delete/<int:id>', methods=['POST'])
def delete_contact(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE contact_id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Contact deleted.', 'success')
    return redirect(url_for('contacts'))

@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    user_skills = ''
    results = None

    if request.method == 'POST':
        user_skills = request.form.get('skills', '').strip()
        skill_set = {s.strip().lower() for s in user_skills.split(',') if s.strip()}

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT jobs.job_id, jobs.job_title, jobs.requirements, companies.company_name
            FROM jobs
            JOIN companies ON jobs.company_id = companies.company_id
        ''')
        all_jobs = cursor.fetchall()
        cursor.close()
        conn.close()

        results = []
        for j in all_jobs:
            if not j['requirements']:
                continue
            req_skills = json.loads(j['requirements']) if isinstance(j['requirements'], str) else j['requirements']
            if not req_skills:
                continue

            matched = [s for s in req_skills if s.lower() in skill_set]
            missing = [s for s in req_skills if s.lower() not in skill_set]
            percent = round((len(matched) / len(req_skills)) * 100)

            results.append({
                'job_title': j['job_title'],
                'company_name': j['company_name'],
                'percent': percent,
                'matched_count': len(matched),
                'total_count': len(req_skills),
                'matched_skills': ', '.join(matched) if matched else 'None',
                'missing_skills': ', '.join(missing)
            })

        results.sort(key=lambda x: (x['percent'], x['matched_count']), reverse=True)

    return render_template('job_match.html', user_skills=user_skills, results=results)

if __name__ == '__main__':
    app.run(debug=True)