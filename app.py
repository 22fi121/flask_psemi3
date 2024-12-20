from flask import Flask, render_template, request, redirect # 変更
from flask_sqlalchemy import SQLAlchemy # 追加
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    details = db.Column(db.String(100))

@app.route("/create", methods=["POST"])
def create():
    title = request.form.get("title")
    details = request.form.get("details")
    new_task = Todo(title=title, details=details)
    
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get(id)
    db.session.delete(delete_task)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    update_task = Todo.query.get(id)
    
    if request.method == "POST":
        # フォームからのデータ取得
        title = request.form.get("title")
        details = request.form.get("details")
        
        # タスクを更新
        update_task.title = title
        update_task.details = details
        db.session.commit()
        
        return redirect('/')
    # GETリクエストのときは現在のタスク情報をフォームに表示
    return render_template("update.html", task=update_task)
@app.route("/")
def index():
    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)
if __name__ == "__main__":
    app.run(debug=True)
