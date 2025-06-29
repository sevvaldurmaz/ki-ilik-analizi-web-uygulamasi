from flask import Flask, render_template, request
from keras.models import load_model
import numpy as np

app = Flask(__name__)

# Modeli yüklüyoruz (model2.h5 dosyası app.py ile aynı klasörde olmalı)
model = load_model("modelim.h5")

# Ana sayfa (formlu HTML sayfası)
@app.route("/")
def home():
    return render_template("index.html")

# Tahmin işlemi POST ile yapılacak
@app.route("/tahmin", methods=["POST"])
def tahmin():
    try:
        # Form verilerini al
        data = [
            float(request.form["Time_spent_Alone"]),
            int(request.form["Stage_fear"]),
            float(request.form["Social_event_attendance"]),
            float(request.form["Going_outside"]),
            int(request.form["Drained_after_socializing"]),
            float(request.form["Friends_circle_size"]),
            float(request.form["Post_frequency"])
        ]
        input_array = np.array([data])
        prediction = model.predict(input_array)[0][0]
        # Bu satırları ekle:
        print("Girilen veriler:", data)
        print("Input array:", input_array)
        print("Tahmin edilen olasılık (prediction):", prediction)

        result = "Dışa Dönük" if prediction > 0.5 else "İçe Dönük"
        probability = f"%{round(prediction * 100, 1)}"
        return render_template("index.html", result=result, probability=probability)


    except Exception as e:
        return f"Hata oluştu: {e}"


if __name__ == "__main__":
    app.run(debug=True)

