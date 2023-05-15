from voter import Voter
from flask import Flask, render_template, request, flash
from AddVoter import add_voter, voters
from datetime import datetime
from block import Block
import os
import time as t

app = Flask(__name__)
app.secret_key = os.urandom(24)

VOTERS=[]
li=[]
Blockchain = []
bc = tuple()


posts = [

    {
        'author': " Department of Information ",
        'title': 'How to cast your vote',
        'content': 'Register your self with Election Commission of India and get a valid Voter ID.',
        'date_posted': str(datetime.date(datetime.now()))+" at "+str(datetime.time(datetime.now()))
    },
    {
        'author': "Press Release  ",
        'title': 'Overview of Electo.ai and general information',
        'content': 'It is online portal beneficial for remote voting with top notch security along with minimal cost.',
        'date_posted': str(datetime.date(datetime.now()))+" at "+str(datetime.time(datetime.now()))
    },
    {
        'author': "It's me , Bharat ",
        'title': 'Technology behind Electo.ai',
        'content': '''This portal is an initial phase of pilot project to test the user interface and evaluate  ability to make online election secure and reliable 
          Blockchain technology can be used in online elections to enhance security, transparency, and accountability. Here are some ways in which blockchain technology can be applied to online elections:
          '1. Identity Verification: Blockchain can be used to verify the identity of voters, ensuring that only eligible voters can participate in the election. A decentralized identity management system can be created using blockchain, where each voter has a unique digital identity that is verified and stored on the blockchain.
          '2. Immutable Records: Blockchain provides an immutable ledger that can store voting records securely and transparently. Each vote can be recorded on the blockchain, ensuring that it cannot be tampered with or deleted. This enhances the transparency and accountability of the election process.
          '3. Decentralization: Blockchain allows for a decentralized election system, where no single entity has control over the process. This reduces the risk of fraud and manipulation, as multiple nodes in the blockchain network would need to be compromised for an attack to be successful.
         '4. Smart Contracts: Smart contracts can be used to automate various aspects of the election process, such as vote counting and results verification. These contracts can be programmed to execute automatically, ensuring that the election process is fair and transparent.
         '5. Increased Security: Blockchain technology provides enhanced security to the online election process by providing cryptographic protection to the stored data, making it almost impossible for anyone to alter or tamper with the election results.
         'Overall, the use of blockchain technology in online elections can provide a more secure, transparent, and democratic process, with increased participation and trust among voters.''',

        'date_posted': str(datetime.date(datetime.now()))+" at "+str(datetime.time(datetime.now()))
    }

    ]



@app.route("/")
def home():
    return render_template("index.html", posts = posts)

@app.route("/generate", methods = ['POST',"GET"])
def generate():
    if request.method == 'POST':
        result = request.form
        voter = add_voter(result['ID'])

        if voter.get_key() in voters:
            flash("Passcode already generated", "info")

            for i in VOTERS:
                if voter.get_key() == i.get_key():
                    result = i.voter.disp()
            return render_template("generate.html", result=result, cond=True)

        if voter.verify():
            flash("Your vote is already registered", "info")

        else:
            voters.append(voter.get_key())
            VOTERS.append(voter)
            pk=voter.get_key()
            li.clear()
            li.append(pk)
            prk=voter.disp()[pk][0]
            li.append(prk)
            return render_template("generate.html",result = voter.disp(), cond = True)

    return render_template("generate.html", cond = False)

@app.route("/voter_login", methods = ['POST','GET'])
def voter_login():
    if request.method == 'POST':
        result = request.form
        public_key = result['public_key']
        private_key = result['private_key']
        permit = False

        for i in VOTERS:
            if i.voter.public_key == public_key and i.voter.private_key == private_key:
                permit = True
                if i.voter.amount == 1:
                    i.voter.trans_vote()
                    return render_template("profile.html",result=li)
                else:
                    flash("Your vote is already registered", "info")
                    break
                break
        if not permit:
            flash("Who are you? Confirm your Identity or Check your credentials ", "danger! danger! danger!")

    if not li:
        flash("Generate your secure passcode first", "info")
        return  render_template("generate.html")

    return render_template("vote.html",pk = li[0], prk =li[1])

@app.route("/profile", methods = ['POST', 'GET'])
def profile():
    trans = {'public_key': '',
             'time': '',
             'candidate': ''}
    if request.method == 'POST':
        result = request.form
        flash("Successfully voted, your session has ended", "success")
        trans['public_key'] = li[0]
        trans['time'] = str(t.time())
        trans['candidate'] = result['candidate']
        Blockchain.append(Block(trans))
        return render_template("ends.html")



@app.route("/candid")
def candid():
    return render_template('candid.html', title="Candidates")

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/schemes")
def schemes():
    return render_template('schemes.html', title='Govenment Schemes')

    
@app.route("/survey")
def survey():
    return render_template('survey.html', title='Survey by Different News Channels')


@app.route("/ends")
def ends():
    return render_template('ends.html', title='Thankyou')

@app.route("/slider")
def slider():
    return render_template('slideshow.html', title='slide show')


    
@app.route("/analysis", methods = ['POST', 'GET'])
def analysis():
    vote_count = {'con':0,'bjp':0,'aap':0,'no':0}
    for i in Blockchain:
        can = i.trans['candidate']
        print(can)
        if can == "CONGRESS":
            vote_count['con'] +=1
        
        elif can == "BJP":
            vote_count['bjp'] +=1
        elif can == "AAP":
            vote_count['aap'] +=1
        else:
            vote_count['no'] +=1

    return render_template("analysis.html",result=vote_count, title="Analysis")




if __name__ == "__main__":
    app.run(debug=True)
