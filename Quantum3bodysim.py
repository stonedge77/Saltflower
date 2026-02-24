import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

# 3 qubits
sx = qt.sigmax()
sz = qt.sigmaz()
I = qt.identity(2)

# Tensors
sx1 = qt.tensor(sx, I, I)
sx2 = qt.tensor(I, sx, I)
sx3 = qt.tensor(I, I, sx)
sz1 = qt.tensor(sz, I, I)
sz2 = qt.tensor(I, sz, I)
sz3 = qt.tensor(I, I, sz)
sz123 = qt.tensor(sz, sz, sz)

# Hamiltonian
J = 1.0
h = 0.5
g = 0.2  # 3-body strength
H = J * (sx1 * sx2 + sx2 * sx3 + sx3 * sx1) + h * (sz1 + sz2 + sz3) + g * sz123

# Initial |000>
psi0 = qt.tensor(qt.basis(2,0), qt.basis(2,0), qt.basis(2,0))

# Time
tlist = np.linspace(0, 10, 100)

# Evolve
result = qt.mesolve(H, psi0, tlist, [], [sz1, sz2, sz3])

# Plot
plt.figure()
plt.plot(tlist, result.expect[0], label='<σ_z1>')
plt.plot(tlist, result.expect[1], label='<σ_z2>')
plt.plot(tlist, result.expect[2], label='<σ_z3>')
plt.xlabel('Time')
plt.ylabel('Expectation Value')
plt.title('Quantum 3-Body Spin Dynamics')
plt.legend()
plt.show()  # Or savefig('quantum_3body.png')
