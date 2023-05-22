from flask import Flask, render_template, abort, request, redirect, send_from_directory
from data import DATA
from datetime import datetime
from smtplib import SMTP

SMTPUSER = 'your gmail id'
SMTPPASS = 'your gmail password'
SMTPHOST = 'smtp.gmail.com'

app = Flask(__name__)
year = datetime.now().year


def get_blog(slug):
    blog_data = False
    for blog in DATA['blogs']:
        if blog['slug'] == slug:
            blog_data = blog
    return blog_data


def send_mail(sub, msg):
    with SMTP(host=SMTPHOST, port=587) as con:
        con.starttls()
        con.login(user=SMTPUSER, password=SMTPPASS)
        message = f"Subject:{sub}\n{msg}"
        con.sendmail(from_addr=SMTPUSER, to_addrs=SMTPUSER, msg=message)
    return True


@app.route('/')
def index():
    DATA['meta_title'] = "Ashish Kumar | Its all about me"
    return render_template('index.html', data=DATA, year=year)


@app.route('/<slug>')
def blog(slug):
    blog_data = get_blog(slug)
    if blog_data:
        DATA['meta_title'] = blog_data['title']
        return render_template('blog.html', data=DATA, year=year, blog=blog_data)
    else:
        abort(404)


@app.route('/submit', methods=["POST"])
def submit():
    name = request.form['name'];
    email = request.form['email']
    comment = request.form['comment']
    subject = f"New query from <{name}>"
    message = f"Hi Admin,\n\n{name} submitted a query from the website contact form. \n\n" \
           f"Here is the details:\nName: {name}\nEmail: {email}\nMessage: {comment}\n\n" \
           f"Thanks,"
    if send_mail(subject, message):
        return redirect('/success')
    else:
        return redirect('/')


@app.route('/success')
def success():
    DATA['meta_title'] = "Thank you"
    return render_template("success.html", data=DATA, year=year)


@app.route('/download')
def download():
    return send_from_directory("static", "resume.pdf", as_attachment=True)


if __name__ == '__main__':
    app.run()
