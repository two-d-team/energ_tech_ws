# Build the image and run the container

```
docker pull mongo
docker build -t mongodb-test . 
docker run -dp 127.0.0.1:27017:27017 mongodb-test
```
