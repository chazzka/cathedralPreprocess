# how to run with python pip:

source venv/bin/activate

pip install

## evaluating with default config.toml
python3 src/main.py 

## evaluating with user defined config
python3 src/main.py myconfig.toml

## tests

python -m unittest test.runtests


# training

training is for creating a new model

traning fits a mathematical model based on the positions of data in the space (time and desired value), this way there is no need for labeled data

use training only if previous trained model is lost or damaged

use training only on the valid dataset

python3 src/train.py login password SUBDAYS getRecrodLstURL updateRecordLstURL idColumn observableColumn timeColumn apiDataIndentifier deviceIdLst

python3 src/main.py a_ulrich@utb.cz EcCNVU/dS76jpE938WxRHRGmjRM= 1000 https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/GetRecordLst https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/RecordLst @ID @iDevdAverageCurrent @dDevdCasZpravy iot_device_data 3


# how to run with docker

## default config toml file

`docker build --network=host --tag cathedral .`

## user defined config toml file

`docker run --network=host cathedral . `





# exit code 1
 - no cluster found