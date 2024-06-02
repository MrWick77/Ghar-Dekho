from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and preprocessor
model = joblib.load('housepred.joblib')
preprocessor = joblib.load('preprocessor.joblib')

# Load city-state mapping and multiplier dictionary
df = pd.read_csv('dataset\\HouseIndia.csv')
df['City'] = df['City'].str.lower()
df['State'] = df['State'].str.lower()
city_state_mapping = df.groupby('City')['State'].agg(pd.Series.mode).to_dict()

city_state_multiplier = {
    'maharashtra': {'mumbai': 1.2, 'pune': 1.1},
    'delhi': {'delhi': 1.15},
    'uttar pradesh': {'noida': 1.05, 'lucknow': 1.08, 'ghaziabad': 1.12},
    'karnataka': {'bangalore': 1.18, 'mangalore': 1.05, 'mysore': 1.07},
    'tamil nadu': {'chennai': 1.22, 'coimbatore': 1.1, 'madurai': 1.08},
    'west bengal': {'kolkata': 1.1, 'siliguri': 1.05, 'durgapur': 1.08},
    'rajasthan': {'jaipur': 1.15, 'udaipur': 1.1, 'jodhpur': 1.08},
    'bihar': {'patna': 1.1, 'gaya': 1.05},
    'jharkhand': {'ranchi': 1.1, 'jamshedpur': 1.05},
    'odisha': {'bhubaneswar': 1.12, 'cuttack': 1.08, 'rourkela': 1.1},
    'kerala': {'kochi': 1.1, 'thiruvananthapuram': 1.05, 'kozhikode': 1.08},
    'assam': {'guwahati': 1.1, 'dibrugarh': 1.05, 'dispur': 1.08},
    'uttarakhand': {'dehradun': 1.05, 'haridwar': 1.08, 'nainital': 1.1},
    'sikkim': {'gangtok': 1.12},
    'mizoram': {'aizawl': 1.15},
    'manipur': {'imphal': 1.1},
    'nagaland': {'kohima': 1.08, 'dimapur': 1.12},
    'meghalaya': {'shillong': 1.1, 'tura': 1.08},
    'arunachal pradesh': {'itanagar': 1.12, 'naharlagun': 1.15},
    'tripura': {'agartala': 1.08, 'udaipur': 1.1, 'dharmanagar': 1.12},
    'telangana': {'hyderabad': 1.15},
    'gujarat': {'ahmedabad': 1.1},
    'punjab': {'chandigarh': 1.1},
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
    area = request.form['area']
    bhk = request.form['bhk']
    age = request.form['age']
    city = request.form['city']
    state = request.form['state']

    # City-state validation (optional)
    city_lower = city.lower()
    state_lower = state.lower()
    if city_lower not in city_state_mapping or city_state_mapping[city_lower] != state_lower:
        error_message = f"Invalid city-state combination. '{city}' does not belong to the state '{state}'."
        return render_template('index.html', error_message=error_message)

    # Input validation (optional)
    try:
        area = int(area)
        bhk = int(bhk)
        age = int(age)
    except ValueError:
        error_message = "Invalid input. Please enter numerical values for area, BHK, and age."
        return render_template('index.html', error_message=error_message)

    # Prepare data and predict price
    input_data = pd.DataFrame([[area, bhk, age, city, state]], columns=['Area', 'BHK', 'Age', 'City', 'State'])
    processed_data = preprocessor.transform(input_data)
    predicted_price = model.predict(processed_data)

    # Apply city-state multiplier (if applicable)
    state_lower = state.lower()
    city_lower = city.lower()
    if state_lower in city_state_multiplier and city_lower in city_state_multiplier[state_lower]:
        predicted_price *= city_state_multiplier[state_lower][city_lower]

    return render_template('index.html', prediction_text=f'Predicted House Price: ₹{predicted_price[0]:,.2f}')

if __name__ == '__main__':
    app.run(debug=True)

