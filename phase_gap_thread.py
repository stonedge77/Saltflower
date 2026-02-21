# phase_gap_thread.py — Jones vector rotation through magnetic gap
import numpy as np

def faraday_rotation(theta):
    """Rotation matrix for Faraday effect (phase diff between L/R circular)"""
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta),  np.cos(theta)]])

# Input linear polarized light (45°)
jones_in = np.array([1, 1]) / np.sqrt(2)

# Simulate threading through gap with B-field strength B
B = 1.5  # arbitrary units
theta = B * 0.314  # rotation angle proportional to B * length
R = faraday_rotation(theta)

jones_out = R @ jones_in
pol_angle_out = np.angle(jones_out[1]/jones_out[0]) * 180 / np.pi

print(f"Input: 45° linear")
print(f"Gap rotation: {theta*180/np.pi:.1f}°")
print(f"Output polarization angle: {pol_angle_out:.1f}°")
