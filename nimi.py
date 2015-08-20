import itertools
import random
import flask
import flask.ext.pymongo

app = flask.Flask(__name__)
mongo = flask.ext.pymongo.PyMongo(app)

EXAMPLE_WORDS = ["correct", "horse", "battery", "stapler"]

@app.route("/")
def root():
  display_routes = [(r["slug"], r["url"])
                    for r in mongo.db.routes.find().limit(40)]
  return flask.render_template("index.html",
                               routes=display_routes)

@app.route("/", methods=["POST"])
def modify():
  if flask.request.form["action"] == "create":
    mongo.db.routes.insert({
      "slug": flask.request.form["slug"],
      "url": flask.request.form["url"],
    })
    return flask.redirect("/")
  if flask.request.form["action"] == "delete":
    slug = flask.request.form["slug"]
    mongo.db.routes.remove({"slug": slug})
    return flask.redirect("/")

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

def get_example_url():
  if random.random() < 0.1:
    return "https://xkcd.com/{}/".format(random.randint(1, 1566))
  else:
    return "http://example.com/{}".format(random.choice(EXAMPLE_WORDS))

if __name__ == "__main__":
  app.debug = True
  app.run()
