from flask import Flask, request
from flask_cors import CORS
import cohere
outcomes = ""
app = Flask(__name__)
CORS(app)
essayOutline = [
    {"title": "Hook", "body": "Engaging opening to capture attention."},
    {"title": "Background", "body": "Brief context to introduce the topic."},
    {"title": "Thesis",
     "body": "Clear statement of the main argument or purpose of the essay."},
    {"title": "Topic Sentence", "body": "Introduces the main idea of the paragraph."},
    {"title": "Evidence", "body": "Supporting examples or information."},
    {"title": "Analysis", "body": "Explanation of the evidence and its relevance."},
    {"title": "Conclusion", "body": "Summarizes the main point of the paragraph."},
    {"title": "Restate Thesis", "body": "Recapitulates the main argument."},
    {"title": "Summary", "body": "Recap of main points from body paragraphs."},
    {"title": "Concluding Statement",
     "body": "Leaves a lasting impression or suggests further consideration."}
]


def getfeedback(parNum, sentenceCount, prelude):
    ssentenceCount = len(sentenceCount.split('.'))
    feedback = []
    co = cohere.Client('[...]')

    response = co.chat(
        preamble=prelude,
        message=f"Give some feedback following the above guidelines on this text. Make sure to reference which paragraph or sentance of the text this feedback applies to. {
            sentenceCount}",
    )
    print(response.text)
    feedback.append({"title": "AI Feedback", "body": response.text})
    # print(parNum, sentenceCount, ssentenceCount)
    return feedback


@ app.route("/")
def hello():
    return "Hello World!"


@ app.route("/gradeAssignment", methods=["POST"])
def gradeAssignment():
    # print("helloabbcbcbcb")
    assignmentdata = request.get_json()
    # print(assignmentdata)
    assignment = assignmentdata['text']
    outcomes = assignmentdata["outcomes"][0]["oc"]
    # outcomeList = []
    preludeBegin = "You are an AI which assists students in writing. You will be given texts. Assess them on the following outcomes: "
    preludeEnd = ". Please try to reference the following common feeback written by the teacher for each outcome in your response. Use the following feedback: "
    for outcome in outcomes:
        # commonFeed.append(outcome["feed"])
        preludeBegin += outcome["desc"] + ". "
        preludeEnd += outcome["feed"] + ". "
    # print(outcomes)
    # assignment = assignment['con']
    print(preludeBegin+preludeEnd)
    prelude = preludeBegin+preludeEnd
    # print(len(assignment['content']))
    sentances = []
    for sen in assignment['content']:
        # print(sen)
        if 'content' in sen:
            if 'text' in sen['content'][0]:
                sentances.append(sen['content'][0]['text'])
    # print(sentances)
    s = []
    sa = 0
    for i in sentances:
        i = i.split(".")
        s.append(i)
        for j in i:
            sa += 1
    # print(assignment['content'][0]['content'][0]['text'])
    # print(sa)
    p = 100*(sa/25)
    # print(p)
    if p > 100:
        p = 100
    return {"prog": p, "feedback": getfeedback(len(sentances), sentances[-1], prelude)}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
