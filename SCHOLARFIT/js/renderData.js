

import { generate_test, submitTest, updateUserProfile, subscribe } from "./apiService.js"
import {saveToSessionStorage, getItemFromSessionStorage, titleCase } from './utils.js'
import {data} from './testData.js'

const TOTAL_SUBJECTS = 4
   
export const loadSubjects = (data) => {
    let subjectDisplay = document.querySelectorAll('.utme__subjects')
    if (data["status"] === 200){
        console.log(data["data"])
        subjectDisplay.forEach(disp => {
            data["data"].forEach(dt => {
                if (dt["name"] !== "english"){
                    let option = document.createElement('option')
                    let subjectName = titleCase(dt["name"])
                    option.text = subjectName
                    option.value = dt["id"]
                    disp.appendChild(option)
                }
            })
        })
    }
    
}
 

const subjectTabs = document.querySelectorAll(".subj")
const nextButton = document.getElementById("nxt_question")
const prevButton = document.getElementById("prev_question")
const submitButton = document.getElementById('submit-test_btn')
const modalSubmitBtn = document.getElementById('modal-submit')

const navigationPad = document.getElementById('navigation__nav')

nextButton.addEventListener('click', () => {
    const currSubject = getItemFromSessionStorage("active_sub")
    const questions = nextQuestions(currSubject["index"], subjectTabs)
    renderQuestion(questions)

})

prevButton.addEventListener('click', () => {
    const currSubject = getItemFromSessionStorage("active_sub")
    const questions = previousQuestions(currSubject["index"], subjectTabs)
    renderQuestion(questions)
})

