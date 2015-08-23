# Nimi Redirector

A simple short link redirection service.

With this service you can type something like oh/cool
into you browser and get to http://gladIDidntHaveToTypeThis.example.com/


# Develop

Clone the repository.

    $ git clone ...

Install the dependencies.

    $ pip install -r requirements.txt

Run the development server

    $ python nimi.py

In a browser go to [http://localhost:5000/](http://localhost:5000/).


# Deploy

To deploy nimi, add an nginx server like this.

```
server {
	server_name n;
	listen 80;

	root /some/path/nimi-redirector/static;

	location / { try_files $uri @app; }
	location @app {
		include uwsgi_params;
		uwsgi_pass unix:/tmp/uwsgi-nimi.sock;
	}
}
```

Install `uwsgi` if it isn't already.

    $ sudo apt-get install uwsgi

Run `uwsgi-run.sh` which will serve nimi:

- Using wsgi.
- Through a socket in `/tmp`.
- As the `www-data` user.
