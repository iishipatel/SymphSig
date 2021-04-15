from flask import Flask, jsonify, request
app = Flask(__name__)
from flask_cors import CORS, cross_origin
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import numpy as np
import pickle
import pickle
import wave

@app.route('/', methods = ['GET'])
@cross_origin()
def check():
    return jsonify({'message':'It works!'})

@app.route('/embed', methods = ['POST'])
@cross_origin()
def embed():
    frame_bytes=bytes(request.json["audio_bytes"],'UTF-8')
    string=request.json["sign"]
    string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)
    frame_modified = frame_modified.decode('UTF-8')


    return jsonify({'modified_audio_bytes':frame_modified})

@app.route('/verify', methods = ['POST'])
@cross_origin()
def verify():
    frame_bytes=bytes(request.json["audio_bytes"],'UTF-8')
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    decoded = string.split("###")[0]


    return jsonify({'digital_sign':decoded})
    

if __name__=='__main__':
    app.run(debug=True, port=8080)