navigationPad.addEventListener('click', (e) => {
    if (e.target.classList.contains('Qc')){
        let num = e.target.textContent
        let question = navigateByQuestionNumber(num)
        
        renderQuestion([question])
    }
})
const setSubjectNames = (data, subjectTabs) => {
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
const selectSubject = (subjectTabs) => {
    subjectTabs.forEach((tab, idx) => {
        tab.addEventListener('click', (e) => {
            let subject = e.target.textContent
            saveToSessionStorage(`active_sub`, {"sub":subject.toLowerCase(), "index": idx})
            subjectTabs.forEach(tb => {
                tb.classList.remove('active__btn') 
                tb.classList.remove('active__finished')
            })
            e.target.classList.add('active__btn')
            if (e.target.classList.contains('finished__btn')){

                e.target.classList.add('active__finished')
            }
            const {page, pages, subj} = getQuestions()
            
            const questions = pages[page]
            buildNavigationCard()
            renderQuestion(questions)
        })
    })
}

const createPages = (subject, subjectData) => {
    
   
    const QUESTIONS_PER_PAGE = 3
    const data = {}
    data["currentPage"] = 0
    data["questionsDone"] = 0
    const pages = []
    data["pages"] = pages
    let x = 0
    
    let number = 1
    let group = []
    subjectData.forEach(sbData => {
        if (group.length === QUESTIONS_PER_PAGE){
                pages.push(group)
                group = []
        }
        if (sbData["passage"]){
            
            sbData["questions"] = sbData["questions"].map(p => {
                p = {...p, 'number': number}
                number++;
                return p
            })
            group.push(sbData)
        }else {

            let question = sbData["questions"][0]
            question = {...question, 'number': number}
            
            group.push(question)
            number++;
        }
            
        
    })
    if (group.length > 0) pages.push(group)
    
    data["totalQuestions"] = number - 1
    saveToSessionStorage(subject.toLowerCase(), data)
}

const loadingScreen = document.getElementById('loading-screen')
export const loadExam = async () => {
    const user = getItemFromSessionStorage("user")
    const profileId = user.profileId
    
    const respData = await generate_test(parseInt(profileId))
    
    const data = respData["data"]
    const testId = data["test_id"]
    saveToSessionStorage("testId", testId)
    saveToSessionStorage("answers", {})
    const exams = data["exam"]
    setTimeout(()=>{
        loadingScreen.classList.add('hide-loading-screen')

    }, 3000)
    
    setSubjectNames(exams, subjectTabs)
    selectSubject(subjectTabs)
    
    exams.forEach(ex => {
        let subName = ex["subject_name"]
        let data = ex["data"]
        createPages(subName, data)
    })
    saveToSessionStorage("answers", {})
    subjectTabs[0].click()
    setTimeout(()=>{
        
        startCountdown(30 * 60)
    },1500)
    
}

const getQuestions = () => {
    
    const activeSubject = getItemFromSessionStorage("active_sub")
    const currentSubjectData = getItemFromSessionStorage(activeSubject["sub"])
    const page = currentSubjectData["currentPage"]
    const questions = currentSubjectData["pages"]
    return {"page": page, "pages": questions, "subject": activeSubject["sub"]}
}
const updateCurrentPage = (currPage, subject)=> {
    let itemToUpdate = getItemFromSessionStorage(subject)
    itemToUpdate["currentPage"] = currPage
    saveToSessionStorage(subject, itemToUpdate)
}


const nextQuestions = (targetIdx, subjectTabs) => {
    const {page, pages, subject} = getQuestions()
    if (page < pages.length - 1){

        updateCurrentPage(page+1,subject)
        return pages[page + 1]
    }

    if (targetIdx < subjectTabs.length - 1){
        subjectTabs[targetIdx + 1].click()
        const {page, pages, subject} = getQuestions()
        return pages[page]
    }
    return pages[page]
}

const previousQuestions = (targetIdx, subjectTabs) => {
    const {page, pages, subject} = getQuestions()
    if (page > 0){
        updateCurrentPage(page -1,subject)
        return pages[page - 1]
    }
    if (targetIdx > 0) {
        subjectTabs[targetIdx - 1].click()
        const {page, pages, subject} = getQuestions()
        return pages[page]
    }
    return pages[page]
}

const navigateByQuestionNumber = (questionNumber) => {
    const activeSub = getItemFromSessionStorage("active_sub")
    const active_subData = getItemFromSessionStorage(activeSub["sub"])
    const pages = active_subData["pages"]
    for (let x = 0; x < pages.length; x++){
        let page = pages[x]
        for (let y = 0; y < page.length; y++){
            let questionObj = page[y]
            if (questionObj["passage"]){
                let questions = questionObj["questions"]
                for (let z = 0; z < questions.length; z++){
                    let question = questions[z]
                    if (question["number"] == questionNumber){
                        updateCurrentPage(x, activeSub["sub"])
                        return questionObj
                    } 
                }
            }
            if (questionObj["number"] == questionNumber){
                updateCurrentPage(x, activeSub["sub"])
                return questionObj  
            } 
        }
    }
}

const updateUserAnswers = (questionId, answer)=> {
    const answers = getItemFromSessionStorage("answers")
    answers[`questionId-${questionId}`] = answer
    saveToSessionStorage("answers", answers)
}   
const getUserAnswers = (questionId) => {
    const answers = getItemFromSessionStorage("answers")
    return answers[`questionId-${questionId}`]
}
const getAnsweredQuestionIds = () => {
    const answers = getItemFromSessionStorage("answers")
    const ids = []
    for (let [key,val] of Object.entries(answers)){
        ids.push(key.split('-')[1])
    }
    return ids
}


const buildNavigationCard = ()=>{
   
    const activeSub = getItemFromSessionStorage("active_sub")
   
    const active_subData = getItemFromSessionStorage(activeSub["sub"])
    
    const totalQuestions = active_subData["totalQuestions"]
    navigationPad.replaceChildren()
    let x = 0
    
    while (x < totalQuestions){
        const div = document.createElement('div')
        div.classList.add('Qc')
        div.textContent = `${x + 1}`
        navigationPad.append(div)
        x++;
    }
    const ids = getAnsweredQuestionIds()
    ids.forEach(id => {
        updateNavigationQuestionAnswered(id)
    })
}
const updateNavigationQuestionAnswered = (questionId)=> {
    const activeSub = getItemFromSessionStorage("active_sub")
    const active_subData = getItemFromSessionStorage(activeSub["sub"])
    const pages = active_subData["pages"]
    let boxToUpdate = null
    for (let x = 0; x < pages.length; x++){
        let page = pages[x]
        for (let y = 0; y < page.length; y++){
            let questionObj = page[y]
            if (questionObj["passage"]){
                let questions = questionObj["questions"]
                for (let z = 0; z < questions.length; z++){
                    let question = questions[z]
                    if (question["question_id"] == questionId){
                        boxToUpdate = question["number"]
                        break
                    } 
                }
            }
            if (questionObj["question_id"] == questionId){
                boxToUpdate = questionObj["number"]
                break
            } 
        }
        if (boxToUpdate) break;
    }
    navigationPad.childNodes.forEach(child => {
        if (child.textContent == boxToUpdate){
            child.classList.add('answered')
        }
    })

}

const activateSuccessButtonState = () => {
    const activeSub = getItemFromSessionStorage("active_sub")
    const active_subData = getItemFromSessionStorage(activeSub["sub"])
    let {questionsDone, totalQuestions } = active_subData
    questionsDone += 1
    active_subData["questionsDone"] = questionsDone
    if (questionsDone == totalQuestions) {
        let currTab = subjectTabs[activeSub["index"]]
        currTab.classList.remove('active__btn')
        currTab.classList.add('finished__btn')
    }
    const completedSubjects = Array.from(subjectTabs).reduce((acc, el)=>{
        if (el.classList.contains('finished__btn')){
            return acc + 1
        }
        return acc
    },0)
    
    if (completedSubjects === subjectTabs.length){
        const submitBtn = document.getElementById('submit-test_btn')
        submitBtn.disabled= false
        submitBtn.classList.toggle('disabled')
        submitBtn.classList.add('btn-primary')
    }
    saveToSessionStorage(activeSub["sub"], active_subData)
    
}

const renderQuestion = (questionObj) => {
    
    const questionPanel = document.getElementById("question-panel")
    questionPanel.replaceChildren()

    const buildQuestionCards = (qObj)=> {
       
        const card = document.createElement('div')
        card.classList.add("card")
        const h3 = document.createElement('h3')
        h3.textContent = `Question ${qObj["number"]}`
        card.append(h3)
        const cardContent = document.createElement('div')
        cardContent.classList.add('card-content')
        const questionParagraph = document.createElement('p')
        let quiz = qObj["question"]
        questionParagraph.textContent = quiz
        cardContent.append(questionParagraph)
                
        const choicesDiv = document.createElement('div')
        choicesDiv.classList.add("choices")
                
        const answers = qObj["answers"]
        const question_id = qObj["question_id"]
    
        let storedAnswerId = getUserAnswers(question_id)   
            
        answers.forEach(answer => {
            const checked = storedAnswerId == answer["answer_id"]
            choicesDiv.innerHTML += `<div class="choice-row">
                <input type="radio" name="answer_${question_id}" id="ans_${answer["answer_id"]}" value="${answer["answer_id"]}" ${checked ? 'checked': ''}>
                <label for="ans_${answer["answer_id"]}" >${answer["text"]}</label>
            </div>`
                    
        })
        choicesDiv.addEventListener('change', (e) => {
            const selectedAnswer = e.target.value
            const questionId = e.target.name.split('_')[1]
            updateUserAnswers(questionId, selectedAnswer)
            updateNavigationQuestionAnswered(questionId)
            activateSuccessButtonState()
                                
        })
        cardContent.append(choicesDiv)
        card.append(cardContent)
        questionPanel.append(card)
    }

    questionObj.forEach(qObj => {
        if (qObj["passage"] != null){
            const passage = document.createElement('p')
            passage.id="passage_text"
            passage.textContent = qObj["passage"]
            questionPanel.append(passage)
            const questions = qObj["questions"]
            questions.forEach(question => {
                buildQuestionCards(question)
                
            })
        }else {
            buildQuestionCards(qObj)
        }
    })   
}

function startCountdown(duration) {
    let timer = duration, hours, minutes, seconds;

    const countdownDisplay = document.getElementById("timer");
    const display = countdownDisplay.children[0]
    const modal = document.getElementById("modal")
    const intervalId = setInterval(() => {
        
        hours = Math.floor(timer / 3600);
        minutes = Math.floor((timer % 3600) / 60);
        seconds = timer % 60;
    
        if (hours == 0 && minutes <= 10 && countdownDisplay.classList.contains('on-time')){
            
            countdownDisplay.classList.remove('on-time')
            countdownDisplay.classList.add('time_danger')
        }
        // Format as hh:mm:ss
        display.textContent = 
            `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        
        if (--timer < 0) {
            clearInterval(intervalId);
            countdownDisplay.classList.remove('time_danger')
            modal.classList.toggle('hide-modal')
            display.textContent = "00:00:00";
        }
    }, 1000);
}


export const submitAnswers = () => {
    const submit = async() => {
        const testId = getItemFromSessionStorage("testId")
        const response = await submitTest(testId)
        console.log(response)
        if (response.status == 200){
            const data = response.data
            saveToSessionStorage("results", data["results"])
            saveToSessionStorage("results_questions", data["questions"])
            window.location.replace('/profilescreen.html')
        }
    }
    submitButton.addEventListener('click', async ()=> {
        await submit()
    })
    modalSubmitBtn.addEventListener('click', async() => {
        await submit()
    })
}

export const renderResults = () => {
    const performanceContainer = document.getElementById("perfomance-breakdown")

    const results = getItemFromSessionStorage("results")
    const qz = getItemFromSessionStorage("results_questions")
    console.log(qz)
    results.forEach(result => {
        const scoreWrapper = document.createElement('div')
        scoreWrapper.classList.add('subject__score_container')
        const subject = document.createElement('p')
        subject.textContent = titleCase(result["subject_name"])
        const score = document.createElement('p')

        let total= 0
        qz.forEach(q => {
            if (titleCase(q["subject_name"]) == titleCase(result["subject_name"])){
                total = q["data"].length
            }
        })
        score.textContent = `${result["score"]}/ ${total}`
        scoreWrapper.append(subject)
        scoreWrapper.append(score)
        performanceContainer.append(scoreWrapper)
    })
}

export const renderRevision = () => {
    const container = document.getElementById("revision")
    const resultsQuestions = getItemFromSessionStorage("results_questions")

    resultsQuestions.forEach(result => {
        const subjectDiv = document.createElement('div')
        const title = document.createElement('h3')
        title.textContent = result["subject_name"]
        subjectDiv.classList.add("subject-results")
        subjectDiv.append(title)
        
        const data = result["data"]
        data.forEach(dt => {
            const questions = dt["questions"]
            // let correctAnswer = null
            questions.forEach(question => {
                let correctAnswer = question["answers"].filter((ans) => ans["is_correct"] === true)
                console.log(correctAnswer[0])

                const quiz = document.createElement('p')
                const ansTxt = document.createElement('p')
                const exp = document.createElement('p')
                quiz.textContent = question["question"]
                ansTxt.textContent = correctAnswer[0]["text"]
                exp.textContent = question["explanation"]
                const qWrapper = document.createElement('div')
                const qTitle = document.createElement('p')
                const ansTitle = document.createElement('p')
                const expTitle = document.createElement('p')

                qTitle.textContent ="Question"
                ansTitle.textContent = "Correct Answer"
                expTitle.textContent = "Explanation"
                qWrapper.append(qTitle)
                qWrapper.append(quiz)
                qWrapper.append(ansTitle)
                qWrapper.append(ansTxt)
                qWrapper.append(expTitle)
                qWrapper.append(exp)
                subjectDiv.append(qWrapper)
            })
        })

        container.append(subjectDiv)
    })

}

