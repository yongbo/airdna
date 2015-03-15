# coding: utf-8
from datetime import datetime, date, timedelta
from flask import render_template, Blueprint, redirect, request, url_for, g, \
    get_template_attribute, json, abort
from ..utils.permissions import VisitorPermission, UserPermission, CollectionEditPermission
from ..models import db, User, Piece, PieceVote, PieceComment, Collection, CollectionPiece
from ..forms import CollectionForm

bp = Blueprint('collection', __name__)


@bp.route('/collection/<int:uid>')
def view(uid):
    collection = Collection.query.get_or_404(uid)
    return render_template('collection/view.html', collection=collection)


@bp.route('/collection_bars/<int:piece_id>', methods=['POST'])
@UserPermission()
def collection_bars(piece_id):
    """Ajax: 返回collection_bars的HTML"""
    collection_bars_macro = get_template_attribute('macro/ui.html', 'render_collection_bars')
    return collection_bars_macro(g.user.collections, piece_id)


@bp.route('/collection/<int:uid>/edit', methods=['GET', 'POST'])
def edit(uid):
    collection = Collection.query.get_or_404(uid)
    permission = CollectionEditPermission(collection)
    if not permission.check():
        return permission.deny()

    form = CollectionForm(obj=collection)
    if form.validate_on_submit():
        form.populate_obj(collection)
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('collection.view', uid=uid))
    return render_template('collection/edit.html', form=form)


@bp.route('/collection/add_and_collect/<int:piece_id>', methods=['POST'])
@UserPermission()
def add_and_collect(piece_id):
    piece = Piece.query.get_or_404(piece_id)
    title = request.form.get('title')
    desc = request.form.get('desc')

    if not title:
        return json.dumps({'result': False})
    collection = g.user.collections.filter(Collection.title == title).first()
    if collection:
        return json.dumps({'result': False, 'error': 'repeat'})

    collection = Collection(title=title, desc=desc, user_id=g.user.id)
    db.session.add(collection)
    collect = CollectionPiece(collection_owner_id=g.user.id, piece_id=piece_id)
    collection.pieces.append(collect)
    db.session.commit()

    collection_bars_macro = get_template_attribute('macro/ui.html', 'render_collection_bars')
    collection_bars_html = collection_bars_macro(g.user.collections, piece_id)
    return json.dumps({'result': True, 'collection_bars_html': collection_bars_html})