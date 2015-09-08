import itertools
import random
import re
import flask
import flask.ext.pymongo

app = flask.Flask(__name__)
mongo = flask.ext.pymongo.PyMongo(app)

EXAMPLE_WORDS = ["correct", "horse", "battery", "stapler"]

def expand_url(url):
  """Expand a url which may or may not include a protocol.

  Adds "http://" to the beginning or urls which do not appear
  to have a protocol specified."""
  match = re.search("^\w+://", url)
  if match:
    return url
  else:
    return "http://{}".format(url)

@app.route("/")
def root():
  display_routes = [(r["slug"], r["url"])
                    for r in mongo.db.routes.find()]
  return flask.render_template("index.html",
                               routes=display_routes)

@app.route("/", methods=["POST"])
def modify():
  if flask.request.form["action"] == "create":
    slug = flask.request.form["slug"]
    url = expand_url(flask.request.form["url"])
    mongo.db.routes.insert({
      "slug": slug,
      "url": url,
    })
    return flask.redirect(slug)
  if flask.request.form["action"] == "delete":
    slug = flask.request.form["slug"]
    mongo.db.routes.remove({"slug": slug})
    return flask.redirect(slug)

  return flask.abort(400)

@app.route("/<path:path>")
def somewhere(path):
  route = mongo.db.routes.find_one({"slug": path})
  if route:
    return flask.redirect(route["url"])
  else:
    return flask.render_template("unmapped.html",
                                 slug=path,
                                 example=get_example_url())

@app.route("/<path:path1> <path:path2>")
def elsewhere(path1, path2):
  route = mongo.db.routes.find_one({"slug": path1})
  if route and "format" in route and route["format"] == "moira":
    url = "{}/list/{}".format(route["url"], path2)
    return flask.redirect(url)
  else:
    compound_url = "{} {}".format(path1, path2)
    return somewhere(path=compound_url)

def get_example_url():
  if random.random() < 0.1:
    return "https://xkcd.com/{}/".format(random.randint(1, 1566))
  else:
    return "http://example.com/{}".format(random.choice(EXAMPLE_WORDS))

if __name__ == "__main__":
  app.debug = True
  app.run()
