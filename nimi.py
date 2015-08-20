import flask
import itertools
import random
app = flask.Flask(__name__)

EXAMPLE_WORDS = ["correct", "horse", "battery", "stapler"]

routes = {
  "findclass": "http://student.mit.edu/catalog/extsearch.cgi",
  "mitpay": "https://student.mit.edu/cgi-bin/mitpay.pl",
  "ist": "https://ist.mit.edu/software-hardware",
  "so": "https://stackoverflow.com/",
  "planner": "http://planner.mit.edu/",
}

@app.route("/")
def root():
  display_routes = itertools.islice(routes.iteritems(), 40)
  return flask.render_template("index.html",
                               routes=display_routes)

@app.route("/", methods=["POST"])
def modify():
  if flask.request.form["action"] == "create":
    slug = flask.request.form["slug"]
    url = flask.request.form["url"]
    routes[slug] = url
    return flask.redirect("/")
  if flask.request.form["action"] == "delete":
    slug = flask.request.form["slug"]
    del routes[slug]
    return flask.redirect("/")

  return flask.abort(400)

@app.route("/<path:path>")
def somewhere(path):
  if path in routes:
    url = routes[path]
    return flask.redirect(url)
  else:
    return flask.render_template("unmapped.html",
                                 slug=path,
                                 example=get_example_url())

def get_example_url():
  if random.random() < 0.1:
    return "https://xkcd.com/{}/".format(random.randint(1, 1566))
  else:
    return "http://example.com/{}".format(random.choice(EXAMPLE_WORDS))

if __name__ == "__main__":
  app.debug = True
  app.run()
