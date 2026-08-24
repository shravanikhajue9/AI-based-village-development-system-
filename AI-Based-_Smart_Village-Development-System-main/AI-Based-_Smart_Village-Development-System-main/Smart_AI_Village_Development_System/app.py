from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import joblib
import pandas as pd
from reportlab.pdfgen import canvas
from flask import send_file
import matplotlib.pyplot as plt
import os
from flask import session


app = Flask(__name__)
app.secret_key = "smart_village_secret_key"

DATABASE = "database.db"
# ======================
# LOAD ML MODEL
# ======================

model = joblib.load("model.pkl")
translations = {

"en":{

"dashboard":"Dashboard",
"village":"Village Analysis",
"crop":"Crop Recommendation",
"employment":"Employment",
"infrastructure":"Infrastructure",
"report":"Report",
"logout":"Logout",
"population":"Population",
"literacy":"Literacy Rate",
"rainfall":"Rainfall",
"schools":"Schools",
"hospitals":"Hospitals",
"employment_rate":"Employment Rate",
"submit":"Submit",
"predict":"Predict",
"result":"Prediction Result",
"suggestions":"AI Suggestions",
"future_score":"Future Development Score",
"development_plan":"Development Plan",
"problems":"Problems",
"village_name":"Village Name",
"select_village":"Select Village",
"crop_title":"AI Crop Recommendation",
"water":"Water Availability",
"soil":"Soil Type",
"low":"Low",
"medium":"Medium",
"high":"High",
"black_soil":"Black Soil",
"red_soil":"Red Soil",
"alluvial_soil":"Alluvial Soil",
"recommend":"Recommend Crops",
"recommended_crops":"Recommended Crops",
"ai_crop":"AI Crop Suggestions",
"back_dashboard":"Back to Dashboard",
"tenth_pass":"10th Passed Population",
"twelfth_pass":"12th Passed Population",
"schemes":"Government Schemes",
"live_statistics":"Live Statistics",
"start_analysis":"Start Village Analysis",
"scheme_title": "Government Scheme Recommendation",
"recommended_scheme": "Recommended Scheme",
"eligible": "You are eligible for these schemes",
"literacy_rate": "Literacy Rate (%)",
"employment_rate": "Employment Rate (%)",
"road_connectivity": "Road Connectivity (%)",
"healthcare_centers": "Healthcare Centers",
"water_availability": "Water Availability",
"internet": "Internet",
"yes": "Yes",
"no": "No",
"available": "Available",
"not_available": "Not Available",
"generate_recommendations": "Generate Recommendations",
"recommended_schemes": "Recommended Schemes",
"main_source": "Local Market",
"select_village": "Select Village",
"local_market": "Local Market",
"agriculture": "Agriculture",
"forest": "Forest",
"water": "Water",
"tourism": "Tourism",
"animal_husbandry": "Animal Husbandry",
"small_business": "Small Business",
"shop_trading": "Shop / Trading",
"handicraft": "Handicraft",
"daily_wage": "Daily Wage Labour",
"government_job": "Government Job",
"private_job": "Private Job",
"other": "Other",
},


"mr":{

"dashboard":"डॅशबोर्ड",
"village":"गाव विश्लेषण",
"crop":"पीक शिफारस",
"employment":"रोजगार",
"infrastructure":"पायाभूत सुविधा",
"report":"अहवाल",
"logout":"बाहेर पडा",
"population":"लोकसंख्या",
"literacy":"साक्षरता दर",
"rainfall":"पाऊस",
"schools":"शाळा",
"hospitals":"रुग्णालये",
"employment_rate":"रोजगार दर",
"submit":"सबमिट करा",
"predict":"भविष्यवाणी करा",
"result":"अंदाज परिणाम",
"suggestions":"एआय सूचना",
"future_score":"भविष्यातील विकास गुण",
"development_plan":"विकास योजना",
"problems":"समस्या",
"village_name":"गावाचे नाव",
"select_village":"गाव निवडा",
"crop_title":"एआय पीक शिफारस",
"water":"पाण्याची उपलब्धता",
"soil":"मातीचा प्रकार",
"low":"कमी",
"medium":"मध्यम",
"high":"जास्त",
"black_soil":"काळी माती",
"red_soil":"लाल माती",
"alluvial_soil":"गाळाची माती",
"recommend":"पीक सुचवा",
"recommended_crops":"शिफारस केलेली पिके",
"ai_crop":"एआय पीक सूचना",
"back_dashboard":"डॅशबोर्डवर परत जा",
"tenth_pass":"१० वी उत्तीर्ण लोकसंख्या",
"twelfth_pass":"१२ वी उत्तीर्ण लोकसंख्या",
"schemes":"शासकीय योजना",
"live_statistics":"थेट आकडेवारी",
"start_analysis":"गाव विश्लेषण सुरू करा",
"scheme_title": "शासकीय योजना शिफारस",
"recommended_scheme": "शिफारस केलेल्या योजना",
"eligible": "तुम्ही खालील योजनांसाठी पात्र आहात",
"literacy_rate": "साक्षरता दर (%)",
"employment_rate": "रोजगार दर (%)",
"road_connectivity": "रस्ता संपर्क (%)",
"healthcare_centers": "आरोग्य केंद्रे",
"water_availability": "पाणी उपलब्धता",
"internet": "इंटरनेट",
"yes": "होय",
"no": "नाही",
"available": "उपलब्ध",
"not_available": "उपलब्ध नाही",
"generate_recommendations": "शिफारसी तयार करा",
"recommended_schemes": "शिफारस केलेल्या योजना",
"main_source": "स्थानिक बाजार",
"local_market": "स्थानिक बाजार",
"agriculture": "कृषी बाजार",
"forest": "वन उत्पादन बाजार",
"water": "जलसंपदा",
"tourism": "पर्यटन",
"animal_husbandry": "पशुपालन",
"small_business": "लघु उद्योग",
"shop_trading": "दुकान / व्यापार",
"handicraft": "हस्तकला",
"daily_wage": "दैनिक मजुरी",
"government_job": "शासकीय नोकरी",
"private_job": "खाजगी नोकरी",
"other": "इतर",
"select_village": "गाव निवडा",
"local_market": "स्थानिक बाजार",
},


"hi":{

"dashboard":"डैशबोर्ड",
"village":"गांव विश्लेषण",
"crop":"फसल सिफारिश",
"employment":"रोजगार",
"infrastructure":"बुनियादी सुविधा",
"report":"रिपोर्ट",
"logout":"लॉगआउट",
"population":"जनसंख्या",
"literacy":"साक्षरता दर",
"rainfall":"वर्षा",
"schools":"स्कूल",
"hospitals":"अस्पताल",
"employment_rate":"रोजगार दर",
"submit":"जमा करें",
"predict":"भविष्यवाणी करें",
"result":"पूर्वानुमान परिणाम",
"suggestions":"एआई सुझाव",
"future_score":"भविष्य विकास स्कोर",
"development_plan":"विकास योजना",
"problems":"समस्याएँ",
"village_name":"गांव का नाम",
"select_village":"गांव चुनें",
"crop_title":"एआई फसल सिफारिश",
"water":"जल उपलब्धता",
"soil":"मिट्टी का प्रकार",
"low":"कम",
"medium":"मध्यम",
"high":"अधिक",
"black_soil":"काली मिट्टी",
"red_soil":"लाल मिट्टी",
"alluvial_soil":"जलोढ़ मिट्टी",
"recommend":"फसल सुझाएँ",
"recommended_crops":"अनुशंसित फसलें",
"ai_crop":"एआई फसल सुझाव",
"back_dashboard":"डैशबोर्ड पर वापस जाएँ",
"tenth_pass":"10वीं पास जनसंख्या",
"twelfth_pass":"12वीं पास जनसंख्या",
"schemes":"सरकारी योजनाएँ",
"live_statistics":"लाइव सांख्यिकी",
"start_analysis":"गांव विश्लेषण शुरू करें",
"scheme_title": "सरकारी योजना अनुशंसा",
"recommended_scheme": "अनुशंसित योजना",
"eligible": "आप इन योजनाओं के लिए पात्र हैं",
"literacy_rate": "साक्षरता दर (%)",
"employment_rate": "रोजगार दर (%)",
"road_connectivity": "सड़क संपर्क (%)",
"healthcare_centers": "स्वास्थ्य केंद्र",
"water_availability": "जल उपलब्धता",
"internet": "इंटरनेट",
"yes": "हाँ",
"no": "नहीं",
"available": "उपलब्ध",
"not_available": "उपलब्ध नहीं",
"generate_recommendations": "अनुशंसाएँ प्राप्त करें",
"recommended_schemes": "अनुशंसित योजनाएँ",
"main_source": "स्थानीय बाजार",
"local_market": "स्थानीय बाजार",
"agriculture": "कृषि बाजार",
"forest": "वन उत्पाद बाजार",
"water": "जल संसाधन",
"tourism": "पर्यटन",
"animal_husbandry": "पशुपालन",
"small_business": "लघु व्यवसाय",
"shop_trading": "दुकान / व्यापार",
"handicraft": "हस्तशिल्प",
"daily_wage": "दैनिक मजदूरी",
"government_job": "सरकारी नौकरी",
"private_job": "निजी नौकरी",
"other": "अन्य",
"select_village": "गाँव चुनें",
"local_market": "स्थानीय बाजार",
}

}

