(() => {
  'use strict';

    // CSRF token retrieval helper
  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  // Mark body for full-viewport immersive chat mode
  document.body.classList.add('ca-fullscreen-chat');

  // Top-level project identifier
  const projectIdMatch = window.location.pathname.match(/\/projects\/(\d+)\//);
  const projectId = projectIdMatch ? projectIdMatch[1] : '1';

  // Core DOM Elements
  const chatStream = document.getElementById('ca-chat-stream');
  const welcomeHero = document.getElementById('ca-welcome-hero');
  const chatForm = document.getElementById('ca-chat-form');
  const chatInput = document.getElementById('ca-chat-input');
  const sendBtn = document.getElementById('ca-send-btn');
  const clearChatBtn = document.getElementById('btn-clear-chat');
  const newBriefingBtn = document.getElementById('btn-new-briefing');
  const activeModelPill = document.getElementById('ca-active-model-pill');
  const promptCards = document.querySelectorAll('.ca-topic-tile-btn, .ca-hero-prompt-card');

  // Gemini API Key Modal Elements
  const geminiModal = document.getElementById('gemini-modal');
  const openGeminiBtn = document.getElementById('btn-open-gemini-modal');
  const closeGeminiBtn = document.getElementById('btn-close-gemini-modal');
  const cancelGeminiBtn = document.getElementById('btn-cancel-gemini-modal');
  const saveGeminiBtn = document.getElementById('btn-save-gemini-key');
  const clearGeminiBtn = document.getElementById('btn-clear-gemini-key');
  const geminiKeyInput = document.getElementById('gemini-key-input');
  const geminiKeyStatus = document.getElementById('gemini-key-status');

  // METMalaysia Feed Elements
  const weatherBtn = document.getElementById('ca-fetch-weather');
  const weatherOut = document.getElementById('ca-weather-result');

  // Session API Key management
  const getStoredGeminiKey = () => localStorage.getItem('aerothermal_gemini_key') || '';
  const setStoredGeminiKey = (key) => {
    if (key) localStorage.setItem('aerothermal_gemini_key', key);
    else localStorage.removeItem('aerothermal_gemini_key');
    updateModelBadge();
  };

  const updateModelBadge = () => {
    const key = getStoredGeminiKey();
    if (activeModelPill) {
      if (key) {
        activeModelPill.textContent = 'Gemini 3.8 Flash (Direct API)';
        activeModelPill.style.background = '#D8F3DC';
        activeModelPill.style.color = '#1B4332';
        activeModelPill.style.borderColor = '#95D5B2';
      } else {
        activeModelPill.textContent = 'AeroThermal NADMA RAG';
        activeModelPill.style.background = '#EDF4EF';
        activeModelPill.style.color = '#2D6A4F';
        activeModelPill.style.borderColor = '#B9D4C3';
      }
    }
  };

  updateModelBadge();

  // Robust Markdown-to-HTML Parser with HTML / SVG Preservation
  const renderMarkdown = (md) => {
    if (!md) return '';

    // 1. Extract and preserve all visual diagrams & raw HTML blocks completely
    const diagrams = [];
    let html = md.replace(/<div class="ca-visual-diagram">[\s\S]*?<\/svg>\s*<\/div>/gim, (match) => {
      diagrams.push(match);
      return `\n\n__CA_DIAG_${diagrams.length - 1}__\n\n`;
    });

    // Headings
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^#### (.*$)/gim, '<h4>$1</h4>');

    // Horizontal Rule
    html = html.replace(/^---$/gim, '<hr>');

    // Blockquotes (> text)
    html = html.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');

    // Bold & Italics
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');

    // Checklist checkboxes
    html = html.replace(/^- \[ \] (.*$)/gim, '<div class="ca-checklist-item"><input type="checkbox" disabled> <span>$1</span></div>');
    html = html.replace(/^- \[x\] (.*$)/gim, '<div class="ca-checklist-item"><input type="checkbox" checked disabled> <span>$1</span></div>');

    // Unordered lists
    html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^- (.*$)/gim, '<li>$1</li>');

    // Wrap consecutive <li> into <ul>
    html = html.replace(/(<li>[\s\S]*?<\/li>)/gm, '<ul>$1</ul>');
    html = html.replace(/<\/ul>\s*<ul>/g, '');

    // Paragraph wrapping for loose lines
    const blocks = html.split(/\n\s*\n/);
    const processed = blocks.map(block => {
      const trimmed = block.trim();
      if (!trimmed) return '';
      if (trimmed.startsWith('__CA_DIAG_')) {
        return trimmed;
      }
      if (trimmed.startsWith('<h') || trimmed.startsWith('<ul') || trimmed.startsWith('<ol') ||
          trimmed.startsWith('<blockquote') || trimmed.startsWith('<hr') ||
          trimmed.startsWith('<div class="ca-checklist-item"')) {
        return trimmed;
      }
      return `<p>${trimmed.replace(/\n/g, '<br>')}</p>`;
    });

    let result = processed.join('\n');

    // Restore preserved diagrams
    diagrams.forEach((diag, idx) => {
      result = result.replace(new RegExp(`__CA_DIAG_${idx}__`, 'g'), diag);
    });

    return result;
  };

  // Internal-only scroller that strictly avoids moving the outer browser window
  const scrollChatInternally = (targetEl) => {
    if (!chatStream) return;
    const msgs = chatStream.querySelectorAll('.ca-msg');
    if (msgs.length <= 2 || !targetEl) {
      // First exchange: stay comfortably static at the top
      chatStream.scrollTop = 0;
      return;
    }
    const offset = Math.max(0, targetEl.offsetTop - chatStream.offsetTop - 12);
    chatStream.scrollTo({ top: offset, behavior: 'smooth' });
  };

  // Append user message
  const appendUserMessage = (text) => {
    if (welcomeHero) welcomeHero.style.display = 'none';

    const timeStr = new Date().toLocaleTimeString('en-MY', { hour: '2-digit', minute: '2-digit', hour12: false });
    const msgDiv = document.createElement('div');
    msgDiv.className = 'ca-msg ca-msg-user';
    msgDiv.innerHTML = `
      <div class="ca-msg-avatar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      </div>
      <div class="ca-msg-bubble">
        <div class="ca-msg-header">
          <span class="ca-msg-time">${timeStr} MYT · Operations Manager</span>
        </div>
        <div class="ca-msg-body">
          <p>${text.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</p>
        </div>
      </div>
    `;
    chatStream.appendChild(msgDiv);
    scrollChatInternally(msgDiv);
  };

  // Show Typing Indicator
  const showTypingIndicator = () => {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'ca-msg ca-msg-ai';
    typingDiv.id = 'ca-typing-indicator-msg';
    typingDiv.innerHTML = `
      <div class="ca-msg-avatar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/></svg>
      </div>
      <div class="ca-msg-bubble">
        <div class="ca-typing-indicator" aria-label="AeroThermal AI is analyzing...">
          <span class="ca-typing-dot"></span>
          <span class="ca-typing-dot"></span>
          <span class="ca-typing-dot"></span>
        </div>
      </div>
    `;
    chatStream.appendChild(typingDiv);
  };

  const removeTypingIndicator = () => {
    const typing = document.getElementById('ca-typing-indicator-msg');
    if (typing) typing.remove();
  };

  // Append AI Response
  const appendAIMessage = (markdownContent, providerName, retrievedSources = []) => {
    removeTypingIndicator();
    const timeStr = new Date().toLocaleTimeString('en-MY', { hour: '2-digit', minute: '2-digit', hour12: false });
    const renderedHtml = renderMarkdown(markdownContent);

    let sourcesDrawerHtml = '';
    if (retrievedSources && retrievedSources.length > 0) {
      const sourceCards = retrievedSources.map((s) => `
        <div class="ca-rag-chunk-card">
          <div class="ca-rag-chunk-head">
            <strong class="ca-rag-doc-badge">${s.source || 'Statutory Source'}</strong>
            <small class="ca-rag-clause">${s.clause || ''}</small>
            <span class="ca-rag-score">Relevance: ${s.score || 'Grounded'}</span>
          </div>
          <div class="ca-rag-chunk-title">${s.title || ''}</div>
          <p class="ca-rag-chunk-text">${s.text || ''}</p>
        </div>
      `).join('');

      sourcesDrawerHtml = `
        <details class="ca-rag-sources-drawer" open>
          <summary class="ca-rag-summary">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/></svg>
            <span>Retrieved Statutory Sources (${retrievedSources.length} matching clauses)</span>
          </summary>
          <div class="ca-rag-sources-list">
            ${sourceCards}
          </div>
        </details>
      `;
    }

    const msgDiv = document.createElement('div');
    msgDiv.className = 'ca-msg ca-msg-ai';
    msgDiv.innerHTML = `
      <div class="ca-msg-avatar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/></svg>
      </div>
      <div class="ca-msg-bubble">
        <div class="ca-msg-header">
          <strong>AeroThermal AI Copilot</strong>
          <span class="ca-msg-time">${timeStr} MYT · ${providerName || 'NADMA RAG Grounded'}</span>
        </div>
        <div class="ca-msg-body">
          ${renderedHtml}
          ${sourcesDrawerHtml}
        </div>
        <div class="ca-msg-actions">
          <button class="ca-action-chip btn-copy-answer" type="button">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
            Copy Briefing
          </button>
          <a class="ca-action-chip" href="/projects/${projectId}/resilience/view/leadership/" target="_blank">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24m6.66 6.66 4.24 4.24M12 2v2m0 16v2M2 12h2m16 0h2"/></svg>
            View METMalaysia Weather on Overview
          </a>
          <button class="ca-action-chip btn-share-ecocool" type="button">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2 11 13"/><path d="m22 2-7 20-4-9-9-4Z"/></svg>
            Broadcast to EcoCool App
          </button>
        </div>
      </div>
    `;

    // Copy action
    const copyBtn = msgDiv.querySelector('.btn-copy-answer');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        // Strip out HTML tags for plain text copying
        const plainText = markdownContent.replace(/<[^>]*>?/gm, '');
        navigator.clipboard.writeText(plainText).then(() => {
          copyBtn.textContent = '✓ Copied!';
          setTimeout(() => {
            copyBtn.innerHTML = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg> Copy Briefing';
          }, 2000);
        });
      });
    }

    // Share EcoCool action
    const shareBtn = msgDiv.querySelector('.btn-share-ecocool');
    if (shareBtn) {
      shareBtn.addEventListener('click', () => {
        alert('Resilience briefing notification staged for push broadcast across City of Elmina parcels via the EcoCool Resident App.');
      });
    }

    chatStream.appendChild(msgDiv);
    const userPrompt = msgDiv.previousElementSibling;
    scrollChatInternally(userPrompt && userPrompt.classList.contains('ca-msg-user') ? userPrompt : msgDiv);
  };

  // Execute query against backend
  const executeQuery = async (queryText) => {
    if (!queryText.trim()) return;

    appendUserMessage(queryText);
    showTypingIndicator();

    if (chatInput) {
      chatInput.value = '';
      chatInput.style.height = 'auto';
    }
    if (sendBtn) sendBtn.disabled = true;

    const chatEndpoint = `/projects/${projectId}/resilience/alerts/chat/`;

    try {
      const payload = {
        query: queryText,
        api_key: getStoredGeminiKey()
      };

      const csrfToken = getCookie('csrftoken') || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
      const response = await fetch(chatEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      const data = await response.json();
      appendAIMessage(data.response, data.provider, data.retrieved_sources);
    } catch (err) {
      console.error('Chat error:', err);
      removeTypingIndicator();
      appendAIMessage(
        `### AeroThermal Telemetry Error\n\nUnable to process inquiry at this moment: \`${err.message}\`.\n\nPlease check your network connection or select any scenario card on the dashboard.`,
        'Error Handler'
      );
    } finally {
      if (sendBtn) sendBtn.disabled = false;
      if (chatInput) chatInput.focus({ preventScroll: true });
    }
  };

  // Form submit handler
  if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (text) executeQuery(text);
    });
  }

  // Auto-grow textarea & Enter key handler
  if (chatInput) {
    chatInput.addEventListener('input', () => {
      chatInput.style.height = 'auto';
      chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
    });

    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
      }
    });
  }

  // Prompt Cards Click
  promptCards.forEach(card => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      const promptText = card.dataset.prompt;
      if (promptText) {
        executeQuery(promptText);
      }
    });
  });

  // Reset / Clear Chat Handler
  const resetConversation = () => {
    chatStream.querySelectorAll('.ca-msg').forEach(el => el.remove());
    if (welcomeHero) welcomeHero.style.display = 'block';
    if (chatInput) {
      chatInput.value = '';
      chatInput.style.height = 'auto';
      chatInput.focus({ preventScroll: true });
    }
  };

  
  // Focus textarea when clicking anywhere in input capsule
  const inputCapsule = document.querySelector('.ca-input-capsule');
  if (inputCapsule && chatInput) {
    inputCapsule.addEventListener('click', (e) => {
      if (e.target !== sendBtn && !sendBtn.contains(e.target)) {
        chatInput.focus({ preventScroll: true });
      }
    });
  }

  if (clearChatBtn) clearChatBtn.addEventListener('click', resetConversation);
  if (newBriefingBtn) newBriefingBtn.addEventListener('click', resetConversation);

  // Gemini API Key Modal Handlers
  
  const openGeminiBtnTop = document.getElementById('btn-open-gemini-modal-top');
  if (openGeminiBtnTop && geminiModal) {
    openGeminiBtnTop.addEventListener('click', () => {
      geminiKeyInput.value = getStoredGeminiKey();
      geminiKeyStatus.textContent = getStoredGeminiKey()
        ? 'Active Key: Gemini 3.8 Flash connected'
        : 'No key set. Using on-premise NADMA Grounded Engine.';
      geminiModal.hidden = false;
      geminiKeyInput.focus();
    });
  }

  if (openGeminiBtn && geminiModal) {
    openGeminiBtn.addEventListener('click', () => {
      geminiKeyInput.value = getStoredGeminiKey();
      geminiKeyStatus.textContent = getStoredGeminiKey()
        ? 'Active Key: Gemini 3.8 Flash connected'
        : 'No key set. Using on-premise NADMA Grounded Engine.';
      geminiModal.hidden = false;
      geminiKeyInput.focus();
    });
  }

  const hideGeminiModal = () => {
    if (geminiModal) geminiModal.hidden = true;
  };

  if (closeGeminiBtn) closeGeminiBtn.addEventListener('click', hideGeminiModal);
  if (cancelGeminiBtn) cancelGeminiBtn.addEventListener('click', hideGeminiModal);
  if (geminiModal) {
    geminiModal.addEventListener('click', (e) => {
      if (e.target === geminiModal) hideGeminiModal();
    });
  }

  if (saveGeminiBtn) {
    saveGeminiBtn.addEventListener('click', () => {
      const key = geminiKeyInput.value.trim();
      setStoredGeminiKey(key);
      hideGeminiModal();
      alert(key ? 'Google Gemini API Key successfully saved for this session.' : 'Key removed. Reverted to NADMA Grounded Engine.');
    });
  }

  if (clearGeminiBtn) {
    clearGeminiBtn.addEventListener('click', () => {
      setStoredGeminiKey('');
      geminiKeyInput.value = '';
      geminiKeyStatus.textContent = 'Key removed. Reverted to NADMA Grounded Engine.';
    });
  }

  // METMalaysia Live Feed Check Handler
  if (weatherBtn && weatherOut) {
    const make = (tag, cls, text) => {
      const n = document.createElement(tag);
      if (cls) n.className = cls;
      n.textContent = text;
      return n;
    };
    const stamp = (s) => {
      const d = new Date(s);
      return Number.isNaN(d.getTime()) ? 'Unknown' : d.toLocaleString('en-MY', { timeZone: 'Asia/Kuala_Lumpur' }) + ' MYT';
    };

    weatherBtn.addEventListener('click', async () => {
      weatherBtn.disabled = true;
      weatherOut.setAttribute('aria-busy', 'true');
      weatherOut.textContent = 'Checking national warning bulletins…';
      const controller = new AbortController(),
        timeout = setTimeout(() => controller.abort(), 12000);

      try {
        const response = await fetch(weatherBtn.dataset.url, {
          credentials: 'same-origin',
          signal: controller.signal,
          headers: { Accept: 'application/json' }
        });
        if (!response.ok) throw Error('Feed unavailable');
        const data = await response.json();
        weatherOut.replaceChildren(make('span', 'ca-pill-badge ca-pill-green', ({
          disabled: 'Feed disabled',
          unavailable: 'Feed unavailable',
          retrieved: 'National Feed Checked'
        })[data.status] || 'Status Unknown'));

        weatherOut.append(make('p', '', data.message || 'Local relevance requires catchment review.'));
        if (data.retrieved_at) weatherOut.append(make('small', '', `Retrieved ${stamp(data.retrieved_at)}`));
        const items = Array.isArray(data.items) ? data.items : [];
        if (data.status === 'retrieved' && !items.length) {
          weatherOut.append(make('p', '', 'No severe weather warning currently issued for Shah Alam catchment. Basin capacity is within normal parameters.'));
        }
        for (const item of items) {
          const box = document.createElement('details');
          box.style.marginTop = '6px';
          box.style.padding = '6px 8px';
          box.style.border = '1px solid #CBD5CF';
          box.style.borderRadius = '6px';
          box.append(
            make('summary', '', item.title || 'Weather Bulletin'),
            make('p', '', item.text || ''),
            make('p', '', item.instruction || ''),
            make('small', '', `Valid until ${stamp(item.valid_to)}`)
          );
          weatherOut.append(box);
        }
      } catch {
        weatherOut.replaceChildren(make('span', 'ca-pill-badge ca-pill-orange', 'Feed Offline'), make('p', '', 'Unable to reach METMalaysia server. Please visit met.gov.my directly.'));
      } finally {
        clearTimeout(timeout);
        weatherBtn.disabled = false;
        weatherOut.removeAttribute('aria-busy');
      }
    });
  }
})();
