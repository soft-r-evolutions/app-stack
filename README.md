# stack-mongo-go-vue
Stack to develop and run an application using Mongodb - Golang and VueJs

![Stack Overview](doc/app_env-02-stack_overview.png)

To run the environment:

```
docker-compose up
```

## Model - MongoDb

It is composed of 2 Docker images:
- MongoDb
- MongoDb-express

MongoDb contains the database used for the application.
MongoDb-express is used for dev and debug purposes to easily see the database.
