# Course Network
The main purpose of this project is to visualize and then analyze the course curriculum network of SFU. However, due to limited resource, only the stem field courses will be analyzed.


### Installation
`pip install -r requirements.txt`

## Project Structure

`/course_network_flask`
    - `visualization.py`: draw the graph using pyvis, and save the graph as html.
    - `app.py`: flask app.
    - `Procfile`: used to depoly on Heroku. Remember to pip install `gunicorn`, this is already included in the `requirements.txt`.
    - `/templates`: used to store `index.html` and the generated graph `graph.html`.