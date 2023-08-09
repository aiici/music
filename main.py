from flask import Flask, request, render_template, jsonify
from requests import get
from lxml import etree
import re

app = Flask(__name__)


def to_char():
    code = ''
    ord_data = [104, 116, 116, 112, 115, 58, 47, 47, 119, 119, 119, 46, 103, 101, 113, 117, 98, 97, 111, 46, 99, 111,
                109]
    for t in ord_data:
        code += chr(t)
    return code


class DownMusic:
    def __init__(self, ):
        self.url = to_char()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "referer": to_char()
        }

    def search_info(self, search_name):
        musics_dict = {}
        res = get(self.url + "/s/" + search_name, headers=self.headers, verify=False).text
        pattern_music_links = r'<a href="(/music/\d+)"'
        music_links = list(set(re.findall(pattern_music_links, res)))
        html = etree.HTML(res)
        text_elements = html.xpath('//div[@class="text-success col-4 col-content"]/text()')
        music_name = html.xpath('//div[@class="col-5 col-content"]/a/text()')
        name_list = []
        song_list = []
        for n in music_name:
            text_n = n.strip()
            name_list.append(text_n)
        for item in text_elements:
            text = item.strip()
            song_list.append(text)
        for n, song in enumerate(song_list):
            musics_dict[n] = {"name": name_list[n], "song": song, "url": music_links[n]}
        return musics_dict

    def get_data(self, url):
        data_url = self.url + url
        res = get(data_url).text
        pattern = r"'(http://.*?\.mp3\?.*?)'"
        match = re.search(pattern, res)
        mp3_link = match.group(1)
        return mp3_link

    # def download(self, aim_url):
    #     res = get(aim_url).content
    #     with open(str(int(time.time() * 100)) + ".mp3", "wb") as f:
    #         f.write(res)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    Music = request.form["searchQuery"]
    megs = download.search_info(Music)
    return jsonify(megs)


@app.route("/download", methods=["POST"])
def to_download():
    data = request.get_json()
    download_url = data.get("downloadUrl")
    aim_url = download.get_data(download_url)
    return jsonify({"aim_url": aim_url})


if __name__ == "__main__":
    download = DownMusic()
    app.run(host='0.0.0.0', threaded=True, port=8089)
