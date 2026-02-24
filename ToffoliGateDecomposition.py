import qutip as qt
import numpy as np

# Single qubit gates
h_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
H = qt.Qobj(h_matrix)
t_matrix = np.diag([1, np.exp(1j * np.pi / 4)])
T = qt.Qobj(t_matrix)
td_matrix = np.diag([1, np.exp(-1j * np.pi / 4)])
Td = qt.Qobj(td_matrix)

# Projectors for CNOT
P0 = qt.basis(2, 0) * qt.basis(2, 0).dag()
P1 = qt.basis(2, 1) * qt.basis(2, 1).dag()
X = qt.sigmax()
I = qt.identity(2)

# CNOT for 3 qubits (q0: control1, q1: control2, q2: target)
cnot02 = qt.tensor(P0, I, I) + qt.tensor(P1, I, X)  # CNOT q0 to q2
cnot01 = qt.tensor(P0, I, I) + qt.tensor(P1, X, I)  # CNOT q0 to q1
cnot12 = qt.tensor(I, P0, I) + qt.tensor(I, P1, X)  # CNOT q1 to q2

# Function to expand single-qubit gate to 3 qubits
def gate1to3(g, target):
    if target == 0:
        return qt.tensor(g, I, I)
    elif target == 1:
        return qt.tensor(I, g, I)
    elif target == 2:
        return qt.tensor(I, I, g)

# Expanded gates
H2 = gate1to3(H, 2)
T0 = gate1to3(T, 0)
T1 = gate1to3(T, 1)
Td1 = gate1to3(Td, 1)
T2 = gate1to3(T, 2)
Td2 = gate1to3(Td, 2)

# Decomposition steps in application order (first applied first)
gates_list = [
    H2,     # 1. H on target (q2)
    cnot12, # 2. CNOT q1 to q2
    Td2,    # 3. T† on q2
    cnot02, # 4. CNOT q0 to q2
    T2,     # 5. T on q2
    cnot12, # 6. CNOT q1 to q2
    Td2,    # 7. T† on q2
    cnot02, # 8. CNOT q0 to q2
    T2,     # 9. T on q2
    T1,     # 10. T on q1
    cnot01, # 11. CNOT q0 to q1
    Td1,    # 12. T† on q1
    T0,     # 13. T on q0
    cnot01, # 14. CNOT q0 to q1
    H2      # 15. H on q2
]

# Build decomposed Toffoli (U = U_last * ... * U_first)
decomposed = qt.qeye([2, 2, 2])
for g in reversed(gates_list):
    decomposed = g * decomposed

# Standard Toffoli matrix for verification
toff_matrix = np.eye(8)
toff_matrix[6, 6] = 0
toff_matrix[7, 7] = 0
toff_matrix[6, 7] = 1
toff_matrix[7, 6] = 1
toff = qt.Qobj(toff_matrix, dims=[[2, 2, 2], [2, 2, 2]])

# Verification: Matrix match up to global phase
matrix_full_decomp = decomposed.full()
matrix_full_toff = toff.full()
nonzero = np.where(np.abs(matrix_full_toff) > 1e-10)
ratio = matrix_full_decomp[nonzero] / matrix_full_toff[nonzero]
phase = np.angle(ratio[0])
norm_toff = matrix_full_toff * np.exp(1j * phase)
matrix_match = np.allclose(matrix_full_decomp, norm_toff, atol=1e-10)

# Test on |111⟩ (should become |110⟩ up to phase)
state_111 = qt.tensor(qt.basis(2, 1), qt.basis(2, 1), qt.basis(2, 1))
out_decomp = decomposed * state_111
out_toff = toff * state_111

# State match up to global phase
amplitudes_decomp = out_decomp.full().flatten()
amplitudes_toff = out_toff.full().flatten()
nonzero_decomp = np.abs(amplitudes_decomp) > 1e-10
nonzero_toff = np.abs(amplitudes_toff) > 1e-10
state_match = False
if np.all(nonzero_decomp == nonzero_toff):
    ratio = amplitudes_decomp[nonzero_decomp] / amplitudes_toff[nonzero_toff]
    phase = np.angle(ratio[0])
    norm_toff_state = amplitudes_toff * np.exp(1j * phase)
    state_match = np.allclose(amplitudes_decomp, norm_toff_state, atol=1e-10)

# Results (from execution)
print("Matrix match (up to phase):", matrix_match)  # True
print("State match on |111⟩ (up to phase):", state_match)  # True
print("Output state from decomposed:", amplitudes_decomp)  # [0.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j 1.+0.j 0.+0.j]import qutip as qt
import numpy as np

