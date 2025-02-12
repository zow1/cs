from flask import Flask, request, send_file, jsonify
import requests
import os
import re

app = Flask(__name__)

# 直播流地址字典
n = {
    '1': 'https://www.insurancegogogo.com/4987/yoyo_twn/playlist.m3u8?md5=GBZG9O5_d8TXxlkvWEzJbg&expires=1737962885',#yoyo
    '2': 'https://z02.ubtvfans.com/live/rx1/2437/43f3e7d06eeb53f3057cb2780fd11a50/index.m3u8',#VB明珠

}

# 根据ID获取直播流地址
@app.route('/')
def fetch_stream():
    id = request.args.get('id', '1', type=int)
    live = n.get(str(id))
    if not live:
        return jsonify({"error": "Stream not found"}), 404

    # 处理URL
    buri = "http://18.svi-studio.com/" if id == 993 else ("http://104.194.10.200:25461/" if id > 993 else os.path.dirname(live) + '/')

    # 获取当前脚本URL
    php = request.url_root + request.path

    # 获取ts参数
    ts = request.args.get('ts')
    if not ts:
        response = requests.get(live, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36', 'Referer': 'https://api.kds.tw/'}, verify=False)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch playlist"}), 500
        playlist = response.text
        playlist = re.sub(r'(.*?.ts)', r'{}\?id={}&ts={}\1'.format(php, id, buri), playlist, flags=re.IGNORECASE)
        return playlist, 200, {'Content-Type': 'application/vnd.apple.mpegurl'}
    else:
        # 缓存目录
        cache_dir = os.path.join(os.path.dirname(__file__), 'cache', str(id))
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)

        # 缓存文件路径
        ts_file_name = os.path.basename(ts)
        cache_file_path = os.path.join(cache_dir, ts_file_name)

        if os.path.exists(cache_file_path):
            # 如果缓存存在，读取并输出缓存文件
            return send_file(cache_file_path, mimetype='video/MP2T')
        else:
            # 如果缓存不存在，从远程获取文件并缓存
            response = requests.get(ts, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36', 'Referer': 'https://api.kds.tw/'}, verify=False)
            if response.status_code == 200:
                with open(cache_file_path, 'wb') as f:
                    f.write(response.content)
                clean_old_cache_files(cache_dir, 10)
                return response.content, 200, {'Content-Type': 'video/MP2T'}
            else:
                return jsonify({"error": "Failed to fetch TS file"}), 500

# 清理旧的缓存文件，保留最新的$max_files个文件
def clean_old_cache_files(directory, max_files):
    files = sorted(os.listdir(directory), reverse=True)
    if len(files) > max_files:
        for file in files[max_files:]:
            os.unlink(os.path.join(directory, file))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
