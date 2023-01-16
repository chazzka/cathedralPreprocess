# how to run with python pip:

source venv/bin/activate

pip install


# evaluating
python3 src/main.py login password SUBDAYS getRecrodLstURL updateRecordLstURL idColumn observableColumn timeColumn apiDataIndentifier deviceIdLst trainedModelPath

python3 src/main.py a_ulrich@utb.cz EcCNVU/dS76jpE938WxRHRGmjRM= 1000 https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/GetRecordLst https://intern.smart.ariscat.com/datasnap/rest/TARSMethods/RecordLst @ID @iDevdAverageCurrent @dDevdCasZpravy iot_device_data 3 models/model.pckl

python -m unittest test.runtests


# training


# how to run with docker

# exit code 1
 - no cluster found