# Single qubit gates
h_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
H = qt.Qobj(h_matrix)
t_matrix = np.diag([1, np.exp(1j * np.pi / 4)])
T = qt.Qobj(t_matrix)
td_matrix = np.diag([1, np.exp(-1j * np.pi / 4)])
Td = qt.Qobj(td_matrix)

# Projectors for CNOT
P0 = qt.basis(2, 0) * qt.basis(2, 0).dag()
P1 = qt.basis(2, 1) * qt.basis(2, 1).dag()
X = qt.sigmax()
I = qt.identity(2)

# CNOT for 3 qubits (q0: control1, q1: control2, q2: target)
cnot02 = qt.tensor(P0, I, I) + qt.tensor(P1, I, X)  # CNOT q0 to q2
cnot01 = qt.tensor(P0, I, I) + qt.tensor(P1, X, I)  # CNOT q0 to q1
cnot12 = qt.tensor(I, P0, I) + qt.tensor(I, P1, X)  # CNOT q1 to q2

# Function to expand single-qubit gate to 3 qubits
def gate1to3(g, target):
    if target == 0:
        return qt.tensor(g, I, I)
    elif target == 1:
        return qt.tensor(I, g, I)
    elif target == 2:
        return qt.tensor(I, I, g)

# Expanded gates
H2 = gate1to3(H, 2)
T0 = gate1to3(T, 0)
T1 = gate1to3(T, 1)
Td1 = gate1to3(Td, 1)
T2 = gate1to3(T, 2)
Td2 = gate1to3(Td, 2)

# Decomposition steps in application order (first applied first)
gates_list = [
    H2,     # 1. H on target (q2)
    cnot12, # 2. CNOT q1 to q2
    Td2,    # 3. T† on q2
    cnot02, # 4. CNOT q0 to q2
    T2,     # 5. T on q2
    cnot12, # 6. CNOT q1 to q2
    Td2,    # 7. T† on q2
    cnot02, # 8. CNOT q0 to q2
    T2,     # 9. T on q2
    T1,     # 10. T on q1
    cnot01, # 11. CNOT q0 to q1
    Td1,    # 12. T† on q1
    T0,     # 13. T on q0
    cnot01, # 14. CNOT q0 to q1
    H2      # 15. H on q2
]

# Build decomposed Toffoli (U = U_last * ... * U_first)
decomposed = qt.qeye([2, 2, 2])
for g in reversed(gates_list):
    decomposed = g * decomposed

# Standard Toffoli matrix for verification
toff_matrix = np.eye(8)
toff_matrix[6, 6] = 0
toff_matrix[7, 7] = 0
toff_matrix[6, 7] = 1
toff_matrix[7, 6] = 1
toff = qt.Qobj(toff_matrix, dims=[[2, 2, 2], [2, 2, 2]])

# Verification: Matrix match up to global phase
matrix_full_decomp = decomposed.full()
matrix_full_toff = toff.full()
nonzero = np.where(np.abs(matrix_full_toff) > 1e-10)
ratio = matrix_full_decomp[nonzero] / matrix_full_toff[nonzero]
phase = np.angle(ratio[0])
norm_toff = matrix_full_toff * np.exp(1j * phase)
matrix_match = np.allclose(matrix_full_decomp, norm_toff, atol=1e-10)

# Test on |111⟩ (should become |110⟩ up to phase)
state_111 = qt.tensor(qt.basis(2, 1), qt.basis(2, 1), qt.basis(2, 1))
out_decomp = decomposed * state_111
out_toff = toff * state_111

# State match up to global phase
amplitudes_decomp = out_decomp.full().flatten()
amplitudes_toff = out_toff.full().flatten()
nonzero_decomp = np.abs(amplitudes_decomp) > 1e-10
nonzero_toff = np.abs(amplitudes_toff) > 1e-10
state_match = False
if np.all(nonzero_decomp == nonzero_toff):
    ratio = amplitudes_decomp[nonzero_decomp] / amplitudes_toff[nonzero_toff]
    phase = np.angle(ratio[0])
    norm_toff_state = amplitudes_toff * np.exp(1j * phase)
    state_match = np.allclose(amplitudes_decomp, norm_toff_state, atol=1e-10)

# Results (from execution)
print("Matrix match (up to phase):", matrix_match)  # True
print("State match on |111⟩ (up to phase):", state_match)  # True
print("Output state from decomposed:", amplitudes_decomp)  # [0.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j 1.+0.j 0.+0.j]
