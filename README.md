### DATAFLOW LAB
---

##### Docker commands

- create docker image `pub-sub-df-env`
- create and run a new container

```Bash

    docker build . -t pub-sub-df-env

    docker run -it \
        -v "$(pwd)/average_speeds.py:/opt/python/average_speeds.py" \
        -v "$(pwd)/src:/opt/python/src" \
         --rm pub-sub-df-env /bin/bash
```