import numpy as np
import torch
import torch.nn as nn
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from transformers import pipeline as hf_pipeline
import soundfile as sf  # For WAV I/O
from scipy.signal import resample
import jiwer  # For WER metric (pip install jiwer)

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
    p = np.polyfit(x, L, 1)
    return -p[0]

# FD Adapter (4D toroidal: bias low-FD paths for (C)V purity)
class FDAdapter(nn.Module):
    def __init__(self, input_dim=80, fd_dim=1):
        super().__init__()
        self.linear = nn.Linear(input_dim + fd_dim, input_dim)  # Concat FD, map back

    def forward(self, features, fd):
        fd_t = torch.tensor([[fd]], dtype=features.dtype, device=features.device)
        concat = torch.cat([features, fd_t], dim=1)
        return self.linear(concat)

# 5D Collapse: Entropy selection for coherent transcript (mock OR reduction)
def entropy_collapse(logits, threshold=-0.5):
    """Mock gravitational OR: low entropy selects coherent path."""
    entropy = -torch.sum(torch.softmax(logits, dim=-1) * torch.log_softmax(logits, dim=-1) + 1e-10, dim=-1).mean()
    if entropy.item() < threshold:
        return "Coherent glide selected"  # Bias toward smooth
    return "Ripple void detected"

# Main Prototype: Load audio → FD extract → Whisper + adapter → collapse → transcript
def fractal_stt_pipeline(audio_path, ground_truth=None, device='cpu'):
    # Load & resample audio to 16kHz (Whisper standard)
    audio, sr = sf.read(audio_path)
    if sr != 16000:
        audio = resample(audio, int(len(audio) * 16000 / sr))
    
    # 3D: Extract FD on raw waveform
    fd = higuchi_fd(audio, fs=16000)
    print(f"Extracted FD: {fd:.3f} (low = glide, high = ripple)")
    
    # Load Whisper-tiny (pretrained, no fine-tune needed)
    processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny").to(device)
    
    # Process audio to mel (input features)
    inputs = processor(audio, sampling_rate=16000, return_tensors="pt").to(device)
    
    # 4D: Adapter inject FD bias (mock: concat to first layer; in full, hook to encoder)
    adapter = FDAdapter().to(device)
    # Mock concat to inputs['input_features'] (80 dims)
    with torch.no_grad():
        adapted_features = adapter(inputs['input_features'], fd)
        inputs['input_features'] = adapted_features  # Replace for inference
    
    # Generate transcript
    generated_ids = model.generate(inputs.input_features, language="mi")  # 'mi' for Māori/te reo
    transcript = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(f"Raw Transcript: {transcript}")
    
    # 5D: Entropy collapse on logits (mock from last hidden)
    logits = model(inputs.input_features).logits  # Last layer
    collapse_hint = entropy_collapse(logits[0, -1])  # Final token entropy
    print(f"Collapse Hint: {collapse_hint}")
    
    # Metrics (if ground truth provided)
    if ground_truth:
        wer = jiwer.wer(ground_truth.lower(), transcript.lower())
        print(f"WER: {wer:.3f}")
    
    return transcript, fd, collapse_hint

# Usage: Run with your WAV
if __name__ == "__main__":
    audio_file = "input.wav"  # Your "kia ora" chant WAV
    ground_truth = "kia ora"  # Optional for WER
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running on {device}")
    
    transcript, fd, hint = fractal_stt_pipeline(audio_file, ground_truth, device)
    print(f"\nFinal Output: {transcript} | FD: {fd:.3f} | Hint: {hint}")