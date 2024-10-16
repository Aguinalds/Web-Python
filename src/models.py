from src import database
from datetime import datetime
from src import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship("Posts", backref='user', lazy=True)

class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    
    # Corrija a relação com Like
    likes = database.relationship("Like", backref='post', lazy=True)

    def count_likes(self):
        return len(self.likes)

    def user_likes(self, user):
        like = Like.query.filter_by(user_id=user.id, post_id=self.id).first()
        return like is not None
    
    def delete_post(self):
        # Exclui todos os likes associados ao post
        Like.query.filter_by(post_id=self.id).delete()

        # Exclui o próprio post
        database.session.delete(self)
        database.session.commit()

class Like(database.Model):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable=False)
