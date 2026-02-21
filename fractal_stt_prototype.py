import numpy as np
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf
from scipy.signal import resample

def higuchi_fd(signal, k_max=10):
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

class FDAdapter(torch.nn.Module):
    def __init__(self, input_dim=80, fd_dim=1):
        super().__init__()
        self.linear = torch.nn.Linear(input_dim + fd_dim, input_dim)

    def forward(self, features, fd):
        B, T, D = features.shape
        fd_t = torch.full((B, T, 1), fd, dtype=features.dtype, device=features.device)
        concat = torch.cat([features, fd_t], dim=-1)  # [B, T, 81]
        return self.linear(concat)

def fractal_stt_pipeline(audio_path, device='cpu'):
    # Load & resample to 16kHz
    audio, sr = sf.read(audio_path)
    if len(audio.shape) > 1: audio = audio.mean(axis=1)  # mono
    if sr != 16000:
        audio = resample(audio, int(len(audio) * 16000 / sr))

    # Higuchi FD on waveform
    fd = higuchi_fd(audio)
    print(f"Extracted FD: {fd:.3f} (low=glide/smooth, high=ripple/turbulent)")

    # Whisper tiny multilingual
    processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny").to(device)

    inputs = processor(audio, sampling_rate=16000, return_tensors="pt").to(device)

    # Optional FD adapter (random → skip for clean baseline; train later)
    # adapter = FDAdapter().to(device)
    # with torch.no_grad():
    #     inputs['input_features'] = adapter(inputs['input_features'], fd)

    # Generate (auto language detect; force 'mi' if needed)
    generated_ids = model.generate(inputs.input_features, language="mi")  # or None for auto
    transcript = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    print(f"Transcript: {transcript}")

    # Mock collapse on last logits
    with torch.no_grad():
        outputs = model(inputs.input_features, output_scores=True, return_dict_in_generate=True)
        last_scores = outputs.scores[-1]  # last token scores [batch, vocab]
        probs = torch.softmax(last_scores, dim=-1)
        entropy = -torch.sum(probs * torch.log(probs + 1e-10), dim=-1).mean().item()
    hint = "Coherent glide selected" if entropy < -0.5 else "Ripple void detected"
    print(f"Collapse Hint (entropy {entropy:.3f}): {hint}")

    return transcript, fd, hint

# Run example
if __name__ == "__main__":
    audio_file = "input.wav"  # your "kia ora" file
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    transcript, fd, hint = fractal_stt_pipeline(audio_file, device)
    print(f"\nFinal: '{transcript}' | FD: {fd:.3f} | {hint}")
