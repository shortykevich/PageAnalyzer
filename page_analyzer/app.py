import os

import requests
from page_analyzer.response_parser import parse_response
from page_analyzer.urls import is_valid_url, normalize_url
from dotenv import load_dotenv
from page_analyzer.database import (
    get_urls_list,
    get_url_by_name,
    get_url_by_id,
    add_url,
    add_url_check,
    get_url_checks,
)
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


@app.get('/')
def index():
    message = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        message=message
    )


@app.get('/urls')
def list_urls():
    urls = get_urls_list()
    return render_template(
        "layout/sites.html",
        urls=urls
    )


@app.get('/urls/<int:id>')
def urls(id):
    url = get_url_by_id(id)
    if not url:
        return render_template("layout/page_not_found.html"), 404

    checks = get_url_checks(id)
    message = get_flashed_messages(with_categories=True)
    return render_template(
        "layout/site_page.html",
        message=message,
        url=url,
        checks=checks
    )


@app.post('/urls/<int:id>/checks')
def checks(id):
    url = get_url_by_id(id)
    try:
        r = requests.get(url['name'])
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for('urls', id=id))

    check = {'id': id, 'code': r.status_code}

    url_info = parse_response(r.text)
    check.update(url_info)

    add_url_check(check)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls', id=id))


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


if __name__ == '__main__':
    app.run()
