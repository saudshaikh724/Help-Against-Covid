from flask import Flask, render_template,request, jsonify
import requests
import test_extrract
from forms import *
import pymongo
client = pymongo.MongoClient("mongodb+srv://saud:mlab3431@hospitals.5loco.mongodb.net/helpagainstcovid?retryWrites=true&w=majority")
mydatabase = client.helpagainstcovid
collection = mydatabase.botdata
hospc=mydatabase.docinfo
LOCATION_IQ_API_KEY = "pk.0db4987d09b5a2c6b19a15ecd68e002b"

dis = ""
st = ""
#initialize the app
app = Flask(__name__)

#Index page
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route("/about", methods = ['GET', 'POST'])
def about():
    return render_template('About.html')

@app.route("/saveDataForVaccine", methods = ['GET', 'POST'])
def saveDataForVaccine():
    global dis, st
    value = request.get_json()
    r = requests.get("https://us1.locationiq.com/v1/reverse.php?key=" + LOCATION_IQ_API_KEY +
                     "&lat=" + str(value["latitude"]) + "&lon=" + str(value["longitude"]) + "&format=json")
    data = r.json()
    dis = data["address"]["state_district"]
    st = data["address"]["state"]
    return jsonify({"server":"Success"})


@app.route('/get')
def get_bot_response():
    message = request.args.get('msg')
    if collection.find_one({'"questions"': message}):
        ans = collection.find_one({'"questions"': message})
        #print('Question',message,' Answer',ans)
        resp = ans['"answer"']
        return str("<div id='sa'>"+message+"<br></div><div id='sb'>"+resp+"</div>")
    else:
        return "<br><div id='sa'>"+message+"<br></div><div id='sb'>Enter Valid Question<br></div><br>"


@app.route("/vaccine", methods = ['GET', 'POST'])
def vaccine():
    global dis, st
    nstlst =[]
    length=0
    slst=[]
    st = ""

    form = TextForm(request.form)
    if request.method == 'POST':
        date = str(form.date.data)
        date = (date[-2:]+date[-6:-3]+"-"+date[0:4])
        stateID = [{"state_id":1,"state_name":"Andaman and Nicobar Islands"},{"state_id":2,"state_name":"Andhra Pradesh"},{"state_id":3,"state_name":"Arunachal Pradesh"},{"state_id":4,"state_name":"Assam"},{"state_id":5,"state_name":"Bihar"},{"state_id":6,"state_name":"Chandigarh"},{"state_id":7,"state_name":"Chhattisgarh"},{"state_id":8,"state_name":"Dadra and Nagar Haveli"},{"state_id":37,"state_name":"Daman and Diu"},{"state_id":9,"state_name":"Delhi"},{"state_id":10,"state_name":"Goa"},{"state_id":11,"state_name":"Gujarat"},{"state_id":12,"state_name":"Haryana"},{"state_id":13,"state_name":"Himachal Pradesh"},{"state_id":14,"state_name":"Jammu and Kashmir"},{"state_id":15,"state_name":"Jharkhand"},{"state_id":16,"state_name":"Karnataka"},{"state_id":17,"state_name":"Kerala"},{"state_id":18,"state_name":"Ladakh"},{"state_id":19,"state_name":"Lakshadweep"},{"state_id":20,"state_name":"Madhya Pradesh"},{"state_id":21,"state_name":"Maharashtra"},{"state_id":22,"state_name":"Manipur"},{"state_id":23,"state_name":"Meghalaya"},{"state_id":24,"state_name":"Mizoram"},{"state_id":25,"state_name":"Nagaland"},{"state_id":26,"state_name":"Odisha"},{"state_id":27,"state_name":"Puducherry"},{"state_id":28,"state_name":"Punjab"},{"state_id":29,"state_name":"Rajasthan"},{"state_id":30,"state_name":"Sikkim"},{"state_id":31,"state_name":"Tamil Nadu"},{"state_id":32,"state_name":"Telangana"},{"state_id":33,"state_name":"Tripura"},{"state_id":34,"state_name":"Uttar Pradesh"},{"state_id":35,"state_name":"Uttarakhand"},{"state_id":36,"state_name":"West Bengal"}]
        sid = 0
        did = 0

        for i in range(len(stateID)):
            if (stateID[i]['state_name']).upper().strip() == st.upper().strip():
                sid=(stateID[i]['state_id'])
        districtID = [{"district_id":391,"district_name":"Ahmednagar"},{"district_id":364,"district_name":"Akola"},{"district_id":366,"district_name":"Amravati"},{"district_id":397,"district_name":"Aurangabad "},{"district_id":384,"district_name":"Beed"},{"district_id":370,"district_name":"Bhandara"},{"district_id":367,"district_name":"Buldhana"},{"district_id":380,"district_name":"Chandrapur"},{"district_id":388,"district_name":"Dhule"},{"district_id":379,"district_name":"Gadchiroli"},{"district_id":378,"district_name":"Gondia"},{"district_id":386,"district_name":"Hingoli"},{"district_id":390,"district_name":"Jalgaon"},{"district_id":396,"district_name":"Jalna"},{"district_id":371,"district_name":"Kolhapur"},{"district_id":383,"district_name":"Latur"},{"district_id":395,"district_name":"Mumbai"},{"district_id":365,"district_name":"Nagpur"},{"district_id":382,"district_name":"Nanded"},{"district_id":387,"district_name":"Nandurbar"},{"district_id":389,"district_name":"Nashik"},{"district_id":381,"district_name":"Osmanabad"},{"district_id":394,"district_name":"Palghar"},{"district_id":385,"district_name":"Parbhani"},{"district_id":363,"district_name":"Pune"},{"district_id":393,"district_name":"Raigad"},{"district_id":372,"district_name":"Ratnagiri"},{"district_id":373,"district_name":"Sangli"},{"district_id":376,"district_name":"Satara"},{"district_id":374,"district_name":"Sindhudurg"},{"district_id":375,"district_name":"Solapur"},{"district_id":392,"district_name":"Thane"},{"district_id":377,"district_name":"Wardha"},{"district_id":369,"district_name":"Washim"},{"district_id":368,"district_name":"Yavatmal"}]

        for i in range(len(districtID)):
            if districtID[i]["district_name"].upper().strip() == dis.upper().strip():
                did = (districtID[i]['district_id'])

        response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=395&date={}".format(date))
        nearbyhospitals = response.json()
        near = nearbyhospitals['sessions'][0:]

        for i in range(len(near)):
            for j in near[i]['slots']:
                st=st+j+", "
            st=st[:-2]
            slst.append(st)
            st = ""
        global sr
        sr=0
        for i in range(len(near)):
            sr=sr+1
            lst =sr,near[i]['name'],near[i]['address'],near[i]['vaccine'],slst[i],near[i]['fee'],near[i]["min_age_limit"]
            nstlst.append(lst)
        length = len(nstlst)
    return render_template('vaccine.html',vaccinetable=nstlst,length=length)


