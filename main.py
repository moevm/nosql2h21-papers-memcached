import os

from flask import Flask, render_template, request
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.set("Issledovanie_matematiki", "Ivanov,2000,publons/1")
mc.set("Issledovanie_fiziki", "Petrov,2001,publons/2")
mc.set("Issledovanie_himii", "Ivanov,2002,pubmed/1")
mc.set("Issledovanie_literatury", "Petrov,2001,elibrary/1")
mc.set("Issledovanie_BZD", "Sidorov,2001,elibrary/1")
mc.set("Ivanov", "Issledovanie_matematiki,Issledovanie_himii")
mc.set("Petrov", "Issledovanie_fiziki,Issledovanie_literatury")
mc.set("Sidorov", "Issledovanie_BZD")
mc.set("2000", "Issledovanie_matematiki")
mc.set("2001", "Issledovanie_fiziki,Issledovanie_literatury,Issledovanie_BZD")
mc.set("2002", "Issledovanie_himii")
mc.set("publons", "Issledovanie_matematiki,Issledovanie_fiziki")
mc.set("pubmed", "Issledovanie_himii")
mc.set("elibrary", "Issledovanie_literatury,Issledovanie_BZD")

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        source = str(request.form["SOURCE"])
        fio = str(request.form["FIO"])
        year = str(request.form["YEAR"])

        source_empty = 1
        fio_empty = 1
        year_empty = 1

        if source != '':
            source_res_set = set(str(mc.get(source)).split(','))
            source_empty = 0
        if fio != '':
            fio_res_set = set(str(mc.get(fio)).split(','))
            fio_empty = 0
        if year != '':
            year_res_set = set(str(mc.get(year)).split(','))
            year_empty = 0

        res_set = source_res_set
        if fio_empty == 0:
            res_set = res_set & fio_res_set
        if year_empty == 0:
            res_set = res_set & year_res_set


        result_keys = list(res_set)
        results = []

        for key in result_keys:
            tmp = mc.get(key)
            results.append(str(tmp).split(',')[-1])

        return render_template("results.html", result = results)
    else:
        return render_template("main.html")


if __name__ == '__main__':
    app.run(host="localhost")
