import dill as pickle
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from flask import Flask,request, jsonify
import waitress

app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def apicall():
    """API Call

    Pandas dataframe (sent as a payload) from API Call
    """
    try:
        test_json = request.get_json()
        test = pd.read_json(test_json, orient='records')

        #To resolve the issue of TypeError: Cannot compare types 'ndarray(dtype=int64)' and 'str'
        test['Dependents'] = [str(x) for x in list(test['Dependents'])]

        #Getting the Loan_IDs separated out
        loan_ids = test['Loan_ID']

    except Exception as e:
        raise e

    clf = 'model_v1.pk'

    if test.empty:
        return 'sORRY'
    else:
        #Load the saved model
        print("Loading the model...")
        #loaded_model = None
        with open('./models/'+clf, 'rb') as f:
            loaded_model = pickle.load(f)

        print("The model has been loaded...doing predictions now...")
        predictions = loaded_model.predict(test)
        prediction_series = list(pd.Series(predictions))

        final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))
        responses = jsonify(predictions=final_predictions.to_json(orient="records"))
        responses.status_code = 200

        return responses
if __name__ == "__main__":
    waitress.serve(app, host='0.0.0.0', port=5000)


