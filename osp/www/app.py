

import os

from flask import Flask, request, render_template, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from osp.common import config
from osp.citations.models import Text_Index
from osp.www import utils
from osp.www.cache import cache
from osp.www.hit import Hit


app = Flask(__name__)
cache.init_app(app)


@app.route('/')
def home():

    """
    Home page + ranking interface.
    """

    return render_template(
        'home.html',
        facets=utils.bootstrap_facets(),
    )


@app.route('/api/ranks')
@use_args(dict(

    query           = fields.Str(missing=None),
    size            = fields.Int(missing=200),
    page            = fields.Int(missing=1),

    corpus          = fields.List(fields.Str(), missing=None),
    field_id        = fields.List(fields.Int(), missing=None),
    subfield_id     = fields.List(fields.Int(), missing=None),
    institution_id  = fields.List(fields.Int(), missing=None),
    state           = fields.List(fields.Str(), missing=None),
    country         = fields.List(fields.Str(), missing=None),

))
def api_ranks(args):

    """
    Ranking API.
    """

    filters = {f: args[f] for f in [
        'corpus',
        'field_id',
        'subfield_id',
        'institution_id',
        'state',
        'country',
    ]}

    results = utils.rank_texts(
        filters=filters,
        query=args['query'],
        size=args['size'],
        page=args['page'],
    )

    return jsonify(**results)


@app.route('/text/<text_id>')
def text(text_id):

    """
    Text profile pages.
    """

    # Load the text.
    text = config.es.get('text', text_id)

    # Assigned-with list.
    siblings = utils.assigned_with(text_id)

    return render_template(
        'text.html',
        text=Hit(text),
        siblings=siblings,
        Hit=Hit,
    )


@app.route('/graph')
def graph():

    """
    Graph viewer.
    """

    return render_template('graph.html')


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=os.getenv('PORT', 5000),
        debug=True,
    )
