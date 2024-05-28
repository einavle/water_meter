from distutils.log import debug 
from fileinput import filename 
from flask import *  
import os
import io
from imageparse import ImageParse
from PIL import Image
import base64

app = Flask(__name__)   
  
parser=0
@app.route('/')   
def main():   
    return render_template("index.html")   

@app.route('/home', methods = ['POST'])   
def home():   
    return main()
  
@app.route('/decode', methods = ['GET','POST'])  
def decode():
     parser.parse()
     if parser.isOK():
         return render_template("Acknowledgement.html", meter_id = parser.getReadings()['meter_number'], meter_count = parser.getReadings()['counting_number']) 
     return render_template("parserError.html")
  
@app.route('/process', methods = ['GET','POST'])   
def process():
    if request.method == 'POST':   
        f = request.files['file'] 
        global parser 
        parser  = ImageParse(f)
    return render_template("process.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)