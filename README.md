required python>=3.9
# How to run with python pip

source venv/bin/activate

pip install

## evaluating with default config.toml
python3 src/main.py 

## evaluating with user defined config
python3 src/main.py myconfig.toml

## tests

python -m unittest test.runtests


# How to run with docker


`docker build --network=host --tag cathedral .`

`docker run --network=host cathedral . `

## user defined config toml file
default config toml file is ./config.toml (specified in Dockerfile)

to change the config.toml path, change in Dockerfile `CMD` argument

`CMD ["python3", "src/main.py", `"./config.toml"`]`

# Output exit codes
## 0
script evaluated successfully, sent POST to the desired endpoint
## 1
A) no cluster found

B) some unexpected error occurred - see ./logs


# Training

training is for creating a new model

traning fits a mathematical model based on the positions of data in the space (time and desired value), this way there is no need for labeled data

use training only if previous trained model is lost or damaged or no longer valid

use training only on the valid dataset

do not forget to set a name for the new model (see config below)

`python3 src/train.py config.toml`

## how to train with docker

change Dockerfile CMD to `CMD ["python3", `"src/train.py"`, "./config.toml"]`

# Logs
automatic logging is implemented, default level is `INFO`

log file can be found in `./logs/debug.log`

`sudo docker run -it --entrypoint /bin/bash cathedral`

log format is: `time - level - message`

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
```

