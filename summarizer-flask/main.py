from beteiligung_interface import reader
from datetime import datetime
from flask import jsonify, Flask, request, abort
import logging
import os
import summarizer
import utils


app = Flask(__name__)
contributions_cached = {}
summarizer_cached = {}


@app.route('/summarize')
def summary():
    # Get the contribution to summarize
    contribid = request.args.get("nid")
    project = request.args.get("proj")
    sumlen = request.args.get("n")

    if contribid == None:
        logging.error(f"Request for '{project}' and '{contribid}' failed, as one was not provided!")
        abort(400, description="Insufficient Parameters provided")

    try:
        contribid = int(contribid)
    except:
        logging.error(f"Request with passed contribution-ID {contribid} failed! Malformed ID.")
        abort(400, description="Invalid Contribution ID! (Numerical only!)")

    # Check if contributions are already cached for the selected project and cache still valid
    contributions = []
    if project in contributions_cached \
            and (datetime.now() - contributions_cached["last_updated"]).total_seconds() <= app.config.get("CACHEVALID"):
        contributions = contributions_cached[project]
    else:  # else read contributions and write to cache
        logging.info(f'Building/Rebuilding cached contributions for project "{project}"')
        contributions_cached[project] = reader.get_all_contributions(project)
        contributions = contributions_cached[project]

    # Check if summarizer is already cached for the selected project and cache still valid
    summer = None
    if project in summarizer_cached \
            and (datetime.now() - summarizer_cached["last_updated"]).total_seconds() <= app.config.get("CACHEVALID"):
        summer = summarizer_cached[project]
    else:  # if not, build it and write to cache
        logging.info(f'Building/Rebuilding cached summarizer for project "{project}"')
        summarizer_cached[project] = summarizer.Summarizer(contributions)
        summer = summarizer_cached[project]

    logging.info("Running summarization for '{project}' and ID '{contribid}'.")

    # Words that do not deliver any content
    # These words are stored in txt databases in the folder "words"
    databases = os.listdir("words")
    exceptwords = []
    for db in databases:
        if db[-4:] == ".txt":
            exceptwords = exceptwords + (utils.get_except_words("words/" + db))

    x = {"id": contribid,
         "summary": summer.get_words(contributions[contribid], sumlen, exceptwords)}
    return jsonify(x)


if __name__ == "__main__":
    # Load the config file
    app.config.from_pyfile('config.cfg')

    # Initialize the summarizer's and contribution cache
    contributions_cached["last_updated"] = datetime.now()
    summarizer_cached["last_updated"] = datetime.now()

    # Prepare the logger
    if app.config.get("LOGTOFILE") == True:
        logging.basicConfig(filename=app.config.get("LOGFILE"), encoding="utf-8",
                            level=eval(str("logging."+app.config.get("LOGLEVEL"))))

    # Start Flask
    port = app.config.get('PORT')
    logging.info(f"Starting server on port {port}")
    app.run(port=port, debug=True)
