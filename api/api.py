from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Создаем приложение Flask
app = Flask(__name__)

# Настраиваем подключение к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\practice Kh\\study_var.db'
db = SQLAlchemy(app)


# Определяем модель таблицы
class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    login = db.Column(db.Text, unique=True, nullable=False)
    course_id = db.Column(db.Integer)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<User {self.user_id}: {self.name} {self.surname}>'


# Маршрут для получения всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {
            'user_id': user.user_id,
            'name': user.name,
            'surname': user.surname,
            'login': user.login,
            'course_id': user.course_id,
            'password': user.password
        }
        result.append(user_data)
    return jsonify(result)


# Маршрут для получения конкретного пользователя по id
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)

    user_data = {
        'user_id': user.user_id,
        'name': user.name,
        'surname': user.surname,
        'login': user.login,
        'course_id': user.course_id,
        'password': user.password
    }

    return jsonify(user_data)


# Маршрут для создания нового пользователя
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    new_user = User(
        name=data['name'],
        surname=data['surname'],
        login=data['login'],
        course_id=data['course_id'],
        password=data['password']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Пользователь успешно создан!'})


# Маршрут для обновления информации о пользователе
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    user = User.query.get_or_404(user_id)

    if 'name' in data:
        user.name = data['name']
    if 'surname' in data:
        user.surname = data['surname']
    if 'login' in data:
        user.login = data['login']
    if 'course_id' in data:
        user.course_id = data['course_id']
    if 'password' in data:
        user.password = data['password']

    db.session.commit()

    return jsonify({'message': 'Информация о пользователе успешно обновлена!'})


# Маршрут для удаления пользователя
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Пользователь успешно удален!'})


# Запускаем сервер
if __name__ == '__main__':
    app.run(debug=True)