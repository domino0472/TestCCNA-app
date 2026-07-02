let allQuestions = [];
let currentQuestion = null;
let currentIndexInAll = 0;
let showOnlyImages = false;
let userStats = {};
let answered = false;

async function fetchQuestions() {
    try {
        const savedStats = localStorage.getItem('ccna_quiz_stats');
        if (savedStats) {
            userStats = JSON.parse(savedStats);
        }

        const response = await fetch('baza_pytan.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        allQuestions = data.filter(q => 
            (q.options && q.options.length > 0) || q.type === 'match'
        );
        
        if (allQuestions.length > 0) {
            renderNavigation();
            loadQuestion(0);
        } else {
            const container = document.getElementById('quiz-container');
            container.innerHTML = '';
            const msg = document.createElement('div');
            msg.className = 'loading';
            msg.innerText = 'No valid questions found.';
            container.appendChild(msg);
        }
    } catch (error) {
        console.error("Failed to load questions", error);
        const container = document.getElementById('quiz-container');
        container.innerHTML = '';
        const msg = document.createElement('div');
        msg.className = 'loading';
        msg.style.color = '#ef4444';
        msg.innerText = 'Error loading questions.';
        container.appendChild(msg);
    }
}

function toggleFilter() {
    showOnlyImages = !showOnlyImages;
    const btn = document.getElementById('filter-btn');
    if (showOnlyImages) {
        btn.classList.add('active');
        btn.innerText = 'Pokaż wszystkie pytania';
    } else {
        btn.classList.remove('active');
        btn.innerText = 'Pokaż tylko pytania z obrazkami';
    }
    renderNavigation();
    
    if (showOnlyImages && currentQuestion && !currentQuestion.image) {
        const firstImgQ = allQuestions.findIndex(q => !!q.image);
        if (firstImgQ !== -1) {
            loadQuestion(firstImgQ);
        }
    }
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

function closeSidebarOnMobile() {
    if (window.innerWidth <= 1024) {
        document.getElementById('sidebar').classList.remove('open');
    }
}

function renderNavigation() {
    const navList = document.getElementById('nav-list');
    navList.innerHTML = '';

    allQuestions.forEach((q, i) => {
        const hasImg = !!q.image;

        if (showOnlyImages && !hasImg) {
            return;
        }

        const item = document.createElement('div');
        item.className = `nav-item ${i === currentIndexInAll ? 'active' : ''}`;
        
        item.innerText = `Pytanie ${q.id}`;

        if (hasImg) {
            const indicator = document.createElement('div');
            indicator.className = 'image-indicator';
            indicator.title = 'Zawiera obrazek';
            item.appendChild(indicator);
        }

        item.addEventListener('click', () => loadQuestion(i));
        navList.appendChild(item);
    });
}

function loadQuestion(index) {
    if (index < 0 || index >= allQuestions.length) return;
    
    currentIndexInAll = index;
    currentQuestion = allQuestions[index];
    answered = false;
    
    renderNavigation();
    closeSidebarOnMobile();
    
    buildQuestionHTML(currentQuestion);
}

function getRobustImagePath(imgPath) {
    if (!imgPath) return null;
    if (imgPath.startsWith('assets/')) return imgPath;
    return `assets/${imgPath}`;
}

function buildQuestionHTML(q) {
    const container = document.getElementById('quiz-container');
    container.innerHTML = '';
    
    const progress = ((currentIndexInAll + 1) / allQuestions.length) * 100;
    const imageSrc = getRobustImagePath(q.image);
    
    const card = document.createElement('div');
    card.className = 'quiz-card';
    card.id = 'quiz-card';
    
    // Progress bar
    const progBar = document.createElement('div');
    progBar.className = 'progress-bar';
    progBar.style.width = `${progress}%`;
    card.appendChild(progBar);
    
    // Image
    if (imageSrc) {
        const img = document.createElement('img');
        img.src = imageSrc;
        img.alt = 'Exhibit';
        img.className = 'exhibit-image';
        card.appendChild(img);
        
        const reportBtn = document.createElement('button');
        reportBtn.className = 'btn';
        reportBtn.style.background = '#6b7280';
        reportBtn.style.marginBottom = '1.5rem';
        reportBtn.style.display = 'block';
        reportBtn.innerText = 'Zgłoś błędny schemat';
        reportBtn.addEventListener('click', async () => {
            if(confirm('Na pewno usunąć ten obrazek? Zostanie odpięty od tego pytania w bazie.')) {
                try {
                    const res = await fetch('/api/remove_image', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ id: q.id })
                    });
                    if (res.ok) {
                        q.image = null;
                        img.remove();
                        reportBtn.remove();
                    } else {
                        alert('Błąd podczas usuwania. Czy uruchomiłeś server.py zamiast domyślnego serwera Pythona?');
                    }
                } catch(e) {
                    alert('Nie udało się połączyć z API. Uruchom "python3 server.py" zamiast "python3 -m http.server".');
                }
            }
        });
        card.appendChild(reportBtn);
    }
    
    // Question text
    const qText = document.createElement('div');
    qText.className = 'question-text';
    qText.innerText = q.question;
    card.appendChild(qText);
    
    // Interactable Section
    if (q.type === 'match') {
        const matchMsg = document.createElement('div');
        matchMsg.style.padding = '1rem';
        matchMsg.style.background = 'rgba(59, 130, 246, 0.1)';
        matchMsg.style.border = '1px solid var(--accent-color)';
        matchMsg.style.borderRadius = '0.5rem';
        matchMsg.style.textAlign = 'center';
        matchMsg.style.marginTop = '1.5rem';
        matchMsg.style.color = 'var(--text-primary)';
        matchMsg.innerText = 'Ten typ pytania wymaga ręcznego dopasowania - sprawdź PDF';
        card.appendChild(matchMsg);
        
    } else {
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'options';
        optionsDiv.id = 'options';
        
        const validOptions = (q.options || []).filter(o => o.text.trim() !== '');
        const isMultiple = (q.type === 'multiple');
        
        validOptions.forEach(optData => {
            const optDiv = document.createElement('div');
            optDiv.className = 'option';
            optDiv.setAttribute('data-text', optData.text);
            optDiv.setAttribute('data-correct', optData.is_correct);
            
            if (isMultiple) {
                const cb = document.createElement('input');
                cb.type = 'checkbox';
                cb.style.marginRight = '1rem';
                cb.style.pointerEvents = 'none';
                cb.className = 'multi-checkbox';
                optDiv.appendChild(cb);
                
                const textSpan = document.createElement('span');
                textSpan.innerText = optData.text;
                optDiv.appendChild(textSpan);
                
                optDiv.addEventListener('click', () => toggleMultipleOption(optDiv));
            } else {
                optDiv.addEventListener('click', () => selectOption(optDiv));
                optDiv.innerText = optData.text;
            }
            
            optionsDiv.appendChild(optDiv);
        });
        card.appendChild(optionsDiv);
    }
    
    // Explanation
    const expCard = document.createElement('div');
    expCard.className = 'explanation-card';
    expCard.id = 'explanation';
    
    const expTitle = document.createElement('h3');
    expTitle.innerText = 'Explanation';
    expCard.appendChild(expTitle);
    
    const expText = document.createElement('div');
    expText.className = 'explanation-text';
    expText.innerText = q.explanation || 'No explanation available.';
    
    if (q.type === 'match' && q.correct_mapping) {
        const table = document.createElement('table');
        table.style.width = '100%';
        table.style.marginTop = '1rem';
        table.style.borderCollapse = 'collapse';
        
        for (const [left, right] of Object.entries(q.correct_mapping)) {
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid #374151';
            
            const td1 = document.createElement('td');
            td1.style.padding = '0.5rem';
            td1.innerText = left;
            
            const td2 = document.createElement('td');
            td2.style.padding = '0.5rem';
            td2.style.color = '#34d399';
            td2.innerText = right;
            
            row.appendChild(td1);
            row.appendChild(td2);
            table.appendChild(row);
        }
        expText.appendChild(table);
    }
    
    expCard.appendChild(expText);
    
    card.appendChild(expCard);
    
    // Controls
    const controls = document.createElement('div');
    controls.className = 'controls';
    
    const statsSpan = document.createElement('span');
    statsSpan.className = 'stats';
    let statusStr = '';
    if (userStats[q.id]) {
        statusStr = ` - ${userStats[q.id] === 'known' ? 'Znane' : 'Do powtórki'}`;
    }
    statsSpan.innerText = `Question ${currentIndexInAll + 1} of ${allQuestions.length}${statusStr}`;
    controls.appendChild(statsSpan);
    
    const actionsFlex = document.createElement('div');
    actionsFlex.style.display = 'flex';
    actionsFlex.style.gap = '1rem';
    
    if (q.type === 'match') {
        const showBtn = document.createElement('button');
        showBtn.className = 'btn';
        showBtn.id = 'check-btn';
        showBtn.innerText = 'Pokaż odpowiedź';
        showBtn.addEventListener('click', showFeedbackAndExplanation);
        actionsFlex.appendChild(showBtn);
    } else if (q.type === 'multiple') {
        const checkBtn = document.createElement('button');
        checkBtn.className = 'btn';
        checkBtn.id = 'check-btn';
        checkBtn.innerText = 'Sprawdź';
        checkBtn.disabled = true;
        checkBtn.addEventListener('click', checkMultiple);
        actionsFlex.appendChild(checkBtn);
    }
    
    const fbDiv = document.createElement('div');
    fbDiv.className = 'feedback-buttons';
    fbDiv.id = 'feedback-buttons';
    
    const btnKnown = document.createElement('button');
    btnKnown.className = 'btn btn-success';
    btnKnown.innerText = 'Wiem';
    btnKnown.addEventListener('click', () => recordStat('known'));
    
    const btnRepeat = document.createElement('button');
    btnRepeat.className = 'btn btn-danger';
    btnRepeat.innerText = 'Muszę powtórzyć';
    btnRepeat.addEventListener('click', () => recordStat('repeat'));
    
    fbDiv.appendChild(btnKnown);
    fbDiv.appendChild(btnRepeat);
    actionsFlex.appendChild(fbDiv);
    
    controls.appendChild(actionsFlex);
    card.appendChild(controls);
    
    container.appendChild(card);
}