# ---------------- LANGUAGE FUNCTION ---------------- #

def get_lang():
    language = session.get("language", "en")
    return translations.get(language, translations["en"])

# ---------------- DATABASE ---------------- #

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return redirect(url_for("login"))

# ---------------- LANGUAGE CHANGE ---------------- #

@app.route("/change_language/<lang>")
def change_language(lang):

    session["language"] = lang

    return redirect(request.referrer)


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:

            session["user"] = username

            return redirect(url_for("dashboard"))

        else:

            flash("Invalid Username or Password")

    return render_template("login.html")


# ---------------- SIGNUP ---------------- #

# @app.route("/signup", methods=["GET", "POST"])
# def signup():

#     if request.method == "POST":

#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]

#         conn = get_connection()

#         conn.execute(
#             "INSERT INTO users(username,email,password) VALUES(?,?,?)",
#             (username, email, password)
#         )

#         conn.commit()

#         conn.close()

#         flash("Account Created Successfully")

#         return redirect(url_for("login"))

#     return render_template("signup.html")
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        otp = request.form["otp"]


        if password != confirm_password:

            flash("Password and Confirm Password do not match")
            return redirect(url_for("signup"))


        if otp != "123456":

            flash("Invalid OTP")
            return redirect(url_for("signup"))


        conn = get_connection()


        conn.execute(
        """
        INSERT INTO users
        (username,email,mobile,password)
        VALUES(?,?,?,?)
        """,
        (username,email,mobile,password)
        )


        conn.commit()
        conn.close()


        flash("Account Created Successfully")

        return redirect(url_for("login"))


    return render_template("signup.html")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(url_for("login"))

    return render_template(
    "dashboard.html",
    username=session["user"],
    lang=translations.get(
        session.get("language","en")
    )
)


