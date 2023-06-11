from flask import Flask, request
from string import Template
app = Flask(__name__)

@app.route('/')
def homepage():
    return """
    <h1>Elinoy's website</h1>

    <iframe src="https://www.youtube.com/embed/eNQIiRGn-A8?autoplay=1&start=90" width="1000" height="650" frameborder="0" allowfullscreen></iframe>
    """


@app.route('/videos/<vid>')
def videos(vid):
    print(f"videos({vid})")
    query = request.args.getlist('start')
    print(query)
    vidtemplate = Template("""
      <h2>
        YouTube video link: 
        <a href="https://www.youtube.com/watch?v=${youtube_id}">
          ${youtube_id}
        </a>
      </h2>
      <iframe src="https://www.youtube.com/embed/${youtube_id}" width="853" height="480" frameborder="0" allowfullscreen></iframe>
    """)


    return vidtemplate.substitute(youtube_id=vid)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
