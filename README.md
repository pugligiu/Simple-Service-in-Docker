# Simple Service in Docker
Example of a simple service in Docker. It is using Redis and Flask. There are some ad hoc unit tests.


## Tree Directory
```
.
├── .gitignore
├── README.md
├── docker-compose.yml
├── Dockerfile
├── .healthcheck.sh
└── src
    ├── code
    │   ├── __init__.py
    │   ├── service.py
    │   └── service_test.py
    └── requirements.txt
```


## Requirements

#### Functional Requirements
Small Service deployed to a docker container that has two endpoints:

  1. */messages*
     - takes a message (a string) as a **POST** and returns the SHA256 hash digest of that message (in hexadecimal format)
  
  2. */messages/\<hash\>*
      - is a **GET** request that returns the original message. A request to a non-existent \<hash\> should return a **404** error.


#### Non-functional Requirements

  1. [Interoperability](https://en.wikipedia.org/wiki/Interoperability)
     - Data format - Bad Request
     - Not availability - Server Error
  2. [Testability](https://en.wikipedia.org/wiki/Software_testability)
     - Test Driven Development - Clear view of testing scenarios before and after the development
     - Integrate the tests with Docker
     - Creating testing structure keeping it similar to the real interaction
      
      
## User Manual

  1. **POST** request
     - `curl -X POST -H "Content-Type: application/json; charset= utf-8" -d '{"message": "foo"}' http://0.0.0.0:8080/messages`
     - 
       ```
        {
         "digest": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
        }
       ```

  2. **GET** request
     - `curl -i http://0.0.0.0:8080/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae`
     - 
        ```
         {
          "message": "foo"
         }
        ```
        
## How to use

#### What do you need
It is necessary to have installed Docker and Docker Compose. Follow the two links

  1. https://docs.docker.com/install/#server to install Docker
    
  2. https://docs.docker.com/compose/install/ to install Docker Compose
    
#### Steps to run
Move inside the main directory then run the following commands
 
  1. `docker-compose up --build` 
     - This creates/pull the images, start the container, run the unit tests, build and run
  2. `docker-compose down --rmi all`
     - The opposite of before
  3. `docker-compose exec web sh`
     - This opens the command line where the microservice is running. It is possible to change the code there.
  4. `docker-compose exec redis sh`
     - This opens the command line where Redis is running
  5. From outside of any container, it is possible to test the POST and GET request.
       
#### Notes
  - The container is exposing the service on 8080 however the application is exposing the service on port 5000
  - It is mounted a volume
  - Docker run the unit tests before to build the images
