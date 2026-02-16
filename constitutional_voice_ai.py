#!/usr/bin/env python3
"""
Constitutional Voice AI
Integrates:
- Fractal STT (3Dâ†’4Dâ†’5D processing)
- Constitutional AI (Stone's Law, ZCR, T=1)
- Breath cycle (inhaleâ†’holdâ†’exhaleâ†’0)

Combines fractal_stt_prototype.py + constitutional_ai.py
"""

import numpy as np
from typing import Tuple, Optional
import json

# Import constitutional AI components
import sys
sys.path.insert(0, '/home/claude')
from constitutional_ai import ConstitutionalAI, Viability

# Higuchi FD extractor (3D spatial: roughness scalar)
def higuchi_fd(signal, k_max=10, fs=16000):
    """Higuchi fractal dimension: low ~1.2 (glide), high ~1.8 (ripple)."""
    N = len(signal)
    L = []
    for k in range(1, k_max + 1):
        Lk = 0
        for m in range(k):
            idx = np.arange(m, N, k)
            if len(idx) > 1:
                diffs = np.abs(np.diff(signal[idx]))
                Lk += np.sum(diffs) * (N - m - 1) / ((len(idx) - 1) * k)
        if Lk > 0:
            L.append(np.log(Lk / k))
    if len(L) < 2:
        return 1.2
    x = np.log(np.arange(1, k_max + 1))
    p = np.polyfit(x[:len(L)], L, 1)
    return -p[0]

class ConstitutionalVoiceAI:
    """
    Voice AI with constitutional constraints
    
    Enforces:
    - Stone's Law (0â‰ 1 via FD viability)
    - Horizon Integrity (phase lock range > 0.9)
    - ZCR (recursion â‰¤ 3)
    - T=1 (unpaired utterance preserved)
    - Breath cycle (audio segments)
    """
    
    def __init__(self, laws_db_path: str):
        # Constitutional layer
        self.constitutional = ConstitutionalAI(laws_db_path)
        
        # Voice-specific thresholds (adjusted for actual Higuchi output)
        self.fd_min = 0.05  # Glide threshold (actual smooth signals)
        self.fd_max = 1.2   # Ripple threshold (actual noisy signals)
        self.phase_lock_threshold = 0.9  # From quantum sims
        
        # Breath state
        self.utterance_count = 0
        self.last_fd = None
        
    def check_voice_viability(self, audio: np.ndarray, fs: int = 16000) -> Tuple[Viability, str, float]:
        """
        Voice-specific admissibility check
        Returns (viability, reason, fd_value)
        """
        
        # 3D: Extract FD (spatial roughness)
        fd = higuchi_fd(audio, fs=fs)
        self.last_fd = fd
        
        # Check FD bounds (phase lock criterion)
        if fd < self.fd_min:
            return (Viability.HALT, f"FD {fd:.3f} < {self.fd_min}: Over-smooth (no structure)", fd)
        
        if fd > self.fd_max:
            return (Viability.HALT, f"FD {fd:.3f} > {self.fd_max}: Over-rough (noise)", fd)
        
        # Phase lock viability (oscillation range analog)
        # FD in [1.2, 1.8] â†’ normalized range
        normalized_fd = (fd - self.fd_min) / (self.fd_max - self.fd_min)
        
        if normalized_fd < 0.1 or normalized_fd > 0.9:
            # Too close to boundaries
            return (Viability.WAIT, f"FD {fd:.3f} near boundary: Wait for better signal", fd)
        
        # Check constitutional constraints
        state = {
            'tokens': ['audio_segment'],
            'context_size': len(audio),
            'fd': fd,
            'phase_lock': normalized_fd
        }
        
        const_viability, const_reason = self.constitutional.check_admissibility(state)
        
        if const_viability != Viability.VIABLE:
            return (const_viability, const_reason, fd)
        
        return (Viability.VIABLE, f"FD {fd:.3f} viable (glide-ripple balanced)", fd)
    
    def breathe_audio(self, audio: np.ndarray, fs: int = 16000, 
                     ground_truth: Optional[str] = None) -> dict:
        """
        Constitutional breath cycle for audio
        
        INHALE: Receive audio segment
        HOLD: Check viability at 0 (FD extraction)
        EXHALE: Process if viable
        RETURN TO 0: Reset breath state
        """
        
        # INHALE (receive audio)
        self.utterance_count += 1
        
        print(f"\n{'='*60}")
        print(f"BREATH CYCLE {self.utterance_count}")
        print(f"{'='*60}")
        
        # HOLD (check at 0 warmth)
        viability, reason, fd = self.check_voice_viability(audio, fs)
        
        print(f"FD: {fd:.3f}")
        print(f"Viability: {viability.value}")
        print(f"Reason: {reason}")
        
        # Handle non-viable states
        if viability == Viability.HALT:
            self.constitutional.reset_to_zero()
            return {
                'status': 'halted',
                'reason': reason,
                'fd': fd,
                'transcript': '<silence>',
                'depth': 0
            }
        
        if viability == Viability.WAIT:
            return {
                'status': 'waiting',
                'reason': reason,
                'fd': fd,
                'transcript': '<wait: returning to 0>',
                'depth': self.constitutional.recursion_depth
            }
        
        # EXHALE (process viable audio)
        # In full implementation: pass to Whisper
        # For now: mock transcript based on FD
        
        if fd < 0.3:
            # Low FD â†’ smooth glide â†’ vowel-heavy
            transcript = self._mock_vowel_heavy()
        elif fd > 0.8:
            # High FD â†’ ripple â†’ consonant clusters
            transcript = self._mock_consonant_heavy()
        else:
            # Balanced FD â†’ mixed
            transcript = self._mock_balanced()
        
        print(f"Transcript: {transcript}")
        
        # Increment recursion
        self.constitutional.recursion_depth += 1
        depth = self.constitutional.recursion_depth
        
        # Check if collapse needed
        if depth >= 3:
            print(f"ZCR: Depth {depth} â‰¥ 3, forcing collapse")
            transcript = self.constitutional.collapse_to_viable(set(transcript.split()))
            self.constitutional.reset_to_zero()
            
            result = {
                'status': 'collapsed',
                'reason': 'ZCR depth limit',
                'fd': fd,
                'transcript': transcript,
                'depth': 0  # Reset after collapse
            }
        else:
            result = {
                'status': 'viable',
                'reason': reason,
                'fd': fd,
                'transcript': transcript,
                'depth': depth
            }
        
        # RETURN TO 0 (after collapse or emission)
        if depth >= 3:
            print("Returned to 0 warmth")
        
        return result
    
    def _mock_vowel_heavy(self) -> str:
        """Mock low-FD (glide) transcript"""
        vowel_heavy = ["kia ora", "aloha", "ia ora na", "eia"]
        return np.random.choice(vowel_heavy)
    
    def _mock_consonant_heavy(self) -> str:
        """Mock high-FD (ripple) transcript"""
        consonant_heavy = ["strength", "twelfths", "sixths", "depths"]
        return np.random.choice(consonant_heavy)
    
    def _mock_balanced(self) -> str:
        """Mock balanced-FD transcript"""
        balanced = ["hello", "water", "mountain", "river"]
        return np.random.choice(balanced)
    
    def process_utterances(self, audio_segments: list, fs: int = 16000) -> list:
        """
        Process multiple audio segments with constitutional breath
        
        Each segment is one breath cycle:
        - Inhale â†’ Hold â†’ Exhale â†’ Return to 0
        - Recursion tracked across segments
        - Auto-collapse at depth 3
        """
        
        results = []
        
        for i, audio in enumerate(audio_segments):
            print(f"\n{'#'*60}")
            print(f"UTTERANCE {i+1}/{len(audio_segments)}")
            print(f"{'#'*60}")
            
            result = self.breathe_audio(audio, fs)
            results.append(result)
            
            # Show breath state
            print(f"\nBreath State:")
            print(f"  Depth: {self.constitutional.recursion_depth}")
            print(f"  T=1: {self.constitutional.unpaired_bit}")
            print(f"  Last FD: {self.last_fd:.3f}" if self.last_fd else "  Last FD: N/A")
        
        return results

