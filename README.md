This project takes the trained model (which should know how regular data look like - see `traning`), based on it, it finds the anomalies and tries to find a cluster amongst them. Report is sent to desired endpoint.

- finding anomalies is `supervised` - traning needs to be run first to tell the model how do anomalies look
- finding clusters is `unsupervised` - based on anomalies (trained model), script can automatically find clusters

# How to run with python pip
required python>=3.9

```sh
source venv/bin/activate
```

```sh
pip install
```

## evaluating with default config.toml
```sh
python3 src/main.py 
```

## evaluating with user defined config
```sh
python3 src/main.py myconfig.toml
```

## tests

```sh
python -m unittest test.runtests
```

# How to run with docker


```
docker build --network=host --tag cathedral .
```

```
docker run --network=host cathedral
```

## user defined config toml file
default config toml file is `./config.toml` (specified in Dockerfile)

to change the config.toml path, change in Dockerfile `CMD` argument

```Dockerfile
CMD ["python3", "-u", "bin/main.py", "./config.toml"]
```

# Output exit codes
## `0`
script evaluated successfully, sent POST to the desired endpoint
## `1`
1. no cluster found
2.  some unexpected error occurred - see `./logs`


# Logs
automatic logging is implemented
- logs are separated into two files
1) logs/debug.log  - contains only error messages
2) logs/info.log - contains all messages (info AND debug)

## how to read output from docker container

```sh
docker build --network=host --tag cathedral .
```

name your image
```sh
docker run --network=host --name=cathedralimage cathedral
```

look at the log file
```sh
docker cp cathedralimage:/app/logs/debug.log /path/in/host/to/store/log
```

log format is:\
 `time - level - message`

# config.toml
input of the script is defined in `config.toml` file

this file can be changed anytime by specifing different toml file in `Dockerfile`

## format:
./config.toml

```toml
auth = ["api_username", "api_password"]

[server]
url = "https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/GetRecordLst"
posturl = "https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/RecordLst"

[args]
daystostrip = 1000 # number of days to subtract from NOW()
idColumnName = "@ID" # name of ID Column
averageColumnName = "@iDevdAverageCurrent" # name of observed column
timeColumnName = "@dDevdCasZpravy" # name of time column
apiDataIndentifier = "iot_device_data" # data identifier form API
deviceIdLst = 3 # device ID
modelPath = "models/model.pckl" # where to find trained model
# only for train.py
newModelName = "newmodel" # how to name new trained model (saved to models/)

[AI]
contamination = 0.02 # (0, 0.5> The amount of contamination for traning of the data set, i.e. the proportion of outliers in the data set. (see training)
eps = 7 # float, The maximum distance between two samples for one to be considered as in the neighborhood of the other
min_samples = 10 # int, The number of samples in a neighborhood for a point to be considered as a cluster point. This includes the point itself.
```

# Training

- for creating a new model to filter out anomalies

Traning fits a mathematical model based on the positions of data in the space (time and desired value).

Use training only if previous trained model is lost or damaged or no longer valid.

We use traning on the dataset with valid data, to teach the model how do valid data look.

Dataset should not contain anomalies, if it does in some small amount, define the percentage using `contamination` parameter in the config file.

Default `contamination` is set to 0.02 (=2%) to allow some disturbances.

- do not forget to set a name for the new model (see config above)
```sh
python3 bin/train.py config.toml
```

## how to train with docker

change Dockerfile CMD to 

```Dockerfile
CMD ["PYTHONPATH=$PYTHONPATH:./src python3", "bin/train.py", "./config.toml"]
```

## Logging config file
Logging config file is a toml file (`loggingconfig.toml`) containing a configuration for logging. The configuration documentation is avaliable here: https://docs.python.org/3/library/logging.config.html