@app.route("/village")
def village():

    if "user" not in session:
        return redirect(url_for("login"))

    df = pd.read_csv(r"C:\Users\Saba\OneDrive\Documents\Aheri_Taluka_Smart_Village_Dataset_Multilingual.csv")

    language = session.get("language", "en")

    if language == "mr":
        villages = sorted(df["Village Marathi"].dropna().unique().tolist())

    elif language == "hi":
        villages = sorted(df["Village Hindi"].dropna().unique().tolist())

    else:
        villages = sorted(df["Village Name"].dropna().unique().tolist())

    return render_template(
    "village_input.html",
    villages=villages,
    lang=get_lang()
    )
# @app.route("/predict", methods=["POST"])
# def predict():

    # print("Predict function hit!")

    # population = request.form.get("population")
    # literacy = request.form.get("literacy")
    # rainfall = request.form.get("rainfall")
    # schools = request.form.get("schools")
    # hospitals = request.form.get("hospitals")
    # employment = request.form.get("employment")

    # return f"""
    # <h2>✔ Prediction Working</h2>
    # <p>Population: {population}</p>
    # <p>Literacy: {literacy}</p>
    # <p>Rainfall: {rainfall}</p>
    # <p>Schools: {schools}</p>
    # <p>Hospitals: {hospitals}</p>
    # <p>Employment: {employment}</p>
    # """
