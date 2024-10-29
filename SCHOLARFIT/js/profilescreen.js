import { getItemFromSessionStorage} from './utils.js'
import { titleCase } from './utils.js'
const calculateScore = ()=> {
    const results = getItemFromSessionStorage('results')
    let total = 0, score = 0
    results.forEach(result => {
        let subjectName = result["subject_name"]
        let quizData = getItemFromSessionStorage(subjectName)
        total += quizData["totalQuestions"]
        score += result["score"]
    }) 
    return {"score": score, "total": total}  
}

const renderScore = ()=> {

    const scoreCard = document.getElementById('score_card')
    const {score, total} = calculateScore()
    
    scoreCard.children[0].textContent = `${score}/${total}`

}

renderScore()

const renderChart = () => {
   const TABLET_DESKTOP_WIDTH = 768
    const SHORT_CODE_NAMES = {
        'mathematics': 'Math',
        'english': 'Eng',
        'physics': 'Phyc',
        'economics': 'Econ',
        'chemistry': 'Chem',
        'accounting': 'Acc',
        'commerce': 'Comm',
        'animal husbandry': 'Anim-Hus',
        'fishery': 'Fis',
        'agricultural science': 'AgSci',
        'geography': 'Geog',
        'goverment': 'Govt',
        'literature in english': 'LitEng',
        'further mathematics': 'FMath'
    }
    const canvas = document.getElementById('subject_bar_graph')
    const results = getItemFromSessionStorage('results')
    const subjectNames = []
    const scores = []
    results.forEach(result => {
        subjectNames.push(SHORT_CODE_NAMES[result["subject_name"]])
        scores.push(result["score"])
    })

    const barOrientation = window.innerWidth >= TABLET_DESKTOP_WIDTH ? 'x' : 'y'
    const maxYScaleValue = Math.max(...scores) + 1
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: subjectNames,
            datasets: [{
                label: 'Subject Scores',
                data: scores,
                borderWidth: 1,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.3)',
                    'rgba(255, 159, 64, 0.3)',
                    'rgba(75, 192, 192, 0.3)',
                    'rgba(54, 162, 235, 0.3)'
                ],
                borderColor: [
                    'rgba(255, 99, 132)',
                    'rgba(255, 159, 64)',
                    'rgba(75, 192, 192)',
                    'rgba(54, 162, 235)'
                ]
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: maxYScaleValue
                }
            },
            indexAxis: barOrientation
        }
    })
}

renderChart()



const subjectTabs = document.querySelectorAll('.subj')
const setSubjectNames = () => {
    const data = getItemFromSessionStorage('results')
    let x = 1
    subjectTabs[0].textContent = "English"
    data.forEach((ex) =>{
        let subject_name = ex["subject_name"].toLowerCase()
        if (subject_name !== "english"){
            subjectTabs[x].textContent = titleCase(subject_name)
            x+= 1
        }    
    })
}

setSubjectNames()

const setTabListeners = () => {
    subjectTabs.forEach((tab) => {
        tab.addEventListener('click', (e) => {
            
            let subject = e.target.textContent
            subjectTabs.forEach(tb => {
                tb.classList.remove('active__btn') 
            })
            e.target.classList.add('active__btn')

            renderRevision(subject)
            
        })
    })
}

setTabListeners()


const evaluateQuestions = () => {
    const data = getItemFromSessionStorage("results_questions")

    const failedQuestions = {}
    let revision = {}
   
     data.map(dt => {
        let questionData = []
        dt["data"].forEach(block => {
                let questions = block["questions"]
                revision["passage"] =block["passage"]
                questions.forEach(question => {
                    revision["explanation"]= question["explanation"]
                    revision["question"] = question["question"]
                    let userAns = question["user_answer_id"]
                    let answers = question["answers"]
                    answers.forEach(ans => {
                        if (ans["is_correct"]){
                            revision["correctAnswer"] = ans["text"]
                        }
                    })
                    for (let x = 0; x < answers.length; x++){
                        let answer = answers[x]
                        if (answer["answer_id"] == userAns && !answer["is_correct"]){
                            let revise = revision
                            revision = {}
                            questionData.push(revise)
                        }
                    }
                })   
        })
        
        failedQuestions[dt["subject_name"].toLowerCase()] = questionData
    })
    return failedQuestions
}


{/* <div class="q_n_a">
                <div class="question row">
                  <p>What is the square root of 25?</p>
                  
                </div>
                <div class="answer">
                  <p>The square root of 25 is 5.</p>
                  <p>The square root of a number is a value that, when multiplied by itself, gives the original number.</p>
                </div>
              </div> */}

const revisionPanel = document.getElementById('revision-panel')
const renderRevision = (subject) => {
    revisionPanel.replaceChildren()

    const failedQuestions= evaluateQuestions()
    const subjectData = failedQuestions[subject.toLowerCase()]

    subjectData.forEach(sub => {
        let passageTag = document.createElement('p')
        const qNaDiv = document.createElement('div')
        qNaDiv.classList.add('q_n_a')
        const questionDiv = document.createElement('div')
        questionDiv.classList.add('question')
        const questionTag = document.createElement('p')
        if (sub["passage"]){
            passageTag.textContent = sub["passage"]
            questionDiv.append(passageTag)
        }
        questionTag.textContent = sub["question"]
        questionDiv.append(questionTag)
        qNaDiv.append(questionDiv)
        const answerDiv = document.createElement('div')
        answerDiv.classList.add('answer')
       
        const answerTag = document.createElement('p')
        answerTag.textContent = sub["correctAnswer"]
        answerDiv.append(answerTag)

        const explanationTag = document.createElement('p')
        explanationTag.textContent = sub["explanation"]
        answerDiv.append(explanationTag)

        qNaDiv.append(answerDiv)
        revisionPanel.append(qNaDiv)
    })   
}

renderRevision('english')
subjectTabs[0].click()
