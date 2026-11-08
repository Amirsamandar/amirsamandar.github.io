"""Full-frame site background: simulated CMB-like polarization field rendered with
line-integral convolution (the visual technique of the Planck polarization maps),
with faint posterior-contour ellipses and a sparse node network. Not Planck data.
Outputs dark and light versions at desktop and mobile sizes."""
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates, gaussian_filter

W, H = 2400, 1500
rng = np.random.default_rng(20261108)


def grf(shape, slope, kmin=1.0, seed=None):
    r = np.random.default_rng(seed)
    ny, nx = shape
    kx = np.fft.fftfreq(nx) * nx
    ky = np.fft.fftfreq(ny) * ny
    k = np.sqrt(kx[None, :] ** 2 + ky[:, None] ** 2)
    k[0, 0] = 1.0
    amp = np.where(k < kmin, 0.0, k ** (-slope / 2.0))
    f = np.fft.ifft2((r.normal(size=shape) + 1j * r.normal(size=shape)) * amp).real
    return (f - f.mean()) / f.std()


import os
CACHE = "fields-cache.npz"
if os.path.exists(CACHE):
    _c = np.load(CACHE)
    lic, I, Hh = _c["lic"], _c["I"], _c["Hh"]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
else:
    # Stokes Q/U with a long coherence length -> polarization orientation
    Q = gaussian_filter(grf((H, W), 3.0, seed=11), 60)
    U = gaussian_filter(grf((H, W), 3.0, seed=12), 60)
    xs = np.linspace(0, 1, W)[None, :]
    ys = np.linspace(0, 1, H)[:, None]
    Q = Q / Q.std() + 0.8 * np.cos(2 * np.pi * (1.1 * xs + 0.3 * ys))
    U = U / U.std() + 0.8 * np.sin(2 * np.pi * (0.7 * ys - 0.4 * xs))
    psi = 0.5 * np.arctan2(U, Q) + np.pi / 2
    vx, vy = np.cos(psi).astype(np.float32), np.sin(psi).astype(np.float32)

    # LIC
    noise = gaussian_filter((rng.random((H, W)) ** 3).astype(np.float32), 0.7)
    L, h = 90, 1.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    acc = noise.copy()
    wsum = np.ones_like(noise)
    for sign in (1.0, -1.0):
        px, py = xx.copy(), yy.copy()
        dx, dy = sign * vx, sign * vy
        for i in range(L):
            sx = map_coordinates(vx, [py, px], order=1, mode="nearest")
            sy = map_coordinates(vy, [py, px], order=1, mode="nearest")
            flip = (sx * dx + sy * dy) < 0
            dx = np.where(flip, -sx, sx)
            dy = np.where(flip, -sy, sy)
            px = np.clip(px + h * dx, 0, W - 1)
            py = np.clip(py + h * dy, 0, H - 1)
            w = np.float32(np.cos(0.5 * np.pi * (i + 1) / (L + 1)) ** 2)
            acc += w * map_coordinates(noise, [py, px], order=1, mode="nearest")
            wsum += w
    lic = acc / wsum
    lic = (lic - lic.mean()) / lic.std()
    lic = np.clip(0.5 + 0.30 * lic, 0, 1)

    # dust-like intensity and a second field for hue variation
    I = gaussian_filter(grf((H, W), 3.4, seed=21), 22)
    I = np.exp(0.8 * I / I.std())
    I = np.clip((I - I.min()) / (np.percentile(I, 99.5) - I.min()), 0, 1)
    Hh = gaussian_filter(grf((H, W), 3.6, seed=31), 40)
    Hh = np.clip(0.5 + 0.28 * Hh / Hh.std(), 0, 1)


    np.savez_compressed(CACHE, lic=lic, I=I, Hh=Hh)

def palette(t, stops):
    pos = np.array([s[0] for s in stops])
    cols = np.array([s[1] for s in stops], np.float32) / 255
    return np.stack([np.interp(np.clip(t, 0, 1), pos, cols[:, c]) for c in range(3)], -1)


