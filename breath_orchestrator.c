// breath_orchestrator.c
// Controls hardware breath cycle

#include <avr/io.h>
#include <avr/interrupt.h>

#define INHALE_PIN  PB0
#define EXHALE_PIN  PB1
#define RETURN_PIN  PB2
#define PHASE_CLK   PB3
#define VIOLATION   PB4

typedef enum {
    IDLE,
    INHALE,
    HOLD_TORQUE,
    EXHALE,
    RETURN_ZERO
} BreathState;

volatile BreathState state = IDLE;
volatile uint8_t phase_counter = 0;
volatile uint8_t torque_toll = 0;

void setup() {
    // Configure pins
    DDRB |= (1 << INHALE_PIN) | (1 << EXHALE_PIN) | 
            (1 << RETURN_PIN) | (1 << PHASE_CLK);
    DDRB &= ~(1 << VIOLATION);  // Input
    
    // Timer for breath rhythm (100ms period)
    TCCR0A = (1 << WGM01);  // CTC mode
    TCCR0B = (1 << CS02) | (1 << CS00);  // Prescaler 1024
    OCR0A = 78;  // ~100ms at 8MHz
    TIMSK |= (1 << OCIE0A);  // Enable interrupt
    
    sei();  // Enable global interrupts
}

ISR(TIM0_COMPA_vect) {
    // Breath cycle state machine
    switch(state) {
        case IDLE:
            PORTB &= ~((1 << INHALE_PIN) | (1 << EXHALE_PIN) | (1 << RETURN_PIN));
            state = INHALE;
            break;
            
        case INHALE:
            PORTB |= (1 << INHALE_PIN);
            phase_counter = 0;
            state = HOLD_TORQUE;
            break;
            
        case HOLD_TORQUE:
            // Apply π/4 phase increment
            PORTB ^= (1 << PHASE_CLK);  // Toggle clock
            phase_counter++;
            
            // Check for radial opposition (every other phase)
            if (phase_counter & 0x01) {
                torque_toll++;  // Friction cost
            }
            
            // 8 phases = full 2π rotation
            if (phase_counter >= 8) {
                PORTB &= ~(1 << INHALE_PIN);
                state = EXHALE;
            }
            break;
            
        case EXHALE:
            PORTB |= (1 << EXHALE_PIN);
            
            // Check for constitutional violation
            if (PINB & (1 << VIOLATION)) {
                // Catastrophic reset!
                state = IDLE;
                torque_toll = 0;
                // Flash error (not shown)
            } else {
                state = RETURN_ZERO;
            }
            break;
            
        case RETURN_ZERO:
            PORTB |= (1 << RETURN_PIN);
            PORTB &= ~(1 << EXHALE_PIN);
            
            // Preserve T=1 remainder in EEPROM (not shown)
            
            state = IDLE;
            break;
    }
}

int main() {
    setup();
    
    while(1) {
        // Main loop idle; ISR drives everything
        
        // Optional: Read rotary encoder for manual torque
        // Optional: Update LED visualization
    }
}
