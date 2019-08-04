import os
from flask import Blueprint, request, render_template, send_from_directory, make_response
from book_down import config
from book_down.book_down import BookDown


view = Blueprint('view',__name__)


@view.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form['book_name']
        if os.path.exists('{}{}.txt'.format(config.book_dir, name)):
            return render_template('book.html', name=name)
        else:
            # try:
            book_down = BookDown(name)
            book_list = book_down.get_book_list()
            return render_template('book_list.html', book_list=book_list)
            # except Exception as e:
            #     return render_template('error.html', error=str(e))

    else:
        return render_template('search.html')


@view.route('/book_down', methods=['GET', 'POST'])
def book_down():
    url = request.args.get('url')
    name = request.args.get('book_name')
    book_down = BookDown(name)
    book_down.down_book_from_bok_url(url)
    return render_template('book.html', name=name)


@view.route('/book_del', methods=['GET', 'POST'])
def book_del():
    name = request.args.get('book_name')
    path = '{}{}'.format(config.book_dir, name)
    if os.path.exists(path):
        os.remove(path)
    return render_template('search.html', name=name)


@view.route('/down_book', methods=['GET', 'POST'])
def down_book():
    name = request.args.get('book_name')
    response = make_response(send_from_directory(config.book_dir, name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(name.encode().decode('latin-1'))
    return response