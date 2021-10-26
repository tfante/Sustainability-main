from flask import Flask, render_template, request, url_for, redirect, session
from pprint import pprint
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from utils import *
app = Flask(__name__,static_folder='static',template_folder='templates')



@app.route("/", methods=['GET', 'POST'])
def homepage():
    #html = build_home_page()
    #logger.info(html)
    descs = home_descriptions()
    addysT = get_all_uniq_addresses()
    addys = get_all_uniq_addresses_list()
    homeimages = os.listdir('../static/images/home/')

    return render_template("pages/home.html", descs=descs,addysT=addysT,homeimages=homeimages,addys=addys)

@app.route('/aboutus.html', methods=['GET','POST'])
def about():
    return render_template("pages/aboutus.html")

@app.route('/team.html', methods=['GET', 'POST'])
def team():
    team = team_page()
    return render_template("pages/team.html", team=team)

@app.route('/exploredata.html', methods=['GET', 'POST'])
def explore():
    kmeans_clustering()
    return render_template("pages/exploredata.html")

@app.route('/<address>', methods=['GET','POST'])
def dynamicPage(address):
    x = get_address_data(address)

    return render_template("pages/address.html")


if __name__ == "__main__":
    app.run(debug=True)