function showFeedbackAndExplanation() {
    document.getElementById('explanation').classList.add('show');
    const checkBtn = document.getElementById('check-btn');
    if (checkBtn) checkBtn.style.display = 'none';
    document.getElementById('feedback-buttons').style.display = 'flex';
}

function recordStat(status) {
    userStats[currentQuestion.id] = status;
    localStorage.setItem('ccna_quiz_stats', JSON.stringify(userStats));
    
    let nextIndex = currentIndexInAll + 1;
    if (showOnlyImages) {
        const nextImgIndex = allQuestions.findIndex((q, i) => i >= nextIndex && !!q.image);
        nextIndex = nextImgIndex !== -1 ? nextImgIndex : allQuestions.length;
    }
    
    if (nextIndex < allQuestions.length) {
        loadQuestion(nextIndex);
    } else {
        const container = document.getElementById('quiz-container');
        container.innerHTML = '';
        
        const card = document.createElement('div');
        card.className = 'quiz-card';
        card.style.textAlign = 'center';
        
        const h2 = document.createElement('h2');
        h2.style.color = '#34d399';
        h2.innerText = 'Koniec pytań!';
        
        const p = document.createElement('p');
        p.innerText = 'Osiągnięto koniec dostępnej listy.';
        
        card.appendChild(h2);
        card.appendChild(p);
        container.appendChild(card);
    }
}

