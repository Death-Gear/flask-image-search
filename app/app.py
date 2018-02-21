import os

from flask import Flask, render_template, request, jsonify

from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher

# create flask instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')


# main route
@app.route('/')
def index():
    return render_template('index.html')


# search route
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":

        RESULTS_ARRAY = []

        # get url
        image_url = request.form.get('img')

        try:

            # initialize the image descriptor
            cd = ColorDescriptor((8, 12, 3))
            # load the query image and describe it
            from skimage import io
            import cv2

            query = io.imread(image_url)
            # query = (query * 255).astype("uint8")
            # (r, g, b) = cv2.split(query)
            # query = cv2.merge([b, g, r])
            # cv2.imshow("Image", query)
            query = cv2.cvtColor(query, cv2.COLOR_BGR2RGB)
            features = cd.describe(query)
            # perform the search
            searcher = Searcher(INDEX)
            results = searcher.search(features)

            # loop over the results, displaying the score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)})


            # return success
            return jsonify(results=(RESULTS_ARRAY[::-1]))
            # return 'ok'

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# run!
if __name__ == '__main__':
    app.run(debug=True)
