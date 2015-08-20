import flask
import itertools
app = flask.Flask(__name__)

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
  for slug, href in display_routes:
    lines.append("<tr><td>{}</td><td>{}</td></tr>".format(
      slug, href))
  lines.append("</table>")
  return "\n".join(lines)

@app.route("/<path:path>")
def somewhere(path):
  if path in routes:
    href = routes[path]
    return flask.redirect(href)
  else:
    return "No such route."

if __name__ == "__main__":
  app.debug = True
  app.run()
