### DATAFLOW LAB<br>

---

###### Exportando 
```bash
export DEVSHELL_PROJECT_ID='__seu_project_id__'
#  nome identificador que compoe a ultima parte do topico 
export TOPIC_NAME='__nome_do_topico__'
export REGION='__regiao_do_projecto__'
```

##### Docker commands

- create docker image `pub-sub-df-env`
- create and run a new container

```Bash

    docker build . -t pub-sub-df-env

    docker run -it \
        --env REGION=$REGION \
        --env TOPIC_NAME=$TOPIC_NAME \
        --env DEVSHELL_PROJECT_ID=$DEVSHELL_PROJECT_ID \
        --env BUCKET=$DEVSHELL_PROJECT_ID \
        --env PROJECT=$DEVSHELL_PROJECT_ID \
        -v "$(pwd)/certificacao-GCP/average_speeds.py:/opt/python/average_speeds.py" \
        -v "$(pwd)/certificacao-GCP/src:/opt/python/src" \
         --rm pub-sub-df-env /bin/bash
```

##### GCP Autentication

- autentication login inside container
- set my account project inside container

```Bash

    gcloud auth login
    
    gcloud auth application-default login

    gcloud config set project $DEVSHELL_PROJECT_ID
```

##### VAR ENV

- set my topic id
- Create a topic and sub-scription by Note.md file (
    I only move on to the first use of the container, when the service has not yet been created in the cloud)
- Create bucket and dataset like example on Note.md

```Bash

    export TOPIC_ID=projects/$DEVSHELL_PROJECT_ID/topics/$TOPIC_NAME
```

[Click here to go to the topic creation file](./NOTE.md)

### Start producer

- Go inside publish folder
- Download dataset

```Bash

     cd publish/
    
    ./download_data.sh
```

- Start producer and open a new bash terminal

```Bash

    ./send_sensor_data.py --speedFactor=60 --project $DEVSHELL_PROJECT_ID
```

- Inside the new terminal, exec the container again

```Bash

    ./average_speeds.py $DEVSHELL_PROJECT_ID $BUCKET CurrentConditions --bigtable
```