"""
vs_query.py
Dependencies: python 3.x, flask

To start the application:
   > python vs_query.py
To terminate the application, use control-c
To use the application within a browser, use the url:
   http://127.0.0.1:5000/

Some test queries to exercise the dummy interface:
king of sweden
<next button>
prince
a of
"""
import shelve
from flask import Flask, render_template, request
from vs_search import dummy_search, dummy_movie_data, dummy_movie_snippet, get_shelve

# Create an instance of the flask application within the appropriate namespace (__name__).
# By default, the application will be listening for requests on port 5000 and assuming the base
# directory for the resource is the directory where this module resides.
app = Flask(__name__, static_folder='static', static_url_path='')


# Welcome page
# Python "decorators" are used by flask to associate url routes to functions.
# A route is the path from the base directory (as it would appear in the url)
# This decorator ties the top level url "localhost:5000" to the query function, which
# renders the query_page.html template.
@app.route("/")
def query():
    """For top level route ("/"), simply present a query page."""
    return render_template('query_page.html')


# This takes the form data produced by submitting a query page request and returns a page displaying
# results (SERP).
@app.route("/results", methods=['POST'])
def results():
    """Generate a result set for a query and present the 10 results starting with <page_num>."""

    page_num = int(request.form['page_num'])
    query = request.form['query']  # Get the raw user query

    movie_ids, num_hits, skipped_terms, unknown_terms = dummy_search(query, page_num, db)

    movie_results = [dummy_movie_snippet(e, db) for e in movie_ids]  # Get movie snippets: title, abstract, etc.

    # render the results page
    return render_template('results_page.html', orig_query=query, movie_results=movie_results, srpn=page_num,
                           len=len(movie_ids), skipped_words=skipped_terms, unknown_terms=unknown_terms,
                           total_hits=num_hits)


# Process requests for movie_data pages
# This decorator uses a parameter in the url to indicate the doc_id of the film to be displayed
@app.route('/movie_data/<film_id>')
def movie_data(film_id):
    """Given the doc_id for a film, present the title and text (optionally structured fields as well)
    for the movie."""
    data = dummy_movie_data(film_id, db)  # Get all of the info for a single movie
    return render_template('doc_data_page.html', data=data)


# If this module is called in the main namespace, invoke app.run().
# This starts the local web service that will be listening for requests on port 5000.
if __name__ == "__main__":
    db = shelve.open('./shelve/shelve.db', flag='r', writeback=True)
    app.run()
    db.close()
# While you are debugging, set app.debug to True, so that the server app will reload
# the code whenever you make a change.  Set parameter to false (default) when you are
# done debugging.
