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
  lines = []
  lines.append("<h1>Nimi Redirector</h1>")
  lines.append("<p>Short link forwarding service.</p>")
  lines.append("<h2>Links</h2>")
  lines.append("<table>")
  display_routes = itertools.islice(routes.iteritems(), 40)
  for slug, url in display_routes:
    lines.append("<tr><td>{}</td><td>{}</td></tr>".format(
      slug, url))
  lines.append("</table>")
  return "\n".join(lines)

@app.route("/<path:path>")
def somewhere(path):
  if path in routes:
    url = routes[path]
    return flask.redirect(url)
  else:
    return flask.render_template("unmapped.html",
                                 slug=path,
                                 example=get_example_url())

@app.route("/<path:path>", methods=["POST"])
def create(path):
  url = flask.request.form["url"]
  routes[path] = url
  return flask.redirect("/")

def get_example_url():
  if random.random() < 0.1:
    return "https://xkcd.com/{}/".format(random.randint(1, 1566))
  else:
    return "http://example.com/{}".format(random.choice(EXAMPLE_WORDS))

if __name__ == "__main__":
  app.debug = True
  app.run()
