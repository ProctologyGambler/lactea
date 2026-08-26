// Lactea sound layer.
//
// Reads per-skin sound URLs from the JSON-script element #skin-sounds
// (populated by the context processor). Exposes a global playSkinSound(slot)
// that respects a localStorage mute toggle. Slots: tap / save / milestone /
// session_end.
//
// All four slots may currently point to the same file (placeholder phase) —
// the layer is designed so this isn't ugly: each slot has its own Audio
// instance so plays don't cut each other off.
(function () {
    const SOUNDS_ELEM = document.getElementById('skin-sounds');
    const SOUNDS = SOUNDS_ELEM ? JSON.parse(SOUNDS_ELEM.textContent) : {};

    const MUTE_KEY = 'lactea.sound.muted';
    const FIRST_SAVE_PROMPT_KEY = 'lactea.sound.firstSavePromptResolved';

    // Per-slot Audio cache so a tap doesn't restart a save mid-play.
    const cache = {};

    function isMuted() {
        return localStorage.getItem(MUTE_KEY) === '1';
    }

    function setMuted(muted) {
        if (muted) {
            localStorage.setItem(MUTE_KEY, '1');
        } else {
            localStorage.removeItem(MUTE_KEY);
        }
        document.body.dataset.soundMuted = muted ? '1' : '0';
        updateMuteButton();
    }

    function getAudio(slot) {
        const url = SOUNDS[slot];
        if (!url) return null;
        if (!cache[slot]) {
            const audio = new Audio(url);
            audio.preload = 'auto';
            cache[slot] = audio;
        }
        return cache[slot];
    }

    window.playSkinSound = function (slot) {
        if (isMuted()) return;
        const audio = getAudio(slot);
        if (!audio) return;
        try {
            audio.currentTime = 0;
            const p = audio.play();
            if (p && typeof p.catch === 'function') {
                p.catch(() => {}); // autoplay policy / interruption — silently ignore
            }
        } catch (e) {
            // older browsers throw on currentTime set; ignore
        }
    };

    window.toggleSkinMute = function () {
        setMuted(!isMuted());
    };

    function updateMuteButton() {
        const btn = document.getElementById('sound-toggle');
        if (!btn) return;
        const muted = isMuted();
        btn.setAttribute('aria-pressed', muted ? 'false' : 'true');
        btn.setAttribute('aria-label', muted ? 'Sound off — tap to enable' : 'Sound on — tap to mute');
        btn.textContent = muted ? '🔇' : '🔊';
    }

    // First-save prompt: called from server-rendered <script> after a save redirect
    // (?just_pumped=1). Shows the prompt only if the user has never resolved it.
    window.maybePromptFirstSaveSound = function () {
        if (localStorage.getItem(FIRST_SAVE_PROMPT_KEY) === '1') return;
        const prompt = document.getElementById('first-save-sound-prompt');
        if (!prompt) return;
        prompt.classList.remove('hidden');
    };

    window.enableSoundFromPrompt = function () {
        localStorage.setItem(FIRST_SAVE_PROMPT_KEY, '1');
        setMuted(false);
        const prompt = document.getElementById('first-save-sound-prompt');
        if (prompt) prompt.classList.add('hidden');
        playSkinSound('save'); // immediate confirmation that it works
    };

    window.dismissSoundPrompt = function () {
        localStorage.setItem(FIRST_SAVE_PROMPT_KEY, '1');
        const prompt = document.getElementById('first-save-sound-prompt');
        if (prompt) prompt.classList.add('hidden');
    };

    function maybeShowPromptFromUrl() {
        const params = new URLSearchParams(window.location.search);
        if (params.get('just_pumped') === '1' && isMuted()) {
            window.maybePromptFirstSaveSound();
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        updateMuteButton();
        maybeShowPromptFromUrl();
    });
})();
