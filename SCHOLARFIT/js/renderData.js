
import { generate_test, signUp, login } from "./apiService.js"
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
export const loadExam = async () => {

   
    const user = getItemFromSessionStorage("user")
    const profileId = user.profileId
    
    const respData = await generate_test(parseInt(profileId))
    const data = respData["data"]
    const testId = data["test_id"]
    saveToSessionStorage("testId", testId)
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

    nextButton.addEventListener('click', (e) => {
        
        let subject = getItemFromSessionStorage(`active_sub`)
        getCurrentQuestion(subject, true)
        
    })

}

const getCurrentQuestion = (subjectName, next=false) => {
    // get exam get current question
    
    let exam = getItemFromSessionStorage(subjectName)
    let currentQuestion = getItemFromSessionStorage(`${subjectName}_current_q`)
    let questions = exam["data"]
    if (next){
        currentQuestion++;
        saveToSessionStorage(`${subjectName}_current_q`, currentQuestion)
    }
    
    if (!questions[currentQuestion]){
        const currSubjectIdx = getItemFromSessionStorage(`${subjectName}_idx`)
        if (currSubjectIdx + 1 === TOTAL_SUBJECTS){
            nextButton.firstChild.textContent='Submit'
            return
        }
        subjectTabs[currSubjectIdx +1].click()
        subjectName = subjectTabs[currSubjectIdx +1].textContent.toLowerCase()
        exam = getItemFromSessionStorage(subjectName)
        currentQuestion = getItemFromSessionStorage(`${subjectName}_current_q`)
        questions = exam["data"]
        renderQuestion(questions[currentQuestion], currentQuestion)
        return

    }
    renderQuestion(questions[currentQuestion], currentQuestion)
    
}



const submitAnswer = () => {

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
        answers.forEach(answer => {
            
            choicesDiv.innerHTML += `<div>
                  <input type="radio" name="answer_${question["question_id"]}" id="ans_${answer["answer_id"]}">
                  <label for="ans_${answer["answer_id"]}" >${answer["text"]}</label>
                </div>`
            
        })
        choicesDiv.addEventListener('change', (e) => {
            // create answer obj here
        })
        qnaDiv.append(choicesDiv)
        flashCard.append(qnaDiv)
        num++;
    })


}
export const loadSubjectTest = (question_order=0) => {
    console.log('load')
    const subjectTab = document.getElementById("subject_tabs")
    const flashCard = document.getElementById("flash_card")

    subjectTab.addEventListener('click', (evt) =>{
        const subject = evt.target.textContent.toLowerCase()
        const testExam = getItemFromSessionStorage(subject)
        const questions = testExam["data"]
        console.log(questions)
        if (subject === "english"){
            questions.forEach(question => {
                if (question["passage"]){
                    const para = document.createElement('p')
                    para.textContent= question["passage"]
                    flashCard.append(para)
                    question["questions"].forEach(q => {
                        const p = document.createElement('p').textContent = q["question"]
                        flashCard.append(p)
                        q["answers"].forEach(ans => {
                            const an = document.createElement('p').textContent = ans["text"]
                            flashCard.append(an)
                        })
                    })
                } else {
                    question["questions"].forEach(q => {
                        const p = document.createElement('p').textContent = q["question"]
                        flashCard.append(p)
                        q["answers"].forEach(ans => {
                            const an = document.createElement('p').textContent = ans["text"]
                            flashCard.append(an)
                        })
                    })
                }
            })
            return
        }
        questions.forEach(question => {
            console.log(question)
        })
    })
}