@app.route("/predict", methods=["POST"])
def predict():
    village_name = request.form["village_name"]
    population = int(request.form["population"])
    literacy = int(request.form["literacy"])
    tenth_pass = int(request.form["tenth_pass"])
    twelfth_pass = int(request.form["twelfth_pass"])
    rainfall = int(request.form["rainfall"])
    schools = int(request.form["schools"])
    hospitals = int(request.form["hospitals"])
    employment = int(request.form["employment"])
    resource = request.form.get("resource", "Agriculture")

    input_data = pd.DataFrame(
    [[
        population,
        literacy,
        rainfall,
        schools,
        hospitals,
        employment
    ]],
    columns=[
        "Population",
        "Literacy Rate (%)",
        "Rainfall (mm)",
        "Number of Schools",
        "Number of Healthcare Centers",
        "Unemployment Rate (%)"
    ]
)

    ml_score = model.predict(input_data)[0]

    future_score = ml_score

    problems = []
    suggestions = []
    development_plan = []
    partners = []

    employment_suggestions = []

    if resource == "Agriculture":

        employment_suggestions.append("""
        🌾 Agriculture Based Employment:

        ✔ Organic Farming
        ✔ Dairy Farming
        ✔ Food Processing Unit
        ✔ Agricultural Equipment Services
        ✔ Vegetable Supply Business
        """)


    elif resource == "Forest":

        employment_suggestions.append("""
        🌳 Forest Based Employment:

        ✔ Bamboo Product Manufacturing
        ✔ Honey Production
        ✔ Herbal Product Processing
        ✔ Forest Product Business
        ✔ Eco Tourism Activities
        """)


    elif resource == "Water":

        employment_suggestions.append("""
        💧 Water Based Employment:

        ✔ Fish Farming
        ✔ Aquaculture Business
        ✔ Water Resource Management Jobs
        ✔ Irrigation Services
        """)


    elif resource == "Tourism":

        employment_suggestions.append("""
        🏞 Tourism Based Employment:

        ✔ Homestay Business
        ✔ Local Guide Service
        ✔ Food Stall Business
        ✔ Tribal Culture Tourism
        ✔ Handicraft Selling
        """)


    elif resource == "Animal Husbandry":

        employment_suggestions.append("""
        🐄 Animal Husbandry Employment:

        ✔ Dairy Farming
        ✔ Poultry Farming
        ✔ Goat Farming
        ✔ Milk Processing Unit
        """)


    elif resource == "Handicraft":

        employment_suggestions.append("""
        🎨 Handicraft Employment:

        ✔ Bamboo Craft
        ✔ Tribal Art Products
        ✔ Online Selling
        ✔ Local Market Business
        """)


    else:

        employment_suggestions.append("""
        💼 General Employment:

        ✔ MSME Units
        ✔ Skill Development Training
        ✔ Self Help Groups
        ✔ Digital Employment
        """)
    
    # Current score
    future_score = ml_score

    

    if literacy < 80:
        development_plan.append("Increase literacy through digital education.")
        future_score += 3

    if schools < 3:
        development_plan.append("Build 2 new schools.")
        future_score += 4

    if hospitals < 3:
        development_plan.append("Build one Primary Health Centre.")
        future_score += 4

    if employment < 75:
        development_plan.append("Start MSME industries and Skill Development Centre.")
        future_score += 5

    if rainfall > 1000:
        development_plan.append("Promote Rice, Sugarcane and Banana cultivation.")
        future_score += 2

    # ==========================
# NGO / CSR / Government Partner Recommendation
# ==========================

    partners = []

    if literacy < 70:
        partners.append("📚 Tata Trusts - Education Support")
        partners.append("📚 Infosys Foundation - Digital Learning")
        partners.append("🏛 Samagra Shiksha Abhiyan")

    if employment < 60:
        partners.append("💼 NABARD - Rural Employment")
        partners.append("💼 Reliance Foundation - Skill Development")
        partners.append("🏭 PMEGP - Self Employment")

    if schools < 3:
        partners.append("🏫 SBI Foundation - School Infrastructure")
        partners.append("🏫 Tata Trusts - Education Development")

    if hospitals < 2:
        partners.append("🏥 HCL Foundation - Healthcare")
        partners.append("🏥 Ayushman Bharat")

    if rainfall < 700:
        partners.append("💧 WOTR - Water Conservation")
        partners.append("🌱 BAIF Development Research Foundation")

    if len(partners) == 0:
        partners.append("✅ Village is suitable for Smart Village Development Programs.") 

    future_score = min(round(future_score,2),100)

 # ==========================
# Create Village Analysis Graph
# ==========================

    labels = [
        "Literacy",
        "Employment",
        "Schools",
        "Hospitals",
        "Rainfall"
    ]

    values = [
        literacy,
        employment,
        schools * 20,
        hospitals * 20,
        rainfall / 20
    ]

    plt.figure(figsize=(8,4))
    plt.bar(labels, values)

    plt.title("Village Analysis")
    plt.xlabel("Parameters")
    plt.ylabel("Score")

    plt.tight_layout()

    plt.savefig("static/graph.png")

    plt.close()
    
    if literacy < 50:
        problems.append("Very Low Literacy Rate")
        suggestions.append("Start adult literacy mission.")
        development_plan.append("Open Digital Learning Centres.")
        future_score += 6

    elif literacy < 80:
        problems.append("Low Literacy Rate")
        suggestions.append("Increase digital education and literacy programs.")
        development_plan.append("Recruit more teachers.")
        future_score += 3

    else:
        suggestions.append("Literacy level is satisfactory.")

# Employment
    if employment < 50:
        problems.append("Very Low Employment Opportunities")
        suggestions.append("Launch MSME industries.")
        development_plan.append("Open Skill Development Centre.")
        future_score += 6

    elif employment < 75:
        problems.append("Low Employment Opportunities")
        suggestions.append("Create MSMEs and skill development centers.")
        development_plan.append("Support Self Help Groups.")
        future_score += 3

    else:
        suggestions.append("Employment level is satisfactory.")

# Hospitals
    if hospitals == 0:
        problems.append("No Healthcare Facility")
        suggestions.append("Construct a Primary Health Centre.")
        development_plan.append("Build PHC and Ambulance Service.")
        future_score += 5

    elif hospitals < 3:
        problems.append("Healthcare Facilities are Limited")
        suggestions.append("Build more healthcare centers.")
        development_plan.append("Upgrade existing hospitals.")
        future_score += 3

    else:
        suggestions.append("Healthcare facilities are good.")

