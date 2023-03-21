# import flask and re
from flask import Flask, request, render_template
import re

#Create the object 
app = Flask(__name__)


# Create an END POINT using routes and bind them with a functionality


@app.route('/', methods=['GET', 'POST'])
def match_txt():
    if request.method == 'POST':
        pattern = request.form['pattern']
        text = request.form['text']
        matches = re.findall(pattern,text)
        count = len(matches)
        return render_template('search.html', matches=matches, text=text, pattern=pattern, count=count)
    else:
        return render_template('search.html')



# Step 4 - Run the app
if __name__ == '__main__':
    app.run(debug=True)