@app.route("/hospital", methods = ['GET', 'POST'])
def hospital():
    return render_template('hospital.html')

@app.route("/plasma", methods = ['GET', 'POST'])
def plasma():
    global sr
    sr=0
    lst = []
    collection = mydatabase.plasmadata
    cursor = collection.find()
    for record in cursor:
        sr=sr+1
        doc = sr, record['info'], record['avail'], record['type'], record['datetime']
        lst.append(doc)
    length = len(lst)
    return render_template('plasmatab.html',length=length,data=lst)
    
@app.route("/oxygen", methods = ['GET', 'POST'])
def oxygen():
    sr=0
    lst = []
    collection = mydatabase.oxygendata
    cursor = collection.find()
    for record in cursor:
        doc = record['user'], record['tweetdata'], record['postdate']
        tuser=record['handle']
        tdata=record['tweetdata']
        pdata=record['postdate']
        lst.append(doc)
    length = len(lst)
    return render_template('oxygen.html',length=length,data=lst)
    
@app.route("/symptoms", methods = ['GET', 'POST'])
def symptoms():
    lst = []
    collection = mydatabase.docinfo
    cursor = collection.find()
    for record in cursor:
        doc = record['name'],record['address'],record['contact no']
        lst.append(doc)
    length = len(lst)
    return render_template('symptoms.html',docttable=lst,length=length)

@app.route('/loc', methods=["POST", "GET"])
def loc():
    if request.method == "GET":
        return render_template('get_location.js')
    else:
        data = request.get_json()
        r = requests.get("https://us1.locationiq.com/v1/reverse.php?key=" + LOCATION_IQ_API_KEY +
                     "&lat=" + str(data["latitude"]) + "&lon=" + str(data["longitude"]) + "&format=json")
        data = r.json()

        state_district = data["address"]["state_district"]
        state = data["address"]["state"]
        country = data["address"]["country"]
        print('#####################################')
        print("Latitude and Longitude: ",data['lat'],data['lon'])
        response = test_extrract.get_data()
        return jsonify(response)

@app.route('/plsdata', methods=["POST", "GET"])
def plasmadata():
    if request.method == "GET":
        return render_template('get_location.js')
    else:
        data = request.get_json()
        r = requests.get("https://us1.locationiq.com/v1/reverse.php?key=" + LOCATION_IQ_API_KEY +
                     "&lat=" + str(data["latitude"]) + "&lon=" + str(data["longitude"]) + "&format=json")
        data = r.json()

        state_district = data["address"]["state_district"]
        state = data["address"]["state"]
        country = data["address"]["country"]
        print('#####################################')
        print("Latitude and Longitude: ",data['lat'],data['lon'])
        response = test_extrract.plasma_data()
        return jsonify(response)
#Run app
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=500, debug=True)
