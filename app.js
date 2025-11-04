/* Tega — simple SPA logic */
(function(){
  const body = document.body;

  const screens = {
    landing: document.getElementById('screen-landing'),
    signup: document.getElementById('screen-signup'),
    quiz: document.getElementById('screen-quiz')
  };

  let selectedRole = null;

  // Navigation helper
  function showScreen(name){
    for(const key of Object.keys(screens)){
      const el = screens[key];
      const active = key === name;
      el.hidden = !active;
      el.classList.toggle('active', active);
    }
    // Theme switch by screen
    if(name === 'quiz') body.className = 'theme-lavender';
    else body.className = 'theme-peach';
  }

  // Landing role buttons
  document.querySelectorAll('.role-card').forEach(btn => {
    btn.addEventListener('click', () => {
      selectedRole = btn.dataset.role;
      showScreen('signup');
      document.getElementById('name').focus();
    });
  });

  // Sign in link simply returns to signup for demo
  document.getElementById('link-signin').addEventListener('click', (e)=>{
    e.preventDefault();
    showScreen('signup');
  });

  // Simple form validation and proceed to quiz
  const signupForm = document.getElementById('signup-form');
  signupForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const password = document.getElementById('password');

    let ok = true;
    // reset errors
    ['name-error','email-error','password-error'].forEach(id=>{document.getElementById(id).textContent=''});

    if(!name.value.trim()){
      document.getElementById('name-error').textContent = 'Please enter a name.';
      ok = false;
    }
    if(email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)){
      document.getElementById('email-error').textContent = 'Please enter a valid email.';
      ok = false;
    }
    if(password.value.length < 6){
      document.getElementById('password-error').textContent = 'Use at least 6 characters.';
      ok = false;
    }

    if(!ok) return;

    // Store a tiny bit for personalization (in-memory for demo)
    window.__tegaUser = { name: name.value.trim(), role: selectedRole || 'student' };
    startQuiz();
  });

  // Quiz data
  const questions = [
    { text: 'I find it easier to learn with pictures and videos' },
    { text: 'Short practice sessions work better for me than long ones' },
    { text: 'I like step-by-step guidance when learning something new' },
    { text: 'I prefer learning at my own pace with personalized tips' }
  ];
  const choices = ['Strongly Agree','Agree','Neutral','Disagree'];
  const answers = new Array(questions.length).fill(null);

  let qIndex = 0;

  const qText = document.getElementById('question-text');
  const optionsEl = document.getElementById('options');
  const progressBar = document.getElementById('progress-bar');
  const progressLabel = document.getElementById('progress-label');
  const btnBack = document.getElementById('btn-back');
  const btnNext = document.getElementById('btn-next');

  function startQuiz(){
    qIndex = 0;
    showScreen('quiz');
    renderQuestion();
  }

  function renderQuestion(){
    const total = questions.length;
    const num = qIndex + 1;
    const pct = Math.round(((qIndex) / total) * 100);
    progressBar.style.width = `${pct}%`;
    progressLabel.textContent = `Question ${num} of ${total}`;

    qText.textContent = questions[qIndex].text;
    optionsEl.innerHTML = '';

    choices.forEach((label, i) => {
      const id = `opt-${qIndex}-${i}`;
      const opt = document.createElement('button');
      opt.type = 'button';
      opt.className = 'option';
      opt.setAttribute('role','radio');
      opt.setAttribute('aria-checked','false');
      opt.setAttribute('id', id);

      opt.innerHTML = `<span class="dot"><input aria-hidden="true"></span><span class="text">${label}</span>`;

      opt.addEventListener('click', () => selectOption(i));
      opt.addEventListener('keydown', (ev)=>{
        // keyboard support for arrow keys
        if(ev.key === 'ArrowRight' || ev.key === 'ArrowDown'){ ev.preventDefault(); selectOption(Math.min(i+1, choices.length-1)); }
        if(ev.key === 'ArrowLeft' || ev.key === 'ArrowUp'){ ev.preventDefault(); selectOption(Math.max(i-1, 0)); }
        if(ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); selectOption(i); }
      });

      optionsEl.appendChild(opt);
    });

    // restore previous selection if exists
    if(answers[qIndex] != null){
      selectOption(answers[qIndex], false);
    } else {
      setSelected(null);
      btnNext.disabled = true;
    }

    btnBack.disabled = qIndex === 0;
    btnNext.textContent = (qIndex === questions.length - 1) ? 'Finish' : 'Next';
  }

  function setSelected(idx){
    document.querySelectorAll('.option').forEach((el, i) => {
      const on = idx === i;
      el.classList.toggle('selected', on);
      el.setAttribute('aria-checked', on ? 'true' : 'false');
    });
  }

  function selectOption(choiceIndex, enableNext = true){
    answers[qIndex] = choiceIndex;
    setSelected(choiceIndex);
    if(enableNext) btnNext.disabled = false;
  }

  btnBack.addEventListener('click', ()=>{
    if(qIndex > 0){ qIndex--; renderQuestion(); }
  });
  btnNext.addEventListener('click', ()=>{
    if(answers[qIndex] == null){ btnNext.disabled = true; return; }
    if(qIndex < questions.length - 1){
      qIndex++;
      renderQuestion();
    } else {
      // finished — simple demo finish screen
      finish();
    }
  });

  function finish(){
    // Simple friendly completion
    screens.quiz.querySelector('.container').innerHTML = `
      <div class="logo-badge">🦉</div>
      <h2 class="headline">Thanks ${window.__tegaUser?.name || ''}!</h2>
      <p class="subhead">You're all set. Tega will personalize your experience based on your answers.</p>
      <div class="question-card" style="max-width:700px">
        <h3 style="margin-top:0">Your preferences</h3>
        <ul style="text-align:left;line-height:1.9;margin:0 auto;max-width:560px">
          ${questions.map((q,i)=>`<li><strong>${q.text}</strong><br/><span style="color:#5f6472">${choices[answers[i]]}</span></li>`).join('')}
        </ul>
      </div>
      <div class="actions"><button class="btn btn-primary" id="btn-restart">Return Home</button></div>
    `;
    body.className = 'theme-lavender';
    const restart = document.getElementById('btn-restart');
    restart?.addEventListener('click', ()=>{ location.reload(); });
  }
})();
