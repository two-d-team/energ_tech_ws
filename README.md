# Build the image and run the container

```
docker pull mongo
docker run -d --name test_mongodb -p 27017:27017 
           -e MONGO_INITDB_ROOT_USERNAME=root 
           -e MONGO_INITDB_ROOT_PASSWORD=pass 
           mongo
```
