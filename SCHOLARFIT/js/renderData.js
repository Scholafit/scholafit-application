
import { generate_test, signUp, login, submitTest } from "./apiService.js"
import {saveToSessionStorage, getItemFromSessionStorage } from './utils.js'

const TOTAL_SUBJECTS = 4

const titleCase = (words) => {

    return words.split(' ').map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

export const submitRegistrationForm = () => {
    
    const registrationForm = document.getElementById('registration_form')
    if (registrationForm) {
        registrationForm.addEventListener('submit', async (evt) => {
    
            evt.preventDefault()
            const formData = new FormData(registrationForm)
            const data = {
                first_name: formData.get("firstname"),
                last_name: formData.get("lastname"),
                email: formData.get('Email'),
                password: formData.get('Password'),
                username: formData.get('Email')
            }
    
            const response = await signUp(data)
            console.log(response)
            if (response.error && response.status !== 201) {
                // show form errors
            }
            
            const respData = response["data"]
            const user = respData["new_user"]
            const profle = respData["new_profile"]
            const userId = user["id"]
            const profileId = profle["id"]
            saveToSessionStorage("user",{"userId": userId, "profileId": profileId})
            window.location.replace('/dashboard.html')
            

        })
    }
} 

export const submitLoginForm = () => {
    
    const loginForm = document.getElementById('login_form')
    if (loginForm) {
        loginForm.addEventListener('submit', async (evt) => {
    
            evt.preventDefault()
            const formData = new FormData(loginForm)
            const data = {
                
                identifier: formData.get('email'),
                password: formData.get('password'),
                username: formData.get('email')
            }
    
            const response = await login(data)
            console.log(response)
            if (response.error && response.status !== 201) {
                // show form errors
            }
            
            const respData = response["data"]
            const user = respData["user"]
            const profile = user["profile_data"]
            const userId = user["id"]
            const profileId = profile["id"]
            saveToSessionStorage("user",{"userId": userId, "profileId": profileId})
            window.location.replace('/dashboard.html')
            

        })
    }
} 


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
const submitButton = document.getElementById('submit__test_btn')
export const loadExam = async () => {
    const user = getItemFromSessionStorage("user")
    const profileId = user.profileId
    
    const respData = await generate_test(parseInt(profileId))
    const data = respData["data"]
    const testId = data["test_id"]
    saveToSessionStorage("testId", testId)
    saveToSessionStorage("answers", {})
    const exams = data["exam"]

    subjectTabs[0].textContent = "English"
    let x = 1
    exams.forEach((exam) =>{
        saveToSessionStorage(exam["subject_name"], exam)
        saveToSessionStorage(`${exam["subject_name"]}_current_q`, 0)
        
        if (exam["subject_name"] !== "english"){
            subjectTabs[x].textContent = titleCase(exam["subject_name"])
            x+= 1
        }   
        
    })

    subjectTabs.forEach((tab, idx) => {
        tab.addEventListener('click', (e) => {
            let subject = e.target.textContent
            saveToSessionStorage(`active_sub`, subject.toLowerCase())
            subjectTabs.forEach(tb => {
                tb.classList.remove('btn_nav__active') 
            })
            e.target.classList.add('btn_nav__active')
            getCurrentQuestion(subject.toLowerCase())
        })
        saveToSessionStorage(`${tab.textContent.toLowerCase()}_idx`, idx)
    })

    subjectTabs[0].click()
    // saveToSessionStorage(`${subjectTabs[0].textContent.toLowerCase()}_current_q`, 1)
    nextButton.addEventListener('click', (e) => {
        
        let subject = getItemFromSessionStorage(`active_sub`)
        getCurrentQuestion(subject, true, false)
        
    })

    prevButton.addEventListener('click', (e) =>{
        
        let subject = getItemFromSessionStorage(`active_sub`)
        getCurrentQuestion(subject, false, true)
        if (!nextButton.firstChild.classList.contains('Sc__active')){
            nextButton.firstChild.classList.add('Sc__active')
        }
    })

}

const getNextQuestion = (subjectName, questions) => {
    let currentQuestion = getItemFromSessionStorage(`${subjectName}_current_q`)
    let currSubjectIdx = getItemFromSessionStorage(`${subjectName}_idx`)
    if (currentQuestion < questions.length - 1){
        currentQuestion++;
        saveToSessionStorage(`${subjectName}_current_q`, currentQuestion)
        return {"question": questions[currentQuestion], "order": currentQuestion, "subject": subjectName}
    } 
    if (currentQuestion === questions.length - 1 && currSubjectIdx != TOTAL_SUBJECTS - 1){
        subjectTabs[currSubjectIdx +1].click()
        let nextSub = subjectTabs[currSubjectIdx + 1].textContent.toLowerCase()
        let nextSubCurrQuestion = getItemFromSessionStorage(`${nextSub}_current_q`)
        return {"question": null, "order": nextSubCurrQuestion, "subject": nextSub}
    }

    let complete = currSubjectIdx === TOTAL_SUBJECTS - 1 ? true: false
    return {"question": null, "order": null, "subject": null, "complete": complete}
}

const getPrevQuestion = (subjectName, questions) => {
    let currentQuestion = getItemFromSessionStorage(`${subjectName}_current_q`)
    let currSubjectIdx = getItemFromSessionStorage(`${subjectName}_idx`)
    if (currentQuestion > 0){

        currentQuestion--;
        saveToSessionStorage(`${subjectName}_current_q`, currentQuestion)
        return {"question": questions[currentQuestion], "order": currentQuestion, "subject": subjectName}
    }
   
    if (currentQuestion === 0 && currSubjectIdx != 0) {
        subjectTabs[currSubjectIdx - 1].click()
        let prevSub = subjectTabs[currSubjectIdx - 1].textContent.toLowerCase()
        let prevSubCurrQuestion = getItemFromSessionStorage(`${prevSub}_current_q`)
        return {"question": null, "order": prevSubCurrQuestion, "subject": prevSub}   
    }
    let start = currSubjectIdx === 0? true: false
    return {"question": null, "order": null, "subject": null, "start": start}
}

const getCurrentQuestion = (subjectName, next=false, prev=false) => {
    // get exam get current question
    
    let exam = getItemFromSessionStorage(subjectName)
    let questions = exam["data"]
    let currentQuestion = getItemFromSessionStorage(`${subjectName}_current_q`)
    if (next) {
        prevButton.firstChild.classList.add('Sc__active')
        const nextQuestionData = getNextQuestion(subjectName, questions)
        const question = nextQuestionData["question"]
        const order = nextQuestionData["order"]
        const sub = nextQuestionData["subject"]
        if (question && order){
            renderQuestion(question, order)
            return
    
        } else if (order && !question){
            console.log(nextQuestionData)
            exam = getItemFromSessionStorage(sub)
            questions = exam["data"]
            renderQuestion(questions[order], order)
            return
        }
        if (nextQuestionData["complete"]){
            alert("Congratulations You have completed the examination.\n Click Submit to submit your answer.")
            nextButton.firstChild.classList.remove('Sc__active')
            submitButton.style.visibility = 'visible'

        }
        return
    }
    if (prev) {
        const prevQuestionData = getPrevQuestion(subjectName, questions)
        const question = prevQuestionData["question"]
        const order = prevQuestionData["order"]
        const sub = prevQuestionData["subject"]
        if (question && order){
            renderQuestion(question, order)
            return
    
        } else if (order && !question){
            exam = getItemFromSessionStorage(sub)
            questions = exam["data"]
            renderQuestion(questions[order], order)
            return
        }
        if (prevQuestionData["start"]){
            prevButton.firstChild.classList.remove('Sc__active')
            console.log('we are at the start')

        }
        return
    }

    renderQuestion(questions[currentQuestion], currentQuestion)
}


const renderQuestion = (questionObj, order) => {
    const flashCard = document.getElementById("flash_card")
    flashCard.innerHTML = ''
    if (questionObj["passage"] != null){
        const passage = document.createElement('p')
        passage.id="passage_text"
        passage.textContent = questionObj["passage"]
        flashCard.append(passage)
    }

    const questions = questionObj["questions"]
    
    let num = order + 1
    questions.forEach(question => {
        const qnaDiv = document.createElement('div')
        const choicesDiv = document.createElement('div')
        qnaDiv.classList.add("q_n_a")
        choicesDiv.classList.add("choices")
        let quiz = question["question"]
        qnaDiv.innerHTML = `<p><span>${num}.</span>${quiz}</p>`
        
        const answers = question["answers"]
        const question_id = question["question_id"]
        const storedAnswers = getItemFromSessionStorage("answers")
        answers.forEach(answer => {
            let val = storedAnswers[`qnID_${question_id}`] 
            const isChecked = val == answer["answer_id"] ? true : false
            
            choicesDiv.innerHTML += `<div>
                  <input type="radio" name="answer_${question_id}" id="ans_${answer["answer_id"]}" value="${answer["answer_id"]}" ${isChecked ? "checked": ""}>
                  <label for="ans_${answer["answer_id"]}" >${answer["text"]}</label>
                </div>`
            
        })
        choicesDiv.addEventListener('change', (e) => {
            const selectedAnswer = e.target.value
            const questionId = e.target.name.split('_')[1]
            
            storedAnswers[`qnID_${questionId}`] = selectedAnswer
            saveToSessionStorage("answers", storedAnswers)
            const updates = getItemFromSessionStorage("answers")
        
        })
        qnaDiv.append(choicesDiv)
        flashCard.append(qnaDiv)
        num++;
    })
}



export const submitAnswers = () => {
    submitButton.addEventListener('click', async ()=> {
        const testId = getItemFromSessionStorage("testId")
        const response = await submitTest(testId)
        if (response.status == 200){
            const data = response.data
            saveToSessionStorage("results", data["results"])
            saveToSessionStorage("results_questions", data["questions"])
            window.location.replace('/profilescreen.html')
        }
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

