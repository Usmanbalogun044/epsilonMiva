/* Tega — simple SPA logic */
(function(){
  const body = document.body;

  const screens = {
    landing: document.getElementById('screen-landing'),
    signup: document.getElementById('screen-signup'),
    quiz: document.getElementById('screen-quiz')
  };

  // Helpers
  function qs(q){ return document.querySelector(q); }
  function qsa(q){ return Array.from(document.querySelectorAll(q)); }
  function getQueryParam(key){ return new URLSearchParams(location.search).get(key); }

  let selectedRole = null;

  // Navigation helper (only toggles existing screens)
  function showScreen(name){
    Object.keys(screens).forEach(key => {
      const el = screens[key];
      if(!el) return;
      const active = key === name;
      el.hidden = !active;
      el.classList.toggle('active', active);
    });
    // Theme switch by screen
    if(name === 'quiz') body.className = 'theme-lavender';
    else body.className = 'theme-peach';
  }

  // Landing role buttons -> navigate to dedicated signup page
  if (screens.landing) {
    qsa('.role-card').forEach(btn => {
      btn.addEventListener('click', () => {
        const role = btn.dataset.role || 'student';
        location.href = `signup.html?role=${encodeURIComponent(role)}`;
      });
    });
  }

  // Signup page wiring
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    selectedRole = getQueryParam('role') || 'student';
    const signinLink = document.getElementById('link-signin');
    if (signinLink) {
      signinLink.addEventListener('click', (e)=>{
        // demo "sign in" just jumps to quiz
        e.preventDefault();
        location.href = 'path.html';
      });
    }

    signupForm.addEventListener('submit', (e)=>{
      e.preventDefault();
      const name = document.getElementById('name');
      const email = document.getElementById('email');
      const password = document.getElementById('password');

      let ok = true;
      ['name-error','email-error','password-error'].forEach(id=>{ const el = document.getElementById(id); if(el) el.textContent=''; });

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

      // Persist minimal info and go to path.html
      const user = { name: name.value.trim(), role: selectedRole };
      try { sessionStorage.setItem('tegaUser', JSON.stringify(user)); } catch {}
      location.href = 'path.html';
    });
  }

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
    if(!screens.quiz) return; // Not on a page with quiz
    qIndex = 0;
    showScreen('quiz');
    renderQuestion();
  }

  function renderQuestion(){
    const total = questions.length;
    const num = qIndex + 1;
    const pct = Math.round(((qIndex) / total) * 100);
  if(progressBar) progressBar.style.width = `${pct}%`;
  if(progressLabel) progressLabel.textContent = `Question ${num} of ${total}`;

  if(qText) qText.textContent = questions[qIndex].text;
  if(optionsEl) optionsEl.innerHTML = '';

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

      optionsEl && optionsEl.appendChild(opt);
    });

    // restore previous selection if exists
    if(answers[qIndex] != null){
      selectOption(answers[qIndex], false);
    } else {
      setSelected(null);
      btnNext.disabled = true;
    }

    if(btnBack) btnBack.disabled = qIndex === 0;
    if(btnNext) btnNext.textContent = (qIndex === questions.length - 1) ? 'Finish' : 'Next';
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
    if(enableNext && btnNext) btnNext.disabled = false;
  }

  if(btnBack){
    btnBack.addEventListener('click', ()=>{
      if(qIndex > 0){ qIndex--; renderQuestion(); }
    });
  }
  if(btnNext){
    btnNext.addEventListener('click', ()=>{
      if(answers[qIndex] == null){ if(btnNext) btnNext.disabled = true; return; }
      if(qIndex < questions.length - 1){
        qIndex++;
        renderQuestion();
      } else {
        finish();
      }
    });
  }

  function finish(){
    // Navigate to results page
    location.href = 'results.html';
  }

  // If index.html loaded with #quiz, start the quiz (legacy support)
  // Or if path.html is loaded, auto-start quiz
  if ((location.hash === '#quiz' || location.pathname.includes('path.html')) && screens.quiz) {
    try { const u = sessionStorage.getItem('tegaUser'); if(u) window.__tegaUser = JSON.parse(u); } catch {}
    startQuiz();
  }

  // Results page handlers
  const startJourneyBtn = document.querySelector('.start-journey-btn');
  const adjustPrefsBtn = document.querySelector('.adjust-prefs-btn');
  const closeBtn = document.querySelector('.close-btn');

  if (startJourneyBtn) {
    startJourneyBtn.addEventListener('click', () => {
      // Navigate to student dashboard
      location.href = 'dashboard.html';
    });
  }

  if (adjustPrefsBtn) {
    adjustPrefsBtn.addEventListener('click', () => {
      // Go back to quiz to adjust preferences
      location.href = 'path.html';
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      location.href = 'index.html';
    });
  }
})();