function selectOption(element) {
    if (answered) return;
    
    answered = true;
    const isCorrect = element.getAttribute('data-correct') === 'true';
    
    if (isCorrect) {
        element.classList.add('selected', 'correct');
    } else {
        element.classList.add('selected', 'wrong');
        const allOpts = document.querySelectorAll('.option');
        allOpts.forEach(opt => {
            if (opt.getAttribute('data-correct') === 'true') {
                opt.classList.add('correct');
            }
        });
    }
    showFeedbackAndExplanation();
}



function toggleMultipleOption(element) {
    if (answered) return;
    const cb = element.querySelector('.multi-checkbox');
    if (!cb) return;

    if (element.classList.contains('selected')) {
        element.classList.remove('selected');
        cb.checked = false;
    } else {
        element.classList.add('selected');
        cb.checked = true;
    }
    
    const selectedCount = document.querySelectorAll('.option.selected').length;
    const checkBtn = document.getElementById('check-btn');
    if (checkBtn) {
        checkBtn.disabled = (selectedCount !== currentQuestion.maxSelections);
    }
}

function checkMultiple() {
    if (answered) return;
    answered = true;
    
    const allOpts = document.querySelectorAll('.option');
    const correctArray = currentQuestion.correct || [];
    
    allOpts.forEach(opt => {
        const isSelected = opt.classList.contains('selected');
        const optText = opt.getAttribute('data-text');
        const isActuallyCorrect = correctArray.includes(optText);
        
        const cb = opt.querySelector('.multi-checkbox');
        if (cb) cb.disabled = true;

        if (isSelected && isActuallyCorrect) {
            opt.classList.add('correct');
        } else if (isSelected && !isActuallyCorrect) {
            opt.classList.add('wrong');
        } else if (!isSelected && isActuallyCorrect) {
            opt.classList.add('correct');
        }
    });
    
    showFeedbackAndExplanation();
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('mobile-menu-btn').addEventListener('click', toggleSidebar);
    document.getElementById('filter-btn').addEventListener('click', toggleFilter);
    document.getElementById('main-content').addEventListener('click', closeSidebarOnMobile);
    fetchQuestions();
});
