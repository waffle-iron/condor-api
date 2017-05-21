# bultin library

# external libraries
from sanic import Sanic
from sanic.response import text, json
from condor.dbutil import requires_db
from condor.models import Bibliography, RankingMatrix, \
    TermDocumentMatrix, Document


app = Sanic(__name__)


@app.route("/ranking", methods=["GET"])
@requires_db
async def list_rankings(db, request):
    ranking_matrices = [
        {
            "eid": matrix.eid,
            "kind": matrix.kind,
            "build_options": matrix.build_options,
            "ranking_matrix_path": matrix.ranking_matrix_path
        }
        for matrix in RankingMatrix.list(db)
    ]
    return json(ranking_matrices)


@app.route("/bibliography")
@requires_db
async def list_bibliographies(db, request):
    bibliographies = [
        {
            "eid": bib.eid,
            "description": bib.description,
            "created": bib.created,
            "modified": bib.modified
        }
        for bib in Bibliography.list(db)
    ]
    return json(bibliographies)


@app.route("/bibliography/<eid>")
@requires_db
async def bibliography(db, request, eid):
    """
    Bibliography associated with a blibliography eid
    """
    bibliography = Bibliography.find_by_eid(db, eid)

    if not bibliography:
        return json({})

    return json(
        {
            "eid": bibliography.eid,
            "description": bibliography.description,
            "created": bibliography.created,
            "modified": bibliography.modified
        }
    )


@app.route('/document')
@requires_db
async def list_documents(database, request):
    """
    List the documents associated with a bibliography.
    """
    bibliography_eid = request.args.get('bibliography', None)
    if not bibliography_eid:
        return json(
            {
                'error': 'You must suply a bibliography eid.',
                'details': 'Fill in the bibliography field.'
            },
            status=400
        )

    documents = [
        {
            'eid': doc.eid,
            'title': doc.title,
            'description': doc.description,
            'created': doc.created,
            'modified': doc.modified
        }
        for doc in Document.list(database, bibliography_eid)
    ]
    return json(documents)


@app.route("/matrix")
@requires_db
async def list_term_document_matrices(db, request):
    document_matrices = [
        {
            "eid": document.eid,
            "bibliography_eid": document.bibliography_eid,
            "bibliography_options": document.bibliography_options,
            "processing_options": document.processing_options,
            "term_list_path": document.term_list_path,
            "matrix_path": document.matrix_path
        }
        for document in TermDocumentMatrix.list(db)
    ]
    return json(document_matrices)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000,
        log_config=None,
    )
