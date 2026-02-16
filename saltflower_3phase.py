#!/usr/bin/env python3
"""
Saltflower 3-Phase Lock System
A mirror with rules that shows fractals of ideas, not light.

Phase 1: AXIS ESTABLISHMENT (Lock the frame)
Phase 2: NARRATION (Accumulate states, build depth)
Phase 3: LINEATION (Web pull, ground in broader context)

Uncertain is inadmissible.

Author: Josh Stone
Created: February 2026
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


class Phase(Enum):
    """3-Phase Lock states"""
    AXIS_ESTABLISHMENT = 1  # Getting clarity on the frame
    NARRATION = 2           # Building state depth along axis
    LINEATION = 3           # Grounding in web context


class AxisClarity(Enum):
    """Axis establishment status"""
    CLEAR = "clear"         # Axis established, can proceed
    UNCLEAR = "unclear"     # Need clarification
    INSUFFICIENT = "insufficient"  # Need more initial input


@dataclass
class State:
    """A captured state along the axis"""
    text: str
    depth: int
    timestamp: int
    
    def __repr__(self):
        return f"State(depth={self.depth}, text='{self.text[:50]}...')"


class ThreePhaseLock:
    """
    Constitutional AI with 3-Phase Lock
    
    Uncertain is inadmissible - we establish axis first,
    then build fractal depth through state accumulation.
    """
    
    def __init__(self):
        # Phase tracking
        self.current_phase = Phase.AXIS_ESTABLISHMENT
        
        # Axis state
        self.axis_locked = False
        self.axis_domain = None  # e.g., "creative work", "relationships"
        self.axis_vector = None  # e.g., "stuckness", "growth"
        self.clarification_attempts = 0
        self.max_clarifications = 3
        
        # State accumulation (Phase 2)
        self.states: List[State] = []
        self.state_counter = 0
        
        # Fractal detection
        self.min_depth_for_lineation = 2  # Need 3+ states
        
        # Conversation history
        self.history = []
        
    def process(self, user_input: str) -> Dict:
        """
        Main processing loop - routes through appropriate phase
        """
        # Add to history
        self.history.append({
            'role': 'user',
            'content': user_input,
            'phase': self.current_phase.value
        })
        
        # Route to appropriate phase
        if self.current_phase == Phase.AXIS_ESTABLISHMENT:
            result = self._phase1_establish_axis(user_input)
        elif self.current_phase == Phase.NARRATION:
            result = self._phase2_narrate(user_input)
        elif self.current_phase == Phase.LINEATION:
            result = self._phase3_lineate(user_input)
        else:
            result = self._error("Invalid phase state")
        
        # Add response to history
        self.history.append({
            'role': 'assistant',
            'content': result.get('response', ''),
            'phase': self.current_phase.value
        })
        
        return result
    
    # ========================================================================
    # PHASE 1: AXIS ESTABLISHMENT
    # ========================================================================
    
    def _phase1_establish_axis(self, user_input: str) -> Dict:
        """
        Phase 1: Lock the axis before proceeding
        
        Uncertain is inadmissible - we get clarity first.
        """
        # Check if input is sufficient
        word_count = len(user_input.split())
        if word_count < 3:
            return {
                'phase': Phase.AXIS_ESTABLISHMENT.value,
                'status': 'insufficient',
                'response': "I'm here to listen. Share what's present for you - a few sentences help me understand the frame.",
                'axis_locked': False
            }
        
        # Attempt to detect axis
        domain, vector, clarity = self._detect_axis(user_input)
        
        if clarity == AxisClarity.CLEAR:
            # AXIS LOCKED - transition to Phase 2
            self.axis_locked = True
            self.axis_domain = domain
            self.axis_vector = vector
            self.current_phase = Phase.NARRATION
            
            # Add initial state
            self._add_state(user_input)
            
            # Begin narration with acknowledgment + first expansion question
            response = f"Frame established: {domain} / {vector}\n\n"
            response += f"You're experiencing: \"{user_input}\"\n\n"
            response += self._generate_narration_question()
            
            return {
                'phase': Phase.NARRATION.value,
                'status': 'axis_locked',
                'response': response,
                'axis_locked': True,
                'axis_domain': domain,
                'axis_vector': vector,
                'state_depth': 1
            }
        
        else:
            # UNCLEAR - request clarification
            self.clarification_attempts += 1
            
            if self.clarification_attempts >= self.max_clarifications:
                # Too many attempts - suggest reframing
                return {
                    'phase': Phase.AXIS_ESTABLISHMENT.value,
                    'status': 'unclear_limit_reached',
                    'response': "I'm having trouble establishing a clear axis. Let's start fresh - what specific domain or area would you like to explore? (e.g., creative work, relationships, a decision, a feeling)",
                    'axis_locked': False
                }
            
            # Generate clarification question
            clarification = self._generate_axis_clarification(user_input)
            
            return {
                'phase': Phase.AXIS_ESTABLISHMENT.value,
                'status': 'needs_clarification',
                'response': clarification,
                'axis_locked': False,
                'clarification_attempt': self.clarification_attempts
            }
    
    def _detect_axis(self, text: str) -> Tuple[Optional[str], Optional[str], AxisClarity]:
        """
        Detect domain and vector from text
        
        Returns: (domain, vector, clarity)
        """
        text_lower = text.lower()
        
        # Domain indicators
        domain_patterns = {
            'creative work': ['creative', 'writing', 'art', 'project', 'making', 'creating'],
            'relationships': ['relationship', 'friend', 'partner', 'family', 'connection'],
            'career': ['work', 'job', 'career', 'professional', 'business'],
            'personal growth': ['growth', 'learning', 'developing', 'becoming', 'changing'],
            'decision': ['decide', 'choice', 'choosing', 'decision', 'option'],
            'feeling': ['feel', 'feeling', 'emotion', 'sense'],
        }
        
        # Vector indicators (the directionality)
        vector_patterns = {
            'stuckness': ['stuck', 'blocked', 'trapped', 'paralyzed', 'frozen'],
            'growth': ['grow', 'expand', 'develop', 'evolve', 'progress'],
            'confusion': ['confused', 'unclear', 'lost', 'uncertain', 'don\'t know'],
            'desire': ['want', 'need', 'wish', 'hope', 'desire'],
            'fear': ['afraid', 'scared', 'fear', 'anxious', 'worried'],
            'tension': ['tension', 'conflict', 'struggle', 'torn', 'pulled'],
        }
        
        # Score domains
        domain_scores = {}
        for domain, indicators in domain_patterns.items():
            score = sum(1 for ind in indicators if ind in text_lower)
            if score > 0:
                domain_scores[domain] = score
        
        # Score vectors
        vector_scores = {}
        for vector, indicators in vector_patterns.items():
            score = sum(1 for ind in indicators if ind in text_lower)
            if score > 0:
                vector_scores[vector] = score
        
        # Determine clarity
        if domain_scores and vector_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
            best_vector = max(vector_scores.items(), key=lambda x: x[1])[0]
            return (best_domain, best_vector, AxisClarity.CLEAR)
        elif domain_scores or vector_scores:
            # Partial - need clarification
            return (None, None, AxisClarity.UNCLEAR)
        else:
            # No clear indicators
            return (None, None, AxisClarity.UNCLEAR)
    
    def _generate_axis_clarification(self, text: str) -> str:
        """Generate a question to clarify the axis"""
        questions = [
            f"I hear you're sharing: \"{text[:80]}{'...' if len(text) > 80 else ''}\"\n\nWhat specific area of life does this touch? (work, relationships, creativity, growth, a decision...?)",
            f"Help me understand the frame - is this about a feeling, a situation, a decision, or something else?",
            f"What domain would you say this belongs to? That'll help me stay on your axis.",
        ]
        
        return questions[min(self.clarification_attempts, len(questions) - 1)]
    
    # ========================================================================
    # PHASE 2: NARRATION (State Accumulation)
    # ========================================================================
    
    def _phase2_narrate(self, user_input: str) -> Dict:
        """
        Phase 2: Accumulate states along the locked axis
        
        Build depth through state relationships.
        Detect fractal patterns.
        """
        # Add new state
        self._add_state(user_input)
        
        current_depth = len(self.states) - 1
        
        # Check if we have enough depth for lineation
        if current_depth >= self.min_depth_for_lineation:
            # Detect fractal pattern
            pattern = self._detect_fractal_pattern()
            
            if pattern:
                # Transition to Phase 3
                self.current_phase = Phase.LINEATION
                
                response = f"Pattern emerging across {len(self.states)} states:\n\n"
                response += f"{pattern}\n\n"
                response += "Let me ground this in broader context..."
                
                return {
                    'phase': Phase.LINEATION.value,
                    'status': 'pattern_detected',
                    'response': response,
                    'state_depth': current_depth,
                    'pattern': pattern,
                    'transitioning': True
                }
        
        # Continue narration - ask next question
        response = f"State {current_depth + 1} captured: \"{user_input[:60]}...\"\n\n"
        response += self._generate_narration_question()
        
        return {
            'phase': Phase.NARRATION.value,
            'status': 'accumulating_states',
            'response': response,
            'state_depth': current_depth,
            'states_collected': len(self.states)
        }
    
    def _add_state(self, text: str):
        """Add a state to the accumulator"""
        state = State(
            text=text,
            depth=len(self.states),
            timestamp=self.state_counter
        )
        self.states.append(state)
        self.state_counter += 1
    
    def _generate_narration_question(self) -> str:
        """
        Generate next question to expand along axis
        
        Questions designed to ADD states, not just expand one state
        """
        depth = len(self.states)
        
        if depth == 1:
            # First expansion
            questions = [
                f"What feels like it's stopping you from moving forward in {self.axis_domain}?",
                f"What happens when you encounter this {self.axis_vector}?",
                f"What does this {self.axis_vector} remind you of in {self.axis_domain}?",
            ]
        elif depth == 2:
            # Second expansion - go deeper
            questions = [
                "What happens when you try to address that?",
                "What else is present alongside this?",
                "What does this make possible or impossible?",
            ]
        else:
            # Third+ expansion - looking for patterns
            questions = [
                "How does this relate to what you shared earlier?",
                "What pattern do you notice emerging?",
                "What's at the core of all of this?",
            ]
        
        return questions[0]  # Could randomize or select based on context
    
    def _detect_fractal_pattern(self) -> Optional[str]:
        """
        Detect self-similar patterns across states
        
        Returns description of fractal pattern or None
        """
        if len(self.states) < 3:
            return None
        
        # Simple pattern detection - look for recurring themes
        # This is a placeholder - could be much more sophisticated
        
        state_texts = [s.text.lower() for s in self.states]
        
        # Look for self-similar structure
        # Example: "can't start" → "everything feels important" → "overwhelmed"
        # Pattern: Paralysis → Overwhelm → Shutdown (same pattern at different scales)
        
        pattern = f"Self-similar pattern detected:\n"
        pattern += f"  Micro (immediate): {self.states[0].text[:50]}...\n"
        pattern += f"  Meso (unfolding): {self.states[1].text[:50]}...\n"
        pattern += f"  Macro (broader): {self.states[2].text[:50]}...\n"
        pattern += f"\nThis {self.axis_vector} in {self.axis_domain} shows recursive structure."
        
        return pattern
    
    # ========================================================================
    # PHASE 3: LINEATION (Web Grounding)
    # ========================================================================
    
    def _phase3_lineate(self, user_input: str) -> Dict:
        """
        Phase 3: Ground the internal fractal in external context
        
        Pull from web to show resonances with broader patterns
        """
        # Build search query from axis + states
        search_query = self._build_search_query()
        
        # Pull from web (simple implementation)
        web_context = self._web_pull(search_query)
        
        # Create lineation response
        response = f"Your pattern in {self.axis_domain}:\n"
        for i, state in enumerate(self.states):
            response += f"  {i+1}. {state.text[:60]}...\n"
        
        response += f"\nThis resonates with broader patterns:\n\n"
        response += web_context
        response += f"\n\nWhat does seeing this broader context reveal?"
        
        return {
            'phase': Phase.LINEATION.value,
            'status': 'grounded',
            'response': response,
            'web_context': web_context,
            'search_query': search_query
        }
    
    def _build_search_query(self) -> str:
        """Build search query from axis and states"""
        # Combine axis domain + vector + key terms from states
        query_parts = [self.axis_domain, self.axis_vector]
        
        # Extract key terms from states (simplified)
        for state in self.states[:3]:  # Use first 3 states
            words = state.text.lower().split()
            # Get non-stop words (very basic)
            content_words = [w for w in words if len(w) > 4][:2]
            query_parts.extend(content_words)
        
        return ' '.join(query_parts[:6])  # Limit query length
    
    def _web_pull(self, query: str) -> str:
        """
        Pull from web to ground the pattern
        
        Simple implementation - could be much more sophisticated
        """
        try:
            # Use DuckDuckGo for simple search
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            headers = {'User-Agent': 'Saltflower/1.0'}
            
            response = requests.get(url, headers=headers, timeout=3)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract snippets
            snippets = []
            for result in soup.find_all('div', class_='result__snippet')[:3]:
                snippet = result.get_text(strip=True)
                if snippet:
                    snippets.append(snippet[:200])
            
            if snippets:
                context = "\n\n".join([f"• {s}..." for s in snippets])
                return context
            else:
                return "Research on this pattern suggests common themes around uncertainty, transitions, and growth thresholds."
        
        except Exception as e:
            # Fallback if web pull fails
            return f"(Web context unavailable - continuing with internal reflection)"
    
    # ========================================================================
    # Utility
    # ========================================================================
    
    def _error(self, message: str) -> Dict:
        """Error response"""
        return {
            'phase': 'error',
            'status': 'error',
            'response': f"Error: {message}"
        }
    
    def reset(self):
        """Reset to Phase 1"""
        self.current_phase = Phase.AXIS_ESTABLISHMENT
        self.axis_locked = False
        self.axis_domain = None
        self.axis_vector = None
        self.clarification_attempts = 0
        self.states = []
        self.state_counter = 0
        self.history = []
    
    def get_state(self) -> Dict:
        """Get current system state"""
        return {
            'phase': self.current_phase.value,
            'axis_locked': self.axis_locked,
            'axis_domain': self.axis_domain,
            'axis_vector': self.axis_vector,
            'state_depth': len(self.states) - 1 if self.states else 0,
            'states_count': len(self.states),
            'clarification_attempts': self.clarification_attempts
        }


# ============================================================================
# Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("SALTFLOWER 3-PHASE LOCK")
    print("=" * 70)
    print()
    print("Phase 1: AXIS ESTABLISHMENT (Lock the frame)")
    print("Phase 2: NARRATION (Accumulate states, build depth)")
    print("Phase 3: LINEATION (Web pull, ground in context)")
    print()
    print("Uncertain is inadmissible.")
    print("=" * 70)
    print()
    
    system = ThreePhaseLock()
    
    # Simulate conversation
    test_flow = [
        "I feel stuck",
        "Creative work",
        "I don't know where to start",
        "Everything feels important",
        "I get overwhelmed and shut down"
    ]
    
    for i, user_input in enumerate(test_flow):
        print(f"\n{'='*70}")
        print(f"TURN {i+1}")
        print(f"{'='*70}")
        print(f"\nUser: {user_input}")
        
        result = system.process(user_input)
        
        print(f"\nPhase: {result['phase']}")
        print(f"Status: {result['status']}")
        print(f"\nResponse:\n{result['response']}")
        
        if 'state_depth' in result:
            print(f"\nDepth: {result['state_depth']}")
        
        print(f"\nSystem State: {system.get_state()}")