def smooth(a, b, t):
    t = np.clip((t - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def render(theme):
    Iv = np.clip(I ** 0.8, 0, 1)
    Hv = smooth(0.25, 0.75, Hh)
    if theme == "dark":
        base = palette(0.15 + 0.85 * I, [(0.0, (10, 16, 44)), (0.25, (16, 38, 88)), (0.45, (24, 84, 124)),
                                          (0.62, (64, 92, 176)), (0.78, (140, 104, 196)), (0.90, (214, 164, 220)),
                                          (1.0, (246, 206, 142))])
        alt = palette(0.15 + 0.85 * I, [(0.0, (12, 14, 40)), (0.30, (26, 32, 96)), (0.55, (74, 58, 150)),
                                         (0.80, (176, 110, 186)), (1.0, (246, 200, 150))])
        base = palette(0.22 + 0.78 * Iv, [(0.0, (10, 16, 44)), (0.25, (16, 40, 92)), (0.42, (18, 92, 128)),
                                           (0.60, (52, 100, 184)), (0.76, (138, 106, 204)), (0.90, (220, 168, 224)),
                                           (1.0, (248, 208, 144))])
        alt = palette(0.22 + 0.78 * Iv, [(0.0, (16, 12, 44)), (0.30, (38, 30, 104)), (0.52, (92, 58, 160)),
                                          (0.74, (186, 106, 188)), (0.90, (236, 150, 170)), (1.0, (250, 206, 150))])
        col = base * (1 - Hv[..., None]) + alt * Hv[..., None]
        img = col * (0.45 + 1.15 * lic[..., None] ** 1.2)
    else:
        lav, sky, peach, rose = (np.array(c, np.float32) / 255 for c in
                                 [(188, 172, 246), (150, 204, 246), (252, 196, 164), (242, 172, 208)])
        col = lav * (1 - Hv[..., None]) + sky * Hv[..., None]
        warm = smooth(0.42, 0.95, Iv)[..., None]
        col = col * (1 - 0.75 * warm) + (peach * 0.6 + rose * 0.4) * 0.75 * warm
        col = 0.20 + 0.80 * col                      # pastel, never grey
        img = col * (0.80 + 0.42 * lic[..., None])   # white sheen on strands, soft grooves
    # gentle vignette
    vig = 1 - 0.18 * (((xx / W - 0.55) ** 2) / 0.35 + ((yy / H - 0.45) ** 2) / 0.5)
    if theme == "dark":
        img = img * np.clip(vig, 0.75, 1)[..., None]
    return np.clip(img, 0, 1)


def overlay(img, theme):
    base = Image.fromarray((img * 255).astype(np.uint8)).convert("RGBA")
    S = 2
    ov = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    if theme == "dark":
        c_ell, c_line, c_node = (226, 206, 246), (214, 206, 246), (246, 220, 168)
        a_ell, a_line, a_node = 95, 52, 210
    else:
        c_ell, c_line, c_node = (92, 60, 160), (92, 60, 160), (110, 76, 170)
        a_ell, a_line, a_node = 90, 48, 170
    for (cx, cy, sx, sy, ang) in [(0.82, 0.22, 80, 38, -28), (0.66, 0.62, 52, 28, 22), (0.18, 0.80, 60, 30, 12)]:
        for k, a in zip((1, 2, 3), (1.0, 0.65, 0.4)):
            t = np.linspace(0, 2 * np.pi, 400)
            ex, ey = k * sx * np.cos(t), k * sy * np.sin(t)
            th = np.deg2rad(ang)
            X = cx * W + ex * np.cos(th) - ey * np.sin(th)
            Y = cy * H + ex * np.sin(th) + ey * np.cos(th)
            pts = [(float(x) * S, float(y) * S) for x, y in zip(X, Y)]
            d.line(pts + [pts[0]], fill=c_ell + (int(a_ell * a),), width=int(1.4 * S))
        d.ellipse([(cx * W - 3) * S, (cy * H - 3) * S, (cx * W + 3) * S, (cy * H + 3) * S], fill=c_node + (a_node,))
    r2 = np.random.default_rng(42)
    pts = []
    while len(pts) < 60:
        x, y = r2.uniform(0.02, 0.98) * W, r2.uniform(0.02, 0.98) * H
        if (0.25 + I[int(y), int(x)]) * (0.4 + 0.6 * (x / W)) > r2.uniform(0.3, 1.2):
            pts.append((x, y))
    P = np.array(pts)
    for p in P:
        dist = np.hypot(*(P - p).T)
        for j in np.argsort(dist)[1:3]:
            if dist[j] < 280:
                d.line([(p[0] * S, p[1] * S), (P[j][0] * S, P[j][1] * S)], fill=c_line + (a_line,), width=S)
    for p in P:
        r = r2.uniform(1.6, 3.2)
        d.ellipse([(p[0] - r) * S, (p[1] - r) * S, (p[0] + r) * S, (p[1] + r) * S], fill=c_node + (a_node,))
    ov = ov.resize((W, H), Image.LANCZOS)
    return Image.alpha_composite(base, ov).convert("RGB")


for theme in ("dark", "light"):
    im = overlay(render(theme), theme)
    im.save(f"site-bg-{theme}.jpg", quality=80, optimize=True, progressive=True)
    im.resize((1200, 750), Image.LANCZOS).save(f"site-bg-{theme}-1200.jpg", quality=78, optimize=True, progressive=True)
    print(theme, "done")