# Schools
    if schools == 0:
        problems.append("No Schools Available")
        suggestions.append("Build Government Schools.")
        development_plan.append("Construct 2 Schools.")
        future_score += 5

    elif schools < 3:
        problems.append("Insufficient Schools")
        suggestions.append("Increase the number of schools.")
        development_plan.append("Build one new school.")
        future_score += 3

    else:
        suggestions.append("Education infrastructure is good.")

# Crops
    if rainfall > 1500:
        suggestions.append("Suitable Crops: Rice, Sugarcane, Banana, Coconut")

    elif rainfall > 1000:
        suggestions.append("Suitable Crops: Rice, Sugarcane, Banana")

    elif rainfall > 700:
        suggestions.append("Suitable Crops: Jowar, Bajra, Tur")

    else:
        suggestions.append("Suitable Crops: Bajra, Gram, Groundnut")

    future_score = min(round(future_score, 2), 100)

    session["population"] = population
    session["literacy"] = literacy
    session["rainfall"] = rainfall
    session["schools"] = schools
    session["hospitals"] = hospitals
    session["employment"] = employment
    session["score"] = round(ml_score, 2)
    session["suggestions"] = suggestions
    session["future_score"] = future_score
    session["development_plan"] = development_plan
    session["problems"] = problems
    session["tenth_pass"] = tenth_pass
    session["twelfth_pass"] = twelfth_pass
    session["village_name"] = village_name
    

    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS village_analysis(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    population INTEGER,
    literacy INTEGER,
    tenth_pass INTEGER,
    twelfth_pass INTEGER,
    rainfall INTEGER,
    schools INTEGER,
    hospitals INTEGER,
    employment INTEGER,
    score REAL
)
""")

    conn.execute("""
    INSERT INTO village_analysis
    (
        population,
        literacy,
        tenth_pass,
        twelfth_pass,
        rainfall,
        schools,
        hospitals,
        employment,
        score
    )
    VALUES (?,?,?,?,?,?,?,?,?)
    """,
    (
        population,
        literacy,
        tenth_pass,
        twelfth_pass,
        rainfall,
    schools,
    hospitals,
    employment,
    round(ml_score, 2)
    )
    )

    conn.commit()
    conn.close()
    

    # ==========================
# Education Based Employment Suggestions
# ==========================

    if tenth_pass < 50:
        suggestions.append(
            "🎓 Increase Secondary School Education to improve employment opportunities."
        )
        development_plan.append(
            "Open skill training centers for 10th pass students."
        )

    else:
        suggestions.append(
            "✅ 10th pass population is satisfactory."
        )

    if twelfth_pass < 30:
        suggestions.append(
            "🎓 Encourage higher secondary education and vocational training."
        )
        development_plan.append(
            "Start ITI, Polytechnic and Skill Development Programs."
        )

    else:
        suggestions.append(
            "✅ 12th pass population is satisfactory."
        )

    return render_template(    
    "prediction.html",
    population=population,
    literacy=literacy,
    rainfall=rainfall,
    schools=schools,
    hospitals=hospitals,
    employment=employment,
    score=round(ml_score,2),
    suggestions=suggestions,
    future_score=future_score,
    development_plan= development_plan,
    problems=problems,
    lang=get_lang(),
    partners=partners,
    village_name=village_name
    )


@app.route("/crop", methods=["GET", "POST"])
def crop():

    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    rainfall = None
    water = None
    soil = None

    if request.method == "POST":

        rainfall = int(request.form["rainfall"])
        water = request.form["water"]
        soil = request.form["soil"]

    # High Rainfall
        if rainfall >= 1500:

            if soil == "Black":
                result = """
            🌾 Rice<br>
            🌿 Sugarcane<br>
            🍌 Banana<br>
            🌽 Maize
            """

            elif soil == "Red":
                result = """
            🌾 Rice<br>
            🌿 Turmeric<br>
            🍍 Pineapple<br>
            🌽 Maize
            """

            else:
                result = """
            🌾 Rice<br>
            🌿 Sugarcane<br>
            🥥 Coconut<br>
            🍌 Banana
            """

    # Medium Rainfall
        elif rainfall >= 900:

            if water == "High":
                result = """
            🌽 Maize<br>
            🌿 Soybean<br>
            🥜 Groundnut<br>
            🌻 Sunflower
            """

            else:
                result = """
            🌱 Jowar<br>
            🌾 Bajra<br>
            🌿 Tur<br>
            🥜 Groundnut
            """

    # Low Rainfall
        else:

            if soil == "Black":
                result = """
            🌾 Cotton<br>
            🌱 Jowar<br>
            🌿 Gram<br>
            🥜 Groundnut
            """

            else:
                result = """
            🌾 Bajra<br>
            🌱 Jowar<br>
            🌿 Gram<br>
            🌻 Sunflower
            """

   
    return render_template(
        "crop.html",
        result=result,
        rainfall=rainfall,
        water=water,
        soil=soil,
        lang=get_lang()
    )
    

# ---------------- GOVERNMENT SCHEME RECOMMENDATION ---------------- #

@app.route("/schemes", methods=["GET", "POST"])
def schemes():

    if "user" not in session:
        return redirect(url_for("login"))

    recommendations = []
    lang = session.get("language", "en")

    if request.method == "POST":

        literacy = int(request.form["literacy"])
        employment = int(request.form["employment"])
        roads = int(request.form["roads"])
        water = request.form["water"]
        healthcare = int(request.form["healthcare"])
        internet = request.form["internet"]
        tenth_pass = session.get("tenth_pass", 0)
        twelfth_pass = session.get("twelfth_pass", 0)


        # Education
        if literacy < 70:

            if lang == "mr":
                recommendations.append("📚 समग्र शिक्षा अभियान - शाळा शिक्षण व डिजिटल शिक्षण सुविधा सुधाराव्यात.")

            elif lang == "hi":
                recommendations.append("📚 समग्र शिक्षा अभियान - विद्यालय शिक्षा और डिजिटल शिक्षा सुविधाओं में सुधार करें।")
            else:
                recommendations.append("📚 Samagra Shiksha Abhiyan - Improve school education and digital learning facilities.")


        # Employment
        if employment < 60:

            if lang == "mr":
                recommendations.append("💼 मनरेगा - ग्रामीण रोजगाराच्या संधी वाढवा.")
                recommendations.append("🏭 पीएमईजीपी - लघुउद्योग व स्वयंरोजगाराला प्रोत्साहन द्या.")

            elif lang == "hi":
                recommendations.append("💼 मनरेगा - ग्रामीण रोजगार के अवसर बढ़ाएँ।")
                recommendations.append("🏭 पीएमईजीपी - छोटे उद्योग एवं स्वरोजगार को बढ़ावा दें।")

            else:
                recommendations.append("💼 MGNREGA - Provide rural employment opportunities.")
                recommendations.append("🏭 PMEGP - Support village level small industries and self employment.")


        # Roads
        if roads < 50:

            if lang == "mr":
                recommendations.append("🛣 प्रधानमंत्री ग्राम सडक योजना - ग्रामीण रस्ते सुधारावेत.")

            elif lang == "hi":
                recommendations.append("🛣 प्रधानमंत्री ग्राम सड़क योजना - ग्रामीण सड़क संपर्क सुधारें।")

            else:
                recommendations.append("🛣 Pradhan Mantri Gram Sadak Yojana (PMGSY) - Improve rural road connectivity.")


        # Water
        if water == "No":

            if lang == "mr":
                recommendations.append("💧 जल जीवन मिशन - सुरक्षित पिण्याच्या पाण्याची सुविधा उपलब्ध करा.")

            elif lang == "hi":
                recommendations.append("💧 जल जीवन मिशन - सुरक्षित पेयजल उपलब्ध कराएँ।")

            else:
                recommendations.append("💧 Jal Jeevan Mission - Provide safe drinking water supply.")


        # Healthcare
        if healthcare < 2:

            if lang == "mr":
                recommendations.append("🏥 आयुष्मान भारत - आरोग्य सुविधा सुधाराव्यात.")

            elif lang == "hi":
                recommendations.append("🏥 आयुष्मान भारत - स्वास्थ्य सुविधाओं में सुधार करें।")

            else:
                recommendations.append("🏥 Ayushman Bharat - Improve healthcare facilities and medical services.")


        # Internet
        if internet == "No":

            if lang == "mr":
                recommendations.append("🌐 डिजिटल इंडिया मिशन - इंटरनेट सुविधा वाढवा.")

            elif lang == "hi":
                recommendations.append("🌐 डिजिटल इंडिया मिशन - इंटरनेट सुविधा बढ़ाएँ।")

            else:
                recommendations.append("🌐 Digital India Mission - Improve internet connectivity and digital services.")


        if len(recommendations) == 0:

            if lang == "mr":
                recommendations.append("✅ गावाचा विकास चांगला आहे. विद्यमान योजना सुरू ठेवा.")

            elif lang == "hi":
                recommendations.append("✅ गाँव का विकास अच्छा है। वर्तमान योजनाएँ जारी रखें।")

            else:
                recommendations.append("✅ Village development indicators are good. Continue existing programs.")


    return render_template(
        "schemes.html",
        recommendations=recommendations,
        lang=get_lang()
    )
@app.route("/employment", methods=["GET", "POST"])
def employment():

    if "user" not in session:
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":

        population = int(request.form["population"])
        literacy = int(request.form["literacy"])
        employment = int(request.form["employment"])
        resource = request.form["resource"]

        # Agriculture
        if resource == "Agriculture":

            if employment < 50:
                result = """
                🌾 Organic Farming<br>
                🚜 Farm Machinery Rental<br>
                🐄 Dairy Farming<br>
                🥛 Milk Collection Center<br>
                ✔ PMEGP<br>
                ✔ MGNREGA
                """

            else:
                result = """
                🌾 Food Processing Unit<br>
                🏭 Agro Industries<br>
                🌽 Seed Production Unit<br>
                🚜 Smart Farming
                """

        # Forest
        elif resource == "Forest":

            result = """
            🎋 Bamboo Products<br>
            🧺 Handicrafts<br>
            🌿 Herbal Products<br>
            🍯 Honey Processing<br>
            ✔ NRLM
            """

        # Water
        elif resource == "Water":

            result = """
            🐟 Fish Farming<br>
            🚣 Eco Tourism<br>
            🌾 Irrigation Services<br>
            💧 Water Management Projects
            """

        
        # Tourism
        elif resource == "Tourism":

            result = """
            🏕 Eco Tourism<br>
            🏨 Homestay Business<br>
            🍴 Local Food Center<br>
            🚖Tourist Transport
            """

# Business
        elif resource == "Business":

            result = """
            🏪 Small Business Development<br>
            💰 Startup Support<br>
            🛒 Local Market Development<br>
            ✔ PMEGP Scheme
            """

# Animal Husbandry
        elif resource == "Animal Husbandry":

            result = """
            🐄 Dairy Farming<br>
            🐐 Goat Farming<br>
            🐓 Poultry Business<br>
            🥛 Milk Processing Unit
            """

# Handicraft
        elif resource == "Handicraft":

            result = """
            🧺 Handicraft Training<br>
            🏠 Cottage Industry Development<br>
            🛍 Online Selling Support<br>
            ✔ Self Help Group Support
            """

# Other
        else:

            result = """
            💼 Skill Development Programs<br>
            🎓 Vocational Training<br>
            🏭 New Employment Opportunities<br>
            ✔ Government Employment Schemes
            """
        # ==========================
        # Education Based Suggestions
        # ==========================

        result += "<hr><h3>🎓 Education Based Employment Suggestions</h3>"
        tenth_pass = session.get("tenth_pass", 0)
        twelfth_pass = session.get("twelfth_pass", 0)

        if tenth_pass < 50:
            result += """
            📘 Increase Secondary School Education<br>
            🛠 Start Skill Development Centers<br>
            👨‍🏭 Promote Vocational Training<br>
            """

        else:
            result += """
            ✅ Good number of 10th pass students.<br>
            """

        if twelfth_pass < 30:
                result += """
                📚 Encourage Higher Secondary Education<br>
                🏫 Open ITI & Polytechnic Colleges<br>
                💻 Computer Training Centers<br>
                """

        else:
            result += """
            ✅ Good number of 12th pass students.<br>
            """

        if employment < 60 and tenth_pass > 100:
            result += """
            🏭 MSME Industries<br>
            🚜 Agriculture Equipment Center<br>
            🛠 Mechanical Workshops<br>
            """

        if employment < 60 and twelfth_pass > 50:
            result += """
            💻 BPO Centers<br>
            🏦 Banking Mitra (CSC)<br>
            📱 Digital Service Centers<br>
            👨‍💼 Government Exam Coaching Center<br>
            """

        if twelfth_pass > 100:
            result += """
            🎓 Degree College<br>
            💼 Startup Incubation Center<br>
            🚀 Entrepreneurship Development Program<br>
            """
    return render_template(
        "employment.html",
        result=result,
        lang=get_lang(),
    )


@app.route("/infrastructure", methods=["GET", "POST"])
def infrastructure():

    if "user" not in session:
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":
        roads = int(request.form.get("roads"))
        schools = int(request.form.get("schools"))
        hospitals = int(request.form.get("hospitals"))
        internet = request.form.get("internet")


        result = ""

# Roads
        if roads <= 20:
            result += "🔴 Very Poor Road Connectivity<br>"
            result += "✔ Construct Concrete Roads<br>"
        elif roads <= 50:
            result += "🟠 Average Road Connectivity<br>"
            result += "✔ Repair Existing Roads<br>"
        else:
            result += "🟢 Excellent Road Connectivity<br>"

# Schools
        if schools == 0:
            result += "<br>🏫 No Schools Available<br>"
            result += "✔ Build Primary & Secondary Schools<br>"
        elif schools <= 2:
            result += "<br>🏫 Insufficient Schools<br>"
            result += "✔ Build More Schools<br>"
        else:
            result += "<br>🏫 Education Infrastructure is Good<br>"

# Hospitals
        if hospitals == 0:
            result += "<br>🏥 No Healthcare Facility<br>"
            result += "✔ Build Primary Health Centre<br>"
        elif hospitals <= 2:
            result += "<br>🏥 Limited Healthcare Facilities<br>"
            result += "✔ Increase Healthcare Centers<br>"
        else:
            result += "<br>🏥 Healthcare Facilities are Good<br>"

# Internet
        if internet == "No":
            result += "<br>🌐 Internet Not Available<br>"
            result += "✔ Install Fiber Internet<br>"
            result += "✔ Digital Education Centre<br>"
        else:
            result += "<br>🌐 Internet Available<br>"

# Overall AI Recommendation
        result += "<hr><b>🤖 AI Recommendation</b><br>"

        if roads < 50 and schools < 3 and hospitals < 3:
            result += """
            🚀 High Priority Development<br>
            ✔Roads<br>
            ✔ Schools<br>
            ✔ Hospitals<br>
            ✔ Solar Energy<br>
            ✔ Water Conservation
            """

        elif roads >= 50 and schools >= 3 and hospitals >= 3:
            result += """
            🟢 Village Infrastructure is Good<br>
            ✔ Smart Street Lights<br>
            ✔ CCTV Security<br>
            ✔ EV Charging Station
            """

        elif schools < 3:
             result += """
            📚 Focus on Education Infrastructure<br>
            ✔ Smart Classrooms<br>
            ✔ Digital Library
            """

        elif hospitals < 3:
            result += """
            ❤️ Focus on Healthcare<br>
            ✔ Ambulance Service<br>
            ✔ Telemedicine Centre
            """

    return render_template(
    "infrastructure.html",
    result=result,
    lang=get_lang()
)

@app.route("/report")
def report():

    if "user" not in session:
        return redirect(url_for("login"))

    # Sample scores (replace these later with your actual prediction)
    current_score = 72
    predicted_score = 89

    labels = ["Current Score", "Predicted Score"]
    values = [current_score, predicted_score]

    plt.figure(figsize=(6,4))

    plt.bar(labels, values)

    plt.ylim(0,100)

    plt.ylabel("Development Score")

    plt.title("Current vs Predicted Development Score")

    graph_path = os.path.join("static", "images", "development_graph.png")

    plt.savefig(graph_path, bbox_inches="tight")

    plt.close()

    return render_template(
        "report.html",
        graph="images/development_graph.png"
    )

@app.route("/download_report")
def download_report():

    pdf = canvas.Canvas("Village_Report.pdf")

    pdf.setTitle("Smart AI Village Report")

    pdf.setFont("Helvetica-Bold",18)
    pdf.drawString(150,800,"Smart AI Village Report")

    pdf.setFont("Helvetica",12)

    y = 760

    pdf.drawString(50,y,f"Population : {session.get('population')}")
    y -= 20

    pdf.drawString(50,y,f"Literacy : {session.get('literacy')} %")
    y -= 20

    pdf.drawString(50,y,f"Rainfall : {session.get('rainfall')} mm")
    y -= 20

    pdf.drawString(50,y,f"Schools : {session.get('schools')}")
    y -= 20

    pdf.drawString(50,y,f"Hospitals : {session.get('hospitals')}")
    y -= 20

    pdf.drawString(50,y,f"Employment : {session.get('employment')} %")
    y -= 30

    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50,y,f"Development Score : {session.get('score')}")
    y -= 40

    pdf.drawString(50, y, f"Future Development Score : {session.get('future_score')}")
    y -= 30

    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50,y,"AI Recommendations")
    y -= 25

    pdf.setFont("Helvetica",12)

    for s in session.get("suggestions", []):
        pdf.drawString(60,y,"- " + s)
        y -= 20

    y -= 20

    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50, y, "Development Plan")
    y -= 25

    pdf.setFont("Helvetica",12)

    for item in session.get("development_plan", []):
        pdf.drawString(60, y, "- " + item)
        y -= 20

    pdf.save()

    return send_file(
        "Village_Report.pdf",
        as_attachment=True
    )
# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

@app.route('/live_dashboard')
def live_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM village_analysis")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(rainfall) FROM village_analysis")
    rainfall = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(employment) FROM village_analysis")
    employment = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(hospitals) FROM village_analysis")
    hospitals = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM village_analysis")
    score = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "live_dashboard.html",
        total=total,
        rainfall=round(rainfall,2),
        employment=round(employment,2),
        hospitals=round(hospitals,2),
        score=round(score,2),
        lang=get_lang()
    )

if __name__ == "__main__":
    app.run(debug=True)


