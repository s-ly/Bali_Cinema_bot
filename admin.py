# Главный модуль админки для Телеграм-бота Кинотеатр Лии.


from flask import Flask, render_template, request
import sql_func


app = Flask(__name__)

about = 't.me/Bali_Cinema_bot ver 0.1 | 2022.11.11'
title = 'Админка для Телеграм-бота - t.me/Bali_Cinema_bot'

@app.route('/')
def index():
    """Перехватывает корневой адрес."""
    SQL = f"SELECT * FROM users;"
    all_data = sql_func.sql_run(SQL)
    print(all_data)

    return render_template(
        'index.html', 
        the_title = title, 
        the_about = about,
        the_all_data = all_data)


@app.route('/user_edit', methods=['POST'])
def user_edit():
    """После изменения свойст пользователя попадаем сюда."""
    # Получение данных из формы.
    user_id = request.form['user_id']

    # Изменение в БД
    sql_func.sql_change_userData(user_id, 'pay_status', 'ok')

    return render_template(
        'user_edit.html',
        the_title = title,
        the_about = about, 
        the_user_id = user_id)


if __name__ == "__main__":
    app.run(debug=True, host='81.163.31.153', port=5101)
    # app.run(debug=True, host='0.0.0.0')