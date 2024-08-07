import os

from page_analyzer.database import (
    get_list_urls,
    get_url_by_name,
    get_url_by_id,
    add_url,
    add_url_check,
    get_url_checks,
)
from page_analyzer.urls import is_valid_url, normalize_url
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    flash,
    request,
    redirect,
    url_for,
    get_flashed_messages,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    message = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        message=message
    )


@app.route('/urls')
def list_urls():
    urls = get_list_urls()
    print(urls)
    return render_template(
        "layout/sites.html",
        urls=urls
    )


@app.route('/urls/<int:id>')
def urls(id):
    url = get_url_by_id(id)
    if not url:
        return render_template("layout/page_not_found.html")

    checks = get_url_checks(id)
    name, created = url['name'], url['created']
    message = get_flashed_messages(with_categories=True)
    return render_template(
        "layout/site_page.html",
        message=message,
        id=id,
        name=name,
        created_at=created,
        checks=checks
    )


@app.post('/urls')
def add():
    form_vals = request.form.to_dict()
    name = form_vals['url']
    if not is_valid_url(name):
        flash('Некорректный URL', 'danger')
        message = get_flashed_messages(with_categories=True)
        return render_template(
            "index.html",
            message=message
        ), 422

    name = normalize_url(name)
    url_in_db = get_url_by_name(name)
    if not url_in_db:
        flash("Страница успешно добавлена", "success")
        url_in_db = add_url(name)
    else:
        flash("Страница уже существует", "info")

    return redirect(url_for('urls', id=url_in_db['id']))


@app.post('/urls/<int:id>/checks')
def checks(id):
    # Make check
    add_url_check(id)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls', id=id))


if __name__ == '__main__':
    app.run()