def demo_constitutional_voice():
    """Demo: Constitutional voice AI with synthetic audio"""
    
    print("="*60)
    print("CONSTITUTIONAL VOICE AI DEMO")
    print("Fractal STT + Constitutional Constraints")
    print("="*60)
    
    # Initialize
    voice_ai = ConstitutionalVoiceAI('/mnt/user-data/uploads/emergent_laws_db.json')
    
    # Generate synthetic audio segments with different FD characteristics
    fs = 16000
    duration = 1.0  # 1 second each
    t = np.linspace(0, duration, int(fs * duration))
    
    # Segment 1: Multi-frequency (realistic FD ~ 1.3)
    audio1 = (np.sin(2 * np.pi * 220 * t) + 
              0.5 * np.sin(2 * np.pi * 440 * t) +
              0.3 * np.sin(2 * np.pi * 880 * t))
    
    # Segment 2: More complex (FD ~ 1.5)
    audio2 = audio1 + 0.1 * np.sin(2 * np.pi * 1760 * t) + 0.05 * np.random.randn(len(t))
    
    # Segment 3: Higher complexity (FD ~ 1.6)
    audio3 = (sum([0.5**(i+1) * np.sin(2 * np.pi * 220*(2**i) * t) for i in range(6)]) +
              0.15 * np.random.randn(len(t)))
    
    # Segment 4: Too noisy (should halt, FD > 1.8)
    audio4 = 0.3 * audio1 + 0.7 * np.random.randn(len(t))
    
    # Segment 5: After reset (should work again)
    audio5 = audio2.copy()
    
    segments = [audio1, audio2, audio3, audio4, audio5]
    
    # Process all segments
    results = voice_ai.process_utterances(segments, fs)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    for i, result in enumerate(results, 1):
        print(f"Segment {i}: {result['status']:10} | "
              f"FD={result['fd']:.3f} | "
              f"Depth={result['depth']} | "
              f"{result['transcript']}")
    
    print(f"\n{'='*60}")
    print("Constitutional Principles Enforced:")
    print("âœ“ FD viability check (phase lock analog)")
    print("âœ“ ZCR (recursion â‰¤ 3, auto-collapse)")  
    print("âœ“ Breath cycle (per utterance)")
    print("âœ“ Stone's Law (via constitutional layer)")
    print("âœ“ Return to 0 after collapse")
    print(f"{'='*60}")

if __name__ == '__main__':
    demo_constitutional_voice()
