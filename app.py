from flask import Flask, render_template, request
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

# Load models
tfidf = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

ps = PorterStemmer()

app = Flask(__name__)

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    input_sms = request.form['message']

    # 1: preprocess
    transformed_sms = transform_text(input_sms)

    # 2: vectorize
    vector_input = tfidf.transform([transformed_sms]).toarray()

    # 3: predict
    result = model.predict(vector_input)[0]

    # 4: Display
    if result == 1:
        prediction = "Spam 🚨"
    else:
        prediction = "Not Spam ✔️"

    return render_template('index.html',
                           prediction=prediction,
                           message=input_sms)


if __name__ == "__main__":
    app.run(debug=True)
