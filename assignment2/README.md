### flask

```bash
$ cd flask
$ source flask/bin/activate
$ export FLASK_APP=app_flask.py
$ flask run
```

After accessing the [website](http://127.0.0.1:5000/get). After sending a request one should see something like this for the named entity part:

![Shadowed Named Entities](./assets/Snipaste_2024-02-15_22-49-13.png)

The results of the dependency parse are also presented and for each sentence one should see something like:

![dependency parse](./assets/Snipaste_2024-02-15_22-51-41.png)

For this assignment, a database backend is integrated into the existing code. The extracted entities are stored and also the relationships they are associated with. Here's a screenshot of the website, displaying the entities and relationships that are fetched from the database.

![entities and relationships stored in the database](./assets/Snipaste_2024-04-02_19-55-30.png)









