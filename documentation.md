# Documetation
<p align="left" >
   How  to  run  this HiveBox Version 
</p>


## Get Started 


## Run  the project 

### Run in Local

#### Start  the Project
</br>
<code> python app.py</code>

</br>

#### Run the unit test

<code> pyhton test.py</code>

### Run  in Docker 
to  run  the docker, use should  
#### build  the image 
 <code> docker build  .  -t HiveBox:0.0.1</code>

#### run the image  
  <code> docker run  -rm -p 5000:5000 --name hivebox HiveBox:0.0.1 </code>


## Project  Strcuture 
``` 
Devops-HANDS-ON-PROJECT-HIVEBOX
│
├── app.py
├── Dockerfile
├── test.py
├── requirements.txt
├── .dockerignore
├── documentation.md
└── README.md

```
## Api Request Structure

### Api Version  
<p>this  api  should  return  the version  of the current  application</p>

``` Bash
 curl -X POST "http://api.example.com/version" 
``` 

### Temperature Average
<p> this  api  should  return  the avergae of temperature  for  each  box </p>


``` Bash
 curl -X POST "http://api.example.com/temperature" 
``` 