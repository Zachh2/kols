from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def get_cookie(user, passw):
    session = requests.Session()
    headers = {
        'authority': 'free.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'dpr': '3',
        'origin': 'https://free.facebook.com',
        'referer': 'https://free.facebook.com/login/?email=%s' % (user),
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.1"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        'viewport-width': '980',
    }
    getlog = session.get(f'https://free.facebook.com/login.php')
    idpass = {
        "lsd": re.search('name="lsd" value="(.*?)"', str(getlog.text)).group(1),
        "jazoest": re.search('name="jazoest" value="(.*?)"', str(getlog.text)).group(1),
        "m_ts": re.search('name="m_ts" value="(.*?)"', str(getlog.text)).group(1),
        "li": re.search('name="li" value="(.*?)"', str(getlog.text)).group(1),
        "try_number": "0",
        "unrecognize_tries": "0",
        "email": user,
        "pass": passw,
        "login": "Log In",
        "bi_xrwh": re.search('name="bi_xrwh" value="(.*?)"', str(getlog.text)).group(1),
    }
    comp = session.post("https://free.facebook.com/login/device-based/regular/login/?shbl=1&refsrc=deprecated", headers=headers, data=idpass, allow_redirects=False)
    jopl = session.cookies.get_dict().keys()
    cookie = ";".join([key + "=" + value for key, value in session.cookies.get_dict().items()])
    if "c_user" in jopl:
        return {"status": "success", "cookie": cookie}
    elif "checkpoint" in jopl:
        return {"status": "error", "message": "Account checkpoint"}
    else:
        return {"status": "error", "message": "Invalid username or password"}

@app.route('/api/getcookie', methods=['GET'])
def get_cookie_api():
    user = request.args.get('gmail')
    passw = request.args.get('password')
    if not user or not passw:
        return jsonify({"status": "error", "message": "Missing input value"}), 400
    result = get_cookie(user, passw)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
