from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from api.blog.model import Blog
from api.tags.model import Tag
from api import db

blog_blueprint = Blueprint('blogs', __name__)


@blog_blueprint.route('/api/v1/blog/add', methods=["POST"])
# @jwt_required
def create_blog():
    data = request.get_json()
    new_blog = Blog(title=data['title'], content=data['content'],
                    image=data['image'])

    for tag in data['tags']:
        current_tag = Tag.query.filter_by(name=tag).first()
        if current_tag:
            current_tag.blogs_associated.append(new_blog)
        else:
            new_tag = Tag(name=tag)
            new_tag.blogs_associated.append(new_blog)
            db.session.add(new_tag)

    db.session.add(new_blog)
    db.session.commit()

    return jsonify({'id': getattr(new_blog, 'id')})


@blog_blueprint.route('/api/v1/blogs', methods=['GET'])
def get_all_blogs():
    all_blog = Blog.query.all()
    serialized_blogs = [blog.serialize for blog in all_blog]

    return jsonify({'all_blogs': serialized_blogs})


@blog_blueprint.route('/api/v1/blog/<int:id>', methods=['GET'])
def get_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    serialized_blog = blog.serialize
    serialized_blog['tags'] = [tag.serialize for tag in blog.tags]

    return jsonify({'blog': serialized_blog})


@blog_blueprint.route('/api/v1/blog/update/<int:id>', methods=['PUT'])
# @jwt_required
def update_blog(id):
    data = request.get_json()
    blog = Blog.query.filter_by(id=id).first()
    blog.title = data['title']
    blog.content = data['content']
    blog.image = data['image']

    db.session.commit()

    return jsonify({'message': 'blog has been updated', 'blog_id': blog.id})


@blog_blueprint.route('/api/v1/blog/delete/<int:id>', methods=['DELETE'])
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()

    return jsonify({'message': 'blog was deleted',
                    'blog_id': id})
