function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const akinatorImages = [
    '../../../media/happy.png',
    '../../../media/frowning.png',
    '../../../media/neutral.png'
];

let currentImageIndex = 0;

const csrftoken = getCookie('csrftoken');

let btn = document.getElementById('start-button');

function displayEnd(begin_year) {
    displayQuestion({
            stage: 'end-year',
            begin_year: begin_year
        }, displayLocation);
}

function displayQuestion(jsonData, listenerFunction) {
    const request = new Request ('/game/', {
        method: "POST",
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        body: JSON.stringify(
            jsonData
        ),
    });
    fetch(request).then((response) => {
        response.json().then((data) => {
            let question = document.getElementById('question');
            let ak_image = document.getElementById('ak-image');
            ak_image.src = akinatorImages[currentImageIndex];
            currentImageIndex = (currentImageIndex + 1) % akinatorImages.length;
            question.innerHTML = data.question;
            document.getElementById('choices').innerHTML = ''
            for (const choice of data.choices){
                let div = document.createElement('div');
                let label = document.createElement('label');
                let input = document.createElement('input');
                input.setAttribute('id', choice);
                input.setAttribute('type', 'radio');
                input.addEventListener('click', () => {listenerFunction(choice);});
                label.setAttribute('for', choice);
                label.innerHTML = choice;
                div.appendChild(input);
                div.appendChild(label);
                document.getElementById('choices').appendChild(div);
            }
        })
    })
}

function displayLocation(end_year) {
    displayQuestion({
            stage: 'location',
            end_year: end_year
        }, displayUssrGeneral);
}

function displayUssrGeneral(location) {
    displayQuestion({
            stage: 'ussr-general',
            location: location
        }, displayGermGeneral);
}

function displayGermGeneral(ussr_glavkom) {
    displayQuestion({
            stage: 'germ-general',
            ussr_glavkom: ussr_glavkom
        }, displayResult);
}

function displayResult(germ_glavkom) {
    const request = new Request ('/game/', {
        method: "POST",
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        body: JSON.stringify(
            {
                stage: 'result',
                germ_glavkom: germ_glavkom
            }
        )
    });
    fetch(request).then((response) => {
        response.json().then((data) => {
            let description = document.createElement('div');
            description.innerHTML = 'Hello world!';
            let question = document.getElementById('question');
            question.appendChild(description);
            question.innerHTML = data.question;
            document.getElementById('choices').innerHTML = '';
            document.getElementById('play-again').style.display = 'block';
        })
    });
}


btn.addEventListener('click', ()=>{
    document.getElementById('intro').style.display='none';
    document.getElementById('akinator-img-wrapper').style.display = 'block';
    displayQuestion({stage: 'begin-year'}, displayEnd);
});

